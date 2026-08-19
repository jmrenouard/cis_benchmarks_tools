#!/usr/bin/env python3
"""
Unit Test Suite for Unified Audit CLI Engine and Target Mapping Integrity.
100% Python Standard Library (PSL ONLY).
"""

import os
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from audit_cis import TARGET_MAP, list_targets, run_single_audit


class TestAuditCisCliEngine(unittest.TestCase):
    """Unit tests for audit_cis CLI target map and execution engine."""

    def test_target_map_integrity(self):
        self.assertIsInstance(TARGET_MAP, dict)
        self.assertEqual(len(TARGET_MAP), 18)
        for key, value in TARGET_MAP.items():
            self.assertEqual(len(value), 3, f"Expected 3 elements for target {key}")
            script_file, label, count = value
            self.assertTrue(script_file.endswith(".py"))
            self.assertIsInstance(label, str)
            self.assertGreater(count, 0)
            script_path = os.path.join(REPO_ROOT, script_file)
            self.assertTrue(os.path.exists(script_path), f"Audit script file missing: {script_path}")

    def test_run_single_audit_invalid_target(self):
        result = run_single_audit("invalid_target_123")
        self.assertFalse(result)

    def test_run_single_audit_parameter_forwarding(self):
        """Test that run_single_audit constructs subprocess command with all forwarded flags."""
        from unittest.mock import patch, MagicMock

        with patch("subprocess.run") as mock_run:
            mock_proc = MagicMock()
            mock_proc.returncode = 0
            mock_run.return_value = mock_proc

            res = run_single_audit(
                "mariadb106",
                output_file="/tmp/test_report.json",
                fmt="json",
                lang="fr",
                mode="ssh",
                remote_host="admin@192.168.1.50",
                ssh_port=2222,
                ssh_key="/root/.ssh/custom_key",
                docker_container="mariadb-prod",
                db_host="127.0.0.1",
                db_port=3306,
                db_user="auditor",
                db_password="audit_password",
                db_name="mysql",
                defaults_file="/etc/mysql/my.cnf",
                use_sudo=True
            )

            self.assertTrue(res)
            self.assertTrue(mock_run.called)
            called_cmd = mock_run.call_args[0][0]

            self.assertIn("--format", called_cmd)
            self.assertIn("json", called_cmd)
            self.assertIn("--lang", called_cmd)
            self.assertIn("fr", called_cmd)
            self.assertIn("--mode", called_cmd)
            self.assertIn("ssh", called_cmd)
            self.assertIn("--remote", called_cmd)
            self.assertIn("admin@192.168.1.50", called_cmd)
            self.assertIn("--ssh-port", called_cmd)
            self.assertIn("2222", called_cmd)
            self.assertIn("--ssh-key", called_cmd)
            self.assertIn("/root/.ssh/custom_key", called_cmd)
            self.assertIn("--docker", called_cmd)
            self.assertIn("mariadb-prod", called_cmd)
            self.assertIn("--db-host", called_cmd)
            self.assertIn("127.0.0.1", called_cmd)
            self.assertIn("--db-port", called_cmd)
            self.assertIn("3306", called_cmd)
            self.assertIn("--db-user", called_cmd)
            self.assertIn("auditor", called_cmd)
            self.assertIn("--db-password", called_cmd)
            self.assertIn("audit_password", called_cmd)
            self.assertIn("--defaults-file", called_cmd)
            self.assertIn("/etc/mysql/my.cnf", called_cmd)
            self.assertIn("--sudo", called_cmd)
            self.assertIn("--output", called_cmd)
            self.assertIn("/tmp/test_report.json", called_cmd)

    def test_auto_detect_target_matching(self):
        """Test auto-detection parser matches container image / names correctly."""
        from unittest.mock import patch
        from audit_cis import auto_detect_and_run

        with patch("subprocess.check_output") as mock_out, patch("audit_cis.run_single_audit") as mock_single:
            mock_out.return_value = "mariadb-server mariadb:10.6\npostgres_db postgres:16-alpine\n"
            mock_single.return_value = True

            auto_detect_and_run()

            self.assertTrue(mock_single.called)
            called_targets = [call[0][0] for call in mock_single.call_args_list]
            self.assertIn("mariadb106", called_targets)
            self.assertIn("postgresql16", called_targets)


if __name__ == "__main__":
    unittest.main()
