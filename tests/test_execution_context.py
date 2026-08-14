#!/usr/bin/env python3
"""
Unit tests for unified execution context detection (Local Bare-Metal, Local Docker, Remote SSH, Remote SSH Docker) (100% PSL ONLY).
"""

import unittest
from unittest.mock import patch


def detect_execution_context(mode="local", remote_host=None, docker_container=None, product_hint=None, runner=None):
    """
    Detect and categorize execution context into structured dictionary (PSL ONLY).
    
    Returns:
        dict: {
            "type": "LOCAL_BAREMETAL" | "LOCAL_DOCKER" | "REMOTE_SSH_BAREMETAL" | "REMOTE_SSH_DOCKER",
            "mode": "local" | "ssh",
            "remote_host": str | None,
            "docker_container": str | None,
            "is_docker": bool,
            "is_remote": bool,
            "label": str
        }
    """
    is_remote = bool(mode == "ssh" or remote_host)
    active_container = docker_container

    # Auto-detect container if not explicitly given
    if not active_container and runner and product_hint:
        try:
            cmd = "docker ps --format '{{.Names}}' 2>/dev/null"
            stdout, stderr, ret = runner(cmd, remote_host=remote_host)
            if ret == 0 and stdout:
                for line in stdout.splitlines():
                    name = line.strip()
                    if product_hint.lower() in name.lower():
                        active_container = name
                        break
        except Exception:
            active_container = None

    is_docker = bool(active_container)

    if is_remote and is_docker:
        ctype = "REMOTE_SSH_DOCKER"
        label = f"Remote SSH + Docker ({remote_host} -> {active_container})"
    elif is_remote:
        ctype = "REMOTE_SSH_BAREMETAL"
        label = f"Remote SSH ({remote_host})"
    elif is_docker:
        ctype = "LOCAL_DOCKER"
        label = f"Local Docker ({active_container})"
    else:
        ctype = "LOCAL_BAREMETAL"
        label = "Local Bare-Metal"

    return {
        "type": ctype,
        "mode": "ssh" if is_remote else "local",
        "remote_host": remote_host if is_remote else None,
        "docker_container": active_container,
        "is_docker": is_docker,
        "is_remote": is_remote,
        "label": label
    }


class TestExecutionContextDetection(unittest.TestCase):
    def test_local_baremetal_context(self):
        ctx = detect_execution_context(mode="local", remote_host=None, docker_container=None)
        self.assertEqual(ctx["type"], "LOCAL_BAREMETAL")
        self.assertFalse(ctx["is_docker"])
        self.assertFalse(ctx["is_remote"])
        self.assertIsNone(ctx["docker_container"])
        self.assertIsNone(ctx["remote_host"])
        self.assertEqual(ctx["label"], "Local Bare-Metal")

    def test_local_explicit_docker_context(self):
        ctx = detect_execution_context(mode="local", remote_host=None, docker_container="cis_mysql_84")
        self.assertEqual(ctx["type"], "LOCAL_DOCKER")
        self.assertTrue(ctx["is_docker"])
        self.assertFalse(ctx["is_remote"])
        self.assertEqual(ctx["docker_container"], "cis_mysql_84")
        self.assertEqual(ctx["label"], "Local Docker (cis_mysql_84)")

    def test_local_autodetect_docker_context(self):
        mock_runner = lambda cmd, remote_host=None: ("redis_db\ncis_mariadb_1011\nnginx", "", 0)
        ctx = detect_execution_context(mode="local", remote_host=None, docker_container=None, product_hint="mariadb", runner=mock_runner)
        self.assertEqual(ctx["type"], "LOCAL_DOCKER")
        self.assertTrue(ctx["is_docker"])
        self.assertEqual(ctx["docker_container"], "cis_mariadb_1011")

    def test_remote_ssh_baremetal_context(self):
        ctx = detect_execution_context(mode="ssh", remote_host="admin@192.168.1.100", docker_container=None)
        self.assertEqual(ctx["type"], "REMOTE_SSH_BAREMETAL")
        self.assertFalse(ctx["is_docker"])
        self.assertTrue(ctx["is_remote"])
        self.assertEqual(ctx["remote_host"], "admin@192.168.1.100")
        self.assertEqual(ctx["label"], "Remote SSH (admin@192.168.1.100)")

    def test_remote_ssh_docker_context(self):
        ctx = detect_execution_context(mode="ssh", remote_host="root@db-server.prod", docker_container="prod_postgres_16")
        self.assertEqual(ctx["type"], "REMOTE_SSH_DOCKER")
        self.assertTrue(ctx["is_docker"])
        self.assertTrue(ctx["is_remote"])
        self.assertEqual(ctx["remote_host"], "root@db-server.prod")
        self.assertEqual(ctx["docker_container"], "prod_postgres_16")
        self.assertEqual(ctx["label"], "Remote SSH + Docker (root@db-server.prod -> prod_postgres_16)")


if __name__ == "__main__":
    unittest.main()
