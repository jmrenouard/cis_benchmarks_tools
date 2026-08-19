#!/usr/bin/env python3
"""
Unit test suite for orchestrator temporal reporting integration (Python PSL ONLY).
"""

import unittest
from unittest.mock import MagicMock, patch

from audit_orchestrator import AuditOrchestrator, TargetAuditExecutionResult
from docker_e2e_engine import E2ERunResult
from temporal_metadata import TemporalAuditMetadata


class TestOrchestratorTemporalReporting(unittest.TestCase):
    """Test suite for temporal metadata propagation in orchestration engines."""

    def test_target_audit_execution_result_temporal_dict(self):
        """Test TargetAuditExecutionResult properly serializes temporal_metadata."""
        t_meta = TemporalAuditMetadata.create_now()
        t_meta.finish()

        res = TargetAuditExecutionResult(
            target_key="mariadb106",
            title="MariaDB 10.6",
            success=True,
            duration_sec=1.5,
            temporal_metadata=t_meta.to_dict()
        )
        d = res.to_dict()

        self.assertIn("temporal_metadata", d)
        self.assertEqual(d["temporal_metadata"]["iso_start"], t_meta.iso_start)
        self.assertEqual(d["temporal_metadata"]["timezone_name"], t_meta.timezone_name)

    def test_e2e_run_result_temporal_dict(self):
        """Test E2ERunResult properly serializes temporal_metadata."""
        t_meta = TemporalAuditMetadata.create_now()
        t_meta.finish()

        res = E2ERunResult(
            target_key="mariadb106",
            container_name="mariadb106-test",
            success=True,
            duration_sec=2.0,
            temporal_metadata=t_meta.to_dict()
        )
        d = res.to_dict()

        self.assertIn("temporal_metadata", d)
        self.assertEqual(d["temporal_metadata"]["iso_start"], t_meta.iso_start)


if __name__ == "__main__":
    unittest.main()
