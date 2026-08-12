#!/usr/bin/env python3
"""
Unit tests for MySQL CIS Benchmark Audit Engine & Docker Auto-Routing (PSL ONLY).
"""

import json
import unittest
from unittest.mock import MagicMock, patch

import audit_cis_mysql_80 as mysql_80


class TestMySQLAuditEngine(unittest.TestCase):

    def setUp(self):
        with open("rules/mysql_80.json", "r", encoding="utf-8") as f:
            self.rules_80 = json.load(f)

    def test_rules_structure_and_types(self):
        """Validate JSON rules structure and automated rule conversion."""
        for rule in self.rules_80:
            self.assertIn("number", rule)
            self.assertIn("name", rule)
            self.assertIn("type", rule)

    @patch("audit_cis_mysql_80.run_command")
    def test_detect_docker_container_active(self, mock_run):
        """Test Docker container auto-detection when a container is active."""
        mock_run.return_value = ("mysql-test-container", "", 0)
        container = mysql_80.detect_docker_container()
        self.assertEqual(container, "mysql-test-container")

    @patch("subprocess.run")
    def test_run_command_docker_wrapping(self, mock_sub):
        """Test that run_command automatically wraps CLI commands inside docker exec when container is specified."""
        mock_process = MagicMock()
        mock_process.stdout = "1\n"
        mock_process.stderr = ""
        mock_process.returncode = 0
        mock_sub.return_value = mock_process

        out, err, ret = mysql_80.run_command("SELECT @@datadir;", docker_container="my_mysql")
        self.assertEqual(ret, 0)
        self.assertEqual(out, "1")
        called_args = mock_sub.call_args[0][0]
        self.assertIn("docker exec -i my_mysql", called_args[2])


if __name__ == "__main__":
    unittest.main()
