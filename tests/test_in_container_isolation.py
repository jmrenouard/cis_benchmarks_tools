#!/usr/bin/env python3
"""
Adversarial in-container isolation and fault resilience test suite (Python PSL ONLY).
Verifies:
  1. Strict in-container namespace isolation (zero-host command leakage).
  2. Non-root user privileges (UID/GID 999).
  3. Read-only rootfs compliance.
  4. Stopped container error classification.
"""

import json
import os
import unittest
from unittest.mock import MagicMock, patch

from audit_diagnostics import FailureCategory
from docker_transport import (
    ContainerInfo,
    DockerContainerDiscovery,
    DockerTransportResolver,
)
from execution_drivers import (
    DockerContainerExecutor,
    ExecutionResult,
    create_executor,
)
from in_container_inspector import InContainerInspector


class TestInContainerIsolation(unittest.TestCase):
    """Adversarial security & isolation test suite for in-container audit execution."""

    @patch("subprocess.run")
    def test_zero_host_leakage_assertion(self, mock_run):
        """Verify that DockerContainerExecutor routes 100% of commands through docker exec."""
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "root /var/lib/mysql\n"
        mock_run.return_value = mock_proc

        executor = DockerContainerExecutor(container_name="mariadb106-test")
        res = executor.execute("whoami && pwd")

        self.assertTrue(res.is_success)
        # Verify subprocess was called with docker exec, not baremetal
        called_args = mock_run.call_args[0][0]
        self.assertIn("docker exec -i", called_args[2])
        self.assertIn("mariadb106-test", called_args[2])

    @patch("subprocess.run")
    def test_non_root_user_execution(self, mock_run):
        """Verify executing commands as non-root user (e.g. mysql:mysql or UID 999)."""
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "uid=999(mysql) gid=999(mysql)\n"
        mock_run.return_value = mock_proc

        executor = DockerContainerExecutor(container_name="mariadb106-test")
        res = executor.execute("id", as_user="999:999")

        self.assertTrue(res.is_success)
        called_args = mock_run.call_args[0][0]
        self.assertIn("-u 999:999", called_args[2])

    @patch("subprocess.run")
    def test_working_directory_isolation(self, mock_run):
        """Verify workdir flag (-w) is respected inside container."""
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "/etc/mysql\n"
        mock_run.return_value = mock_proc

        executor = DockerContainerExecutor(container_name="mariadb106-test")
        res = executor.execute("pwd", cwd="/etc/mysql")

        self.assertTrue(res.is_success)
        called_args = mock_run.call_args[0][0]
        self.assertIn("-w /etc/mysql", called_args[2])

    @patch("subprocess.run")
    def test_stopped_container_error_classification(self, mock_run):
        """Verify error classification when target container is stopped or nonexistent."""
        mock_proc = MagicMock()
        mock_proc.returncode = 125
        mock_proc.stdout = ""
        mock_proc.stderr = "Error response from daemon: Container mariadb106-test is not running\n"
        mock_run.return_value = mock_proc

        executor = DockerContainerExecutor(container_name="mariadb106-test")
        res = executor.execute("mariadb --version")

        self.assertFalse(res.is_success)
        self.assertTrue(res.is_environment_error)
        self.assertIn(res.failure_category, [FailureCategory.CONNECTION_ERROR, FailureCategory.UNKNOWN_ERROR])

    @patch("docker_transport.DockerContainerDiscovery.inspect_container")
    def test_readonly_rootfs_detection(self, mock_inspect):
        """Verify detection of read-only root filesystem in container."""
        mock_c = ContainerInfo(
            container_id="112233445566",
            name="mariadb106-readonly",
            image="mariadb:10.6",
            status="Up",
            is_running=True
        )
        mock_inspect.return_value = mock_c

        mock_exec = MagicMock()
        mock_exec.execute.return_value = ExecutionResult(stdout="RO\n", returncode=0)
        inspector = InContainerInspector(mock_exec)

        self.assertTrue(inspector.is_rootfs_readonly())


if __name__ == "__main__":
    unittest.main()
