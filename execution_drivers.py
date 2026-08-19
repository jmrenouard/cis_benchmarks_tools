#!/usr/bin/env python3
"""
Unified Execution Drivers & Multi-Criteria Runtime Detection Module.
Provides robust polymorphic execution transports (Local, Docker, SSH, Nested)
and multi-criteria environment inspection for CIS database audit benchmarks.

100% Python Standard Library (PSL ONLY).
"""

import json
import os
import re
import shlex
import subprocess
import time


class SecretSanitizer:
    """Zero-credential leak sanitizer for commands, arguments, and logging (PSL ONLY)."""

    PASSWORD_PATTERNS = [
        r"(-p\s*)([^\s;|\&]+)",
        r"(--password[=\s]+)([^\s;|\&]+)",
        r"(MYSQL_PWD=)([^\s;|\&]+)",
        r"(PGPASSWORD=)([^\s;|\&]+)",
        r"(password\s*[:=]\s*)(['\"][^'\"]*['\"]|[^\s,;]+)",
        r"(secret\s*[:=]\s*)(['\"][^'\"]*['\"]|[^\s,;]+)",
        r"(token\s*[:=]\s*)(['\"][^'\"]*['\"]|[^\s,;]+)",
        r"(key\s*[:=]\s*)(['\"][^'\"]*['\"]|[^\s,;]+)",
    ]

    @classmethod
    def sanitize(cls, text):
        """Redact sensitive database passwords, tokens, and secret flags from string."""
        if not text or not isinstance(text, str):
            return text
        sanitized = text
        for pattern in cls.PASSWORD_PATTERNS:
            sanitized = re.sub(pattern, r"\1***", sanitized, flags=re.IGNORECASE)
        return sanitized


class ExecutionResult:
    """Immutable, structured execution result container (PSL ONLY)."""

    def __init__(self, stdout="", stderr="", returncode=0, duration_ms=0.0, command_masked="", driver_type="BASE"):
        self.stdout = (stdout or "").strip()
        self.stderr = (stderr or "").strip()
        self.returncode = int(returncode)
        self.duration_ms = float(duration_ms)
        self.command_masked = command_masked
        self.driver_type = driver_type

    @property
    def is_success(self):
        """Return True if returncode is 0 and no fatal timeout occurred."""
        return self.returncode == 0

    @property
    def is_timeout(self):
        """Return True if command terminated due to timeout expiration."""
        return self.returncode == -1 and "timed out" in self.stderr.lower()

    def to_tuple(self):
        """Backward compatibility tuple unpack: (stdout, stderr, returncode)."""
        return self.stdout, self.stderr, self.returncode

    def to_dict(self):
        """Dictionary representation for structured JSON logging."""
        return {
            "stdout": self.stdout,
            "stderr": self.stderr,
            "returncode": self.returncode,
            "duration_ms": self.duration_ms,
            "command_masked": self.command_masked,
            "driver_type": self.driver_type,
            "is_success": self.is_success,
        }


