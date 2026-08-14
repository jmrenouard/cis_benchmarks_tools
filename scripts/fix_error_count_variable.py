#!/usr/bin/env python3
"""
Ensure error_count is defined in SafeDict across all 18 audit scripts (100% PSL ONLY).
"""

import glob
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Fixing error_count in SafeDict across {len(audit_files)} audit scripts...")

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Add error_count to SafeDict
    if "error_count=" not in content:
        content = content.replace(
            "error_checks=total_errors if 'total_errors' in locals() else 0,",
            "error_checks=total_errors if 'total_errors' in locals() else 0,\n        error_count=total_errors if 'total_errors' in locals() else 0,"
        )

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Successfully fixed error_count in SafeDict across all audit scripts!")
