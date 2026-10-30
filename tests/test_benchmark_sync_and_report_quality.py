#!/usr/bin/env python3
"""Tests for CIS Benchmarks document tracking, rules, and report quality (PSL ONLY)."""

import json
import os
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.verify_benchmarks_and_reports import (
    audit_benchmark_documents,
    audit_rules_engine,
    analyze_report_quality,
)


class TestBenchmarkSyncAndReportQuality(unittest.TestCase):
    """Test suite verifying document tracking, rule schemas, and report quality."""

    def test_audit_benchmark_documents_inventory(self):
        docs = audit_benchmark_documents()
        self.assertGreaterEqual(len(docs), 15)
        for doc in docs:
            self.assertIn("target", doc)
            self.assertTrue(doc["version"])

    def test_audit_rules_engine_validates_json_rules(self):
        report = audit_rules_engine()
        self.assertEqual(report["invalid_files_count"], 0, f"Errors: {report['errors']}")
        self.assertGreaterEqual(report["valid_files_count"], 18)
        self.assertGreaterEqual(report["total_rules_count"], 800)

    def test_analyze_report_quality_html(self):
        valid = "<html><head><script>function toggleDarkMode(){}</script></head><body><svg></svg></body></html>"
        ok, _ = analyze_report_quality("t.html", content_str=valid)
        self.assertTrue(ok)
        ok, msg = analyze_report_quality("t.html", content_str="<html><body>No svg</body></html>")
        self.assertFalse(ok)
        self.assertIn("SVG", msg)

    def test_analyze_report_quality_json_and_xml(self):
        valid_j = json.dumps({"benchmark": "mysql80", "results": []})
        self.assertTrue(analyze_report_quality("t.json", content_str=valid_j)[0])
        self.assertFalse(analyze_report_quality("t.json", content_str="{bad json}")[0])
        self.assertTrue(analyze_report_quality("t.xml", content_str="<audit/>")[0])
        self.assertFalse(analyze_report_quality("t.xml", content_str="<bad")[0])

    def test_analyze_report_quality_txt(self):
        valid_t = "CIS BENCHMARK AUDIT REPORT - MYSQL\nCATEGORY BREAKDOWN & COMPLIANCE SUMMARY TABLE\n"
        self.assertTrue(analyze_report_quality("t.txt", content_str=valid_t)[0])
        self.assertFalse(analyze_report_quality("t.txt", content_str="Invalid text")[0])

    def test_rhel_engines_and_ssh_warn_regex(self):
        import audit_cis_rhel_8, audit_cis_rhel_9, audit_cis_rhel_10, re, tempfile, xml.etree.ElementTree as ET
        from scripts.clean_ssh_warnings_from_reports import SSH_WARN_PAT
        res = [{"id": "1", "category": "A", "status": "PASS"}, {"id": "2", "category": "A", "status": "FAIL"}]
        for mod in (audit_cis_rhel_8, audit_cis_rhel_9, audit_cis_rhel_10):
            score, cats = mod.calculate_scores(res)
            self.assertEqual(score, 50.0)
            with tempfile.TemporaryDirectory() as td:
                out = os.path.join(td, "r.html")
                mod.generate_html_report(res, score, cats, filename=out)
                with open(out, encoding="utf-8") as f:
                    self.assertIn("<svg", f.read())
        j = json.loads(re.sub(SSH_WARN_PAT, "", '{"e": "Warning: Permanently added \'127.0.0.1\' (ED25519) to the list of known hosts.", "c": 0}'))
        self.assertEqual(j["e"], "")
        x = ET.fromstring(re.sub(SSH_WARN_PAT, "", '<testsuite><testcase><error>Warning: Permanently added \'10.0.0.1\' (ED25519) to the list of known hosts.</error></testcase></testsuite>'))
        self.assertEqual(x.tag, "testsuite")

    def test_all_audit_engines_have_utf8_stream_reconfiguration(self):
        """Verify all 18 CIS audit engines reconfigure stdout and stderr for UTF-8."""
        import glob
        engines = sorted(glob.glob("audit_cis_*.py"))
        self.assertEqual(len(engines), 18)
        for eng in engines:
            with open(eng, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("sys.stdout.reconfigure", content, f"{eng} missing stdout.reconfigure")
            self.assertIn("sys.stderr.reconfigure", content, f"{eng} missing stderr.reconfigure")


if __name__ == "__main__":
    unittest.main()
