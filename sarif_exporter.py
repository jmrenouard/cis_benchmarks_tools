#!/usr/bin/env python3
"""SARIF v2.1.0 exporter for CIS Benchmarks Tools Suite (100% PSL ONLY)."""
import datetime, hashlib, json, os, re
from audit_diagnostics import CommandFailureClassifier
from execution_drivers import SecretSanitizer
from post_execution_publisher import atomic_write_text
from temporal_metadata import TemporalAuditMetadata

SARIF_SCHEMA_URI = "https://json.schemastore.org/sarif-2.1.0.json"
SARIF_VERSION, TOOL_NAME = "2.1.0", "cis-benchmarks-tools"
TOOL_INFO_URI = "https://github.com/jmrenouard/cis_benchmarks_tools"
_STATES = {k: v for ks, v in (
    (("PASS", "PASSED", "SUCCESS", "SUCCES", "SUCCÈS"), ("Pass", "pass", "none")),
    (("FAIL", "FAILED"), ("Fail", "fail", "error")), (("ERROR", "ERREUR"), ("Error", "open", "warning")),
    (("MANUAL", "MANUEL"), ("Manual", "review", "note")),
    (("N/A", "NA", "NOT APPLICABLE", "NOT_APPLICABLE", "NON APPLICABLE", "NON_APPLICABLE"), ("Not Applicable", "notApplicable", "none")),
) for k in ks}


def _clean(v):
    return "" if v is None else str(SecretSanitizer.sanitize(str(v))).strip()


def _version(ov=None):
    if ov:
        return str(ov).strip()
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "VERSION"), encoding="utf-8") as f:
            return f.read().strip() or "2.10.0"
    except OSError:
        return "2.10.0"


def resolve_rule_spec(target_name):
    from audit_orchestrator import CANONICAL_TARGETS, normalize_target_key
    raw = str(target_name or "")
    k = normalize_target_key(raw)
    if k in CANONICAL_TARGETS:
        return CANONICAL_TARGETS[k]["rule_spec"]
    low = re.sub(r"[^a-z0-9]+", "", raw.lower())
    for m in CANONICAL_TARGETS.values():
        if re.sub(r"[^a-z0-9]+", "", m["title"].lower()) == low:
            return m["rule_spec"]
    return re.sub(r"[^a-z0-9]+", "_", raw.lower()).strip("_") or "cis_target"


def map_compliance_state(status, control_type=""):
    raw = str(status or "").strip().upper()
    if raw in _STATES:
        return _STATES[raw]
    return ("Manual", "review", "note") if ("MANUAL" in raw or str(control_type or "").strip().lower() == "manual") else ("Error", "open", "warning")


def normalize_control_results(results):
    if isinstance(results, dict):
        raw = [{**c, "category": c.get("category") or str(cat)} for cat, cs in results.items() if isinstance(cs, list) for c in cs if isinstance(c, dict)]
    else:
        raw = [dict(c) for c in results if isinstance(c, dict)] if isinstance(results, list) else []
    out = []
    for i, r in enumerate(raw, 1):
        cid, st = str(r.get("number") or r.get("id") or f"CTRL-{i}").strip(), str(r.get("status") or "").strip()
        out.append({"control_id": cid, "title": _clean(r.get("name") or r.get("title") or f"CIS {cid}"),
                    "category": _clean(r.get("category") or "General"),
                    "type": str(r.get("type") or ("Manual" if "MANUAL" in st.upper() else "Automated")).strip(),
                    "status": st, "command": _clean(r.get("test_procedure") or r.get("audit") or ""),
                    "output": _clean(r.get("output") or r.get("stdout") or r.get("stderr") or ""),
                    "remediation": _clean(r.get("remediation") or "")})
    return out