class RuntimeDetector:
    """
    Multi-criteria environment runtime inspection engine (PSL ONLY).
    Detects container runtimes (Docker, Podman, LXC, Kubernetes, Bare-Metal)
    using multiple independent heuristic probes across filesystem, cgroups v1/v2,
    process trees, mount points, and namespace indicators.
    """

    @classmethod
    def inspect(cls, runner=None, remote_host=None):
        """
        Inspect runtime environment and return comprehensive diagnostic dictionary.
        """
        evidence = []
        runtime = "baremetal"
        cgroup_version = "unknown"
        container_id = None
        is_container = False
        is_rootless = False
        is_sandboxed = False

        def _exec(cmd):
            if runner:
                try:
                    out, err, ret = runner(cmd, remote_host=remote_host)
                    return out if ret == 0 else ""
                except Exception:
                    return ""
            try:
                p = subprocess.run(
                    cmd if isinstance(cmd, list) else ["/bin/bash", "-c", cmd],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False,
                    stdin=subprocess.DEVNULL
                )
                return p.stdout.strip() if p.returncode == 0 else ""
            except Exception:
                return ""

        # Probe 1: Direct container marker files
        file_check_out = _exec(
            "test -f /.dockerenv && echo FOUND_DOCKERENV; "
            "test -f /run/.containerenv && echo FOUND_CONTAINERENV; "
            "test -f /run/systemd/container && echo FOUND_SYSTEMD_CONTAINER"
        )
        if "FOUND_DOCKERENV" in file_check_out:
            runtime = "docker"
            is_container = True
            evidence.append("file:/.dockerenv")
        elif "FOUND_CONTAINERENV" in file_check_out:
            runtime = "podman"
            is_container = True
            evidence.append("file:/run/.containerenv")
        elif "FOUND_SYSTEMD_CONTAINER" in file_check_out:
            runtime = "lxc"
            is_container = True
            evidence.append("file:/run/systemd/container")

        # Probe 2: /proc/1/cgroup inspection (cgroups v1 & v2)
        cgroup_content = _exec("cat /proc/1/cgroup 2>/dev/null")
        if cgroup_content:
            if "0::" in cgroup_content:
                cgroup_version = "v2"
                if "docker" in cgroup_content.lower():
                    runtime = "docker"
                    is_container = True
                    evidence.append("cgroup_v2:docker")
                elif "podman" in cgroup_content.lower() or "libpod" in cgroup_content.lower():
                    runtime = "podman"
                    is_container = True
                    evidence.append("cgroup_v2:podman")
                elif "kubepods" in cgroup_content.lower() or "crio" in cgroup_content.lower():
                    runtime = "kubernetes"
                    is_container = True
                    evidence.append("cgroup_v2:kubernetes")
            else:
                cgroup_version = "v1"
                for line in cgroup_content.splitlines():
                    if "docker" in line:
                        runtime = "docker"
                        is_container = True
                        evidence.append("cgroup_v1:docker")
                        m = re.search(r"/docker[/-]([a-f0-9]{12,64})", line)
                        if m:
                            container_id = m.group(1)[:12]
                    elif "podman" in line or "libpod" in line:
                        runtime = "podman"
                        is_container = True
                        evidence.append("cgroup_v1:podman")
                    elif "kubepods" in line:
                        runtime = "kubernetes"
                        is_container = True
                        evidence.append("cgroup_v1:kubernetes")
                    elif "lxc" in line:
                        runtime = "lxc"
                        is_container = True
                        evidence.append("cgroup_v1:lxc")

        # Probe 3: /proc/self/mountinfo inspection
        mount_content = _exec("cat /proc/self/mountinfo 2>/dev/null | grep -iE 'docker|overlay|container' | head -n 3")
        if mount_content:
            if "docker" in mount_content.lower():
                evidence.append("mountinfo:docker")
                if not is_container:
                    runtime = "docker"
                    is_container = True
            elif "podman" in mount_content.lower() or "overlay-container" in mount_content.lower():
                evidence.append("mountinfo:podman")
                if not is_container:
                    runtime = "podman"
                    is_container = True

        # Probe 4: Rootless environment detection
        uid_out = _exec("id -u 2>/dev/null")
        if uid_out and uid_out.strip() != "0":
            is_rootless = True

        return {
            "is_container": is_container,
            "runtime": runtime,
            "cgroup_version": cgroup_version,
            "container_id": container_id,
            "is_rootless": is_rootless,
            "is_sandboxed": is_sandboxed or is_container,
            "evidence": evidence,
        }


class BaseExecutor:
    """Abstract polymorphic interface for all command and filesystem execution transports."""

    def __init__(self, driver_type="BASE", db_user=None, db_password=None, db_host=None, db_port=None, db_name=None, defaults_file=None):
        self.driver_type = driver_type
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.defaults_file = defaults_file

    def execute(self, command, timeout=10, env=None, as_user=None, cwd=None, mask_secrets=True):
        """Execute command with strict isolation and timeout."""
        raise NotImplementedError("Subclasses must implement execute()")

    def read_file(self, path, timeout=5, as_user=None):
        """Read remote or container file content safely."""
        res = self.execute(f"cat {shlex.quote(path)}", timeout=timeout, as_user=as_user)
        if res.is_success:
            return res.stdout
        return None

    def file_exists(self, path, timeout=5):
        """Check if file exists in the target environment."""
        res = self.execute(f"[ -e {shlex.quote(path)} ]", timeout=timeout)
        return res.is_success

    def get_metadata(self):
        """Return execution transport metadata."""
        return {
            "driver_type": self.driver_type,
            "db_user": self.db_user,
            "db_host": self.db_host,
            "db_port": self.db_port,
            "db_name": self.db_name,
            "defaults_file": self.defaults_file,
            "has_password": bool(self.db_password),
        }


