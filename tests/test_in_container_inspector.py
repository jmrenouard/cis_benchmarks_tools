#!/usr/bin/env python3
"""
Unit test suite for in_container_inspector.py (PSL ONLY).
"""

import unittest
from unittest.mock import MagicMock

from execution_drivers import ExecutionResult
from in_container_inspector import InContainerInspector, PosixStatResult


class TestInContainerInspector(unittest.TestCase):
    """Test suite for InContainerInspector."""

    def setUp(self):
        self.mock_executor = MagicMock()
        self.inspector = InContainerInspector(self.mock_executor)

    def test_read_file_success(self):
        """Test reading container configuration file."""
        self.mock_executor.execute.return_value = ExecutionResult(
            stdout="[mysqld]\nmax_connections = 150\n",
            returncode=0
        )
        content = self.inspector.read_file("/etc/mysql/my.cnf")
        self.assertIsNotNone(content)
        self.assertIn("max_connections", content)

    def test_file_exists(self):
        """Test checking file existence in container."""
        self.mock_executor.execute.return_value = ExecutionResult(returncode=0)
        self.assertTrue(self.inspector.file_exists("/var/lib/mysql"))

        self.mock_executor.execute.return_value = ExecutionResult(returncode=1)
        self.assertFalse(self.inspector.file_exists("/nonexistent/path"))

    def test_stat_path_regular_file(self):
        """Test POSIX stat inspection on regular file."""
        self.mock_executor.execute.return_value = ExecutionResult(
            stdout="600 999 999 mysql mysql regular file\n",
            returncode=0
        )
        stat_res = self.inspector.stat_path("/var/lib/mysql/ibdata1")
        self.assertTrue(stat_res.exists)
        self.assertEqual(stat_res.mode_octal, "0600")
        self.assertEqual(stat_res.uid, 999)
        self.assertEqual(stat_res.gid, 999)
        self.assertEqual(stat_res.user, "mysql")
        self.assertEqual(stat_res.group, "mysql")
        self.assertTrue(stat_res.is_file)
        self.assertFalse(stat_res.is_directory)

    def test_stat_path_directory(self):
        """Test POSIX stat inspection on directory."""
        self.mock_executor.execute.return_value = ExecutionResult(
            stdout="750 0 0 root root directory\n",
            returncode=0
        )
        stat_res = self.inspector.stat_path("/etc/mysql")
        self.assertTrue(stat_res.exists)
        self.assertEqual(stat_res.mode_octal, "0750")
        self.assertTrue(stat_res.is_directory)

    def test_is_port_listening(self):
        """Test port listening check in container namespace."""
        self.mock_executor.execute.return_value = ExecutionResult(returncode=0)
        self.assertTrue(self.inspector.is_port_listening(3306))

    def test_is_process_running(self):
        """Test process running check."""
        self.mock_executor.execute.return_value = ExecutionResult(returncode=0)
        self.assertTrue(self.inspector.is_process_running("mysqld"))

    def test_is_rootfs_readonly(self):
        """Test read-only rootfs check."""
        self.mock_executor.execute.return_value = ExecutionResult(stdout="RO\n", returncode=0)
        self.assertTrue(self.inspector.is_rootfs_readonly())

        self.mock_executor.execute.return_value = ExecutionResult(stdout="RW\n", returncode=0)
        self.assertFalse(self.inspector.is_rootfs_readonly())

    def test_execute_db_query_mysql(self):
        """Test executing query via container MySQL/MariaDB CLI."""
        self.mock_executor.execute.return_value = ExecutionResult(
            stdout="have_ssl\tYES\n",
            returncode=0
        )
        res = self.inspector.execute_db_query(
            query="SHOW VARIABLES LIKE 'have_ssl';",
            db_type="mysql",
            user="root"
        )
        self.assertTrue(res.is_success)
        self.assertIn("have_ssl", res.stdout)


if __name__ == "__main__":
    unittest.main()