def _utc(s):
    if not isinstance(s, str) or not s.strip():
        return None
    try:
        dt = datetime.datetime.fromisoformat(s.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return (dt.astimezone(datetime.timezone.utc) if dt.tzinfo else dt.replace(tzinfo=datetime.timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_sarif_document(results, overall_score=0.0, categories_scores=None, target_name="CIS Target", execution_context=None, temporal_metadata=None, tool_version=None):
    spec, norm = resolve_rule_spec(target_name), normalize_control_results(results)
    uri, tm = f"rules/{spec}.json", temporal_metadata or TemporalAuditMetadata.create_now()
    td = tm.to_dict() if isinstance(tm, TemporalAuditMetadata) else (dict(tm) if isinstance(tm, dict) else {})
    t0, t1 = _utc(td.get("iso_start")), _utc(td.get("iso_end") or td.get("iso_start"))
    ctx = _clean(execution_context.get("label") if isinstance(execution_context, dict) else (execution_context or "Local Bare-Metal"))
    rules, r_idx, s_res, cnt = [], {}, [], {"Pass": 0, "Fail": 0, "Error": 0, "Manual": 0, "Not Applicable": 0}
    for c in norm:
        cid, rid = c["control_id"], f"CIS-{spec.upper()}-{re.sub(r'[^A-Za-z0-9._-]+', '_', c['control_id'])}"
        if rid not in r_idx:
            r_idx[rid] = len(rules)
            m = c["type"].lower() == "manual"
            rules.append({"id": rid, "shortDescription": {"text": c["title"]}, "help": {"text": c["remediation"] or f"Review CIS {cid}."}, "defaultConfiguration": {"level": "note" if m else "error"}, "properties": {"tags": ["security", spec]}})
        st, kind, lvl = map_compliance_state(c["status"], c["type"])
        cnt[st] = cnt.get(st, 0) + 1
        props = {"compliance_state": st, "category": c["category"], "control_id": cid, "command": c["command"], "output": c["output"], "remediation": c["remediation"]}
        if st in ("Error", "Fail"):
            props["failure_category"] = CommandFailureClassifier.classify_control_result({"status": st.upper(), "output": c["output"], "test_procedure": c["command"], "remediation": c["remediation"]}, target_hint=spec).category
        fp = hashlib.sha256(f"{spec}|{cid}|{uri}".encode("utf-8")).hexdigest()[:32]
        s_res.append({"ruleId": rid, "ruleIndex": r_idx[rid], "kind": kind, "level": lvl, "message": {"text": _clean(f"[{st}] CIS {cid}: {c['title']} - {c['output'][:160] or c['title']}")}, "locations": [{"physicalLocation": {"artifactLocation": {"uri": uri}, "region": {"startLine": 1}}, "logicalLocations": [{"name": cid, "fullyQualifiedName": f"{spec}/{c['category']}/{cid}", "kind": "rule"}]}], "partialFingerprints": {"primaryLocationLineHash": fp}, "properties": props})
    inv = {"executionSuccessful": True, **({"startTimeUtc": t0} if t0 else {}), **({"endTimeUtc": t1} if t1 else {})}
    return {"$schema": SARIF_SCHEMA_URI, "version": SARIF_VERSION, "runs": [{"tool": {"driver": {"name": TOOL_NAME, "version": _version(tool_version), "informationUri": TOOL_INFO_URI, "rules": rules}}, "invocations": [inv], "results": s_res, "properties": {"target": _clean(target_name), "rule_spec": spec, "overall_score": round(float(overall_score or 0.0), 2), "execution_context": ctx, "counts": cnt, "categories": categories_scores or {}, "temporal_metadata": td}}]}


def validate_sarif_document(doc):
    """Validate structural SARIF v2.1.0 and GitHub Code Scanning invariants."""
    if not isinstance(doc, dict) or doc.get("version") != SARIF_VERSION:
        return False, "Invalid SARIF root or version"
    runs = doc.get("runs")
    if not isinstance(runs, list) or not runs or not isinstance(runs[0], dict):
        return False, "Missing SARIF runs[0]"
    drv, res = (runs[0].get("tool") or {}).get("driver"), runs[0].get("results")
    if not isinstance(drv, dict) or not drv.get("name") or not isinstance(drv.get("rules"), list) or not isinstance(res, list):
        return False, "Invalid SARIF tool.driver or results"
    rids = {r.get("id") for r in drv["rules"] if isinstance(r, dict)}
    for i, r in enumerate(res):
        locs = r.get("locations") if isinstance(r, dict) else None
        uri = ((locs[0].get("physicalLocation") or {}).get("artifactLocation") or {}).get("uri") if isinstance(locs, list) and locs else None
        if not isinstance(r, dict) or r.get("ruleId") not in rids or not uri or not r.get("partialFingerprints"):
            return False, f"Invalid SARIF result[{i}]"
    return True, f"Valid SARIF v2.1.0 ({len(res)} results, {len(drv['rules'])} rules)"


def export_sarif_report(results, overall_score, categories_scores, target_name, filename=None, execution_context=None, temporal_metadata=None):
    fn = filename or f"reports/rapport_cis_{resolve_rule_spec(target_name)}.sarif"
    doc = build_sarif_document(results, overall_score, categories_scores, target_name, execution_context, temporal_metadata)
    written = atomic_write_text(fn, json.dumps(doc, indent=2))
    print(f"SARIF Report generated: {fn}")
    return written
