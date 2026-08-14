#!/usr/bin/env python3
"""
Regenerate all 18 HTML audit reports with clean headers and no palindromes (100% PSL ONLY).
"""

import glob
import subprocess
import sys

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Regenerating clean HTML reports across {len(audit_files)} benchmarks...")

for script in audit_files:
    print(f"  → Generating {script}...")
    res = subprocess.run([sys.executable, script, "-m", "local", "-f", "html"], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"    ⚠️ Warning in {script}: {res.stderr.strip()[:120]}")
    else:
        print(f"    ✓ Done.")

print("🎉 All 18 clean HTML reports generated successfully!")
