#!/usr/bin/env python3
"""
Clean legacy Chart.js <script> blocks and <canvas> templates from HTML_TEMPLATE across all 18 audit scripts.
Replaces them with 100% self-contained Inline SVG Donut & Stacked Bar Charts (PSL ONLY, 100% offline).
"""

import glob
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Cleaning legacy Chart.js blocks across {len(audit_files)} audit scripts...")

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Clean Chart.js CDN script tags from <head>
    content = re.sub(r'<script src="https://cdn.jsdelivr.net/npm/chart.js.*?"></script>', '', content)

    # 2. Clean overall canvas block in HTML_TEMPLATE
    content = re.sub(
        r'<div class="chart-container">\s*<canvas id="overallScoreChart"></canvas>\s*</div>',
        r'{svg_global_chart_html}',
        content
    )

    # 3. Clean category canvas template
    content = re.sub(
        r'CATEGORY_CHART_CANVAS_TEMPLATE = """\s*<div class="category-chart-container".*?>.*?</div>\s*"""',
        r'CATEGORY_CHART_CANVAS_TEMPLATE = "{svg_category_chart_html}"',
        content,
        flags=re.DOTALL
    )

    # 4. Remove Chart.js <script> initialization block at bottom of HTML_TEMPLATE
    content = re.sub(r'<script>\s*// Données pour le graphique global.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'/\* Hauteur augmentée \*/', '', content)
    content = re.sub(r'\{\s*/\* Hauteur augmentée \*/\s*\}', '', content)

    # 5. In generate_html_report, format svg_global_chart_html & svg_category_chart_html properly
    if 'svg_global_chart_html = build_inline_svg_donut_chart(' in content and 'svg_global_chart_html=svg_global_chart_html' not in content:
        content = content.replace(
            'categories_reports=categories_html,',
            'categories_reports=categories_html,\n        svg_global_chart_html=svg_global_chart_html,'
        )

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Legacy Chart.js blocks completely cleaned across all 18 audit scripts!")
