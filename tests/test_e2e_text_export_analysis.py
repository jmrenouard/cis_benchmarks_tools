#!/usr/bin/env python3
"""
Comprehensive End-to-End (E2E) Text Export & Analysis Test Suite (PSL ONLY).
Validates that every target audit produces structured, compliant .txt text exports,
verifies that parsed reports contain 0 execution errors, and confirms authentic CIS manual distribution.
"""

import importlib
import inspect
import os
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import audit_cis
from scripts.analyze_e2e_reports import parse_txt_report

# Expected authentic CIS benchmark rule counts & manual controls distribution (887 rules total)
AUTHENTIC_CIS_DISTRIBUTION = {
    "mysql_80": {"total": 70, "manual": 25, "auto": 45},
    "mysql_community_84": {"total": 79, "manual": 31, "auto": 48},
    "mysql_enterprise_84": {"total": 70, "manual": 26, "auto": 44},
    "mysql_community_97": {"total": 70, "manual": 25, "auto": 45},
    "mysql_enterprise_97": {"total": 70, "manual": 26, "auto": 44},
    "mariadb_106": {"total": 74, "manual": 29, "auto": 45},
    "mariadb_1011": {"total": 75, "manual": 30, "auto": 45},
    "postgresql_16": {"total": 71, "manual": 29, "auto": 42},
    "postgresql_17": {"total": 71, "manual": 28, "auto": 43},
    "postgresql_18": {"total": 71, "manual": 28, "auto": 43},
    "mongodb_7": {"total": 23, "manual": 11, "auto": 12},
    "mongodb_8": {"total": 23, "manual": 11, "auto": 12},
    "cassandra_40": {"total": 20, "manual": 8, "auto": 12},
    "cassandra_41": {"total": 20, "manual": 8, "auto": 12},
    "cassandra_50": {"total": 20, "manual": 8, "auto": 12},
    "rhel_8": {"total": 20, "manual": 0, "auto": 20},
    "rhel_9": {"total": 20, "manual": 0, "auto": 20},
    "rhel_10": {"total": 20, "manual": 0, "auto": 20},
}


class TestE2ETextExportAndAnalysis(unittest.TestCase):

    def test_e2e_text_export_and_analysis_all_18_targets(self):
        """Execute audit text export across all 18 targets, parse .txt output, and assert 0 errors."""
        def mock_cmd(cmd, *args, **kwargs):
            return ("1", "", 0)

        for target_key, expected in AUTHENTIC_CIS_DISTRIBUTION.items():
            with self.subTest(target=target_key):
                mod_name = f"audit_cis_{target_key}"
                try:
                    mod = importlib.import_module(mod_name)
                except ImportError as e:
                    self.fail(f"Failed to import {mod_name}: {e}")

                rules = mod.load_recommendations(target_key)
                self.assertEqual(len(rules), expected["total"], f"Rule count mismatch for {target_key}")

                # Simulate successful container/environment execution for mock checks
                with patch.object(mod, "run_command", side_effect=mock_cmd):
                    sig = inspect.signature(mod.perform_checks)
                    if "docker_container" in sig.parameters:
                        check_results = mod.perform_checks(rules, docker_container="simulated-container")
                    else:
                        check_results = mod.perform_checks(rules)

                overall_score, cat_scores, *rest = mod.calculate_scores(check_results)

                # Export to temporary .txt file
                with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
                    tmp_path = tmp.name

                try:
                    mod.export_results(
                        check_results,
                        overall_score,
                        cat_scores,
                        target_name=target_key,
                        filename=tmp_path,
                        fmt="txt",
                        lang="en"
                    )

                    self.assertTrue(os.path.exists(tmp_path))
                    self.assertGreater(os.path.getsize(tmp_path), 200)

                    with open(tmp_path, "r", encoding="utf-8") as f:
                        text_content = f.read()

                    # Header assertions
                    self.assertIn("CIS BENCHMARK AUDIT REPORT", text_content)
                    self.assertIn("Report Date", text_content)
                    self.assertIn("Global Score", text_content)
                    self.assertIn("CATEGORY BREAKDOWN & COMPLIANCE SUMMARY TABLE", text_content)
                    self.assertIn("DETAILED CONTROL RESULTS", text_content)

                    # Parse and analyze text report structure
                    parsed = parse_txt_report(tmp_path)
                    self.assertEqual(parsed["total"], expected["total"])
                    self.assertEqual(parsed["manual"], expected["manual"], f"Manual count mismatch for {target_key}")
                    self.assertEqual(parsed["error"], 0, f"Command execution errors detected in {target_key} text report: {parsed['error']}")

                    # Check status occurrences directly in raw text
                    error_matches = re.findall(r"^\[ERROR\]", text_content, re.MULTILINE)
                    self.assertEqual(len(error_matches), 0, f"Found [ERROR] entries in text output for {target_key}")

                    manual_matches = re.findall(r"^\[MANUAL\]", text_content, re.MULTILINE)
                    self.assertEqual(len(manual_matches), expected["manual"], f"Raw [MANUAL] count mismatch in text for {target_key}")

                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

    def test_live_docker_mysql80_text_export_and_analysis_if_running(self):
        """If mysql80-test Docker container is running, execute live audit with text export and verify 0 errors."""
        res = subprocess.run(["docker", "ps", "-q", "-f", "name=mysql80-test"], capture_output=True, text=True)
        if not res.stdout.strip():
            self.skipTest("mysql80-test Docker container is not currently running")

        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            live_txt_path = tmp.name

        try:
            cmd = [
                sys.executable,
                os.path.join(REPO_ROOT, "audit_cis_mysql_80.py"),
                "-f", "txt",
                "-o", live_txt_path,
                "--docker", "mysql80-test"
            ]
            exec_res = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(exec_res.returncode, 0, f"Live audit failed: {exec_res.stderr}")

            parsed = parse_txt_report(live_txt_path)
            self.assertEqual(parsed["total"], 70)
            self.assertEqual(parsed["error"], 0, f"Live Docker execution produced errors: {parsed['error']}")
            self.assertEqual(parsed["pass"], 22)
            self.assertEqual(parsed["fail"], 18)
            self.assertEqual(parsed["manual"], 23)
            self.assertEqual(parsed["na"], 7)
        finally:
            if os.path.exists(live_txt_path):
                os.remove(live_txt_path)


if __name__ == "__main__":
    unittest.main()
