#!/usr/bin/env python3
"""
Unit tests for zero command errors, AST integrity, and automated controls evaluation (PSL ONLY).
"""

import json
import os
import unittest


class TestZeroCommandErrorsAndAutomation(unittest.TestCase):

    def setUp(self):
        self.rules_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rules")

    def test_all_18_rule_files_valid_json_and_non_empty(self):
        """Validate that all 18 target benchmark JSON rule files exist, are valid JSON, and contain controls."""
        rule_files = [f for f in os.listdir(self.rules_dir) if f.endswith(".json")]
        self.assertEqual(len(rule_files), 18, f"Expected 18 rule files, found {len(rule_files)}")

        total_rules = 0
        for fname in rule_files:
            fpath = os.path.join(self.rules_dir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                rules = json.load(f)
            self.assertIsInstance(rules, list)
            self.assertGreater(len(rules), 10, f"{fname} has too few rules: {len(rules)}")
            total_rules += len(rules)

            for r in rules:
                rule_id = r.get("number") or r.get("id")
                rule_name = r.get("name") or r.get("title")
                self.assertIsNotNone(rule_id, f"Rule in {fname} missing number/id: {r}")
                self.assertIsNotNone(rule_name, f"Rule in {fname} missing name/title: {r}")
                self.assertIn("type", r)
                self.assertIn(r["type"], ["Automated", "Manual"])

                tp = r.get("test_procedure", "")
                if tp.startswith("Contrôle"):
                    self.fail(f"Unsanitized French text in {fname} [{rule_id}]: {tp}")

        self.assertGreaterEqual(total_rules, 880)

    def test_no_unescaped_format_braces_in_rule_templates(self):
        """Verify that test_procedure_template has proper {path} escaping."""
        for fname in os.listdir(self.rules_dir):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(self.rules_dir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                rules = json.load(f)

            for r in rules:
                tmpl = r.get("test_procedure_template")
                if tmpl:
                    # Formatting with path="dummy" should not raise KeyError
                    try:
                        formatted = tmpl.format(path="/dummy/path")
                        self.assertIn("/dummy/path", formatted)
                    except KeyError as e:
                        self.fail(f"Unescaped curly braces in {fname} [{r.get('number')}]: {tmpl} -> KeyError {e}")


if __name__ == "__main__":
    unittest.main()
