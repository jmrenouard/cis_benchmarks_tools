#!/usr/bin/env python3
"""
Docker In-Container Transport, Runtime Discovery & Health Probe Module.
Provides deterministic transport resolution, container discovery, daemon health inspection,
and high-fidelity in-container execution primitives.

100% Python Standard Library (PSL ONLY).
"""

import json
import os
import re
import shlex
import subprocess
import time
from typing import Dict, List, Optional, Tuple, Any


class DockerDaemonProbe:
    """Probes and validates local or remote Docker daemon accessibility (PSL ONLY)."""

    @classmethod
    def is_daemon_available(cls, container_cli: str = "docker", timeout: int = 5) -> bool:
        """Check if Docker daemon is responsive."""
        try:
            p = subprocess.run(
                [container_cli, "info", "--format", "{{.ServerVersion}}"],
                capture_output=True, text=True, timeout=timeout, check=False, stdin=subprocess.DEVNULL
            )
            return p.returncode == 0 and len(p.stdout.strip()) > 0
        except Exception:
            return False

    @classmethod
    def get_daemon_info(cls, container_cli: str = "docker", timeout: int = 5) -> Dict[str, Any]:
        """Inspect Docker daemon and return structured configuration details."""
        try:
            p = subprocess.run(
                [container_cli, "info", "--format", "{{json .}}"],
                capture_output=True, text=True, timeout=timeout, check=False, stdin=subprocess.DEVNULL
            )
            if p.returncode == 0 and p.stdout.strip():
                data = json.loads(p.stdout.strip())
                return {
                    "available": True,
                    "server_version": data.get("ServerVersion", "unknown"),
                    "operating_system": data.get("OperatingSystem", "unknown"),
                    "architecture": data.get("Architecture", "unknown"),
                    "containers_running": data.get("ContainersRunning", 0),
                    "containers_total": data.get("Containers", 0),
                    "cgroup_version": data.get("CgroupVersion", "unknown"),
                    "root_dir": data.get("DockerRootDir", "/var/lib/docker"),
                    "driver": data.get("Driver", "overlay2"),
                }
        except Exception:
            pass

        return {"available": False, "server_version": None, "operating_system": None, "architecture": None, "containers_running": 0, "containers_total": 0, "cgroup_version": "unknown", "root_dir": None, "driver": None}


class ContainerInfo:
    """Rich structured descriptor for a target Docker container."""

    def __init__(self, container_id: str, name: str, image: str, status: str, is_running: bool, ip_address: Optional[str] = None, ports: Optional[List[str]] = None, mounts: Optional[List[Dict[str, str]]] = None, labels: Optional[Dict[str, str]] = None, created_at: Optional[str] = None, entrypoint: Optional[List[str]] = None, cmd: Optional[List[str]] = None):
        self.container_id = container_id
        self.short_id = container_id[:12] if container_id else ""
        self.name = name.lstrip("/") if name else ""
        self.image = image or ""
        self.status = status or ""
        self.is_running = is_running
        self.ip_address = ip_address
        self.ports = ports or []
        self.mounts = mounts or []
        self.labels = labels or {}
        self.created_at = created_at
        self.entrypoint = entrypoint or []
        self.cmd = cmd or []

    def to_dict(self) -> Dict[str, Any]:
        return {"container_id": self.container_id, "short_id": self.short_id, "name": self.name, "image": self.image, "status": self.status, "is_running": self.is_running, "ip_address": self.ip_address, "ports": self.ports, "mounts": self.mounts, "labels": self.labels, "created_at": self.created_at, "entrypoint": self.entrypoint, "cmd": self.cmd}


