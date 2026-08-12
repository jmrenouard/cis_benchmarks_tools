#!/usr/bin/env python3
"""
Add StrictHostKeyChecking=no and UserKnownHostsFile=/dev/null to run_command SSH execution (PSL ONLY).
"""

import glob

audit_files = sorted(glob.glob("audit_cis_*.py") + ["audit_cis.py"])
print(f"Updating SSH options across {len(audit_files)} audit scripts...")

old_ssh = '["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", remote_host]'
new_ssh = '["ssh", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", remote_host]'

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    if old_ssh in content:
        content = content.replace(old_ssh, new_ssh)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)

print("✅ Successfully updated SSH options across all audit scripts!")
