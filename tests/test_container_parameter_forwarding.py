#!/usr/bin/env python3
"""Unit tests for docker_container forwarding in automated checks (PSL ONLY)."""

import os, sys, unittest
from unittest.mock import patch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import audit_cis_postgresql_16, audit_cis_postgresql_17, audit_cis_postgresql_18
import audit_cis_mongodb_7, audit_cis_mongodb_8
import audit_cis_cassandra_40, audit_cis_cassandra_41, audit_cis_cassandra_50


class TestContainerParameterForwarding(unittest.TestCase):
    def test_all_engines_forward_docker_container(self):
        targets = [
            (audit_cis_postgresql_16, "General", "psql -c 'SELECT 1;'"),
            (audit_cis_postgresql_17, "General", "psql -c 'SELECT 1;'"),
            (audit_cis_postgresql_18, "General", "psql -c 'SELECT 1;'"),
            (audit_cis_mongodb_7, audit_cis_mongodb_7.RECOMMENDATIONS_DATA[0]["category"], "mongosh --eval 'db.version()'"),
            (audit_cis_mongodb_8, audit_cis_mongodb_8.RECOMMENDATIONS_DATA[0]["category"], "mongosh --eval 'db.version()'"),
            (audit_cis_cassandra_40, audit_cis_cassandra_40.RECOMMENDATIONS_DATA[0]["category"], "nodetool status"),
            (audit_cis_cassandra_41, audit_cis_cassandra_41.RECOMMENDATIONS_DATA[0]["category"], "nodetool status"),
            (audit_cis_cassandra_50, audit_cis_cassandra_50.RECOMMENDATIONS_DATA[0]["category"], "nodetool status"),
        ]
        for mod, cat, cmd in targets:
            recs = [
                {"id": "1", "number": "1", "name": "C1", "category": cat, "type": "Automated", "test_procedure": cmd},
                {"id": "2", "number": "2", "name": "C2", "category": cat, "type": "Automated", "path_command": "echo /p", "test_procedure_template": "cat {path}"}
            ]
            with patch.object(mod, "run_command", return_value=("/p", "", 0)) as m_run:
                mod.perform_checks(recs, docker_container="c-123")
                self.assertGreaterEqual(m_run.call_count, 1)
                for call in m_run.call_args_list:
                    self.assertEqual(call.kwargs.get("docker_container"), "c-123", f"{mod.__name__} dropped container")


if __name__ == "__main__":
    unittest.main()
