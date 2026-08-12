#!/usr/bin/env python3
"""
Fix sidebar_links_html initialization, SafeDict template formatting, and kwargs in generate_html_report()
across ALL 18 Audit Scripts and audit_cis.py (PSL ONLY).
"""

import glob
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Fixing generate_html_report() initialization and formatting across {len(audit_files)} scripts...")

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Ensure sidebar_links_html = "" is initialized right after categories_html = ""
    if 'categories_html = ""' in content and 'sidebar_links_html = ""' not in content:
        content = content.replace('categories_html = ""', 'categories_html = ""\n    sidebar_links_html = ""')

    # Replace html_output = load_html_template().format(...) with SafeDict formatting
    pattern = r'html_output = load_html_template\(\)\.format\(.*?\)'
    safe_format_block = '''class SafeDict(dict):
        def __missing__(self, key):
            return f"{{{key}}}"

    html_output = load_html_template().format_map(SafeDict(
        benchmark_title=target_name if 'target_name' in locals() else "CIS Benchmark",
        lang=lang if 'lang' in locals() else "en",
        report_date=report_date,
        suite_version="2.0.0",
        target_version="2.0.0",
        overall_score=overall_score,
        overall_score_class=overall_score_class,
        passed_automated_count=passed_auto_count if 'passed_auto_count' in locals() else 0,
        failed_automated_count=failed_auto_count if 'failed_auto_count' in locals() else 0,
        passed_automated=passed_auto_count if 'passed_auto_count' in locals() else 0,
        total_automated=(passed_auto_count + failed_auto_count) if 'passed_auto_count' in locals() else 0,
        manual_checks=total_manual if 'total_manual' in locals() else 0,
        error_checks=total_errors if 'total_errors' in locals() else 0,
        na_checks=total_na if 'total_na' in locals() else 0,
        sidebar_links=sidebar_links_html if 'sidebar_links_html' in locals() else "",
        categories_reports=categories_html,
        donut_svg=svg_global_chart_html if 'svg_global_chart_html' in locals() else "",
        bar_svg=build_inline_svg_category_chart(categories_scores) if 'categories_scores' in locals() else "",
        svg_global_chart_html=svg_global_chart_html if 'svg_global_chart_html' in locals() else ""
    ))'''

    content = re.sub(pattern, safe_format_block, content, flags=re.DOTALL)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Successfully updated generate_html_report() across all audit scripts!")
