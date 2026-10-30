#!/usr/bin/env python3
"""
Populate Category Stacked Bar Chart counts directly from categories_scores
in generate_html_report across ALL 18 Audit Scripts (PSL ONLY).
"""

import glob
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Fixing Category Chart Data across {len(audit_files)} audit scripts...")

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # In generate_html_report, automatically extract category counts if categories_scores is present
    extract_logic = r'''    if categories_scores and isinstance(categories_scores, dict):
        category_labels = list(categories_scores.keys())
        category_pass_counts = [categories_scores[c].get("passed_automated", categories_scores[c].get("passed", 0)) for c in category_labels]
        category_fail_counts = [categories_scores[c].get("failed_automated", categories_scores[c].get("failed", 0)) for c in category_labels]
        category_error_counts = [categories_scores[c].get("error_checks", categories_scores[c].get("errors", 0)) for c in category_labels]
        category_na_counts = [categories_scores[c].get("na_checks", categories_scores[c].get("na", 0)) for c in category_labels]
    else:
        category_labels, category_pass_counts, category_fail_counts, category_error_counts, category_na_counts = [], [], [], [], []

    svg_category_chart_html = build_inline_svg_category_chart(category_labels, category_pass_counts, category_fail_counts, category_error_counts, category_na_counts)
'''

    # Replace category extraction line in generate_html_report
    content = re.sub(
        r'svg_category_chart_html = build_inline_svg_category_chart\(.*?\)\n',
        extract_logic,
        content
    )

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Successfully fixed Category Stacked Bar Chart data extraction across all 18 audit scripts!")
