#!/usr/bin/env python3
"""
Clean SSH host key warning noise ('Warning: Permanently added...') across all generated reports.
100% Python Standard Library (PSL ONLY).
"""

import glob, os, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SSH_WARN_PAT = r"(?:\\n|\n)?Warning: Permanently added [^<\r\n\"]+ to the list of known hosts\.?(?:\\n|\n)?"
SSH_WARN_HTML_PAT = r"(?:\\n|\n)?Warning: Permanently added &#x27;[^<\r\n\"]+&#x27; to the list of known hosts\.?(?:\\n|\n)?"

report_files = sorted(glob.glob("reports/*"))
cleaned_count = 0

for fpath in report_files:
    if not os.path.isfile(fpath):
        continue
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    if "Warning: Permanently added" in content:
        cleaned_count += 1
        new_content = re.sub(SSH_WARN_PAT, "", content)
        new_content = re.sub(SSH_WARN_HTML_PAT, "", new_content)
        with open(fpath, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_content)

print(f"✅ Cleaned SSH warning noise from {cleaned_count} report files in reports/")
