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
        self.assertAlmostEqual(ov, 200.0 / 3.0, places=4)
        self.assertEqual((sc.overall_score, sc.categories_scores, cats["1. Log"]["score"], cats["2. Auth"]["score"]), (ov, cats, 50.0, 100.0))
        o, c, man, err, na, p, f, e2, na2, lj, pj, fj, ej, naj = sc
        self.assertEqual((o, p, f, na, json.loads(lj)), (ov, 2, 1, 1, ["1. Log", "2. Auth"]))

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

    def test_finding_10_numeric_and_none_conditions(self):
        tc = lambda t, v=None, **kw: dict(type=t, **({"value": v} if v is not None else {}), **kw)
        gt, le = (lambda v: tc("stdout_is_numeric_greater_than", v)), (lambda v: tc("stdout_is_numeric_less_equal", v))
        cases = [
            (gt(0), "Warn 10.6\n0", False), (gt(0), "Warn 10.6\n5", True), (le(365), "Warn 10.6\n0", False), (le(365), "Warn 10.6\n90", True),
            (gt(0), "error 404", False), (le(365), "HTTP/1.1 200 OK", False), (gt(-10), "-5", True), (gt(0), "-5", False),
            (le(365), "-1", False), (le(365), "0", False), (tc("stdout_is_numeric_greater_than"), "10", False), (gt(None), "10", False),
            (tc("stdout_is_numeric_less_equal"), "10", False), (le(None), "10", False), (gt("5"), "10", True), (gt("bad"), "10", False),
            (gt(5), "bad", False), (gt(5), "", False), (tc("stdout_contains", None), "none", False),
            (tc("stdout_not_contains", None), "ok", False), (tc("stdout_equals", None), "None", False),
            (tc("stdout_not_equals", None), "ok", False), (tc("stdout_contains_any", values=None), "ok", False),
            (tc("stdout_not_contains_any", values=None), "ok", False), (tc("stdout_regex_match", pattern="["), "ok", False),
            (tc("all_lines_match_regex", patterns=[r"PEM:", r"CA:"]), "PEM: /ssl\nCA: /ca", True),
            (tc("all_lines_match_regex", patterns=[r"PEM:", r"CA:"]), "PEM: /ssl\nother", False),
            (tc("all_lines_match_regex", patterns=[]), "PEM: /ssl", False),
        ]
        for c, o, exp in cases: self.assertEqual(core.evaluate_condition(c, o, "", 0), exp)

    def test_finding_3_compliance_scoring_standardization(self):
        sc_a = core.calculate_scores({"1. Benchmark": [{"status": "FAIL"}] + [{"status": "N/A"}] * 9})
        self.assertEqual((sc_a.overall_score, sc_a.categories_scores["1. Benchmark"]["score"], sc_a.categories_scores["1. Benchmark"]["total_automated"], sc_a.categories_scores["1. Benchmark"]["na_checks"]), (0.0, 0.0, 1, 9))
        self.assertEqual((core.calculate_scores([{"status": "PASS"}, {"status": "FAIL"}] + [{"status": "NOT APPLICABLE"}] * 8).overall_score, core.calculate_scores([{"status": "N/A"}] * 10).overall_score), (50.0, 0.0))
        sc_d = core.calculate_scores([{"status": "PASS"}, {"status": "FAIL"}, {"status": "MANUAL", "type": "Manual"}, {"status": "ERROR"}])
        self.assertEqual((sc_d.overall_score, sc_d[2], sc_d[3], core.calculate_scores({}).overall_score), (50.0, 1, 1, 0.0))
        p, f, na, m = {"status": "PASS"}, {"status": "FAIL"}, {"status": "N/A"}, {"status": "MANUAL", "type": "Manual"}
        sc_f = core.calculate_scores({"Auth": [p]*8 + [f]*2 + [na]*5 + [m]*3, "Storage": [na]*4 + [m]*2, "Network": [p]*2 + [na]})
        self.assertEqual((sc_f.categories_scores["Auth"]["score"], sc_f.categories_scores["Storage"]["score"], sc_f.categories_scores["Network"]["score"]), (80.0, 0.0, 100.0))
        self.assertAlmostEqual(sc_f.overall_score, 1000.0 / 12.0, places=4)
        self.assertIn("Auth: 50.0%", core.build_inline_svg_category_chart(["Auth"], [1], [1], [2], [5]))


if __name__ == "__main__":
    unittest.main()
