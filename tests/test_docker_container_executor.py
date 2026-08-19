#!/usr/bin/env python3
"""
Unit test suite for DockerContainerExecutor and in-container driver features (PSL ONLY).
"""

import unittest
from unittest.mock import MagicMock, patch

from docker_transport import ContainerInfo
from execution_drivers import (
    DockerContainerExecutor,
    DockerExecutor,
    create_executor,
)


class TestDockerContainerExecutor(unittest.TestCase):
    """Test suite for Docker in-container executor driver."""

    def test_alias_equality(self):
        """Test DockerContainerExecutor is an alias for DockerExecutor."""
        self.assertIs(DockerContainerExecutor, DockerExecutor)

    @patch("subprocess.run")
    def test_execute_in_container_success(self, mock_run):
        """Test command execution inside Docker container."""
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "mariadb 10.6.15-MariaDB\n"
        mock_proc.stderr = ""
        mock_run.return_value = mock_proc

        executor = DockerContainerExecutor(
            container_name="mariadb106-test",
            db_user="root",
            db_password="secretpassword"
        )
        res = executor.execute("mariadb --version")
        self.assertTrue(res.is_success)
        self.assertIn("10.6.15", res.stdout)
        self.assertEqual(res.driver_type, "LOCAL_DOCKER")
        self.assertNotIn("secretpassword", res.command_masked)

    @patch("subprocess.run")
    def test_is_container_running(self, mock_run):
        """Test container running probe."""
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "true\n"
        mock_run.return_value = mock_proc

        executor = DockerContainerExecutor(container_name="mariadb106-test")
        self.assertTrue(executor.is_container_running())

    @patch("docker_transport.DockerContainerDiscovery.inspect_container")
    def test_get_container_info(self, mock_inspect):
        """Test retrieving container runtime info."""
        mock_c = ContainerInfo(
            container_id="112233445566",
            name="mariadb106-test",
            image="mariadb:10.6",
            status="Up",
            is_running=True
        )
        mock_inspect.return_value = mock_c

        executor = DockerContainerExecutor(container_name="mariadb106-test")
        info = executor.get_container_info()
        self.assertIsNotNone(info)
        self.assertEqual(info.name, "mariadb106-test")

    @patch("docker_transport.DockerContainerDiscovery.find_container_for_product")
    def test_create_executor_auto_discovery(self, mock_find):
        """Test create_executor resolves DockerExecutor when product_hint container exists."""
        mock_c = ContainerInfo(
            container_id="aabbccddeeff",
            name="mariadb106-test",
            image="mariadb:10.6",
            status="Up",
            is_running=True
        )
        mock_find.return_value = mock_c

        executor = create_executor(mode="local", product_hint="mariadb106")
        self.assertIsInstance(executor, DockerExecutor)
        self.assertEqual(executor.container_name, "mariadb106-test")


if __name__ == "__main__":
    unittest.main()
