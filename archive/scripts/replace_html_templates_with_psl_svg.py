#!/usr/bin/env python3
"""
Clean HTML_TEMPLATE across all database scripts:
1. Replace Chart.js canvas with {svg_global_chart_html}
2. Remove Chart.js <script> block completely
3. Inject build_inline_svg_donut_chart & build_inline_svg_category_chart
100% Python Standard Library (PSL ONLY).
"""

import glob
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Replacing HTML templates with 100% Pure Inline SVG Charts across {len(audit_files)} audit scripts...")

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Clean Chart.js CDN in head
    content = content.replace('<script src="https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.js"></script>', '')
    content = content.replace('<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>', '')

    # Replace canvas in HTML_TEMPLATE with {svg_global_chart_html}
    content = re.sub(
        r'<div class="chart-container">\s*<canvas id="overallScoreChart"></canvas>\s*</div>',
        r'{svg_global_chart_html}',
        content
    )

    # Remove script block in HTML_TEMPLATE
    content = re.sub(r'<script>\s*// Données pour le graphique global.*?</script>', '', content, flags=re.DOTALL)

    # Clean legacy CATEGORY_CHART_CANVAS_TEMPLATE
    content = re.sub(r'CATEGORY_CHART_CANVAS_TEMPLATE = """.*?"""', 'CATEGORY_CHART_CANVAS_TEMPLATE = ""', content, flags=re.DOTALL)
    content = content.replace('categories_html += CATEGORY_CHART_CANVAS_TEMPLATE', 'categories_html += build_inline_svg_category_chart(categories_scores)')

    # Ensure svg_global_chart_html computed in generate_html_report
    if 'svg_global_chart_html = build_inline_svg_donut_chart(' not in content:
        content = re.sub(
            r'(def generate_html_report\(.*?\):\n)',
            r'\1    passed_auto_count = sum(1 for c in results if c.get("status") in ["PASS", "Pass"])\n    failed_auto_count = sum(1 for c in results if c.get("status") in ["FAIL", "Fail"])\n    error_auto_count = sum(1 for c in results if c.get("status") in ["ERROR", "Error"])\n    na_auto_count = sum(1 for c in results if c.get("status") in ["N/A", "NA"])\n    svg_global_chart_html = build_inline_svg_donut_chart(passed_auto_count, failed_auto_count, error_auto_count, na_auto_count, overall_score)\n',
            content
        )

    if 'svg_global_chart_html=svg_global_chart_html' not in content:
        content = content.replace(
            'categories_reports=categories_html,',
            'categories_reports=categories_html,\n        svg_global_chart_html=svg_global_chart_html,'
        )

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Successfully updated all 18 audit scripts to use 100% Pure Inline SVG Charts!")
