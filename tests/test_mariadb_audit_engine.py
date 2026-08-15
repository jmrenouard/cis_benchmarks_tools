#!/usr/bin/env python3
"""
Unit tests for MariaDB CIS Benchmark Audit Engine & Docker Auto-Routing (PSL ONLY).
"""

import json
import unittest
from unittest.mock import MagicMock, patch

import audit_cis_mariadb_1011 as mariadb_1011
import audit_cis_mariadb_106 as mariadb_106


class TestMariaDBAuditEngine(unittest.TestCase):

    def setUp(self):
        with open("rules/mariadb_1011.json", "r", encoding="utf-8") as f:
            self.rules_1011 = json.load(f)
        with open("rules/mariadb_106.json", "r", encoding="utf-8") as f:
            self.rules_106 = json.load(f)

    def test_rules_structure_and_types(self):
        """Validate JSON rules structure and authentic CIS rule types."""
        for rule in self.rules_1011:
            self.assertIn("number", rule)
            self.assertIn("name", rule)
            self.assertIn("type", rule)
            self.assertIn(rule["type"], ["Automated", "Manual"])
            if rule["number"] in ["1.2", "1.3", "1.4", "1.5", "1.6"]:
                self.assertEqual(rule["type"], "Automated", f"Rule {rule['number']} should be Automated")
            if rule["number"] in ["1.1", "1.7", "2.4", "5.1", "5.2", "5.3"]:
                self.assertEqual(rule["type"], "Manual", f"Rule {rule['number']} should be Manual per CIS spec")

    @patch("audit_cis_mariadb_1011.run_command")
    def test_detect_docker_container_active(self, mock_run):
        """Test Docker container auto-detection when a container is active."""
        mock_run.return_value = ("mariadb-test-container", "", 0)
        container = mariadb_1011.detect_docker_container()
        self.assertEqual(container, "mariadb-test-container")

    @patch("audit_cis_mariadb_1011.run_command")
    def test_detect_docker_container_none(self, mock_run):
        """Test Docker container auto-detection when no container is running."""
        mock_run.return_value = ("", "", 1)
        container = mariadb_1011.detect_docker_container()
        self.assertIsNone(container)

    @patch("subprocess.run")
    def test_run_command_docker_wrapping(self, mock_sub):
        """Test that run_command automatically wraps CLI commands inside docker exec when container is specified."""
        mock_process = MagicMock()
        mock_process.stdout = "1\n"
        mock_process.stderr = ""
        mock_process.returncode = 0
        mock_sub.return_value = mock_process

        out, err, ret = mariadb_1011.run_command("SELECT @@datadir;", docker_container="my_mariadb")
        self.assertEqual(ret, 0)
        self.assertEqual(out, "1")
        # Check command args passed to subprocess.run
        called_args = mock_sub.call_args[0][0]
        self.assertIn("docker exec -i my_mariadb", called_args[2])

    @patch("audit_cis_mariadb_1011.run_command")
    def test_perform_checks_zero_execution_errors(self, mock_run):
        """Ensure perform_checks handles command failures cleanly without throwing exceptions."""
        mock_run.return_value = ("", "ERROR 1045 (28000): Access denied for user", 1)
        
        sample_rules = [
            {
                "category": "1. Configuration",
                "number": "1.1",
                "name": "Datadir partition",
                "type": "Automated",
                "path_command": "mysql -N -B -e \"SELECT @@datadir;\"",
                "test_procedure_template": "df -P {path}",
                "expected_output": {"type": "stdout_not_equals", "value": "/"},
                "remediation": "Move datadir"
            }
        ]

        results = mariadb_1011.perform_checks(sample_rules)
        self.assertIn("1. Configuration", results)
        check_res = results["1. Configuration"][0]
        self.assertEqual(check_res["status"], "Error")
        self.assertIn("Error lors de l'obtention du chemin", check_res["output"])

    def test_evaluate_condition_stdout_equals(self):
        """Test evaluate_condition stdout_equals."""
        cond = {"type": "stdout_equals", "value": "0"}
        self.assertTrue(mariadb_1011.evaluate_condition(cond, "0", "", 0))
        self.assertFalse(mariadb_1011.evaluate_condition(cond, "1", "", 0))

    def test_evaluate_condition_stdout_contains_any(self):
        """Test evaluate_condition stdout_contains_any."""
        cond = {"type": "stdout_contains_any", "values": ["ACTIVE", "ENABLED"]}
        self.assertTrue(mariadb_1011.evaluate_condition(cond, "ACTIVE", "", 0))
    @patch("audit_cis_mariadb_1011.run_command")
    def test_perform_checks_empty_path_command_returns_not_applicable(self, mock_run):
        """Ensure perform_checks sets Not Applicable when path_command returns empty string with returncode 0."""
        mock_run.return_value = ("", "", 0)
        
        sample_rules = [
            {
                "category": "3. Permissions Fichiers",
                "number": "3.3",
                "name": "Permissions sur 'log_error'",
                "type": "Automated",
                "path_command": "mysql -N -B -e \"SELECT @@log_error;\"",
                "test_procedure_template": "stat -c '%a' {path}",
                "expected_output": {"type": "stdout_regex_match", "pattern": r"^6[04]0$"},
                "remediation": "Appliquer des permissions restrictives (ex: 640 ou 600)."
            }
        ]

        results = mariadb_1011.perform_checks(sample_rules)
        self.assertIn("3. Permissions Fichiers", results)
        check_res = results["3. Permissions Fichiers"][0]
        self.assertEqual(check_res["status"], "Not Applicable")
        self.assertIn("non configuré", check_res["output"].lower())

    def test_mysql_history_rule_syntax(self):
        """Verify that rule 1.3 for mysql_history in MariaDB rules includes ; true for clean 0 exit code."""
        rule_106_13 = next((r for r in self.rules_106 if r.get("number") == "1.3"), None)
        self.assertIsNotNone(rule_106_13)
        self.assertTrue(rule_106_13["test_procedure"].endswith("; true"), "Rule 1.3 in mariadb_106 must end with '; true'")

        rule_1011_13 = next((r for r in self.rules_1011 if r.get("number") == "1.3"), None)
        self.assertIsNotNone(rule_1011_13)
        self.assertTrue(rule_1011_13["test_procedure"].endswith("; true"), "Rule 1.3 in mariadb_1011 must end with '; true'")


if __name__ == "__main__":
    unittest.main()
