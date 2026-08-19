#!/usr/bin/env python3
"""
Exhaustive unit tests for Execution Drivers & Multi-Criteria Runtime Detection (100% PSL ONLY).
"""

import unittest
from unittest.mock import MagicMock, patch

from execution_drivers import (
    BaseExecutor,
    DockerExecutor,
    ExecutionResult,
    LocalExecutor,
    RemoteSSHContainerExecutor,
    RuntimeDetector,
    SecretSanitizer,
    SSHExecutor,
    create_executor,
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

    @patch("subprocess.run")
    def test_ssh_executor_success(self, mock_run):
        mock_proc = MagicMock()
        mock_proc.stdout = "SSH_OK\n"
        mock_proc.stderr = "Warning: Permanently added '10.0.0.1' (ED25519) to the list of known hosts.\n"
        mock_proc.returncode = 0
        mock_run.return_value = mock_proc

        executor = SSHExecutor(remote_host="admin@10.0.0.1")
        res = executor.execute("uptime")

        self.assertTrue(res.is_success)
        self.assertEqual(res.stdout, "SSH_OK")
        self.assertEqual(res.stderr, "")
        self.assertEqual(res.driver_type, "REMOTE_SSH_BAREMETAL")

    @patch("subprocess.run")
    def test_ssh_executor_custom_options(self, mock_run):
        mock_proc = MagicMock()
        mock_proc.stdout = "OK\n"
        mock_proc.stderr = ""
        mock_proc.returncode = 0
        mock_run.return_value = mock_proc

        executor = SSHExecutor(
            remote_host="admin@10.0.0.1",
            ssh_port=2222,
            ssh_key="/root/.ssh/custom_id_rsa"
        )
        res = executor.execute("hostname")

        self.assertTrue(res.is_success)
        called_args = mock_run.call_args[0][0]
        self.assertIn("-p", called_args)
        self.assertIn("2222", called_args)
        self.assertIn("-i", called_args)
        self.assertIn("/root/.ssh/custom_id_rsa", called_args)

    @patch("subprocess.run")
    def test_remote_ssh_container_executor(self, mock_run):
        mock_proc = MagicMock()
        mock_proc.stdout = "CONTAINER_REMOTE_OK\n"
        mock_proc.stderr = ""
        mock_proc.returncode = 0
        mock_run.return_value = mock_proc

        executor = RemoteSSHContainerExecutor(remote_host="admin@10.0.0.1", container_name="mariadb-prod")
        res = executor.execute("mysql -e 'SELECT 1;'")

        self.assertTrue(res.is_success)
        self.assertEqual(res.stdout, "CONTAINER_REMOTE_OK")
        self.assertEqual(res.driver_type, "REMOTE_SSH_DOCKER")

    @patch("subprocess.run")
    def test_base_executor_read_file_and_exists(self, mock_run):
        mock_proc = MagicMock()
        mock_proc.stdout = "config_data_123\n"
        mock_proc.stderr = ""
        mock_proc.returncode = 0
        mock_run.return_value = mock_proc

        executor = LocalExecutor()
        content = executor.read_file("/etc/mysql/my.cnf")
        self.assertEqual(content, "config_data_123")
        self.assertTrue(executor.file_exists("/etc/mysql/my.cnf"))

        meta = executor.get_metadata()
        self.assertEqual(meta["driver_type"], "LOCAL_BAREMETAL")


class TestExecutorFactory(unittest.TestCase):
    def test_create_local_baremetal(self):
        executor = create_executor(mode="local", remote_host=None, docker_container=None)
        self.assertIsInstance(executor, LocalExecutor)
        self.assertEqual(executor.driver_type, "LOCAL_BAREMETAL")

    def test_create_local_docker(self):
        executor = create_executor(mode="local", remote_host=None, docker_container="mariadb106-test")
        self.assertIsInstance(executor, DockerExecutor)
        self.assertEqual(executor.driver_type, "LOCAL_DOCKER")
        self.assertEqual(executor.container_name, "mariadb106-test")

    def test_create_remote_ssh(self):
        executor = create_executor(mode="ssh", remote_host="root@db.example.com", docker_container=None)
        self.assertIsInstance(executor, SSHExecutor)
        self.assertEqual(executor.driver_type, "REMOTE_SSH_BAREMETAL")

    def test_create_remote_ssh_docker(self):
        executor = create_executor(mode="ssh", remote_host="root@db.example.com", docker_container="db_container")
        self.assertIsInstance(executor, RemoteSSHContainerExecutor)
        self.assertEqual(executor.driver_type, "REMOTE_SSH_DOCKER")


if __name__ == "__main__":
    unittest.main()
