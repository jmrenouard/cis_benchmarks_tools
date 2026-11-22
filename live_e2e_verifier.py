#!/usr/bin/env python3
"""Live multi-db-docker-env before/after remediation E2E verifier (100% PSL ONLY)."""
import argparse, json, os, re, subprocess, sys, tempfile
from post_execution_publisher import atomic_write_text
from remediation_generator import build_remediation_plan, render_remediation
from sarif_exporter import map_compliance_state, normalize_control_results, validate_sarif_document

ROOT, _DC = os.path.dirname(os.path.abspath(__file__)), "docker-compose.yml"
EPHEMERAL_MARKERS = ("-ephemeral", "-lab", "-test")
_CNAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
_PK = ("compose", "service", "container", "port", "user")
MULTI_DB_PROFILES = {k: dict(zip(_PK, v)) for k, v in (
    ("mariadb106", (_DC, "mariadb106", "mariadb-10.6", 3306, "root")),
    ("mariadb1011", (_DC, "mariadb1011", "mariadb-10.11", 3306, "root")),
    ("mysql80", (_DC, "mysql80", "mysql-8.0", 3306, "root")),
    ("mysql-community84", (_DC, "mysql84", "mysql-8.4", 3306, "root")),
    ("mysql-community97", (_DC, "mysql97", "mysql-9.7", 3306, "root")),
    ("postgresql16", (_DC, "postgres16", "postgres-16", 5432, "postgres")),
    ("postgresql17", (_DC, "postgres17", "postgres-17", 5432, "postgres")),
    ("postgresql18", (_DC, "postgres18", "postgres-18", 5432, "postgres")),
    ("mongodb7", ("docker-compose-mongo-rs.yml", "mongo1", "mongo1", 27017, "")),
    ("mongodb8", ("docker-compose-mongo8-rs.yml", "mongo8_n1", "mongo8_n1", 27017, "")),
    ("cassandra40", (_DC, "cassandra40", "cassandra-4.0", 9042, "cassandra")),
)}


def build_audit_env(db_password=None):
    env = os.environ.copy()
    if db_password is not None: env["CIS_DB_PASSWORD"] = str(db_password)
    return env


def inspect_container_labels(container, runner=subprocess.run):
    try:
        r = runner(["docker", "inspect", "--format", "{{json .Config.Labels}}", container], capture_output=True, text=True, check=True)
        d = json.loads((r.stdout or "{}").strip() or "{}")
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def is_ephemeral_lab_container(container_name, labels=None):
    lbls = labels if isinstance(labels, dict) else {}
    if str(lbls.get("cis.ephemeral_lab", "")).strip().lower() == "true": return True
    low = str(container_name or "").strip().lower()
    return low.startswith("cis-e2e-") or any(m in low for m in EPHEMERAL_MARKERS)


def _state_map(doc):
    raw = doc.get("results", doc) if isinstance(doc, dict) else (doc if isinstance(doc, list) else [])
    cnt, by = {"Pass": 0, "Fail": 0, "Error": 0, "Manual": 0, "Not Applicable": 0}, {}
    for c in normalize_control_results(raw):
        st, _, _ = map_compliance_state(c["status"], c["type"])
        cnt[st] = cnt.get(st, 0) + 1
        by[c["control_id"]] = st
    return by, cnt


def compute_compliance_delta(before_doc, after_doc):
    bm, bc = _state_map(before_doc)
    am, ac = _state_map(after_doc)
    sb = float(before_doc.get("overall_score") or 0.0) if isinstance(before_doc, dict) else 0.0
    sa = float(after_doc.get("overall_score") or 0.0) if isinstance(after_doc, dict) else 0.0
    return {"score_before": round(sb, 2), "score_after": round(sa, 2), "score_delta": round(sa - sb, 2),
            "counts_before": bc, "counts_after": ac,
            "fixed_controls": sorted(k for k, st in bm.items() if st in ("Fail", "Error") and am.get(k) == "Pass"),
            "regressed_controls": sorted(k for k, st in bm.items() if st == "Pass" and am.get(k) in ("Fail", "Error")),
            "error_count_before": bc["Error"], "error_count_after": ac["Error"]}


