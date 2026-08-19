#!/usr/bin/env python3
"""
Unit test suite for docker_transport.py (Python PSL ONLY).
Tests Docker daemon probing, container discovery heuristics, and deterministic transport resolution.
"""

import json
import unittest
from unittest.mock import MagicMock, patch

from docker_transport import (
    ContainerInfo,
    DockerContainerDiscovery,
    DockerDaemonProbe,
    DockerTransportResolver,
)


class TestDockerTransport(unittest.TestCase):
    """Test suite for Docker transport discovery and resolution."""

    def test_container_info_properties(self):
        """Verify ContainerInfo serialization and properties."""
        c = ContainerInfo(
            container_id="abcdef1234567890abcdef",
            name="/mariadb106-test",
            image="mariadb:10.6",
            status="Up 2 hours",
            is_running=True,
            ip_address="172.17.0.2",
            ports=["3306/tcp"],
            mounts=[{"source": "/var/lib/mysql", "destination": "/var/lib/mysql", "mode": "rw", "rw": True}],
            labels={"cis.benchmark": "mariadb106"}
        )
        self.assertEqual(c.short_id, "abcdef123456")
        self.assertEqual(c.name, "mariadb106-test")
        self.assertTrue(c.is_running)
        self.assertEqual(c.ip_address, "172.17.0.2")

        d = c.to_dict()
        self.assertEqual(d["name"], "mariadb106-test")
        self.assertEqual(d["short_id"], "abcdef123456")
        self.assertEqual(d["labels"]["cis.benchmark"], "mariadb106")

    @patch("subprocess.run")
    def test_daemon_probe_available(self, mock_run):
        """Test Docker daemon availability check when daemon is running."""
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "24.0.5\n"
        mock_run.return_value = mock_proc

        self.assertTrue(DockerDaemonProbe.is_daemon_available())

    @patch("subprocess.run")
    def test_daemon_probe_unavailable(self, mock_run):
        """Test Docker daemon availability check when daemon is unreachable."""
        mock_proc = MagicMock()
        mock_proc.returncode = 1
        mock_proc.stdout = ""
        mock_proc.stderr = "Cannot connect to the Docker daemon"
        mock_run.return_value = mock_proc

        self.assertFalse(DockerDaemonProbe.is_daemon_available())

    @patch("subprocess.run")
    def test_daemon_get_info(self, mock_run):
        """Test daemon info extraction."""
        info_json = json.dumps({
            "ServerVersion": "24.0.7",
            "OperatingSystem": "Ubuntu 22.04.3 LTS",
            "Architecture": "x86_64",
            "ContainersRunning": 3,
            "Containers": 5,
            "CgroupVersion": "2",
            "DockerRootDir": "/var/lib/docker",
            "Driver": "overlay2"
        })
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = info_json
        mock_run.return_value = mock_proc

        d = DockerDaemonProbe.get_daemon_info()
        self.assertTrue(d["available"])
        self.assertEqual(d["server_version"], "24.0.7")
        self.assertEqual(d["containers_running"], 3)
        self.assertEqual(d["cgroup_version"], "2")

    @patch("subprocess.run")
    def test_list_containers(self, mock_run):
        """Test listing multiple containers from Docker ps output."""
        line1 = json.dumps({"ID": "111122223333", "Names": "mariadb106-test", "Image": "mariadb:10.6", "Status": "Up 1 hour", "State": "running", "Ports": "3306/tcp"})
        line2 = json.dumps({"ID": "444455556666", "Names": "postgresql16-test", "Image": "postgres:16", "Status": "Exited (0) 5 mins ago", "State": "exited", "Ports": ""})

        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = f"{line1}\n{line2}\n"
        mock_run.return_value = mock_proc

        containers = DockerContainerDiscovery.list_containers()
        self.assertEqual(len(containers), 2)
        self.assertEqual(containers[0].name, "mariadb106-test")
        self.assertTrue(containers[0].is_running)
        self.assertEqual(containers[1].name, "postgresql16-test")
        self.assertFalse(containers[1].is_running)

    @patch("docker_transport.DockerContainerDiscovery.list_containers")
    @patch("docker_transport.DockerContainerDiscovery.inspect_container")
    def test_find_container_for_product(self, mock_inspect, mock_list):
        """Test finding container for benchmark product."""
        mock_c = ContainerInfo(
            container_id="aabbccddeeff",
            name="mariadb106-test",
            image="mariadb:10.6",
            status="Up 10m",
            is_running=True
        )
        mock_list.return_value = [mock_c]
        mock_inspect.return_value = mock_c

        found = DockerContainerDiscovery.find_container_for_product("mariadb106")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "mariadb106-test")

    @patch("docker_transport.DockerDaemonProbe.is_daemon_available")
    @patch("docker_transport.DockerContainerDiscovery.find_container_for_product")
    def test_transport_resolver_container_priority(self, mock_find, mock_daemon):
        """Test that Docker transport resolver chooses CONTAINER_EXEC when container found."""
        mock_daemon.return_value = True
        mock_c = ContainerInfo(
            container_id="1234567890ab",
            name="mariadb106-test",
            image="mariadb:10.6",
            status="Up",
            is_running=True
        )
        mock_find.return_value = mock_c

        mode, target_c, meta = DockerTransportResolver.resolve_transport(
            mode="local",
            product_hint="mariadb106"
        )
        self.assertEqual(mode, DockerTransportResolver.TRANSPORT_CONTAINER_EXEC)
        self.assertIsNotNone(target_c)
        self.assertEqual(target_c.name, "mariadb106-test")
        self.assertEqual(meta["transport"], DockerTransportResolver.TRANSPORT_CONTAINER_EXEC)

    @patch("docker_transport.DockerDaemonProbe.is_daemon_available")
    @patch("docker_transport.DockerContainerDiscovery.find_container_for_product")
    def test_transport_resolver_fallback_baremetal(self, mock_find, mock_daemon):
        """Test transport resolver falls back to LOCAL_BAREMETAL with warning when no container matches."""
        mock_daemon.return_value = True
        mock_find.return_value = None

        mode, target_c, meta = DockerTransportResolver.resolve_transport(
            mode="local",
            product_hint="rhel9"
        )
        self.assertEqual(mode, DockerTransportResolver.TRANSPORT_LOCAL_BAREMETAL)
        self.assertIsNone(target_c)
        self.assertIn("warning", meta)

    def test_transport_resolver_ssh_modes(self):
        """Test transport resolver in SSH modes."""
        mode, _, meta = DockerTransportResolver.resolve_transport(
            mode="ssh",
            remote_host="192.168.1.10",
            docker_container="mariadb106-prod"
        )
        self.assertEqual(mode, DockerTransportResolver.TRANSPORT_SSH_CONTAINER_EXEC)
        self.assertEqual(meta["container_name"], "mariadb106-prod")

        mode2, _, meta2 = DockerTransportResolver.resolve_transport(
            mode="ssh",
            remote_host="192.168.1.10"
        )
        self.assertEqual(mode2, DockerTransportResolver.TRANSPORT_SSH_HOST)


if __name__ == "__main__":
    unittest.main()
