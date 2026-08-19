#!/usr/bin/env python3
"""
Environmental Fault Injection & Non-Regression Test Harness for CIS Benchmark Audit Suite.
Simulates environmental faults (missing binaries, permission errors, auth failures,
connection timeouts, socket errors) and validates RCA classification & report persistence.
100% Python Standard Library (PSL ONLY).
"""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from audit_diagnostics import (
    FailureCategory,
    FailureDiagnostic,
    CommandFailureClassifier,
    AuditDiagnosticSummary
)
from audit_orchestrator import (
    CANONICAL_TARGETS,
    AuditOrchestrator,
    TargetAuditExecutionResult
)
from execution_drivers import (
    LocalExecutor,
    DockerExecutor,
    SSHExecutor,
    ExecutionResult
)


class TestEnvironmentalFaultInjectionAndRCA(unittest.TestCase):

    def test_fault_missing_binary_rca(self):
        """Simulate missing binary and assert RCA classification."""
        res = CommandFailureClassifier.classify(
            command="cqlsh -u cassandra -e 'DESCRIBE CLUSTER;'",
            stdout="",
            stderr="/bin/sh: line 1: cqlsh: command not found",
            returncode=127
        )
        self.assertEqual(res.category, FailureCategory.MISSING_BINARY)
        self.assertTrue(res.is_environment_error)
        self.assertEqual(res.severity, "HIGH")
        self.assertIn("cqlsh", res.remediation_suggestion)

    def test_fault_permission_denied_rca(self):
        """Simulate permission denied and assert RCA classification."""
        res = CommandFailureClassifier.classify(
            command="ls -la /var/lib/mysql",
            stdout="",
            stderr="ls: cannot open directory '/var/lib/mysql': Permission denied",
            returncode=1
        )
        self.assertEqual(res.category, FailureCategory.PERMISSION_DENIED)
        self.assertTrue(res.is_environment_error)
        self.assertIn("sudo", res.remediation_suggestion)

    def test_fault_database_auth_failure_rca(self):
        """Simulate bad password and assert RCA classification."""
        res = CommandFailureClassifier.classify(
            command="mariadb -u root -pInvalidPassword -e 'SELECT 1;'",
            stdout="",
            stderr="ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)",
            returncode=1
        )
        self.assertEqual(res.category, FailureCategory.AUTH_FAILURE)
        self.assertTrue(res.is_environment_error)
        self.assertIn("credentials", res.remediation_suggestion)

    def test_fault_connection_refused_rca(self):
        """Simulate unreachable server and assert RCA classification."""
        res = CommandFailureClassifier.classify(
            command="psql -h 10.0.0.99 -p 5432 -U postgres -c 'SELECT 1;'",
            stdout="",
            stderr="psql: error: could not connect to server: Connection refused",
            returncode=2
        )
        self.assertEqual(res.category, FailureCategory.CONNECTION_ERROR)
        self.assertTrue(res.is_environment_error)

    def test_fault_timeout_expired_rca(self):
        """Simulate command timeout and assert RCA classification."""
        res = CommandFailureClassifier.classify(
            command="find / -name my.cnf",
            stdout="",
            stderr="Command execution timed out after 10.0 seconds",
            returncode=-1,
            elapsed_sec=10.0
        )
        self.assertEqual(res.category, FailureCategory.TIMEOUT)
        self.assertTrue(res.is_environment_error)

    def test_orchestrator_resilience_under_target_failure(self):
        """Verify orchestrator continues multi-target execution and persists reports even when a target fails."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            orchestrator = AuditOrchestrator(
                mode="local",
                output_dir=tmp_dir,
                formats=["json", "txt"]
            )

            # Target 1: Valid (with mocked execution)
            # Target 2: Invalid / failing
            with patch("audit_cis_mariadb_106.run_command", return_value=("1", "", 0)):
                results = orchestrator.execute_all_targets(
                    targets=["mariadb106", "non_existent_product_xyz"],
                    parallel_workers=2
                )

            self.assertEqual(len(results), 2)
            # MariaDB 10.6 should succeed
            maria_res = next(r for r in results if r.target_key == "mariadb106")
            self.assertTrue(maria_res.success)
            self.assertTrue(os.path.exists(maria_res.generated_reports["json"]))

            # Invalid product should be recorded gracefully as failed without aborting pipeline
            fail_res = next(r for r in results if r.target_key == "non_existent_product_xyz")
            self.assertFalse(fail_res.success)
            self.assertIn("not registered", fail_res.exception_msg)

            # Generate dashboard
            dash_path = os.path.join(tmp_dir, "fleet_rca_dashboard.md")
            orchestrator.generate_suite_rca_dashboard(results, report_filename=dash_path)
            self.assertTrue(os.path.exists(dash_path))

            with open(dash_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn("mariadb106", content)
            self.assertIn("non_existent_product_xyz", content)

    def test_local_executor_handles_missing_command_cleanly(self):
        """Verify LocalExecutor safely returns missing binary diagnostic."""
        executor = LocalExecutor()
        res = executor.execute("__non_existent_binary_xyz_12345__", timeout=2)
        self.assertFalse(res.is_success)
        self.assertEqual(res.failure_category, FailureCategory.MISSING_BINARY)
        self.assertTrue(res.is_environment_error)


if __name__ == "__main__":
    unittest.main()
