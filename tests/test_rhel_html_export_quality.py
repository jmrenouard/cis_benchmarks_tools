#!/usr/bin/env python3
"""Unit tests for RHEL HTML report generation and category score calculation (PSL ONLY)."""

import os
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import audit_cis_rhel_8
import audit_cis_rhel_9
import audit_cis_rhel_10


class TestRhelHtmlExportQuality(unittest.TestCase):
    """Test suite verifying RHEL 8, 9, 10 category scores and report generation."""

    def setUp(self):
        self.mods = [audit_cis_rhel_8, audit_cis_rhel_9, audit_cis_rhel_10]
        self.sample = [
            {"id": "1.1", "category": "Setup", "type": "Automated", "status": "PASS"},
            {"id": "1.2", "category": "Setup", "type": "Automated", "status": "FAIL"},
            {"id": "2.1", "category": "Services", "type": "Automated", "status": "PASS"},
            {"id": "2.2", "category": "Services", "type": "Automated", "status": "ERROR"},
            {"id": "3.1", "category": "Logging", "type": "Manual", "status": "MANUAL"},
        ]

    def test_calculate_scores_populates_category_scores(self):
        for mod in self.mods:
            score, cats = mod.calculate_scores(self.sample)
            self.assertEqual(score, 50.0)
            self.assertIn("Setup", cats)
            self.assertEqual(cats["Setup"]["passed_automated"], 1)
            self.assertEqual(cats["Setup"]["failed_automated"], 1)
            self.assertEqual(cats["Setup"]["score"], 50.0)
            self.assertEqual(cats["Services"]["error_checks"], 1)
            self.assertEqual(cats["Logging"]["manual_checks"], 1)

    def test_build_inline_svg_category_chart_signatures(self):
        for mod in self.mods:
            _, cats = mod.calculate_scores(self.sample)
            self.assertIn("Setup", mod.build_inline_svg_category_chart(cats))
            self.assertIn("CatA", mod.build_inline_svg_category_chart(["CatA"], [1], [0], [0], [0]))

    def test_generate_html_and_txt_reports(self):
        for mod in self.mods:
            score, cats = mod.calculate_scores(self.sample)
            with tempfile.TemporaryDirectory() as td:
                h_path = os.path.join(td, "r.html")
                mod.generate_html_report(self.sample, score, cats, filename=h_path)
                with open(h_path, encoding="utf-8") as f:
                    self.assertIn("<svg", f.read())

                t_path = os.path.join(td, "r.txt")
                mod.export_results(self.sample, score, cats, target_name="RHEL", filename=t_path, fmt="txt")
                with open(t_path, encoding="utf-8") as f:
                    txt = f.read()
                    self.assertIn("CATEGORY BREAKDOWN", txt)
                    self.assertIn("Setup", txt)


if __name__ == "__main__":
    unittest.main()
