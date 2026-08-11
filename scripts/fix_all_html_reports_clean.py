#!/usr/bin/env python3
"""
Unify and standardize `generate_html_report(results, overall_score, categories_scores, filename=None, lang="en")`
across ALL 18 Audit Scripts with 100% Pure Inline SVG Charts (PSL ONLY).
"""

import glob
import os
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Standardizing generate_html_report across {len(audit_files)} audit scripts...")

for fpath in audit_files:
    target_key = os.path.basename(fpath).replace("audit_cis_", "").replace(".py", "")
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Clean export_results call
    content = re.sub(
        r'try:\s*generate_html_report\(results, overall_score, categories_scores, filename=filename, lang=lang\).*?generate_html_report\(results, overall_score, categories_scores, 0, 0, 0, 0, 0, 0, 0, \[\], \[\], \[\], \[\], \[\], filename\)',
        r'generate_html_report(results, overall_score, categories_scores, filename=filename, lang=lang)',
        content,
        flags=re.DOTALL
    )

    # 2. Fix generate_html_report definition signature
    content = re.sub(
        r'def generate_html_report\(results, overall_score, categories_scores.*?\):\n',
        r'def generate_html_report(results, overall_score, categories_scores, filename=None, lang="en"):\n',
        content
    )

    # 3. Replace start of generate_html_report body
    clean_body_head = f'''    if not filename:
        filename = "reports/rapport_cis_{target_key}.html"

    report_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    overall_score_class = get_score_class(overall_score)
    categories_html = ""

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

    svg_global_chart_html = build_inline_svg_donut_chart(passed_auto_count, failed_auto_count, error_auto_count, na_auto_count, overall_score)
'''

    content = re.sub(
        r'def generate_html_report\(results, overall_score, categories_scores, filename=None, lang="en"\):\n.*?(?=category_order =)',
        f'def generate_html_report(results, overall_score, categories_scores, filename=None, lang="en"):\n{clean_body_head}\n    ',
        content,
        flags=re.DOTALL
    )

    # 4. Clean HTML_TEMPLATE.format block
    clean_format = '''    html_output = HTML_TEMPLATE.format(
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

    content = re.sub(
        r'html_output = HTML_TEMPLATE\.format\(.*?\)',
        clean_format,
        content,
        flags=re.DOTALL
    )

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Successfully unified generate_html_report across all audit scripts!")
