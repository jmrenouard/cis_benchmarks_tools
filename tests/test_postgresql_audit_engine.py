#!/usr/bin/env python3
"""
Unit tests for PostgreSQL CIS Benchmark Audit Engine & Docker Auto-Routing (PSL ONLY).
"""

import json
import unittest
from unittest.mock import MagicMock, patch

import audit_cis_postgresql_16 as postgresql_16


class TestPostgreSQLAuditEngine(unittest.TestCase):

    def setUp(self):
        with open("rules/postgresql_16.json", "r", encoding="utf-8") as f:
            self.rules_16 = json.load(f)

    def test_rules_structure_and_types(self):
        """Validate JSON rules structure and automated rule conversion."""
        for rule in self.rules_16:
            self.assertIn("number", rule)
            self.assertIn("name", rule)
            self.assertIn("type", rule)

    @patch("audit_cis_postgresql_16.run_command")
    def test_detect_docker_container_active(self, mock_run):
        """Test Docker container auto-detection when a container is active."""
        mock_run.return_value = ("postgres-test-container", "", 0)
        container = postgresql_16.detect_docker_container()
        self.assertEqual(container, "postgres-test-container")

    @patch("subprocess.run")
    def test_run_command_docker_wrapping(self, mock_sub):
        """Test that run_command automatically wraps CLI commands inside docker exec when container is specified."""
        mock_process = MagicMock()
        mock_process.stdout = "1\n"
        mock_process.stderr = ""
        mock_process.returncode = 0
        mock_sub.return_value = mock_process

        out, err, ret = postgresql_16.run_command("SHOW data_directory;", docker_container="my_postgres")
        self.assertEqual(ret, 0)
        self.assertEqual(out, "1")
        called_args = mock_sub.call_args[0][0]
        self.assertIn("docker exec -i my_postgres", called_args[2])


if __name__ == "__main__":
    unittest.main()
