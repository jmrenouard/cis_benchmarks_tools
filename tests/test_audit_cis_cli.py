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
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8", errors="replace")

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
            self.assertNotIn("--db-password", called_cmd)
            self.assertNotIn("audit_password", called_cmd)
            called_env = mock_run.call_args[1].get("env", {})
            self.assertEqual(called_env.get("CIS_DB_PASSWORD"), "audit_password")
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

    def test_sync_and_verify_cis_cli_dispatch(self):
        from unittest.mock import patch
        import audit_cis
        with patch("sys.argv", ["audit_cis.py", "--verify-cis", "-t", "mariadb106"]), patch("subprocess.run") as m, self.assertRaises(SystemExit):
            m.return_value.returncode = 0
            audit_cis.main()
        c = m.call_args[0][0]
        self.assertTrue(any("download_cis_benchmarks.py" in str(x) for x in c) and "--verify-only" in c and "mariadb106" in c)
        with patch("sys.argv", ["audit_cis.py", "--sync-cis", "-t", "mariadb106", "--force", "--dry-run", "--cis-types", "md", "--base-url", "u"]), patch("subprocess.run") as m2, self.assertRaises(SystemExit):
            m2.return_value.returncode = 0
            audit_cis.main()
        self.assertTrue(all(k in m2.call_args[0][0] for k in ["--force", "--dry-run", "--types", "md", "--base-url", "u"]))

    def test_audit_cis_dynamic_version_resolution_fallback(self):
        """Finding 8: Verify dynamic version resolution from VERSION file with fallback."""
        import audit_cis
        self.assertTrue(hasattr(audit_cis, "_resolve_version"))
        resolved = audit_cis._resolve_version()
        self.assertRegex(resolved, r"^\d+\.\d+\.\d+(?:[-.][a-zA-Z0-9.]+)?$")
        self.assertEqual(audit_cis.__version__, resolved)

    def test_bundle_audit_cis_preserves_custom_code_and_syncs_version(self):
        """Finding 8: Verify bundle_audit_cis preserves custom code and syncs version."""
        import tempfile
        from scripts.bundle_audit_cis import generate_unified_audit_script

        src = '#!/usr/bin/env python3\n"""Unified CIS Benchmark Audit Engine v1.0.0"""\ndef _resolve_version() -> str: return "1.0.0"\ncustom_flag = 42\n'
        with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tf:
            tf.write(src)
            path = tf.name
        try:
            self.assertTrue(generate_unified_audit_script(target_file=path))
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("custom_flag = 42", content)
            self.assertIn('return "2.10.0"', content)
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_bundle_audit_cis_prerelease_and_multipass_semver_sync(self):
        """Finding 8: Verify bundle_audit_cis supports pre-release and multi-pass semver tags without code loss."""
        import tempfile
        from unittest.mock import patch
        import scripts.bundle_audit_cis as bundler

        src = (
            '#!/usr/bin/env python3\n'
            '"""\n'
            'Unified CIS Benchmark Audit Engine v2.9.2-rc1\n'
            'Automated security audit suite.\n'
            '"""\n\n'
            'def _resolve_version() -> str:\n'
            '    return "2.9.2-rc1"\n\n'
            '__version__ = "2.9.2-rc1"\n'
            'custom_payload = {"magic": 42, "status": "active"}\n'
        )
        with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tf:
            tf.write(src)
            path = tf.name

        try:
            # Pass 1: Bump from 2.9.2-rc1 to 3.0.0.beta.1
            with patch.object(bundler, "VERSION", "3.0.0.beta.1"):
                self.assertTrue(bundler.generate_unified_audit_script(target_file=path))

            with open(path, "r", encoding="utf-8") as f:
                c1 = f.read()

            self.assertIn('custom_payload = {"magic": 42, "status": "active"}', c1)
            self.assertNotIn("-rc1", c1, "Residual -rc1 suffix left in docstring header")
            self.assertIn("Unified CIS Benchmark Audit Engine v3.0.0.beta.1", c1)
            self.assertIn('return "3.0.0.beta.1"', c1)
            self.assertIn('__version__ = "3.0.0.beta.1"', c1)

            # Pass 2: Verify idempotency on identical pre-release version
            with patch.object(bundler, "VERSION", "3.0.0.beta.1"):
                self.assertTrue(bundler.generate_unified_audit_script(target_file=path))

            with open(path, "r", encoding="utf-8") as f:
                c2 = f.read()

            self.assertEqual(c1, c2, "Idempotency broken: same version modified content")

            # Pass 3: Bump from 3.0.0.beta.1 to final 3.0.0
            with patch.object(bundler, "VERSION", "3.0.0"):
                self.assertTrue(bundler.generate_unified_audit_script(target_file=path))

            with open(path, "r", encoding="utf-8") as f:
                c3 = f.read()

            self.assertIn('custom_payload = {"magic": 42, "status": "active"}', c3)
            self.assertNotIn("beta", c3, "Residual beta suffix left in docstring header")
            self.assertIn("Unified CIS Benchmark Audit Engine v3.0.0", c3)
            self.assertIn('return "3.0.0"', c3)
            self.assertIn('__version__ = "3.0.0"', c3)
        finally:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()
