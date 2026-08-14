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

    def test_all_18_engines_zero_errors_and_authentic_cis_distribution(self):
        """Simulate and verify that all 18 target engines return 0 command errors and authentic CIS manual counts under Docker mode."""
        import importlib
        import inspect
        from unittest.mock import patch

        audit_modules = [
            ("audit_cis_mysql_80", "mysql_80", 25),
            ("audit_cis_mysql_community_84", "mysql_community_84", 31),
            ("audit_cis_mysql_enterprise_84", "mysql_enterprise_84", 26),
            ("audit_cis_mysql_community_97", "mysql_community_97", 25),
            ("audit_cis_mysql_enterprise_97", "mysql_enterprise_97", 26),
            ("audit_cis_mariadb_106", "mariadb_106", 29),
            ("audit_cis_mariadb_1011", "mariadb_1011", 30),
            ("audit_cis_postgresql_16", "postgresql_16", 29),
            ("audit_cis_postgresql_17", "postgresql_17", 28),
            ("audit_cis_postgresql_18", "postgresql_18", 28),
            ("audit_cis_mongodb_7", "mongodb_7", 11),
            ("audit_cis_mongodb_8", "mongodb_8", 11),
            ("audit_cis_cassandra_40", "cassandra_40", 8),
            ("audit_cis_cassandra_41", "cassandra_41", 8),
            ("audit_cis_cassandra_50", "cassandra_50", 8),
            ("audit_cis_rhel_8", "rhel_8", 0),
            ("audit_cis_rhel_9", "rhel_9", 0),
            ("audit_cis_rhel_10", "rhel_10", 0),
        ]

        def mock_run_cmd(cmd, remote_host=None, docker_container=None, **kwargs):
            return ("1", "", 0)

        total_manuals = 0
        total_errors = 0

        for mod_name, target_key, expected_manual_cnt in audit_modules:
            mod = importlib.import_module(mod_name)
            rules = mod.load_recommendations(target_key)

            with patch.object(mod, "run_command", side_effect=mock_run_cmd):
                sig = inspect.signature(mod.perform_checks)
                if "docker_container" in sig.parameters:
                    results = mod.perform_checks(rules, docker_container="simulated-container")
                else:
                    results = mod.perform_checks(rules)

                flat_checks = []
                if isinstance(results, dict):
                    for cat_list in results.values():
                        flat_checks.extend(cat_list)
                elif isinstance(results, list):
                    flat_checks = results

                manuals = [r for r in flat_checks if r.get("status") == "Manual"]
                errors = [r for r in flat_checks if r.get("status") == "Error"]
                total_manuals += len(manuals)
                total_errors += len(errors)

                self.assertEqual(len(errors), 0, f"Found unexpected error checks in {mod_name}: {[e.get('number') for e in errors]}")
                self.assertEqual(len(manuals), expected_manual_cnt, f"Expected {expected_manual_cnt} manual checks in {mod_name}, got {len(manuals)}")

        self.assertEqual(total_errors, 0, "Total command errors across all engines must be 0")
        self.assertEqual(total_manuals, 323, "Total manual checks across all 18 targets must be 323")


if __name__ == "__main__":
    unittest.main()

