#!/usr/bin/env python3
"""
Extract RECOMMENDATIONS_DATA from all 18 Python audit scripts into external JSON rule files
under the `rules/` directory.
100% Python Standard Library (PSL ONLY).
"""

import glob
import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_DIR = os.path.join(REPO_ROOT, "rules")
os.makedirs(RULES_DIR, exist_ok=True)

audit_files = sorted(glob.glob(os.path.join(REPO_ROOT, "audit_cis_*.py")))
print(f"Extracting audit rules into `{RULES_DIR}` across {len(audit_files)} audit scripts...")

for fpath in audit_files:
    target_key = os.path.basename(fpath).replace("audit_cis_", "").replace(".py", "")
    json_path = os.path.join(RULES_DIR, f"{target_key}.json")

    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Slice content from beginning to the first helper function
    cut_idx = content.find("\ndef run_command")
    if cut_idx == -1:
        cut_idx = content.find("\ndef evaluate_condition")
    if cut_idx == -1:
        cut_idx = content.find("\ndef perform_checks")

    script_head = content[:cut_idx] if cut_idx != -1 else content
    namespace = {}
    try:
        exec(script_head, namespace)
        if "RECOMMENDATIONS_DATA" in namespace:
            rules_data = namespace["RECOMMENDATIONS_DATA"]
            with open(json_path, "w", encoding="utf-8") as jf:
                json.dump(rules_data, jf, indent=2, ensure_ascii=False)
            print(f"  ✓ Extracted {len(rules_data)} controls for {target_key} -> rules/{target_key}.json")
        else:
            print(f"  ⚠️ RECOMMENDATIONS_DATA not found in {target_key}")
    except Exception as e:
        print(f"  ❌ Error extracting rules for {target_key}: {e}")

print("✅ Externalized all audit rules into `rules/` directory!")
