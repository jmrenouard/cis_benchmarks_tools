#!/usr/bin/env python3
"""
In-Container POSIX, Filesystem & Process Inspection Abstraction (PSL ONLY).
Ensures 100% of CIS benchmark probes run strictly inside the target container namespace,
preventing any unintended host command escapes or false positives.
"""

import json
import os
import re
import shlex
import sys
from typing import Dict, List, Optional, Tuple, Any

from execution_drivers import BaseExecutor, DockerExecutor, ExecutionResult


class PosixStatResult:
    """Encapsulates POSIX file/directory metadata inside target container."""

    def __init__(
        self,
        path: str,
        exists: bool,
        mode_octal: str = "0000",
        uid: int = -1,
        gid: int = -1,
        user: str = "unknown",
        group: str = "unknown",
        is_directory: bool = False,
        is_file: bool = False,
        error: Optional[str] = None
    ):
        self.path = path
        self.exists = exists
        self.mode_octal = mode_octal
        self.uid = int(uid)
        self.gid = int(gid)
        self.user = user
        self.group = group
        self.is_directory = is_directory
        self.is_file = is_file
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "exists": self.exists,
            "mode_octal": self.mode_octal,
            "uid": self.uid,
            "gid": self.gid,
            "user": self.user,
            "group": self.group,
            "is_directory": self.is_directory,
            "is_file": self.is_file,
            "error": self.error
        }


class InContainerInspector:
    """High-level in-container inspection engine for CIS benchmark audits (PSL ONLY)."""

    def __init__(self, executor: BaseExecutor):
        self.executor = executor

    def read_file(self, path: str, max_bytes: int = 200000) -> Optional[str]:
        """Safely read in-container file content without mounting volumes."""
        cmd = f"head -c {max_bytes} {shlex.quote(path)} 2>/dev/null"
        res = self.executor.execute(cmd, timeout=5)
        if res.is_success and res.stdout:
            return res.stdout
        return None

    def file_exists(self, path: str) -> bool:
        """Check if path exists inside the container."""
        res = self.executor.execute(f"[ -e {shlex.quote(path)} ]", timeout=3)
        return res.is_success

    def stat_path(self, path: str) -> PosixStatResult:
        """Inspect in-container POSIX permissions (octal, uid, gid, user, group)."""
        cmd = f"stat -c '%a %u %g %U %G %F' {shlex.quote(path)} 2>/dev/null"
        res = self.executor.execute(cmd, timeout=5)

        if not res.is_success or not res.stdout.strip():
            return PosixStatResult(path=path, exists=False, error=res.stderr or "Path not found")

        parts = res.stdout.strip().split()
        if len(parts) >= 6:
            mode_oct = parts[0].zfill(4)
            uid = int(parts[1]) if parts[1].isdigit() else -1
            gid = int(parts[2]) if parts[2].isdigit() else -1
            user = parts[3]
            group = parts[4]
            ftype = " ".join(parts[5:]).lower()
            return PosixStatResult(
                path=path,
                exists=True,
                mode_octal=mode_oct,
                uid=uid,
                gid=gid,
                user=user,
                group=group,
                is_directory="directory" in ftype,
                is_file="regular" in ftype or "file" in ftype
            )

        return PosixStatResult(path=path, exists=True, mode_octal="0000")

    def is_port_listening(self, port: int) -> bool:
        """Check if a network port is listening inside the container's network namespace."""
        hex_port = f"{port:04X}"
        cmd = f"grep -i ':{hex_port} ' /proc/net/tcp /proc/net/tcp6 2>/dev/null || ss -tln | grep -q ':{port} '"
        res = self.executor.execute(cmd, timeout=5)
        return res.is_success

    def is_process_running(self, proc_pattern: str) -> bool:
        """Check if a target process name/pattern is running in container's PID namespace."""
        cmd = f"pgrep -f {shlex.quote(proc_pattern)} >/dev/null 2>&1 || ps -ef | grep -v grep | grep -q {shlex.quote(proc_pattern)}"
        res = self.executor.execute(cmd, timeout=5)
        return res.is_success

    def is_rootfs_readonly(self) -> bool:
        """Check if root filesystem is mounted read-only inside container."""
        cmd = "test -w / && echo RW || echo RO"
        res = self.executor.execute(cmd, timeout=3)
        return res.stdout.strip() == "RO"

    def execute_db_query(
        self,
        query: str,
        db_type: str = "mysql",
        user: Optional[str] = None,
        database: Optional[str] = None,
        timeout: int = 10
    ) -> ExecutionResult:
        """Execute a database query directly inside container CLI."""
        db_t = db_type.lower()
        if "maria" in db_t or "mysql" in db_t:
            u_flag = f"-u {shlex.quote(user)}" if user else ""
            d_flag = f"{shlex.quote(database)}" if database else ""
            cli_cmd = f"mariadb {u_flag} {d_flag} -e {json.dumps(query)} 2>/dev/null || mysql {u_flag} {d_flag} -e {json.dumps(query)}"
        elif "postgres" in db_t or "psql" in db_t:
            u_flag = f"-U {shlex.quote(user or 'postgres')}"
            d_flag = f"-d {shlex.quote(database or 'postgres')}"
            cli_cmd = f"psql {u_flag} {d_flag} -c {json.dumps(query)}"
        elif "mongo" in db_t:
            cli_cmd = f"mongosh --quiet --eval {json.dumps(query)} 2>/dev/null || mongo --quiet --eval {json.dumps(query)}"
        elif "cassandra" in db_t:
            cli_cmd = f"cqlsh -e {json.dumps(query)}"
        else:
            cli_cmd = query

        return self.executor.execute(cli_cmd, timeout=timeout)
