#!/usr/bin/env python3
"""
Unit tests for audit_orchestrator.py Multi-Product Orchestration Engine (PSL ONLY).
"""

import os
import tempfile
import unittest
from unittest.mock import patch
from audit_orchestrator import (
    CANONICAL_TARGETS,
    normalize_target_key,
    TargetAuditExecutionResult,
    AuditOrchestrator
)
from audit_diagnostics import FailureCategory, AuditDiagnosticSummary


class TestAuditOrchestrator(unittest.TestCase):

    def test_canonical_targets_catalog_completeness(self):
        """Assert all 18 canonical targets are cataloged."""
        self.assertEqual(len(CANONICAL_TARGETS), 18)
        expected_keys = [
            "mariadb106", "mariadb1011",
            "mysql80", "mysql-community84", "mysql-enterprise84",
            "mysql-community97", "mysql-enterprise97",
            "postgresql16", "postgresql17", "postgresql18",
            "mongodb7", "mongodb8",
            "cassandra40", "cassandra41", "cassandra50",
            "rhel8", "rhel9", "rhel10"
        ]
        for k in expected_keys:
            self.assertIn(k, CANONICAL_TARGETS)

    def test_normalize_target_key(self):
        """Test target normalization and aliases."""
        self.assertEqual(normalize_target_key("mariadb"), "mariadb106")
        self.assertEqual(normalize_target_key("mysql"), "mysql80")
        self.assertEqual(normalize_target_key("postgres"), "postgresql16")
        self.assertEqual(normalize_target_key("postgresql"), "postgresql16")
        self.assertEqual(normalize_target_key("mongo"), "mongodb7")
        self.assertEqual(normalize_target_key("cassandra"), "cassandra40")
        self.assertEqual(normalize_target_key("rhel"), "rhel9")
        self.assertEqual(normalize_target_key("mariadb106"), "mariadb106")
        self.assertEqual(normalize_target_key("mysql_enterprise_84"), "mysql-enterprise84")

    @patch("audit_cis_mariadb_106.run_command", return_value=("1", "", 0))
    def test_orchestrator_execute_single_target(self, mock_cmd):
        """Test orchestrator execution on a single target."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            orchestrator = AuditOrchestrator(
                mode="local",
                output_dir=tmp_dir,
                formats=["json", "txt"]
            )
            res = orchestrator.execute_single_target("mariadb106")
            self.assertTrue(res.success)
            self.assertEqual(res.target_key, "mariadb106")
            self.assertGreater(res.total_controls, 50)
            self.assertIn("json", res.generated_reports)
            self.assertIn("txt", res.generated_reports)
            self.assertTrue(os.path.exists(res.generated_reports["json"]))
            self.assertTrue(os.path.exists(res.generated_reports["txt"]))

    def test_orchestrator_execute_unknown_target_fault_isolation(self):
        """Test orchestrator handles unknown target gracefully without crash."""
        orchestrator = AuditOrchestrator(mode="local")
        res = orchestrator.execute_single_target("non_existent_db_99")
        self.assertFalse(res.success)
        self.assertIn("not registered", res.exception_msg)

    @patch("audit_cis_mariadb_106.run_command", return_value=("1", "", 0))
    @patch("audit_cis_mysql_80.run_command", return_value=("1", "", 0))
    def test_orchestrator_execute_multiple_targets_and_rca_dashboard(self, mock_mysql_cmd, mock_maria_cmd):
        """Test orchestrator executes multiple targets and produces RCA dashboard."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            orchestrator = AuditOrchestrator(
                mode="local",
                output_dir=tmp_dir,
                formats=["json", "txt"]
            )
            results = orchestrator.execute_all_targets(
                targets=["mariadb106", "mysql80"],
                parallel_workers=2
            )
            self.assertEqual(len(results), 2)
            self.assertTrue(results[0].success)
            self.assertTrue(results[1].success)

            dash_path = os.path.join(tmp_dir, "rca_dashboard.md")
            orchestrator.generate_suite_rca_dashboard(results, report_filename=dash_path)
            self.assertTrue(os.path.exists(dash_path))

            with open(dash_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn("Root Cause Analysis (RCA) & Audit Diagnostics Dashboard", content)
            self.assertIn("mariadb106", content)
            self.assertIn("mysql80", content)

            json_summary_path = dash_path.replace(".md", ".json")
            self.assertTrue(os.path.exists(json_summary_path))


    def test_container_info_telemetry(self):
        """Test TargetAuditExecutionResult serialization with container info."""
        res = TargetAuditExecutionResult(
            target_key="mariadb106",
            title="MariaDB 10.6",
            success=True,
            duration_sec=1.2,
            container_info={"name": "mariadb106-test", "short_id": "112233445566"}
        )
        d = res.to_dict()
        self.assertIn("container_info", d)
        self.assertEqual(d["container_info"]["name"], "mariadb106-test")


if __name__ == "__main__":
    unittest.main()
