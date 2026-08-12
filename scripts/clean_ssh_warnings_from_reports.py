#!/usr/bin/env python3
"""
Clean SSH host key warning noise ('Warning: Permanently added...') across all generated reports.
100% Python Standard Library (PSL ONLY).
"""

import glob
import os
import re

report_files = sorted(glob.glob("reports/*"))
cleaned_count = 0

for fpath in report_files:
    if not os.path.isfile(fpath):
        continue
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    if "Warning: Permanently added" in content:
        cleaned_count += 1
        new_content = re.sub(r"\n?Warning: Permanently added [^\n\r]+", "", content)
        new_content = re.sub(r"\n?Warning: Permanently added &#x27;[^\n\r]+", "", new_content)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)

print(f"✅ Cleaned SSH warning noise from {cleaned_count} report files in reports/")