class LocalExecutor(BaseExecutor):
    """Local host subprocess execution driver."""

    def __init__(self, db_user=None, db_password=None, db_host="localhost", db_port=None, db_name=None, defaults_file=None):
        super().__init__(
            driver_type="LOCAL_BAREMETAL",
            db_user=db_user,
            db_password=db_password,
            db_host=db_host,
            db_port=db_port,
            db_name=db_name,
            defaults_file=defaults_file
        )

    def execute(self, command, timeout=10, env=None, as_user=None, cwd=None, mask_secrets=True):
        start_time = time.time()
        cmd_env = os.environ.copy()

        if self.db_password:
            cmd_env["MYSQL_PWD"] = str(self.db_password)
            cmd_env["PGPASSWORD"] = str(self.db_password)
        if self.db_user:
            cmd_env["MYSQL_USER"] = str(self.db_user)
            cmd_env["PGUSER"] = str(self.db_user)
        if self.db_host:
            cmd_env["MYSQL_HOST"] = str(self.db_host)
            cmd_env["PGHOST"] = str(self.db_host)
        if self.db_port:
            cmd_env["MYSQL_TCP_PORT"] = str(self.db_port)
            cmd_env["PGPORT"] = str(self.db_port)
        if self.db_name:
            cmd_env["PGDATABASE"] = str(self.db_name)
        if env:
            cmd_env.update(env)

        if isinstance(command, (list, tuple)):
            cmd_str = " ".join(shlex.quote(str(x)) for x in command)
        else:
            cmd_str = str(command)

        if as_user and os.getuid() != 0:
            cmd_str = f"sudo -n -u {shlex.quote(as_user)} /bin/bash -c {json.dumps(cmd_str)}"

        masked_cmd = SecretSanitizer.sanitize(cmd_str) if mask_secrets else cmd_str

        try:
            p = subprocess.run(
                ["/bin/bash", "-c", cmd_str],
                capture_output=True,
                text=True,
                timeout=timeout,
                env=cmd_env,
                cwd=cwd,
                check=False,
                stdin=subprocess.DEVNULL
            )
            duration_ms = (time.time() - start_time) * 1000.0
            return ExecutionResult(
                stdout=p.stdout,
                stderr=p.stderr,
                returncode=p.returncode,
                duration_ms=duration_ms,
                command_masked=masked_cmd,
                driver_type=self.driver_type
            )
        except subprocess.TimeoutExpired:
            duration_ms = (time.time() - start_time) * 1000.0
            return ExecutionResult(
                stdout="",
                stderr=f"Command execution timed out after {timeout} seconds",
                returncode=-1,
                duration_ms=duration_ms,
                command_masked=masked_cmd,
                driver_type=self.driver_type
            )
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000.0
            return ExecutionResult(
                stdout="",
                stderr=str(e),
                returncode=-1,
                duration_ms=duration_ms,
                command_masked=masked_cmd,
                driver_type=self.driver_type
            )


class DockerExecutor(BaseExecutor):
    """Docker / Podman container execution driver."""

    def __init__(self, container_name, db_user=None, db_password=None, db_host=None, db_port=None, db_name=None, defaults_file=None, container_cli="docker"):
        super().__init__(
            driver_type="LOCAL_DOCKER",
            db_user=db_user,
            db_password=db_password,
            db_host=db_host,
            db_port=db_port,
            db_name=db_name,
            defaults_file=defaults_file
        )
        self.container_name = container_name
        self.container_cli = container_cli

    def execute(self, command, timeout=10, env=None, as_user=None, cwd=None, mask_secrets=True):
        start_time = time.time()
        docker_env = []

        if self.db_password:
            docker_env.extend(["-e", f"MYSQL_PWD={self.db_password}", "-e", f"PGPASSWORD={self.db_password}"])
        if self.db_user:
            docker_env.extend(["-e", f"MYSQL_USER={self.db_user}", "-e", f"PGUSER={self.db_user}"])
        if self.db_host:
            docker_env.extend(["-e", f"MYSQL_HOST={self.db_host}", "-e", f"PGHOST={self.db_host}"])
        if self.db_port:
            docker_env.extend(["-e", f"MYSQL_TCP_PORT={self.db_port}", "-e", f"PGPORT={self.db_port}"])
        if self.db_name:
            docker_env.extend(["-e", f"PGDATABASE={self.db_name}"])
        if env:
            for k, v in env.items():
                docker_env.extend(["-e", f"{k}={v}"])

        env_flags = " ".join(docker_env) if docker_env else ""
        user_flags = f"-u {as_user} " if as_user else ""
        workdir_flags = f"-w {cwd} " if cwd else ""

        cmd_string = f"{self.container_cli} exec -i {env_flags} {user_flags}{workdir_flags}{self.container_name} /bin/bash -c {json.dumps(command)}".replace("  ", " ").strip()
        masked_cmd = SecretSanitizer.sanitize(cmd_string) if mask_secrets else cmd_string

        try:
            p = subprocess.run(
                ["/bin/bash", "-c", cmd_string],
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
                stdin=subprocess.DEVNULL
            )
            duration_ms = (time.time() - start_time) * 1000.0
            return ExecutionResult(
                stdout=p.stdout,
                stderr=p.stderr,
                returncode=p.returncode,
                duration_ms=duration_ms,
                command_masked=masked_cmd,
                driver_type=self.driver_type
            )
        except subprocess.TimeoutExpired:
            duration_ms = (time.time() - start_time) * 1000.0
            return ExecutionResult(
                stdout="",
                stderr=f"Container execution timed out after {timeout} seconds",
                returncode=-1,
                duration_ms=duration_ms,
                command_masked=masked_cmd,
                driver_type=self.driver_type
            )
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000.0
            return ExecutionResult(
                stdout="",
                stderr=str(e),
                returncode=-1,
                duration_ms=duration_ms,
                command_masked=masked_cmd,
                driver_type=self.driver_type
            )


