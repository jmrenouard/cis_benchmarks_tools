#!/usr/bin/env python3
"""
Remove 2>/dev/null across all 18 rules/*.json files so that stderr is captured
cleanly for post-audit diagnostic inspection without silencing error details (100% PSL ONLY).
"""

import glob
import json
import os
import re

print("Removing 2>/dev/null across all rules/*.json files to preserve full diagnostic telemetry...")

for fpath in sorted(glob.glob("rules/*.json")):
    with open(fpath, "r", encoding="utf-8") as f:
        rules = json.load(f)

    modified = False
    for r in rules:
        for field in ["test_procedure", "pre_condition", "path_command"]:
            if field in r and isinstance(r[field], str) and "2>/dev/null" in r[field]:
                # Clean out 2>/dev/null
                cleaned = r[field].replace(" 2>/dev/null", "").replace("2>/dev/null", "").strip()
                # Clean up any leftover empty constructs or trailing pipes/logical operators
                cleaned = re.sub(r"\s+\|\|\s+echo\s+'MANUAL_[^']+'", "", cleaned)
                cleaned = re.sub(r"\s+\|\|\s+echo\s+'PASS_[^']+'", "", cleaned)
                cleaned = re.sub(r"\s+\|\|\s+echo\s+'VERIF_[^']+'", "", cleaned)
                r[field] = cleaned
                modified = True

    if modified:
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(rules, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Preserved full diagnostic stderr in {fpath}")

print("✅ Successfully removed 2>/dev/null across all benchmark rules!")
