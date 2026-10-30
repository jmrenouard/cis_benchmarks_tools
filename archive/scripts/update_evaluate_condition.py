#!/usr/bin/env python3
import glob

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Updating evaluate_condition for stdout_is_empty in {len(audit_files)} scripts...")

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    if 'elif condition_type == "stdout_is_empty":' not in content:
        content = content.replace(
            'elif condition_type == "stdout_not_empty":',
            'elif condition_type == "stdout_is_empty":\n        return stdout.strip() == ""\n    elif condition_type == "stdout_not_empty":'
        )

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Added stdout_is_empty handler across all audit scripts!")
