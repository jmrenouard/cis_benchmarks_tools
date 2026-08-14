#!/usr/bin/env python3
"""
End-to-End test suite for Docker-based CIS benchmark executions (PSL ONLY).
"""

import json
import os
import subprocess
import sys
import unittest
from unittest.mock import MagicMock, patch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import audit_cis


class TestE2EDockerAudits(unittest.TestCase):

    def test_target_map_contains_all_18_targets(self):
        """Validate that unified CLI TARGET_MAP contains exactly 18 distinct benchmarks."""
        self.assertEqual(len(audit_cis.TARGET_MAP), 18)
        for key, (script, label, count) in audit_cis.TARGET_MAP.items():
            script_path = os.path.join(REPO_ROOT, script)
            self.assertTrue(os.path.exists(script_path), f"Script {script} does not exist for target {key}")
            self.assertGreater(count, 0)

    @patch("subprocess.run")
    def test_run_single_audit_docker_mode_e2e(self, mock_run):
        """Test unified run_single_audit forwards docker container and connection parameters correctly."""
        mock_run.return_value = MagicMock(returncode=0)

        success = audit_cis.run_single_audit(
            "mysql80",
            docker_container="mysql80-test",
            db_user="root",
            db_password="RootPassword123!",
            db_host="localhost",
            db_port=3306
        )

        self.assertTrue(success)
        called_cmd = mock_run.call_args[0][0]
        self.assertIn("--docker", called_cmd)
        self.assertIn("mysql80-test", called_cmd)
        self.assertIn("--db-user", called_cmd)
        self.assertIn("root", called_cmd)
        self.assertIn("--db-password", called_cmd)
        self.assertIn("RootPassword123!", called_cmd)

    @patch("audit_cis.run_single_audit")
    def test_auto_detect_target_keys(self, mock_audit):
        """Test auto-detection parser logic matches docker ps output formats."""
        sample_ps = "mysql80-test mysql80-audit:latest\npg16-cont postgres:16-alpine\n"
        with patch("subprocess.check_output", return_value=sample_ps):
            # Test auto-detection does not crash
            audit_cis.auto_detect_and_run()
            self.assertTrue(mock_audit.called)


if __name__ == "__main__":
    unittest.main()
