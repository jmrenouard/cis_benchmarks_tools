#!/usr/bin/env python3
"""
Generate All Reports (HTML, JSON, XML, TXT) for All 18 Audit Targets.
100% Python Standard Library (PSL ONLY).
"""

import glob
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

os.chdir(REPO_ROOT)
os.makedirs("reports", exist_ok=True)

audit_scripts = sorted(glob.glob("audit_cis_*.py"))
formats = ["html", "json", "xml", "txt"]

print(f"🚀 Generating reports in all 4 formats (html, json, xml, txt) across {len(audit_scripts)} audit targets...")

total_generated = 0
for script in audit_scripts:
    target_key = script.replace("audit_cis_", "").replace(".py", "")
    for fmt in formats:
        out_file = os.path.join("reports", f"rapport_cis_{target_key}.{fmt}")
        cmd = [sys.executable, script, "-f", fmt, "-o", out_file]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if os.path.exists(out_file) and os.path.getsize(out_file) > 50:
            total_generated += 1
            print(f"  ✓ {out_file} ({os.path.getsize(out_file)} bytes)")
        else:
            print(f"  ❌ Failed to generate {out_file}: {res.stderr.strip()}", file=sys.stderr)

print(f"\n🎉 Successfully generated {total_generated} reports in reports/!")
