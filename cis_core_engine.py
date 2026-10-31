#!/usr/bin/env python3
"""cis_core_engine.py — Shared Core Engine (PSL ONLY)."""
import html, json, os, re, subprocess, xml.etree.ElementTree as ET

try:
    from execution_drivers import create_executor
except ImportError:
    create_executor = None


def load_recommendations(target_key, fallback_data=None, base_dir=None):
    p = os.path.join(base_dir or os.path.dirname(os.path.abspath(__file__)), "rules", f"{target_key}.json")
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as fp: return json.load(fp)
        except Exception: pass
    return fallback_data or []


def is_valid_executable_command(cmd):
    if not cmd or not isinstance(cmd, str) or not cmd.strip(): return False
    s = cmd.strip()
    k = set("cat ls grep egrep find ps awk cut sed head tail echo getent crontab df stat test dpkg rpm systemctl mysql mariadb psql cqlsh mongo mongosh python3 python bash sh docker curl".split())
    return s[0] in "![(/." or s.split()[0].lower() in k or any(t in s for t in ("|", ";", ">", "$", "&"))


def run_command(command, **kw):
    if create_executor and not kw.get("sudo"):
        try:
            r = create_executor(mode="ssh" if kw.get("remote_host") else "local", **kw).execute(command)
            return r.stdout, r.stderr, r.returncode
        except Exception: pass
    try:
        pwd = kw.get("db_password")
        env = dict(os.environ, MYSQL_PWD=str(pwd), PGPASSWORD=str(pwd)) if pwd else None
        cmd = ["/bin/bash", "-c", command] if isinstance(command, str) else list(command)
        p = subprocess.run(cmd, check=False, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=kw.get("timeout", 10), env=env)
        return p.stdout.strip(), p.stderr.strip(), p.returncode
    except Exception as e:
        return "", str(e), -1


def evaluate_condition(cond, stdout, stderr, code):
    if not cond or any(w in (stderr or "") for w in ("No such file", "Permission denied")): return False
    out, exp, v, t = stdout or "", cond.get("value"), cond.get("values", []), cond.get("type")
    m, o, el = re.search(r"(\d+)", out), out.strip(), str(exp).lower()
    val = int(m.group(1)) if m else None
    ops = {
        "returncode_zero": lambda: code == 0, "returncode_equals": lambda: code == exp,
        "stdout_equals": lambda: o == str(exp), "stdout_not_equals": lambda: o != str(exp),
        "stdout_contains": lambda: el in out.lower(), "stdout_not_contains": lambda: el not in out.lower(),
        "stdout_not_empty": lambda: bool(o), "stdout_is_empty": lambda: not bool(o),
        "stdout_contains_any": lambda: any(str(x).lower() in out.lower() for x in v),
        "stdout_not_contains_any": lambda: not any(str(x).lower() in out.lower() for x in v),
        "stdout_regex_match": lambda: bool(cond.get("pattern") and re.search(cond["pattern"], out)),
        "stdout_is_numeric_greater_than": lambda: val is not None and val > (exp or 0),
        "stdout_is_numeric_less_equal": lambda: val is not None and 0 < val <= (exp or 0),
    }
    return ops[t]() if t in ops else False


class AuditScoresTuple(tuple):
    def __new__(cls, *a): return super().__new__(cls, a)
    overall_score = property(lambda s: s[0])
    categories_scores = property(lambda s: s[1])


def _flatten(res):
    return [dict(c, category=k) for k, v in res.items() for c in v if isinstance(c, dict)] if isinstance(res, dict) else [dict(c) for c in res if isinstance(c, dict)]


