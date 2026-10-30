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
        self.assertFalse(r.is_environment_error)
        self.assertEqual(r.failure_category, "CLEAN_PASS")
        self.assertEqual(r.to_tuple(), ("hello", "", 0))
        d = r.to_dict()
        self.assertEqual(d["stdout"], "hello")
        self.assertEqual(d["returncode"], 0)
        self.assertIn("diagnostic", d)

    def test_timeout_detection(self):
        r = ExecutionResult(stdout="", stderr="Command execution timed out after 10 seconds", returncode=-1)
        self.assertTrue(r.is_timeout)
        self.assertFalse(r.is_success)
        self.assertTrue(r.is_environment_error)
        self.assertEqual(r.failure_category, "TIMEOUT")

    def test_missing_binary_diagnostic(self):
        r = ExecutionResult(command_masked="mongosh --eval 'db.version()'", stdout="", stderr="/bin/bash: mongosh: command not found", returncode=127)
        self.assertFalse(r.is_success)
        self.assertTrue(r.is_environment_error)
        self.assertEqual(r.failure_category, "MISSING_BINARY")
        self.assertIn("mongosh", r.diagnostic.remediation_suggestion)


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
        called_args = mock_run.call_args[0][0]
        self.assertEqual(called_args[:3], ["docker", "exec", "-i"])
        self.assertIn("mariadb106-test", called_args)
        self.assertIn("systemctl is-active mariadb", called_args)

    @patch("subprocess.run")
    def test_docker_executor_db_password_not_in_argv(self, mock_run):
        """Finding 6: verify DockerExecutor passes -e MYSQL_PWD without secret in argv, secret in env."""
        mock_proc = MagicMock(stdout="ok\n", stderr="", returncode=0)
        mock_run.return_value = mock_proc

        executor = DockerExecutor(container_name="mariadb106-test", db_password="SuperSecretPassword999!")
        res = executor.execute("mariadb -e 'SELECT 1;'")

        self.assertTrue(res.is_success)
        called_args = mock_run.call_args[0][0]
        called_cmd = " ".join(called_args)
        self.assertNotIn("SuperSecretPassword999!", called_cmd)
        self.assertIn("-e", called_args)
        self.assertIn("MYSQL_PWD", called_args)
        called_env = mock_run.call_args[1].get("env", {})
        self.assertEqual(called_env.get("MYSQL_PWD"), "SuperSecretPassword999!")
        self.assertEqual(called_env.get("PGPASSWORD"), "SuperSecretPassword999!")

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
    def test_docker_executor_bypasses_host_shell(self, mock_run):
        """Finding 5: verify DockerExecutor does not invoke /bin/bash on host and passes parts directly."""
        mock_proc = MagicMock(stdout="ok\n", stderr="", returncode=0)
        mock_run.return_value = mock_proc

        executor = DockerExecutor(container_name="test_cont")
        dangerous_cmd = 'echo $USER $(id) `whoami` && cat /tmp/test'
        res = executor.execute(dangerous_cmd)

        self.assertTrue(res.is_success)
        called_cmd = mock_run.call_args[0][0]
        # Must be invoked directly without host bash
        self.assertEqual(called_cmd[0], "docker")
        self.assertEqual(called_cmd[1], "exec")
        self.assertNotIn("/bin/bash", called_cmd[0:2])
        # The command must be passed verbatim to in-container bash without host shell evaluation
        self.assertIn(dangerous_cmd, called_cmd)

    @patch("subprocess.run")
    def test_ssh_executor_as_user_quoting(self, mock_run):
        """Finding 5: verify SSHExecutor quotes as_user safely."""
        mock_proc = MagicMock(stdout="ok\n", stderr="", returncode=0)
        mock_run.return_value = mock_proc

        executor = SSHExecutor(remote_host="user@host")
        executor.execute("id", as_user="test user; rm -rf /")

        called_cmd = mock_run.call_args[0][0]
        # In ssh_args, target_cmd is quoted for remote /bin/bash -c
        ssh_payload = called_cmd[-1]
        self.assertIn("sudo -n -u", ssh_payload)
        self.assertIn("test user; rm -rf /", ssh_payload)
        # Verify semicolon does not terminate command
        self.assertNotIn("; rm -rf / /bin/bash", ssh_payload)

    @patch("subprocess.run")
    def test_remote_ssh_container_executor_quoting(self, mock_run):
        """Finding 5: verify RemoteSSHContainerExecutor quotes command and flags safely."""
        mock_proc = MagicMock(stdout="ok\n", stderr="", returncode=0)
        mock_run.return_value = mock_proc

        executor = RemoteSSHContainerExecutor(remote_host="user@host", container_name="my_cont")
        executor.execute("echo $HOST_VAR", as_user="app user", cwd="/var/my dir")

        called_cmd = mock_run.call_args[0][0]
        ssh_payload = called_cmd[-1]
        self.assertIn("-u", ssh_payload)
        self.assertIn("app user", ssh_payload)
        self.assertIn("-w", ssh_payload)
        self.assertIn("/var/my dir", ssh_payload)
        self.assertIn("echo $HOST_VAR", ssh_payload)

    @patch("subprocess.run")
    def test_ssh_executor_hardened_connection_options(self, mock_run):
        """Finding 14 / IMP-006: verify SSHExecutor constructs hardened timeout and keepalive flags."""
        mock_proc = MagicMock(stdout="ok\n", stderr="", returncode=0)
        mock_run.return_value = mock_proc

        executor = SSHExecutor(remote_host="user@example.com")
        res = executor.execute("uptime")

        self.assertTrue(res.is_success)
        called_args = mock_run.call_args[0][0]
        self.assertIn("-o", called_args)
        self.assertIn("ConnectTimeout=10", called_args)
        self.assertIn("BatchMode=yes", called_args)
        self.assertIn("ServerAliveInterval=15", called_args)
        self.assertIn("ServerAliveCountMax=3", called_args)
        self.assertIn("StrictHostKeyChecking=no", called_args)
        self.assertIn("UserKnownHostsFile=/dev/null", called_args)
        self.assertIn("TCPKeepAlive=yes", called_args)
        self.assertEqual(mock_run.call_args[1].get("timeout"), 15)
        called_cmd_str = " ".join(called_args)
        self.assertNotIn("ControlMaster", called_cmd_str)
        self.assertNotIn("ControlPath", called_cmd_str)

    @patch("subprocess.run")
    def test_remote_ssh_container_executor_hardened_connection_options(self, mock_run):
        """Finding 14 / IMP-006: verify RemoteSSHContainerExecutor constructs hardened options."""
        mock_proc = MagicMock(stdout="ok\n", stderr="", returncode=0)
        mock_run.return_value = mock_proc

        executor = RemoteSSHContainerExecutor(remote_host="user@example.com", container_name="db")
        res = executor.execute("echo 1")

        self.assertTrue(res.is_success)
        called_args = mock_run.call_args[0][0]
        self.assertIn("ConnectTimeout=10", called_args)
        self.assertIn("BatchMode=yes", called_args)
        self.assertIn("ServerAliveInterval=15", called_args)
        self.assertIn("ServerAliveCountMax=3", called_args)
        self.assertIn("StrictHostKeyChecking=no", called_args)
        self.assertIn("UserKnownHostsFile=/dev/null", called_args)
        self.assertIn("TCPKeepAlive=yes", called_args)
        self.assertEqual(mock_run.call_args[1].get("timeout"), 15)
        called_cmd_str = " ".join(called_args)
        self.assertNotIn("ControlMaster", called_cmd_str)
        self.assertNotIn("ControlPath", called_cmd_str)

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
