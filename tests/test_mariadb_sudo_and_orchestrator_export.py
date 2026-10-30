#!/usr/bin/env python3
"""
Unit tests for MariaDB sudo propagation, Orchestrator export adaptation,
and CLI DB argument parsing (PSL ONLY).
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import audit_cis_mariadb_106 as mariadb_106
import audit_cis_mariadb_1011 as mariadb_1011
from audit_orchestrator import CANONICAL_TARGETS, AuditOrchestrator, build_cli_parser


class TestMariaDBSudoAndOrchestratorExport(unittest.TestCase):
    """Test suite verifying sudo preservation and orchestrator export resilience."""

    def test_mariadb_sudo_propagation(self):
        """Verify that MariaDB engines handle sudo=True (local & SSH) and sudo=False."""
        for mod in (mariadb_106, mariadb_1011):
            with patch("subprocess.run") as mock_sub:
                mock_sub.return_value = MagicMock(stdout="root\n", stderr="", returncode=0)
                mod.run_command("whoami", sudo=True)
                self.assertEqual(mock_sub.call_args[0][0][:2], ["sudo", "-n"], f"{mod.__name__} local sudo failed")
                mod.run_command("whoami", remote_host="db.example.org", sudo=True)
                cmd = mock_sub.call_args[0][0]
                idx = cmd.index("db.example.org")
                self.assertEqual(cmd[idx + 1:idx + 3], ["sudo", "-n"], f"{mod.__name__} ssh sudo failed")
                mod.run_command("whoami", sudo=False)
                self.assertNotIn("sudo", mock_sub.call_args[0][0], f"{mod.__name__} no_sudo failed")

    def test_orchestrator_export_all_18_targets(self):
        """Verify that all 18 canonical targets export json and txt reports without TypeError."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            orch = AuditOrchestrator(mode="local", output_dir=tmp_dir, formats=["json", "txt"])
            for target, meta in CANONICAL_TARGETS.items():
                mod_name = meta["module"]
                with patch(f"{mod_name}.run_command", return_value=("1", "", 0)):
                    res = orch.execute_single_target(target)
                    self.assertTrue(res.success, f"Target {target} failed: {res.exception_msg}")
                    self.assertIn("json", res.generated_reports, f"Missing json report for {target}")
                    self.assertIn("txt", res.generated_reports, f"Missing txt report for {target}")
                    self.assertTrue(os.path.exists(res.generated_reports["json"]))
                    self.assertTrue(os.path.exists(res.generated_reports["txt"]))

    def test_orchestrator_cli_db_arguments_parsing(self):
        """Verify that audit_orchestrator CLI parser parses and sets database credential arguments."""
        parser = build_cli_parser()
        args = parser.parse_args([
            "-t", "mariadb106", "-u", "admin_user", "-p", "secret_pass",
            "-H", "192.168.1.50", "-P", "3307", "-D", "audit_db",
            "--defaults-file", "/etc/mysql/my.cnf", "--auth-db", "admin"
        ])
        self.assertEqual(args.db_user, "admin_user")
        self.assertEqual(args.db_password, "secret_pass")
        self.assertEqual(args.db_host, "192.168.1.50")
        self.assertEqual(args.db_port, 3307)
        self.assertEqual(args.db_name, "audit_db")
        self.assertEqual(args.defaults_file, "/etc/mysql/my.cnf")
        self.assertEqual(args.auth_db, "admin")

    def test_orchestrator_check_kwargs_forwarding(self):
        """Verify that check_kwargs property forwards DB credentials to engines."""
        orch = AuditOrchestrator(
            db_user="test_user", db_password="secret_pass", db_host="127.0.0.1",
            db_port=5432, db_name="app_db", defaults_file="/path/to/defaults.cnf",
            auth_db="auth_admin", ssh_port=2222, ssh_key="/root/.ssh/custom_id_rsa", sudo=True
        )
        kwargs = orch.check_kwargs
        self.assertEqual(kwargs.get("db_user"), "test_user")
        self.assertEqual(kwargs.get("db_password"), "secret_pass")
        self.assertEqual(kwargs.get("db_host"), "127.0.0.1")
        self.assertEqual(kwargs.get("db_port"), 5432)
        self.assertEqual(kwargs.get("db_name"), "app_db")
        self.assertEqual(kwargs.get("defaults_file"), "/path/to/defaults.cnf")
        self.assertEqual(kwargs.get("auth_db"), "auth_admin")
        self.assertEqual(kwargs.get("ssh_port"), 2222)
        self.assertEqual(kwargs.get("ssh_key"), "/root/.ssh/custom_id_rsa")
        self.assertTrue(kwargs.get("sudo"))


if __name__ == "__main__":
    unittest.main()
