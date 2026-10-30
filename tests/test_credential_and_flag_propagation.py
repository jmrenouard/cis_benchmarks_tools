#!/usr/bin/env python3
"""Unit tests for credential and flag propagation across engines (PSL ONLY)."""

import ast, os, sys, unittest
from unittest.mock import patch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

ACTIVE_ENGINES = [
    "audit_cis_cassandra_40.py", "audit_cis_cassandra_41.py", "audit_cis_cassandra_50.py",
    "audit_cis_mariadb_106.py", "audit_cis_mariadb_1011.py",
    "audit_cis_mongodb_7.py", "audit_cis_mongodb_8.py",
    "audit_cis_mysql_80.py", "audit_cis_mysql_community_84.py", "audit_cis_mysql_community_97.py",
    "audit_cis_mysql_enterprise_84.py", "audit_cis_mysql_enterprise_97.py",
    "audit_cis_postgresql_16.py", "audit_cis_postgresql_17.py", "audit_cis_postgresql_18.py",
]


class TestCredentialAndFlagPropagation(unittest.TestCase):
    def test_database_engines_pass_credentials_in_main(self):
        expected = {"db_user", "db_password", "db_host", "db_port", "db_name", "defaults_file", "auth_db"}
        for f in ACTIVE_ENGINES:
            with open(os.path.join(REPO_ROOT, f), encoding="utf-8") as src:
                tree = ast.parse(src.read(), filename=f)
            calls = [
                {kw.arg for kw in node.keywords}
                for node in ast.walk(tree)
                if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "perform_checks"
            ]
            self.assertTrue(any(expected.issubset(c) for c in calls), f"{f} drops credentials in __main__")

    def test_perform_checks_forwards_credentials_to_run_command(self):
        import audit_cis_postgresql_16, audit_cis_postgresql_17, audit_cis_postgresql_18, audit_cis_mariadb_106, audit_cis_mariadb_1011, audit_cis_mysql_80, audit_cis_mysql_community_84, audit_cis_mysql_enterprise_84, audit_cis_mysql_community_97
        recs = [{"id": "1", "name": "C1", "category": "General", "type": "Manual", "test_procedure": "echo 1"}]
        for mod in (audit_cis_postgresql_16, audit_cis_postgresql_17, audit_cis_postgresql_18, audit_cis_mariadb_106, audit_cis_mariadb_1011, audit_cis_mysql_80, audit_cis_mysql_community_84, audit_cis_mysql_enterprise_84, audit_cis_mysql_community_97):
            with patch.object(mod, "run_command", return_value=("", "", 0)) as m:
                mod.perform_checks(recs, db_user="u", db_password="p", db_host="h", db_port=5432, db_name="d", defaults_file="f", auth_db="a", ssh_port=2222, ssh_key="/tmp/k", sudo=True)
                self.assertEqual(m.call_args.kwargs.get("db_user"), "u")
                self.assertEqual(m.call_args.kwargs.get("db_password"), "p")
                self.assertEqual(m.call_args.kwargs.get("ssh_port"), 2222)
                self.assertEqual(m.call_args.kwargs.get("ssh_key"), "/tmp/k")
                self.assertTrue(m.call_args.kwargs.get("sudo"))
    def test_orchestrator_ssh_flag_propagation(self):
        from audit_orchestrator import AuditOrchestrator
        orch = AuditOrchestrator(ssh_port=2222, ssh_key="/tmp/id_rsa", sudo=True)
        self.assertEqual(orch.ssh_port, 2222)
        self.assertEqual(orch.ssh_key, "/tmp/id_rsa")
        self.assertTrue(orch.sudo)
        kwargs = orch.check_kwargs
        self.assertEqual(kwargs.get("ssh_port"), 2222)
        self.assertEqual(kwargs.get("ssh_key"), "/tmp/id_rsa")
        self.assertTrue(kwargs.get("sudo"))

    def test_rhel_engines_forward_ssh_flags_to_run_command(self):
        import audit_cis_rhel_8, audit_cis_rhel_9, audit_cis_rhel_10
        recs = [{"id": "1", "name": "C1", "category": "General", "type": "Automated", "audit": "echo 1", "condition": {"type": "exit_code_equal", "value": 0}}]
        for mod in (audit_cis_rhel_8, audit_cis_rhel_9, audit_cis_rhel_10):
            with patch.object(mod, "run_command", return_value=("", "", 0)) as m:
                mod.perform_checks(recs, remote_host="user@host", docker_container="c1", ssh_port=2222, ssh_key="/tmp/k", sudo=True)
                self.assertEqual(m.call_args.kwargs.get("ssh_port"), 2222)
                self.assertEqual(m.call_args.kwargs.get("ssh_key"), "/tmp/k")
                self.assertTrue(m.call_args.kwargs.get("sudo"))


if __name__ == "__main__":
    unittest.main()

