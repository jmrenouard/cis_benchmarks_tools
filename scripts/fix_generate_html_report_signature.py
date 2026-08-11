#!/usr/bin/env python3
"""
Unify `generate_html_report(results, overall_score, categories_scores, filename=None, lang="en")`
across ALL 18 Audit Scripts with 100% Pure Inline SVG Donut and Category Bar Charts (PSL ONLY).
"""

import glob
import os
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Unifying generate_html_report across {len(audit_files)} audit scripts...")

for fpath in audit_files:
    target_key = os.path.basename(fpath).replace("audit_cis_", "").replace(".py", "")
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Normalize generate_html_report signature
    content = re.sub(
        r'def generate_html_report\(results, overall_score, categories_scores.*?\):\n',
        f'def generate_html_report(results, overall_score, categories_scores, filename=None, lang="en"):\n',
        content
    )

    # Insert flat_results calculation at start of generate_html_report
    flat_calc = f'''    if not filename:
        filename = "reports/rapport_cis_{target_key}.html"

    flat_results = []
    if isinstance(results, dict):
        for cat, checks in results.items():
            for c in checks:
                flat_results.append(c)
    else:
        flat_results = results

    passed_auto_count = sum(1 for c in flat_results if c.get("status") in ["PASS", "Pass"])
    failed_auto_count = sum(1 for c in flat_results if c.get("status") in ["FAIL", "Fail"])
    error_auto_count = sum(1 for c in flat_results if c.get("status") in ["ERROR", "Error"])
    na_auto_count = sum(1 for c in flat_results if c.get("status") in ["N/A", "NA"])
    total_manual = sum(1 for c in flat_results if c.get("status") in ["MANUAL", "Manual"])
    total_errors = error_auto_count
    total_na = na_auto_count
    passed_automated = passed_auto_count
    total_automated = passed_auto_count + failed_auto_count
    svg_global_chart_html = build_inline_svg_donut_chart(passed_auto_count, failed_auto_count, error_auto_count, na_auto_count, overall_score)
'''

    content = re.sub(
        r'def generate_html_report\(results, overall_score, categories_scores, filename=None, lang="en"\):\n.*?(?=report_date =)',
        f'def generate_html_report(results, overall_score, categories_scores, filename=None, lang="en"):\n{flat_calc}\n    ',
        content,
        flags=re.DOTALL
    )

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Successfully unified generate_html_report variables across all 18 audit scripts!")
