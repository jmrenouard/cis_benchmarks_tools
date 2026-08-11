#!/usr/bin/env python3
"""
Clean HTML_TEMPLATE.format(...) in all database audit scripts to remove legacy Chart.js kwargs.
100% Python Standard Library (PSL ONLY).
"""

import glob
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Cleaning HTML_TEMPLATE.format kwargs across {len(audit_files)} audit scripts...")

clean_format_block = '''    html_output = HTML_TEMPLATE.format(
        report_date=report_date,
        overall_score=overall_score,
        overall_score_class=overall_score_class,
        passed_automated=passed_auto_count,
        total_automated=passed_auto_count + failed_auto_count,
        manual_checks=total_manual,
        error_checks=total_errors,
        na_checks=total_na,
        categories_reports=categories_html,
        svg_global_chart_html=svg_global_chart_html
    )'''

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    if "HTML_TEMPLATE.format(" in content:
        content = re.sub(
            r'html_output = HTML_TEMPLATE\.format\(.*?\n    \)',
            clean_format_block,
            content,
            flags=re.DOTALL
        )

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Successfully cleaned HTML_TEMPLATE.format kwargs across all audit scripts!")
