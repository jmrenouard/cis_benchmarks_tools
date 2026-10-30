#!/usr/bin/env python3
"""
Replace Chart.js CDN dependency with 100% Pure Inline SVG & HTML5 Charts across ALL 18 Audit Scripts.
Zero External JS, Zero CDN dependencies. Works 100% offline in pure Python PSL.
"""

import glob
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Converting Chart.js to 100% Pure Inline SVG Charts across {len(audit_files)} audit scripts...")

svg_builder_code = r'''
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
    <div style="display: flex; align-items: center; justify-content: center; gap: 30px; margin: 20px 0; flex-wrap: wrap;">
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
'''

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Clean Chart.js CDN script tag
    content = content.replace('<script src="https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.js"></script>', '')
    content = content.replace('<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>', '')

    # Inject builder function
    if "def build_inline_svg_donut_chart(" not in content:
        content = content.replace("def generate_html_report(", svg_builder_code + "\n\n\ndef generate_html_report(")

    # Replace <canvas id="overallScoreChart"></canvas>
    content = re.sub(
        r'<div class="chart-container">\s*<canvas id="overallScoreChart"></canvas>\s*</div>',
        r'{svg_chart_html}',
        content
    )

    # In generate_html_report implementation, calculate svg_chart_html
    if 'svg_chart_html = build_inline_svg_donut_chart(' not in content:
        content = re.sub(
            r'(def generate_html_report\(.*?\):\n)',
            r'\1    svg_chart_html = build_inline_svg_donut_chart(passed_auto_count if "passed_auto_count" in locals() else 0, failed_auto_count if "failed_auto_count" in locals() else 0, error_auto_count if "error_auto_count" in locals() else 0, na_auto_count if "na_auto_count" in locals() else 0, overall_score)\n',
            content
        )

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Converted Chart.js to 100% Pure Inline SVG Charts across all audit scripts!")
