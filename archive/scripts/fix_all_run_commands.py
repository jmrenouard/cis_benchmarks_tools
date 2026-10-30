#!/usr/bin/env python3
"""
Add stdin=subprocess.DEVNULL and timeout=5 to run_command across all audit scripts
to prevent blocking on password prompts or hanging network connections.
100% Python Standard Library (PSL ONLY).
"""

import glob
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Updating run_command timeout & stdin=DEVNULL across {len(audit_files)} scripts...")

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Match process = subprocess.run(...) and ensure timeout=5 and stdin=subprocess.DEVNULL
    new_run_func = '''def run_command(command, remote_host=None):
    """Execute command safely with timeout=5 and stdin=DEVNULL."""
    try:
        if isinstance(command, str):
            cmd_args = ["/bin/bash", "-c", command]
        else:
            cmd_args = command

        if remote_host:
            cmd_args = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", remote_host] + cmd_args

        process = subprocess.run(cmd_args, check=False, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=5)
        return process.stdout.strip(), process.stderr.strip(), process.returncode
    except subprocess.TimeoutExpired:
        return "", "Command execution timed out after 5 seconds", -1
    except Exception as e:
        return "", str(e), -1
'''

    content = re.sub(r'def run_command\(.*?\):\n.*?(?=\n\ndef evaluate_condition|\nRECOMMENDATIONS_DATA|\ndef perform_checks)', new_run_func + "\n", content, flags=re.DOTALL)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Added timeout=5 and stdin=DEVNULL to all run_command functions!")