class DockerContainerDiscovery:
    """Discovers and inspects active and dormant Docker containers (PSL ONLY)."""

    PRODUCT_CONTAINER_HINTS: Dict[str, List[str]] = {
        "mariadb106": ["mariadb106-test", "mariadb-10.6", "mariadb106", "mariadb_106"],
        "mariadb1011": ["mariadb1011-test", "mariadb-10.11", "mariadb1011", "mariadb_1011"],
        "mysql80": ["mysql80-test", "mysql-8.0", "mysql80", "mysql_80"],
        "mysql-community84": ["mysql-community84-test", "mysql-community-8.4", "mysql84-community"],
        "mysql-enterprise84": ["mysql-enterprise84-test", "mysql-enterprise-8.4", "mysql84-enterprise"],
        "mysql-community97": ["mysql-community97-test", "mysql-community-9.7", "mysql97-community"],
        "mysql-enterprise97": ["mysql-enterprise97-test", "mysql-enterprise-9.7", "mysql97-enterprise"],
        "postgresql16": ["postgresql16-test", "postgres-16", "postgres16", "postgresql_16"],
        "postgresql17": ["postgresql17-test", "postgres-17", "postgres17", "postgresql_17"],
        "postgresql18": ["postgresql18-test", "postgres-18", "postgres18", "postgresql_18"],
        "mongodb7": ["mongodb7-test", "mongo-7.0", "mongo7", "mongodb_7"],
        "mongodb8": ["mongodb8-test", "mongo-8.0", "mongo8", "mongodb_8"],
        "cassandra40": ["cassandra40-test", "cassandra-4.0", "cassandra40"],
        "cassandra41": ["cassandra41-test", "cassandra-4.1", "cassandra41"],
        "cassandra50": ["cassandra50-test", "cassandra-5.0", "cassandra50"],
    }

    @classmethod
    def list_containers(cls, container_cli: str = "docker", all_containers: bool = True, timeout: int = 5) -> List[ContainerInfo]:
        """List and inspect all containers via Docker CLI (PSL ONLY)."""
        cmd = [container_cli, "ps", "--format", "{{json .}}"]
        if all_containers: cmd.append("-a")
        containers: List[ContainerInfo] = []
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False, stdin=subprocess.DEVNULL)
            if p.returncode == 0 and p.stdout.strip():
                for line in p.stdout.strip().splitlines():
                    if not line.strip(): continue
                    try:
                        raw = json.loads(line.strip())
                        state = str(raw.get("State", "")).lower()
                        containers.append(ContainerInfo(
                            container_id=raw.get("ID", ""),
                            name=raw.get("Names", ""),
                            image=raw.get("Image", ""),
                            status=raw.get("Status", ""),
                            is_running=(state == "running" or "up" in raw.get("Status", "").lower()),
                            ports=raw.get("Ports", "").split(",") if raw.get("Ports") else [],
                            created_at=raw.get("CreatedAt", "")
                        ))
                    except json.JSONDecodeError:
                        continue
        except Exception:
            pass
        return containers

    @classmethod
    def inspect_container(cls, container_name_or_id: str, container_cli: str = "docker", timeout: int = 5) -> Optional[ContainerInfo]:
        """Deep inspect a specific container by name or ID (PSL ONLY)."""
        if not container_name_or_id: return None
        try:
            p = subprocess.run([container_cli, "inspect", container_name_or_id], capture_output=True, text=True, timeout=timeout, check=False, stdin=subprocess.DEVNULL)
            if p.returncode == 0 and p.stdout.strip():
                data = json.loads(p.stdout.strip())
                if isinstance(data, list) and len(data) > 0:
                    raw = data[0]
                    c_id = raw.get("Id", "")
                    name = raw.get("Name", "").lstrip("/")
                    config = raw.get("Config", {})
                    state = raw.get("State", {})
                    net = raw.get("NetworkSettings", {})
                    mounts = raw.get("Mounts", [])
                    ip_addr = net.get("IPAddress")
                    if not ip_addr and net.get("Networks"):
                        for _, n_info in net.get("Networks", {}).items():
                            if n_info.get("IPAddress"):
                                ip_addr = n_info.get("IPAddress")
                                break
                    mount_list = [{"source": m.get("Source", ""), "destination": m.get("Destination", ""), "mode": m.get("Mode", ""), "rw": m.get("RW", True)} for m in mounts]
                    return ContainerInfo(
                        container_id=c_id, name=name, image=config.get("Image", ""), status=state.get("Status", "unknown"),
                        is_running=state.get("Running", False), ip_address=ip_addr, mounts=mount_list,
                        labels=config.get("Labels", {}) or {}, created_at=raw.get("Created", ""),
                        entrypoint=config.get("Entrypoint", []) or [], cmd=config.get("Cmd", []) or []
                    )
        except Exception:
            pass
        return None

    @classmethod
    def find_container_for_product(cls, product_key: str, container_cli: str = "docker", must_be_running: bool = False) -> Optional[ContainerInfo]:
        """Automatically find the matching container for a CIS benchmark product."""
        containers = cls.list_containers(container_cli=container_cli, all_containers=True)
        norm_key = product_key.lower().replace("-", "").replace("_", "")
        hints = cls.PRODUCT_CONTAINER_HINTS.get(product_key, [product_key])
        for c in containers:
            if must_be_running and not c.is_running: continue
            for h in hints:
                if c.name == h or c.name.lower() == h.lower():
                    return cls.inspect_container(c.container_id, container_cli=container_cli) or c
        for c in containers:
            if must_be_running and not c.is_running: continue
            for h in hints:
                if h in c.name or h in c.image:
                    return cls.inspect_container(c.container_id, container_cli=container_cli) or c
        for c in containers:
            if must_be_running and not c.is_running: continue
            c_norm = c.name.lower().replace("-", "").replace("_", "")
            if norm_key in c_norm or c_norm in norm_key:
                return cls.inspect_container(c.container_id, container_cli=container_cli) or c
        return None


