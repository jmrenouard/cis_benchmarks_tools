#!/usr/bin/env python3
"""
Unit test suite for docker_e2e_engine.py (Python PSL ONLY).
"""

import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from docker_e2e_engine import DockerE2EOrchestrator, E2ERunResult, TargetE2ESpec
from docker_transport import ContainerInfo


class TestDockerE2EEngine(unittest.TestCase):
    """Test suite for Docker E2E engine."""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.orchestrator = DockerE2EOrchestrator(output_dir=self.tmp_dir)

    def test_spec_and_result_classes(self):
        """Test TargetE2ESpec and E2ERunResult data structures."""
        spec = TargetE2ESpec(
            key="mariadb106",
            dockerfile="docker/Dockerfile_mariadb106",
            image_name="mariadb106-audit",
            container_name="mariadb106-test",
            script_name="audit_cis_mariadb_106.py",
            report_prefix="rapport_cis_mariadb_106"
        )
        self.assertEqual(spec.key, "mariadb106")
        self.assertEqual(spec.container_name, "mariadb106-test")

        res = E2ERunResult(
            target_key="mariadb106",
            container_name="mariadb106-test",
            success=True,
            duration_sec=1.5,
            format_validations={"html": (True, "Valid (1000B)"), "json": (True, "Valid (500B)")},
            extracted_reports={"html": "/tmp/test.html"}
        )
        d = res.to_dict()
        self.assertTrue(d["success"])
        self.assertEqual(d["target_key"], "mariadb106")
        self.assertEqual(d["format_validations"]["html"]["valid"], True)

    @patch("docker_transport.DockerContainerDiscovery.inspect_container")
    def test_execute_target_flow_container_not_running(self, mock_inspect):
        """Test failure handling when container is not running."""
        mock_inspect.return_value = None
        spec = TargetE2ESpec(
            key="mariadb106",
            dockerfile="",
            image_name="",
            container_name="nonexistent-container",
            script_name="audit_cis_mariadb_106.py",
            report_prefix="rapport_cis_mariadb_106"
        )
        res = self.orchestrator.execute_target_flow(spec)
        self.assertFalse(res.success)
        self.assertIn("not running or not found", res.error_message)

    @patch("docker_transport.DockerContainerDiscovery.inspect_container")
    @patch("subprocess.run")
    def test_execute_target_flow_success(self, mock_run, mock_inspect):
        """Test successful in-container E2E workflow."""
        mock_c = ContainerInfo(
            container_id="1234567890ab",
            name="mariadb106-test",
            image="mariadb:10.6",
            status="Up",
            is_running=True
        )
        mock_inspect.return_value = mock_c

        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = ""
        mock_run.return_value = mock_proc

        spec = TargetE2ESpec(
            key="mariadb106",
            dockerfile="",
            image_name="",
            container_name="mariadb106-test",
            script_name="audit_cis_mariadb_106.py",
            report_prefix="rapport_cis_mariadb_106"
        )

        with patch.object(self.orchestrator, "execute_in_container_audit") as mock_exec:
            mock_exec.return_value = (
                {"html": (True, "Valid"), "json": (True, "Valid")},
                {"html": f"{self.tmp_dir}/rep.html", "json": f"{self.tmp_dir}/rep.json"}
            )
            res = self.orchestrator.execute_target_flow(spec, formats=["html", "json"])
            self.assertTrue(res.success)
            self.assertEqual(res.target_key, "mariadb106")

    def test_generate_e2e_summary_dashboard(self):
        """Test generating E2E summary dashboard."""
        results = [
            E2ERunResult(
                target_key="mariadb106",
                container_name="mariadb106-test",
                success=True,
                duration_sec=2.1,
                format_validations={"html": (True, "Valid")},
                extracted_reports={"html": "/tmp/rep.html"}
            )
        ]
        out_file = os.path.join(self.tmp_dir, "test_dashboard.md")
        res_file = self.orchestrator.generate_e2e_summary_dashboard(results, output_file=out_file)
        self.assertTrue(os.path.exists(res_file))
        with open(res_file, "r") as f:
            content = f.read()
        self.assertIn("mariadb106", content)
        self.assertIn("✅ PASS", content)


if __name__ == "__main__":
    unittest.main()
