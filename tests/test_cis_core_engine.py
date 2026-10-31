#!/usr/bin/env python3
"""Unit tests for cis_core_engine.py (Finding 9, PSL ONLY)."""
import json, os, sys, tempfile, unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cis_core_engine as core


class TestCisCoreEngine(unittest.TestCase):
    def test_scores_tuple_dual_unpacking(self):
        res = {"1. Log": [{"status": "PASS"}, {"status": "FAIL"}], "2. Auth": [{"status": "PASS"}, {"status": "N/A"}]}
        sc = core.calculate_scores(res)
        self.assertIsInstance(sc, (core.AuditScoresTuple, tuple))
        ov, cats = sc[:2]
        self.assertEqual((ov, sc.overall_score, sc.categories_scores), (75.0, 75.0, cats))
        o, c, man, err, na, p, f, e2, na2, lj, pj, fj, ej, naj = sc
        self.assertEqual((o, p, f, na), (75.0, 2, 1, 1))
        self.assertEqual(json.loads(lj), ["1. Log", "2. Auth"])

    def test_flat_list_results_rhel_style(self):
        sc = core.calculate_scores([{"category": "FS", "status": "PASS"}, {"category": "Log", "status": "FAIL"}])
        self.assertEqual((sc[0], sc[1]["FS"]["score"]), (50.0, 100.0))

    def test_svg_donut_and_category_charts(self):
        self.assertIn("80.0%", core.build_inline_svg_donut_chart(4, 1, 0, 1, 80.0))
        self.assertIn("FS", core.build_inline_svg_category_chart({"FS": {"score": 100.0}}))
        self.assertIn("Net", core.build_inline_svg_category_chart(["Net"], [3], [1], [0], [0]))

    def test_evaluate_condition_rules(self):
        cases = [
            ({"type": "returncode_zero"}, "", 0, True), ({"type": "returncode_zero"}, "", 1, False),
            ({"type": "stdout_contains", "value": "a"}, "a", 0, True),
            ({"type": "stdout_regex_match", "pattern": r"\d+"}, "1", 0, True),
            ({"type": "stdout_is_numeric_greater_than", "value": 5}, "9", 0, True),
            ({"type": "stdout_is_numeric_less_equal", "value": 50}, "9", 0, True),
            ({"type": "stdout_not_empty"}, " ", 0, False), ({"type": "stdout_is_empty"}, "", 0, True),
        ]
        for c, o, cd, exp in cases: self.assertEqual(core.evaluate_condition(c, o, "", cd), exp)

    def test_is_valid_executable_command(self):
        self.assertTrue(core.is_valid_executable_command("cat /etc/issue") and core.is_valid_executable_command("/bin/cat /etc/issue"))
        self.assertFalse(core.is_valid_executable_command("Verify") or core.is_valid_executable_command(""))

    def test_base_audit_engine_lifecycle_and_export(self):
        eng = core.BaseAuditEngine("m106", "MariaDB 10.6")
        res = {"Gen": [{"id": "1", "status": "PASS"}]}
        sc = eng.calculate_scores(res)
        self.assertEqual(sc.overall_score, 100.0)
        with tempfile.TemporaryDirectory() as td:
            j, x = os.path.join(td, "r.json"), os.path.join(td, "r.xml")
            eng.export(res, sc.overall_score, sc.categories_scores, filename=j, fmt="json")
            eng.export(res, sc.overall_score, sc.categories_scores, filename=x, fmt="xml")
            self.assertTrue(os.path.exists(j) and os.path.exists(x))
            with open(j, "r", encoding="utf-8") as f: self.assertEqual(json.load(f)["overall_score"], 100.0)

    def test_run_command_fallback_and_executor(self):
        with patch("subprocess.run") as m:
            m.return_value = MagicMock(stdout="ok", stderr="", returncode=0)
            self.assertEqual(core.run_command("echo ok", db_password="secret"), ("ok", "", 0))


if __name__ == "__main__":
    unittest.main()
