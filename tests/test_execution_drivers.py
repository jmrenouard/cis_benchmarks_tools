#!/usr/bin/env python3
"""
Unit tests for LocalExecutor and DockerExecutor (100% PSL ONLY).
"""

import unittest
from unittest.mock import MagicMock, patch

from execution_drivers import (
    BaseExecutor,
    DockerExecutor,
    ExecutionResult,
    LocalExecutor,
    RuntimeDetector,
    SecretSanitizer,
)


class TestSecretSanitizer(unittest.TestCase):
    def test_sanitize_mysql_pwd(self):
        raw = "export MYSQL_PWD=SuperSecretPassword123; mysql -u root"
        sanitized = SecretSanitizer.sanitize(raw)
        self.assertNotIn("SuperSecretPassword123", sanitized)
        self.assertIn("MYSQL_PWD=***", sanitized)

    def test_sanitize_pgpassword(self):
        raw = "PGPASSWORD='my_pg_pass' psql -U postgres"
        sanitized = SecretSanitizer.sanitize(raw)
        self.assertNotIn("my_pg_pass", sanitized)
        self.assertIn("PGPASSWORD=***", sanitized)

    def test_sanitize_cli_flag(self):
        raw = "mariadb -u root -pSecret123 -e 'SELECT 1;'"
        sanitized = SecretSanitizer.sanitize(raw)
        self.assertNotIn("Secret123", sanitized)
        self.assertIn("-p***", sanitized)


class TestRuntimeDetector(unittest.TestCase):
    def test_detect_dockerenv_file(self):
        def mock_runner(cmd, remote_host=None):
            if "dockerenv" in cmd:
                return "FOUND_DOCKERENV", "", 0
            return "", "", 1

        res = RuntimeDetector.inspect(runner=mock_runner)
        self.assertTrue(res["is_container"])
        self.assertEqual(res["runtime"], "docker")
        self.assertIn("file:/.dockerenv", res["evidence"])

    def test_detect_podman_containerenv_file(self):
        def mock_runner(cmd, remote_host=None):
            if "containerenv" in cmd:
                return "FOUND_CONTAINERENV", "", 0
            return "", "", 1

        res = RuntimeDetector.inspect(runner=mock_runner)
        self.assertTrue(res["is_container"])
        self.assertEqual(res["runtime"], "podman")
        self.assertIn("file:/run/.containerenv", res["evidence"])

    def test_detect_cgroups_v1_docker(self):
        def mock_runner(cmd, remote_host=None):
            if "cat /proc/1/cgroup" in cmd:
                return "1:name=systemd:/docker/a1b2c3d4e5f67890\n2:cpu:/docker/a1b2c3d4e5f67890", "", 0
            return "", "", 1

        res = RuntimeDetector.inspect(runner=mock_runner)
        self.assertTrue(res["is_container"])
        self.assertEqual(res["runtime"], "docker")
        self.assertEqual(res["cgroup_version"], "v1")
        self.assertEqual(res["container_id"], "a1b2c3d4e5f6")

    def test_detect_cgroups_v2_docker_slice(self):
        def mock_runner(cmd, remote_host=None):
            if "cat /proc/1/cgroup" in cmd:
                return "0::/system.slice/docker-1234567890ab.scope", "", 0
            return "", "", 1

        res = RuntimeDetector.inspect(runner=mock_runner)
        self.assertTrue(res["is_container"])
        self.assertEqual(res["runtime"], "docker")
        self.assertEqual(res["cgroup_version"], "v2")

    def test_detect_baremetal(self):
        def mock_runner(cmd, remote_host=None):
            if "cat /proc/1/cgroup" in cmd:
                return "0::/init.scope", "", 0
            return "", "", 1

        res = RuntimeDetector.inspect(runner=mock_runner)
        self.assertFalse(res["is_container"])
        self.assertEqual(res["runtime"], "baremetal")


class TestExecutionResult(unittest.TestCase):
    def test_result_properties(self):
        r = ExecutionResult(stdout="hello", stderr="", returncode=0, duration_ms=12.5, driver_type="LOCAL_BAREMETAL")
        self.assertTrue(r.is_success)
        self.assertFalse(r.is_timeout)
        self.assertEqual(r.to_tuple(), ("hello", "", 0))
        d = r.to_dict()
        self.assertEqual(d["stdout"], "hello")
        self.assertEqual(d["returncode"], 0)

    def test_timeout_detection(self):
        r = ExecutionResult(stdout="", stderr="Command execution timed out after 10 seconds", returncode=-1)
        self.assertTrue(r.is_timeout)
        self.assertFalse(r.is_success)


class TestExecutors(unittest.TestCase):
    @patch("subprocess.run")
    def test_local_executor_success(self, mock_run):
        mock_proc = MagicMock()
        mock_proc.stdout = "10.6.18-MariaDB\n"
        mock_proc.stderr = ""
        mock_proc.returncode = 0
        mock_run.return_value = mock_proc

        executor = LocalExecutor(db_user="root", db_password="secret_password")
        res = executor.execute("mariadb -e 'SELECT @@version;'", timeout=5)

        self.assertTrue(res.is_success)
        self.assertEqual(res.stdout, "10.6.18-MariaDB")
        self.assertEqual(res.driver_type, "LOCAL_BAREMETAL")
        self.assertTrue(mock_run.called)
        called_env = mock_run.call_args[1]["env"]
        self.assertEqual(called_env.get("MYSQL_PWD"), "secret_password")

    @patch("subprocess.run")
    def test_docker_executor(self, mock_run):
        mock_proc = MagicMock()
        mock_proc.stdout = "ACTIVE\n"
        mock_proc.stderr = ""
        mock_proc.returncode = 0
        mock_run.return_value = mock_proc

        executor = DockerExecutor(container_name="mariadb106-test", db_user="auditor")
        res = executor.execute("systemctl is-active mariadb")

        self.assertTrue(res.is_success)
        self.assertEqual(res.stdout, "ACTIVE")
        self.assertEqual(res.driver_type, "LOCAL_DOCKER")
        self.assertTrue(mock_run.called)
        called_cmd = mock_run.call_args[0][0][2]
        self.assertIn("docker exec -i", called_cmd)
        self.assertIn("mariadb106-test", called_cmd)

    @patch("subprocess.run")
    def test_local_executor_escalation(self, mock_run):
        mock_proc = MagicMock()
        mock_proc.stdout = "root_data\n"
        mock_proc.stderr = ""
        mock_proc.returncode = 0
        mock_run.return_value = mock_proc

        executor = LocalExecutor()
        res = executor.execute("cat /var/lib/mysql/ibdata1", as_user="mysql")

        self.assertTrue(res.is_success)
        self.assertEqual(res.stdout, "root_data")
        called_cmd = mock_run.call_args[0][0][2]
        self.assertIn("sudo -n -u mysql", called_cmd)


if __name__ == "__main__":
    unittest.main()
