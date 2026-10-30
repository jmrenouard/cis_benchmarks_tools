#!/usr/bin/env python3
"""
Remove legacy Chart.js <script> blocks and <canvas> tags from HTML_TEMPLATE across all 18 audit scripts.
Replaces canvas with {svg_global_chart_html} and category canvas with {svg_category_chart_html}.
100% Python Standard Library (PSL ONLY).
"""

import glob
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Cleaning HTML_TEMPLATE script blocks across {len(audit_files)} audit scripts...")

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Clean Chart.js CDN script tag from head
    content = content.replace('<script src="https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.js"></script>', '')
    content = content.replace('<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>', '')

    # Replace overall score canvas with {svg_global_chart_html}
    content = re.sub(
        r'<div class="chart-container">\s*<canvas id="overallScoreChart"></canvas>\s*</div>',
        r'{svg_global_chart_html}',
        content
    )

    # Replace category score canvas with {svg_category_chart_html}
    content = re.sub(
        r'<div class="category-chart-container".*?>\s*<canvas id="categoryChart"></canvas>\s*</div>',
        r'{svg_category_chart_html}',
        content
    )

    # Remove Chart.js <script> initialization block from HTML_TEMPLATE
    content = re.sub(r'<script>\s*// Données pour le graphique global.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'CATEGORY_CHART_CANVAS_TEMPLATE = """.*?"""', 'CATEGORY_CHART_CANVAS_TEMPLATE = ""', content, flags=re.DOTALL)
    content = content.replace('{/* Hauteur augmentée */}', '')

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Successfully cleaned legacy Chart.js script blocks across all audit scripts!")
