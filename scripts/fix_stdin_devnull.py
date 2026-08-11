#!/usr/bin/env python3
import glob

rhel_files = glob.glob("audit_cis_rhel_*.py") + ["audit_cis.py"]

for fpath in rhel_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    if "stdin=subprocess.DEVNULL" not in content:
        content = content.replace(
            "capture_output=True, text=True, timeout=30)",
            "stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10)"
        ).replace(
            "capture_output=True, text=True, timeout=15)",
            "stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10)"
        )

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Added stdin=subprocess.DEVNULL to prevent hanging on interactive password prompts!")