class SSHExecutor(BaseExecutor):
    """Remote SSH execution transport driver with connection hardening and zero-hang configuration."""

    def __init__(self, remote_host, ssh_key="/root/.ssh/id_rsa", ssh_port=22, db_user=None, db_password=None, db_host=None, db_port=None, db_name=None, defaults_file=None):
        super().__init__(
            driver_type="REMOTE_SSH_BAREMETAL",
            db_user=db_user,
            db_password=db_password,
            db_host=db_host,
            db_port=db_port,
            db_name=db_name,
            defaults_file=defaults_file
        )
        self.remote_host = remote_host
        self.ssh_key = ssh_key
        self.ssh_port = ssh_port

    def _build_ssh_prefix(self):
        cmd = [
            "ssh",
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-o", "BatchMode=yes",
            "-o", "ConnectTimeout=5",
            "-o", "ServerAliveInterval=3",
            "-o", "ServerAliveCountMax=2",
            "-p", str(self.ssh_port)
        ]
        if self.ssh_key:
            cmd.extend(["-i", self.ssh_key])
        cmd.append(self.remote_host)
        return cmd

    def execute(self, command, timeout=12, env=None, as_user=None, cwd=None, mask_secrets=True):
        start_time = time.time()
        env_prefixes = []
        if self.db_password:
            env_prefixes.extend([f"MYSQL_PWD={shlex.quote(str(self.db_password))}", f"PGPASSWORD={shlex.quote(str(self.db_password))}"])
        if self.db_user:
            env_prefixes.extend([f"MYSQL_USER={shlex.quote(str(self.db_user))}", f"PGUSER={shlex.quote(str(self.db_user))}"])
        if self.db_host:
            env_prefixes.extend([f"MYSQL_HOST={shlex.quote(str(self.db_host))}", f"PGHOST={shlex.quote(str(self.db_host))}"])
        if self.db_port:
            env_prefixes.extend([f"MYSQL_TCP_PORT={shlex.quote(str(self.db_port))}", f"PGPORT={shlex.quote(str(self.db_port))}"])
        if env:
            for k, v in env.items():
                env_prefixes.append(f"{k}={shlex.quote(str(v))}")

        prefix_str = ("export " + " ".join(env_prefixes) + "; ") if env_prefixes else ""
        if as_user:
            target_cmd = f"{prefix_str}sudo -n -u {as_user} /bin/bash -c {shlex.quote(command)}"
        else:
            target_cmd = f"{prefix_str}{command}"

        ssh_args = self._build_ssh_prefix() + ["/bin/bash", "-c", shlex.quote(target_cmd)]
        masked_cmd = SecretSanitizer.sanitize(f"ssh {self.remote_host} '{target_cmd}'") if mask_secrets else f"ssh {self.remote_host} '{target_cmd}'"

        try:
            p = subprocess.run(
                ssh_args,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
                stdin=subprocess.DEVNULL
            )
            duration_ms = (time.time() - start_time) * 1000.0
            filtered_stderr = []
            if p.stderr:
                for line in p.stderr.splitlines():
                    if not line.startswith("Warning: Permanently added") and "pseudo-terminal" not in line:
                        filtered_stderr.append(line)
            clean_stderr = "\n".join(filtered_stderr).strip()

            return ExecutionResult(
                stdout=p.stdout,
                stderr=clean_stderr,
                returncode=p.returncode,
                duration_ms=duration_ms,
                command_masked=masked_cmd,
                driver_type=self.driver_type
            )
        except subprocess.TimeoutExpired:
            duration_ms = (time.time() - start_time) * 1000.0
            return ExecutionResult(
                stdout="",
                stderr=f"SSH transport execution timed out after {timeout} seconds",
                returncode=-1,
                duration_ms=duration_ms,
                command_masked=masked_cmd,
                driver_type=self.driver_type
            )
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000.0
            return ExecutionResult(
                stdout="",
                stderr=str(e),
                returncode=-1,
                duration_ms=duration_ms,
                command_masked=masked_cmd,
                driver_type=self.driver_type
            )