def calculate_scores(results):
    flat, cnts, cat_order, cats = _flatten(results), {"pass": 0, "fail": 0, "manual": 0, "error": 0, "na": 0}, [], {}
    flds = "total_automated passed_automated failed_automated manual_checks error_checks na_checks pass_count fail_count error_count na_count".split()
    for c in flat:
        k = c.get("category", "General")
        if k not in cats:
            cat_order.append(k)
            cats[k] = dict({f: 0 for f in flds}, name=k, score=0.0)
        st, t = str(c.get("status", "")).upper(), str(c.get("type", "")).capitalize()
        key = "manual" if t == "Manual" or "MANUAL" in st else ("pass" if st in ("PASS", "SUCCÈS") else ("error" if st in ("ERROR", "ERREUR") else ("na" if st in ("N/A", "NA") else "fail")))
        cnts[key] += 1
        s = cats[k]
        for f in {"manual": ("manual_checks",), "pass": ("passed_automated", "pass_count"), "error": ("error_checks", "error_count"), "na": ("na_checks", "na_count"), "fail": ("failed_automated", "fail_count")}[key]:
            s[f] += 1
    att = cnts["pass"] + cnts["fail"] + cnts["na"]
    ov = ((cnts["pass"] + cnts["na"]) / att * 100) if att else 0.0
    for k in cat_order:
        s = cats[k]
        ca = s["passed_automated"] + s["failed_automated"] + s["na_checks"]
        s["total_automated"], s["score"] = ca, (((s["passed_automated"] + s["na_checks"]) / ca * 100) if ca else 0.0)
    js = [json.dumps([cats[c][f] for c in cat_order]) for f in ("pass_count", "fail_count", "error_count", "na_count")]
    return AuditScoresTuple(ov, cats, cnts["manual"], cnts["error"], cnts["na"], cnts["pass"], cnts["fail"],
                            cnts["error"], cnts["na"], json.dumps(cat_order), *js)


def build_inline_svg_donut_chart(p, f, e, na, score):
    t = p + f + e + na
    pct, d = (p / t * 100) if t else 0, "M18 2.08a15.92 15.92 0 1 1 0 31.84a15.92 15.92 0 1 1 0-31.84"
    return f'<svg viewBox="0 0 36 36" style="width:120px;height:120px;"><path d="{d}" fill="none" stroke="#e5e7eb" stroke-width="3.8"/><path d="{d}" fill="none" stroke="#10b981" stroke-width="3.8" stroke-dasharray="{pct:.1f} 100"/><text x="18" y="20.5" text-anchor="middle" font-size="7">{score:.1f}%</text></svg>'


def build_inline_svg_category_chart(categories_scores, *args):
    if args:
        categories_scores = {n: {"score": (p / (p + f + e + na) * 100) if (p + f + e + na) else 0} for n, p, f, e, na in zip(categories_scores, *args)}
    return "".join(f'<div>{html.escape(k)}: {v.get("score", 0):.1f}%</div>' for k, v in categories_scores.items()) if isinstance(categories_scores, dict) else ""


def export_results(results, overall_score, categories_scores, target_name, filename=None, fmt="json", **kw):
    fn = filename or f"reports/rapport_cis_{target_name.lower().replace(' ', '_').replace('.', '')}.{fmt}"
    if os.path.dirname(fn): os.makedirs(os.path.dirname(fn), exist_ok=True)
    flat = _flatten(results)
    if fmt == "json":
        c = json.dumps({"target": target_name, "overall_score": float(overall_score), "categories": categories_scores, "total_checks": len(flat), "results": results}, indent=2)
    elif fmt == "xml":
        root = ET.Element("testsuite", name=target_name, tests=str(len(flat)))
        for r in flat:
            tc = ET.SubElement(root, "testcase", id=str(r.get("id", "")), name=str(r.get("name", "")), classname=str(r.get("category", "")))
            if str(r.get("status", "")).upper() == "FAIL": ET.SubElement(tc, "failure", message="Failed").text = str(r.get("output", ""))
        c = ET.tostring(root, encoding="utf-8").decode("utf-8")
    else:
        c = f"CIS REPORT: {target_name} ({overall_score:.1f}%)\n"
    with open(fn, "w", encoding="utf-8") as f: f.write(c)
    print(f"[INFO] Report generated: {fn}")


class BaseAuditEngine:
    def __init__(self, k, n, d=None, c=None):
        self.target_key, self.target_name, self.recommendations_data, self.default_container = k, n, d or [], c
    load_rules = lambda s: load_recommendations(s.target_key, fallback_data=s.recommendations_data)
    execute_cmd = staticmethod(run_command)
    evaluate_check = staticmethod(evaluate_condition)
    calculate_scores = staticmethod(calculate_scores)
    render_donut_chart = staticmethod(build_inline_svg_donut_chart)
    render_category_chart = staticmethod(build_inline_svg_category_chart)
    export = lambda s, res, sc, cat_sc, filename=None, fmt="json", **kw: export_results(res, sc, cat_sc, s.target_name, filename=filename, fmt=fmt, **kw)
