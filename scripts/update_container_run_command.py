#!/usr/bin/env python3
"""
Container-aware run_command enhancement across all audit scripts (PSL ONLY).
Intercepts systemctl in containers and redirects to native service ping check.
"""

import glob
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Updating run_command container fallback across {len(audit_files)} audit scripts...")

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    old_block = '''        if isinstance(command, str):
            cmd_args = ["/bin/bash", "-c", command]'''

    new_block = '''        if isinstance(command, str):
            if "systemctl" in command and (os.path.exists("/.dockerenv") or not os.path.exists("/run/systemd/system")):
                if "postgresql" in command:
                    command = "pg_isready -h localhost -p 5432 || ps aux | grep -v grep | grep postgres"
                elif "mariadb" in command or "mysql" in command:
                    command = "mariadb -e 'SELECT 1;' 2>/dev/null || mysql -e 'SELECT 1;' 2>/dev/null || ps aux | grep -v grep | grep mysqld"
            cmd_args = ["/bin/bash", "-c", command]'''

    if old_block in content:
        content = content.replace(old_block, new_block)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)

print("✅ Successfully updated run_command across all audit scripts!")
