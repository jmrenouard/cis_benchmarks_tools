#!/usr/bin/env python3
"""
Integrate unified detect_execution_context() and execution context reporting across all 18 audit scripts (100% PSL ONLY).
"""

import glob
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Integrating execution context engine across {len(audit_files)} audit scripts...")

context_helper_code = '''def detect_execution_context(mode="local", remote_host=None, docker_container=None, product_hint=None):
    """Detect and categorize execution context into structured dictionary (PSL ONLY)."""
    is_remote = bool(mode == "ssh" or remote_host)
    active_container = docker_container

    if not active_container and product_hint:
        try:
            cmd = "docker ps --format '{{.Names}}' 2>/dev/null"
            stdout, stderr, ret = run_command(cmd, remote_host=remote_host)
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
'''

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace or add detect_execution_context before detect_docker_container
    if "def detect_execution_context(" not in content:
        content = content.replace("def detect_docker_container(", context_helper_code + "\n\ndef detect_docker_container(")

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Integrated execution context engine across all audit scripts!")
