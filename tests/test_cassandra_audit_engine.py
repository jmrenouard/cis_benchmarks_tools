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

    def test_control_3_2_no_hardcoded_password_in_command(self):
        """Verify control 3.2 does not leak default password on CLI."""
        import audit_cis_cassandra_41 as cassandra_41
        import audit_cis_cassandra_50 as cassandra_50

        for mod in (cassandra_40, cassandra_41, cassandra_50):
            rule_32 = next(r for r in mod.RECOMMENDATIONS_DATA if r.get("number") == "3.2")
            self.assertNotIn("-p cassandra", rule_32["test_procedure"])

        for path in ("rules/cassandra_40.json", "rules/cassandra_41.json", "rules/cassandra_50.json"):
            with open(path, "r", encoding="utf-8") as f:
                rules = json.load(f)
            rule_32 = next(r for r in rules if r.get("number") == "3.2")
            self.assertNotIn("-p cassandra", rule_32["test_procedure"])


if __name__ == "__main__":
    unittest.main()
