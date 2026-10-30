#!/usr/bin/env python3
"""
Update generate_html_report() parameters across all 18 audit scripts to pass
product_title, benchmark_version, suite_version, and execution_context cleanly without duplicates (100% PSL ONLY).
"""

import glob
import os
import re

BENCHMARK_META = {
    "audit_cis_mysql_80.py": ("MySQL 8.0", "1.4.0"),
    "audit_cis_mysql_community_84.py": ("MySQL Community 8.4", "1.0.0"),
    "audit_cis_mysql_community_97.py": ("MySQL Community 9.7", "1.0.0"),
    "audit_cis_mysql_enterprise_84.py": ("MySQL Enterprise 8.4", "1.0.0"),
    "audit_cis_mysql_enterprise_97.py": ("MySQL Enterprise 9.7", "1.0.0"),
    "audit_cis_mariadb_106.py": ("MariaDB 10.6", "1.0.0"),
    "audit_cis_mariadb_1011.py": ("MariaDB 10.11", "1.1.0"),
    "audit_cis_postgresql_16.py": ("PostgreSQL 16", "1.0.0"),
    "audit_cis_postgresql_17.py": ("PostgreSQL 17", "1.0.0"),
    "audit_cis_postgresql_18.py": ("PostgreSQL 18", "1.0.0"),
    "audit_cis_mongodb_7.py": ("MongoDB 7", "1.0.0"),
    "audit_cis_mongodb_8.py": ("MongoDB 8", "1.0.0"),
    "audit_cis_cassandra_40.py": ("Cassandra 4.0", "1.0.0"),
    "audit_cis_cassandra_41.py": ("Cassandra 4.1", "1.0.0"),
    "audit_cis_cassandra_50.py": ("Cassandra 5.0", "1.0.0"),
    "audit_cis_rhel_8.py": ("RHEL 8", "3.0.0"),
    "audit_cis_rhel_9.py": ("RHEL 9", "2.0.0"),
    "audit_cis_rhel_10.py": ("RHEL 10", "1.0.0"),
}

suite_version = "2.3.0"
if os.path.exists("VERSION"):
    with open("VERSION", "r", encoding="utf-8") as vf:
        v = vf.read().strip().lstrip("v")
        if v:
            suite_version = v

print(f"Updating HTML report metadata across {len(BENCHMARK_META)} audit scripts (Tool Version: v{suite_version})...")

for fname, (prod_title, bm_version) in BENCHMARK_META.items():
    if not os.path.exists(fname):
        continue

    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()

    # Update generate_html_report signature to accept execution_context
    content = re.sub(
        r'def generate_html_report\([^)]+\):',
        r'def generate_html_report(results, overall_score, categories_scores, filename=None, lang="en", execution_context=None):',
        content
    )

    # In generate_html_report, update SafeDict bindings
    content = re.sub(
        r'html_output = load_html_template\(\)\.format_map\(SafeDict\(.*?\)\)',
        f'''ctx_label = execution_context if execution_context else "Local Bare-Metal"
    html_output = load_html_template().format_map(SafeDict(
        product_title="{prod_title}",
        benchmark_title="{prod_title}",
        benchmark_version="{bm_version}",
        suite_version="{suite_version}",
        execution_context=ctx_label,
        lang=lang if 'lang' in locals() else "en",
        report_date=report_date,
        overall_score=overall_score,
        overall_score_class=overall_score_class,
        passed_automated_count=passed_auto_count if 'passed_auto_count' in locals() else 0,
        failed_automated_count=failed_auto_count if 'failed_auto_count' in locals() else 0,
        passed_automated=passed_auto_count if 'passed_auto_count' in locals() else 0,
        total_automated=(passed_auto_count + failed_auto_count) if 'passed_auto_count' in locals() else 0,
        manual_checks=total_manual if 'total_manual' in locals() else 0,
        error_checks=total_errors if 'total_errors' in locals() else 0,
        error_count=total_errors if 'total_errors' in locals() else 0,
        na_checks=total_na if 'total_na' in locals() else 0,
        sidebar_links=sidebar_links_html if 'sidebar_links_html' in locals() else "",
        categories_reports=categories_html,
        donut_svg=svg_global_chart_html if 'svg_global_chart_html' in locals() else "",
        bar_svg=build_inline_svg_category_chart(categories_scores) if 'categories_scores' in locals() else "",
        svg_global_chart_html=svg_global_chart_html if 'svg_global_chart_html' in locals() else ""
    ))''',
        content,
        flags=re.DOTALL
    )

    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Successfully updated report titles, benchmark versions, and suite versions across all scripts!")
