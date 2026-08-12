#!/usr/bin/env python3
"""
Fix category_manual_counts list comprehension to use dict.get() safely across all audit scripts.
"""

import glob
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Fixing category_manual_counts safely across {len(audit_files)} scripts...")

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'category_manual_counts = json\.dumps\(\[categories_scores\[cat\]\["manual_checks"\] for cat in category_order\]\)'
    replacement = 'category_manual_counts = json.dumps([categories_scores.get(cat, {}).get("manual_checks", 0) for cat in category_order])'

    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)

print("✅ Successfully updated category_manual_counts across all audit scripts!")
