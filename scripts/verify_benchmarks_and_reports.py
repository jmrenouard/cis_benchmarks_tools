#!/usr/bin/env python3
"""CIS Benchmarks Document Tracking, Rules Engine & Quality Campaign (PSL ONLY)."""

import argparse
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

TARGET_MAP = [
    ("cassandra", "cassandra"), ("mariadb", "mariadb"),
    ("mongodb", "mongodb"), ("mysql", "mysql"),
    ("postgresql", "postgresql"), ("red_hat", "rhel"),
    ("rhel", "rhel"), ("github", "github")
]


def audit_benchmark_documents(data_dir=None):
    """Scan CIS_DATA/ and extract benchmark PDF metadata."""
    data_dir = data_dir or os.path.join(REPO_ROOT, "CIS_DATA")
    if not os.path.isdir(data_dir):
        return []

    ver_re = re.compile(r'v(\d+\.\d+(?:\.\d+)?)', re.IGNORECASE)
    docs = []
    for pdf in sorted(glob.glob(os.path.join(data_dir, "*.pdf"))):
        fname = os.path.basename(pdf)
        vm = ver_re.search(fname)
        low = fname.lower()
        tgt = next((val for key, val in TARGET_MAP if key in low), "unknown")
        docs.append({
            "filename": fname,
            "target": tgt,
            "version": vm.group(1) if vm else "unknown",
            "has_md_extract": os.path.isfile(pdf[:-4] + ".md"),
            "file_size": os.path.getsize(pdf),
        })
    return docs


def audit_rules_engine(rules_dir=None):
    """Validate JSON syntax and schema completeness across rules/*.json."""
    rules_dir = rules_dir or os.path.join(REPO_ROOT, "rules")
    rep = {"valid_files_count": 0, "invalid_files_count": 0, "total_rules_count": 0, "files": {}, "errors": []}
    if not os.path.isdir(rules_dir):
        rep["errors"].append(f"Directory not found: {rules_dir}")
        return rep

    for r_path in sorted(glob.glob(os.path.join(rules_dir, "*.json"))):
        fname = os.path.basename(r_path)
        try:
            with open(r_path, "r", encoding="utf-8") as f:
                rules = json.load(f)
            if not isinstance(rules, list):
                rep["invalid_files_count"] += 1
                rep["errors"].append(f"{fname}: root must be a list")
                continue

            valid = all(
                ("id" in r or "number" in r) and ("title" in r or "name" in r) and "category" in r
                for r in rules
            )
            if valid:
                rep["valid_files_count"] += 1
                rep["total_rules_count"] += len(rules)
                rep["files"][fname] = {"count": len(rules), "status": "VALID"}
            else:
                rep["invalid_files_count"] += 1
                rep["errors"].append(f"{fname}: missing required fields (id/number, title/name, category)")
        except Exception as e:
            rep["invalid_files_count"] += 1
            rep["errors"].append(f"{fname}: parse error: {e}")
    return rep


def analyze_report_quality(filepath, content_str=None):
    """Analyze generated report for completeness, charts, and valid syntax."""
    if content_str is None:
        if not os.path.exists(filepath):
            return False, "File missing"
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    else:
        content = content_str

    if len(content.strip()) < 5:
        return False, "Content too short"

    low = filepath.lower()
    if low.endswith(".html"):
        if "<html" not in content or "</html>" not in content:
            return False, "Malformed HTML structure"
        if "<svg" not in content:
            return False, "Missing Inline SVG charts"
        if "toggleDarkMode" not in content:
            return False, "Missing Dark Mode UI control script"
    elif low.endswith(".json"):
        try:
            data = json.loads(content)
            if not isinstance(data, dict):
                return False, "JSON root is not a dictionary"
        except Exception as e:
            return False, f"Invalid JSON syntax: {e}"
    elif low.endswith(".xml"):
        try:
            ET.fromstring(content)
        except Exception as e:
            return False, f"Invalid XML syntax: {e}"
    elif low.endswith(".txt"):
        if "CIS BENCHMARK AUDIT REPORT" not in content and "Report Date" not in content:
            return False, "Missing TXT report header"
        if "CATEGORY BREAKDOWN & COMPLIANCE SUMMARY TABLE" not in content:
            return False, "Missing TXT ASCII summary compliance table"

    return True, "Quality criteria passed"


def run_quality_campaign(reports_dir=None):
    """Validate all existing report files in reports/ across formats."""
    reports_dir = reports_dir or os.path.join(REPO_ROOT, "reports")
    res = {"total": 0, "passed": 0, "failed": 0, "details": []}
    if not os.path.isdir(reports_dir):
        return res

    for rf in sorted(glob.glob(os.path.join(reports_dir, "rapport_cis_*.*"))):
        res["total"] += 1
        ok, msg = analyze_report_quality(rf)
        res["passed" if ok else "failed"] += 1
        res["details"].append({"file": os.path.basename(rf), "status": "PASS" if ok else "FAIL", "msg": msg})
    return res


def main():
    p = argparse.ArgumentParser(description="CIS Benchmarks Tracking, Rules Engine & Quality Campaign")
    p.add_argument("--audit-docs", action="store_true", help="Audit CIS_DATA documents")
    p.add_argument("--check-rules", action="store_true", help="Validate rules/*.json schemas")
    p.add_argument("--test-reports", action="store_true", help="Validate reports quality")
    p.add_argument("--all", action="store_true", help="Execute complete tracking and quality suite")
    args = p.parse_args()

    run_all = args.all or (not args.audit_docs and not args.check_rules and not args.test_reports)
    print("🔍 [CIS Suite] Running CIS Benchmarks Tracking & Quality Campaign...")

    if run_all or args.audit_docs:
        docs = audit_benchmark_documents()
        print(f"📚 [1/3] Discovered {len(docs)} CIS Benchmark PDF documents in CIS_DATA/:")
        for d in docs:
            print(f"  - [{d['target'].upper()}] {d['filename']} (v{d['version']}) [MD: {'✓' if d['has_md_extract'] else '✗'}]")

    if run_all or args.check_rules:
        rep = audit_rules_engine()
        print(f"⚙️ [2/3] Rules Engine: {rep['valid_files_count']} files valid ({rep['total_rules_count']} controls)")
        if rep["errors"]:
            for err in rep["errors"]:
                print(f"  ❌ {err}", file=sys.stderr)
            sys.exit(1)

    if run_all or args.test_reports:
        qc = run_quality_campaign()
        print(f"📊 [3/3] Reports Quality: {qc['total']} evaluated, {qc['passed']} passed, {qc['failed']} failed")

    print("\n✅ Verification and Quality Campaign completed successfully!")


if __name__ == "__main__":
    main()
