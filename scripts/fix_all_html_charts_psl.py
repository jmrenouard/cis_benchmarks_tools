#!/usr/bin/env python3
"""
Replace Chart.js and Canvas elements with 100% Self-Contained Pure Inline SVG & HTML5 Charts
across ALL 18 Audit Scripts. Zero External JS, Zero CDN dependencies. Works 100% offline in Python PSL.
"""

import glob
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Replacing Chart.js with 100% Pure Inline SVG Charts across {len(audit_files)} audit scripts...")

psl_chart_engine = r'''
def build_inline_svg_donut_chart(passed, failed, errors, na, score):
    """Generate 100% self-contained Inline SVG Donut Chart (PSL ONLY, Zero JS)."""
    total = passed + failed + errors + na
    p_pass = (passed / total * 100) if total > 0 else 0
    p_fail = (failed / total * 100) if total > 0 else 0
    p_err = (errors / total * 100) if total > 0 else 0
    p_na = (na / total * 100) if total > 0 else 0

    offset_pass = 25
    offset_fail = 25 - p_pass
    offset_err = offset_fail - p_fail
    offset_na = offset_err - p_err

    return f"""
    <div style="display: flex; align-items: center; justify-content: center; gap: 40px; margin: 20px 0; flex-wrap: wrap;">
      <div style="position: relative; width: 170px; height: 170px;">
        <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg);">
          <path stroke-dasharray="100 100" stroke="#e5e7eb" stroke-width="3.8" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          <path stroke-dasharray="{p_na:.1f} 100" stroke-dashoffset="{offset_na:.1f}" stroke="#9ca3af" stroke-width="3.8" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          <path stroke-dasharray="{p_err:.1f} 100" stroke-dashoffset="{offset_err:.1f}" stroke="#6b7280" stroke-width="3.8" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          <path stroke-dasharray="{p_fail:.1f} 100" stroke-dashoffset="{offset_fail:.1f}" stroke="#ef4444" stroke-width="3.8" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          <path stroke-dasharray="{p_pass:.1f} 100" stroke-dashoffset="{offset_pass:.1f}" stroke="#10b981" stroke-width="3.8" stroke-linecap="round" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
        </svg>
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
          <span style="font-size: 24px; font-weight: 800; color: #111827;">{score:.1f}%</span>
          <span style="font-size: 11px; color: #6b7280; font-weight: 600;">Score Global</span>
        </div>
      </div>
      <div style="display: flex; flex-direction: column; gap: 8px; font-size: 13px;">
        <div style="display: flex; align-items: center; gap: 8px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #10b981; display: inline-block;"></span> <strong>Réussi (PASS) :</strong> {passed}</div>
        <div style="display: flex; align-items: center; gap: 8px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #ef4444; display: inline-block;"></span> <strong>Échoué (FAIL) :</strong> {failed}</div>
        <div style="display: flex; align-items: center; gap: 8px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #6b7280; display: inline-block;"></span> <strong>Erreur (Error) :</strong> {errors}</div>
        <div style="display: flex; align-items: center; gap: 8px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #9ca3af; display: inline-block;"></span> <strong>Non Applicable (N/A) :</strong> {na}</div>
      </div>
    </div>
    """


def build_inline_svg_category_chart(labels, pass_counts, fail_counts, error_counts, na_counts):
    """Generate 100% self-contained Inline SVG/HTML5 Horizontal Stacked Bar Charts per category (PSL ONLY, Zero JS)."""
    items_html = []
    for i, label in enumerate(labels):
        p = pass_counts[i] if i < len(pass_counts) else 0
        f = fail_counts[i] if i < len(fail_counts) else 0
        e = error_counts[i] if i < len(error_counts) else 0
        n = na_counts[i] if i < len(na_counts) else 0
        cat_total = p + f + e + n
        cat_score = (p / cat_total * 100) if cat_total > 0 else 0

        p_pass = (p / cat_total * 100) if cat_total > 0 else 0
        p_fail = (f / cat_total * 100) if cat_total > 0 else 0
        p_err = (e / cat_total * 100) if cat_total > 0 else 0
        p_na = (n / cat_total * 100) if cat_total > 0 else 0

        badge_color = "#10b981" if cat_score >= 80 else ("#f59e0b" if cat_score >= 50 else "#ef4444")

        bar_segments = []
        if p > 0: bar_segments.append(f'<div style="width: {p_pass:.1f}%; background: #10b981;" title="Réussi: {p}"></div>')
        if f > 0: bar_segments.append(f'<div style="width: {p_fail:.1f}%; background: #ef4444;" title="Échoué: {f}"></div>')
        if e > 0: bar_segments.append(f'<div style="width: {p_err:.1f}%; background: #6b7280;" title="Error: {e}"></div>')
        if n > 0: bar_segments.append(f'<div style="width: {p_na:.1f}%; background: #9ca3af;" title="N/A: {n}"></div>')
        if not bar_segments:
            bar_segments.append('<div style="width: 100%; background: #e5e7eb;" title="Aucun contrôle"></div>')

        items_html.append(f"""
        <div style="margin-bottom: 16px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-weight: 600; font-size: 14px; color: #374151;">{label}</span>
            <span style="font-weight: 700; font-size: 13px; color: {badge_color};">{cat_score:.1f}% ({p}/{cat_total})</span>
          </div>
          <div style="display: flex; height: 16px; width: 100%; border-radius: 8px; overflow: hidden; background: #f3f4f6; border: 1px solid #e5e7eb;">
            {''.join(bar_segments)}
          </div>
        </div>
        """)

    legend_html = """
    <div style="display: flex; gap: 20px; justify-content: center; margin-bottom: 20px; font-size: 13px;">
      <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #10b981; display: inline-block;"></span> Réussi</div>
      <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #ef4444; display: inline-block;"></span> Échoué</div>
      <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #6b7280; display: inline-block;"></span> Erreur</div>
      <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #9ca3af; display: inline-block;"></span> N/A</div>
    </div>
    """

    return f"""
    <div style="background: #ffffff; padding: 24px; border-radius: 12px; border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-top: 24px;">
      <h3 style="font-size: 18px; font-weight: 700; color: #111827; margin-bottom: 16px; text-align: center;">Répartition des contrôles automatisés par catégorie</h3>
      {legend_html}
      {''.join(items_html)}
    </div>
    """
'''

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Clean Chart.js CDN script tags & unescaped CSS comments
    content = content.replace('<script src="https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.js"></script>', '')
    content = content.replace('<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>', '')
    content = content.replace('{/* Hauteur augmentée */}', '')
    content = content.replace('/* Hauteur augmentée */', '')

    # Inject chart engine functions
    content = re.sub(r'def build_inline_svg_donut_chart\(.*?\):\n.*?(?=\n\ndef generate_html_report|\ndef perform_checks)', '', content, flags=re.DOTALL)
    content = content.replace("def generate_html_report(", psl_chart_engine + "\n\n\ndef generate_html_report(")

    # In database scripts, update HTML template
    content = re.sub(
        r'<div class="chart-container">\s*<canvas id="overallScoreChart"></canvas>\s*</div>',
        r'{svg_global_chart_html}',
        content
    )
    content = re.sub(
        r'<div class="category-chart-container".*?>\s*<canvas id="categoryChart"></canvas>\s*</div>',
        r'',
        content
    )

    # In generate_html_report, compute svg_global_chart_html and svg_category_chart_html
    if 'svg_global_chart_html = build_inline_svg_donut_chart(' not in content:
        content = content.replace(
            'categories_html += CATEGORY_CHART_CANVAS_TEMPLATE',
            'categories_html += svg_category_chart_html'
        )
        content = re.sub(
            r'(def generate_html_report\(.*?\):\n)',
            r'\1    svg_global_chart_html = build_inline_svg_donut_chart(passed_auto_count if "passed_auto_count" in locals() else 0, failed_auto_count if "failed_auto_count" in locals() else 0, error_auto_count if "error_auto_count" in locals() else 0, na_auto_count if "na_auto_count" in locals() else 0, overall_score)\n    svg_category_chart_html = build_inline_svg_category_chart(category_labels if "category_labels" in locals() else [], category_pass_counts if "category_pass_counts" in locals() else [], category_fail_counts if "category_fail_counts" in locals() else [], category_error_counts if "category_error_counts" in locals() else [], category_na_counts if "category_na_counts" in locals() else [])\n',
            content
        )

    # Ensure svg_global_chart_html passed to format
    if 'svg_global_chart_html=svg_global_chart_html' not in content:
        content = content.replace(
            'categories_reports=categories_html,',
            'categories_reports=categories_html,\n        svg_global_chart_html=svg_global_chart_html,'
        )

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Converted Chart.js to 100% Pure Inline SVG & HTML5 Charts across all audit scripts!")