class DockerTransportResolver:
    """Deterministically resolves optimal execution transport with container-first priority."""

    TRANSPORT_CONTAINER_EXEC = "CONTAINER_EXEC"
    TRANSPORT_SSH_CONTAINER_EXEC = "SSH_CONTAINER_EXEC"
    TRANSPORT_SSH_HOST = "SSH_HOST"
    TRANSPORT_LOCAL_BAREMETAL = "LOCAL_BAREMETAL"

    @classmethod
    def resolve_transport(cls, mode: str = "local", remote_host: Optional[str] = None, docker_container: Optional[str] = None, product_hint: Optional[str] = None, container_cli: str = "docker") -> Tuple[str, Optional[ContainerInfo], Dict[str, Any]]:
        """Resolves transport: (transport_mode, target_container_info, telemetry_meta)."""
        telemetry: Dict[str, Any] = {
            "requested_mode": mode, "remote_host": remote_host, "requested_container": docker_container,
            "product_hint": product_hint, "resolved_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "daemon_available": DockerDaemonProbe.is_daemon_available(container_cli=container_cli),
        }
        if mode == "ssh" or remote_host:
            if docker_container:
                telemetry["transport"] = cls.TRANSPORT_SSH_CONTAINER_EXEC
                telemetry["container_name"] = docker_container
                return cls.TRANSPORT_SSH_CONTAINER_EXEC, None, telemetry
            telemetry["transport"] = cls.TRANSPORT_SSH_HOST
            return cls.TRANSPORT_SSH_HOST, None, telemetry

        target_container: Optional[ContainerInfo] = None
        if docker_container:
            target_container = DockerContainerDiscovery.inspect_container(docker_container, container_cli=container_cli) or ContainerInfo(container_id=docker_container, name=docker_container, image="unknown", status="specified", is_running=True)
        elif product_hint:
            target_container = DockerContainerDiscovery.find_container_for_product(product_hint, container_cli=container_cli, must_be_running=False)

        if target_container:
            telemetry["transport"] = cls.TRANSPORT_CONTAINER_EXEC
            telemetry["container_name"] = target_container.name
            telemetry["container_id"] = target_container.container_id
            telemetry["is_running"] = target_container.is_running
            return cls.TRANSPORT_CONTAINER_EXEC, target_container, telemetry

        telemetry["transport"] = cls.TRANSPORT_LOCAL_BAREMETAL
        telemetry["warning"] = "Operating in local bare-metal mode: no matching Docker container resolved."
        return cls.TRANSPORT_LOCAL_BAREMETAL, None, telemetry
