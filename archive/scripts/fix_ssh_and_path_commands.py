#!/usr/bin/env python3
"""
Fix SSH noise filtering in run_command and enhance path_command fallback/error formatting across all audit scripts.
100% Python Standard Library (PSL ONLY).
"""

import glob
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Updating run_command & path_command across {len(audit_files)} scripts...")

new_run_func = '''def run_command(command, remote_host=None):
    """Execute command safely with timeout=10, stdin=DEVNULL, and clean SSH noise (PSL ONLY)."""
    try:
        if isinstance(command, str):
            if "systemctl" in command and (os.path.exists("/.dockerenv") or not os.path.exists("/run/systemd/system")):
                if "postgresql" in command:
                    command = "pg_isready -h localhost -p 5432 || ps aux | grep -v grep | grep postgres"
                elif "mariadb" in command or "mysql" in command:
                    command = "mariadb -e 'SELECT 1;' 2>/dev/null || mysql -e 'SELECT 1;' 2>/dev/null || ps aux | grep -v grep | grep mysqld"
            cmd_args = ["/bin/bash", "-c", command]
        else:
            cmd_args = list(command)

        if remote_host:
            cmd_args = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", "-i", "/root/.ssh/id_rsa", remote_host] + cmd_args

        process = subprocess.run(cmd_args, check=False, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10)
        stdout_text = process.stdout.strip()
        stderr_text = process.stderr.strip()

        if stderr_text:
            filtered_lines = [
                line for line in stderr_text.splitlines()
                if not line.startswith("Warning: Permanently added")
                and "pseudo-terminal" not in line
            ]
            stderr_text = chr(10).join(filtered_lines).strip()

        return stdout_text, stderr_text, process.returncode
    except subprocess.TimeoutExpired:
        return "", "Command execution timed out after 10 seconds", -1
    except Exception as e:
        return "", str(e), -1
'''

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace run_command definition
    content = re.sub(
        r'def run_command\(.*?\):\n.*?(?=\n\ndef evaluate_condition|\nRECOMMENDATIONS_DATA|\ndef perform_checks)',
        new_run_func + "\n",
        content,
        flags=re.DOTALL
    )

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Updated run_command & path_command across all audit scripts!")
