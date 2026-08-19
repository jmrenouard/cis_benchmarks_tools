#!/usr/bin/env python3
"""
Unit tests for audit_diagnostics.py Root Cause Analysis (RCA) and Failure Classifier (PSL ONLY).
"""

import unittest
from audit_diagnostics import (
    FailureCategory,
    FailureDiagnostic,
    CommandFailureClassifier,
    AuditDiagnosticSummary
)


class TestAuditDiagnostics(unittest.TestCase):

    def test_classify_clean_pass(self):
        diag = CommandFailureClassifier.classify(
            command="mariadb -e 'SELECT @@version;'",
            stdout="10.6.18-MariaDB",
            stderr="",
            returncode=0
        )
        self.assertEqual(diag.category, FailureCategory.CLEAN_PASS)
        self.assertFalse(diag.is_environment_error)
        self.assertEqual(diag.severity, "INFO")

    def test_classify_missing_binary(self):
        diag = CommandFailureClassifier.classify(
            command="cqlsh -e 'DESCRIBE KEYSPACES;'",
            stdout="",
            stderr="/bin/bash: cqlsh: command not found",
            returncode=127
        )
        self.assertEqual(diag.category, FailureCategory.MISSING_BINARY)
        self.assertTrue(diag.is_environment_error)
        self.assertEqual(diag.severity, "HIGH")
        self.assertIn("cqlsh", diag.remediation_suggestion)

    def test_classify_permission_denied(self):
        diag = CommandFailureClassifier.classify(
            command="cat /etc/shadow",
            stdout="",
            stderr="cat: /etc/shadow: Permission denied",
            returncode=1
        )
        self.assertEqual(diag.category, FailureCategory.PERMISSION_DENIED)
        self.assertTrue(diag.is_environment_error)
        self.assertIn("sudo", diag.remediation_suggestion)

    def test_classify_auth_failure(self):
        diag = CommandFailureClassifier.classify(
            command="psql -U postgres -c '\\l'",
            stdout="",
            stderr="psql: error: password authentication failed for user 'postgres'",
            returncode=2
        )
        self.assertEqual(diag.category, FailureCategory.AUTH_FAILURE)
        self.assertTrue(diag.is_environment_error)

    def test_classify_connection_error(self):
        diag = CommandFailureClassifier.classify(
            command="mysql -h 127.0.0.1 -P 3306 -e 'SELECT 1;'",
            stdout="",
            stderr="ERROR 2003 (HY000): Can't connect to MySQL server on '127.0.0.1' (111 Connection refused)",
            returncode=1
        )
        self.assertEqual(diag.category, FailureCategory.CONNECTION_ERROR)
        self.assertTrue(diag.is_environment_error)

    def test_classify_timeout(self):
        diag = CommandFailureClassifier.classify(
            command="sleep 15",
            stdout="",
            stderr="Command execution timed out after 10 seconds",
            returncode=-1,
            elapsed_sec=10.0
        )
        self.assertEqual(diag.category, FailureCategory.TIMEOUT)
        self.assertTrue(diag.is_environment_error)

    def test_classify_syntax_error(self):
        diag = CommandFailureClassifier.classify(
            command="mysql -e 'SELEC 1;'",
            stdout="",
            stderr="ERROR 1064 (42000): You have an error in your SQL syntax near 'SELEC 1'",
            returncode=1
        )
        self.assertEqual(diag.category, FailureCategory.SYNTAX_ERROR)
        self.assertFalse(diag.is_environment_error)

    def test_classify_control_result_genuine_fail(self):
        control = {
            "number": "2.1.1",
            "name": "Ensure password policy is enabled",
            "status": "Fail",
            "output": "STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION",
            "remediation": "Set sql_mode to include STRICT_ALL_TABLES"
        }
        diag = CommandFailureClassifier.classify_control_result(control)
        self.assertEqual(diag.category, FailureCategory.SECURITY_NON_COMPLIANCE)
        self.assertFalse(diag.is_environment_error)
        self.assertIn("STRICT_ALL_TABLES", diag.remediation_suggestion)

    def test_classify_control_result_hidden_connection_error(self):
        control = {
            "number": "1.1",
            "name": "Ensure database is configured properly",
            "status": "Fail",
            "output": "could not connect to server: Connection refused",
            "remediation": "Verify server configuration"
        }
        diag = CommandFailureClassifier.classify_control_result(control)
        self.assertEqual(diag.category, FailureCategory.CONNECTION_ERROR)
        self.assertTrue(diag.is_environment_error)

    def test_diagnostic_summary_markdown_and_dict(self):
        summary = AuditDiagnosticSummary(target_name="mariadb_106")
        summary.add(CommandFailureClassifier.classify("cmd1", stdout="OK", returncode=0))
        summary.add(CommandFailureClassifier.classify("cmd2", stderr="Permission denied", returncode=1))
        summary.add(CommandFailureClassifier.classify_control_result({
            "number": "3.1",
            "status": "Manual",
            "output": "Manual check required"
        }))
        summary.add(CommandFailureClassifier.classify_control_result({
            "number": "4.1",
            "status": "Fail",
            "output": "0",
            "remediation": "Enable encryption"
        }))

        self.assertEqual(summary.total_checks, 4)
        self.assertEqual(summary.clean_passes, 1)
        self.assertEqual(summary.environment_errors, 1)
        self.assertEqual(summary.manual_checks, 1)
        self.assertEqual(summary.security_failures, 1)

        d = summary.to_dict()
        self.assertEqual(d["target"], "mariadb_106")
        self.assertIn("category_breakdown", d)

        md = summary.generate_markdown_report()
        self.assertIn("Root Cause Analysis (RCA) Diagnostic Report", md)
        self.assertIn("mariadb_106", md)
        self.assertIn("PERMISSION_DENIED", md)


if __name__ == "__main__":
    unittest.main()