def run_audit_pair(target, container, out_dir, prefix="before", db_user=None, db_port=None, db_password=None, runner=subprocess.run):
    audit_py, env, paths = os.path.join(ROOT, "audit_cis.py"), build_audit_env(db_password), {}
    for fmt in ("json", "sarif"):
        p = os.path.join(out_dir, f"{prefix}_{target}.{fmt}")
        cmd = [sys.executable, audit_py, "--target", target, "--docker", container, "--format", fmt, "--output", p]
        if db_user: cmd.extend(["--db-user", str(db_user)])
        if db_port: cmd.extend(["--db-port", str(db_port)])
        runner(cmd, env=env, check=True)
        paths[fmt] = p
    with open(paths["json"], encoding="utf-8") as fp: jdoc = json.load(fp)
    with open(paths["sarif"], encoding="utf-8") as fp: sdoc = json.load(fp)
    ok, msg = validate_sarif_document(sdoc)
    if not ok: raise ValueError(f"Invalid SARIF ({prefix}): {msg}")
    return jdoc, sdoc, paths["json"], paths["sarif"]


def verify_target(target, container=None, out_dir=None, db_user=None, db_port=None, db_password=None,
                  allow_ephemeral_apply=False, container_labels=None, runner=subprocess.run):
    prof = MULTI_DB_PROFILES.get(target, {})
    cname = container or prof.get("container")
    if not cname or not _CNAME_RE.fullmatch(str(cname)): raise ValueError(f"Invalid container: {cname!r}")
    if allow_ephemeral_apply:
        lbls = container_labels if container_labels is not None else inspect_container_labels(cname, runner)
        if not is_ephemeral_lab_container(cname, lbls): raise PermissionError(f"Non-ephemeral container: '{cname}'")
    user, port = (db_user if db_user is not None else prof.get("user")), (db_port if db_port is not None else prof.get("port"))
    work = out_dir or tempfile.mkdtemp(prefix=f"cis_e2e_{target}_")
    os.makedirs(work, exist_ok=True)
    b_json, _, b_jp, b_sp = run_audit_pair(target, cname, work, "before", user, port, db_password, runner)
    plan = build_remediation_plan(b_json.get("results", b_json) if isinstance(b_json, dict) else b_json, target_name=target, dry_run=True)
    dp, sp = os.path.join(work, f"remediation_{target}.diff"), os.path.join(work, f"remediation_{target}.sh")
    atomic_write_text(dp, render_remediation(plan, "diff"))
    atomic_write_text(sp, render_remediation(plan, "shell"))
    applied, a_json, a_jp, a_sp = False, b_json, b_jp, b_sp
    if allow_ephemeral_apply:
        env = build_audit_env(db_password)
        for it in plan["items"]:
            if it["action_type"] != "manual_only" and it.get("shell"):
                runner(["docker", "exec", cname, "sh", "-lc", it["shell"]], env=env, check=True)
        applied = True
        a_json, _, a_jp, a_sp = run_audit_pair(target, cname, work, "after", user, port, db_password, runner)
    summary = {"target": target, "container": cname, "applied": applied, "remediation_items": plan["total_items"],
               "artifacts": dict(zip(("before_json", "before_sarif", "after_json", "after_sarif", "diff", "shell"), (b_jp, b_sp, a_jp, a_sp, dp, sp))),
               "delta": compute_compliance_delta(b_json, a_json)}
    atomic_write_text(os.path.join(work, f"verification_{target}.json"), json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def main(argv=None):
    p = argparse.ArgumentParser(description="Live multi-db-docker-env CIS verifier")
    for fl, n, kw in (("-t", "target", {"required": True}), ("-c", "container", {}), ("-o", "output-dir", {}), ("-u", "db-user", {}), ("-P", "db-port", {"type": int})):
        p.add_argument(fl, f"--{n}", **kw)
    p.add_argument("--allow-ephemeral-apply", action="store_true")
    a = p.parse_args(argv)
    sys.stdout.write(json.dumps(verify_target(a.target, a.container, a.output_dir, a.db_user, a.db_port, os.environ.get("CIS_DB_PASSWORD"), a.allow_ephemeral_apply), indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
