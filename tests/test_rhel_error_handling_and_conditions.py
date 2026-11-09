#!/usr/bin/env python3
"""Tests for RHEL 8, 9, 10 error handling, returncode triage, None safety (Finding 4, PSL ONLY)."""
import os, sys, unittest
from unittest.mock import patch
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import audit_cis_rhel_8 as r8, audit_cis_rhel_9 as r9, audit_cis_rhel_10 as r10

class TestRhelErrorHandlingAndConditions(unittest.TestCase):
    def setUp(self):
        self.mods = [r8, r9, r10]

    def test_manual_and_error_triage_and_ssh_safety(self):
        r_man = {"id": "1", "type": "Manual", "audit": "echo m"}
        r_neg = {"id": "2", "type": "Automated", "audit": "lsmod", "condition": {"type": "stdout_not_contains", "value": "c"}}
        for m in self.mods:
            with patch.object(m, "run_command", return_value=("m", "", 0)):
                res = m.perform_checks([r_man])
                self.assertEqual((res[0]["status"], res[0]["type"], res[0]["test_procedure"]), ("MANUAL", "Manual", "echo m"))
            for code, host in [(-1, None), (126, None), (127, None), (255, "h")]:
                with patch.object(m, "run_command", return_value=("", "err", code)):
                    self.assertEqual(m.perform_checks([r_neg], remote_host=host)[0]["status"], "ERROR")
            with patch.object(m, "run_command", return_value=("", "", 1)):
                self.assertEqual(m.perform_checks([r_neg])[0]["status"], "PASS")

    def test_evaluate_condition_and_fallback(self):
        crx = {"type": "stdout_regex_match", "pattern": r"^v\d+"}
        cases = [(None, "o", 0, False), ({}, "o", 0, False),
                 ({"type": "stdout_contains", "value": None}, "o", 0, False),
                 ({"type": "stdout_not_contains", "value": None}, "o", 0, False),
                 ({"type": "stdout_contains", "value": 42}, "42", 0, True),
                 ({"type": "stdout_not_contains", "value": 42}, "x", 0, True),
                 ({"type": "returncode_zero"}, "", 0, True), ({"type": "returncode_zero"}, "", 1, False)]
        for m in self.mods:
            self.assertTrue(m.evaluate_condition(crx, "v2", "", 0) and not m.evaluate_condition(crx, "x", "", 0))
            orig = m.core_evaluate_condition
            try:
                m.core_evaluate_condition = None
                for cond, out, rc, exp in cases:
                    self.assertEqual(m.evaluate_condition(cond, out, "", rc), exp)
            finally:
                m.core_evaluate_condition = orig

    def test_calculate_scores_counts(self):
        c = [{"id": str(i), "category": "S", "type": "Manual" if i == 4 else "Automated", "status": s} for i, s in enumerate(["PASS", "FAIL", "ERROR", "MANUAL"], 1)]
        for m in self.mods:
            _, cats = m.calculate_scores(c)
            self.assertEqual((cats["S"]["passed_automated"], cats["S"]["failed_automated"], cats["S"]["error_checks"], cats["S"]["manual_checks"]), (1, 1, 1, 1))

if __name__ == "__main__":
    unittest.main()
