#!/usr/bin/env python3
"""
Unit tests for Cassandra CIS Benchmark Audit Engine & Docker Auto-Routing (PSL ONLY).
"""

import json
import unittest
from unittest.mock import MagicMock, patch

import audit_cis_cassandra_40 as cassandra_40


class TestCassandraAuditEngine(unittest.TestCase):

    def setUp(self):
        with open("rules/cassandra_40.json", "r", encoding="utf-8") as f:
            self.rules_40 = json.load(f)

    def test_rules_structure_and_types(self):
        """Validate JSON rules structure."""
        for rule in self.rules_40:
            self.assertIn("number", rule)
            self.assertIn("name", rule)
            self.assertIn("type", rule)

    @patch("audit_cis_cassandra_40.run_command")
    def test_detect_docker_container_active(self, mock_run):
        """Test Docker container auto-detection when a container is active."""
        mock_run.return_value = ("cassandra-test-container", "", 0)
        container = cassandra_40.detect_docker_container()
        self.assertEqual(container, "cassandra-test-container")


if __name__ == "__main__":
    unittest.main()
