#!/usr/bin/env python3
"""
Multi-Product CIS Audit RCA Report Generator & Telemetry Engine (Python PSL ONLY).
Scans reports/ and produces unified Markdown, JSON, and HTML diagnostic reports:
  - reports/analyse_diagnostique_rca.md
  - reports/analyse_diagnostique_rca.json
  - reports/analyse_diagnostique_rca.html
"""

import glob
import json
import os
import re
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from audit_diagnostics import (
    FailureCategory,
    FailureDiagnostic,
    CommandFailureClassifier,
    AuditDiagnosticSummary
)

REPORTS_DIR = os.path.join(REPO_ROOT, "reports")


def parse_txt_report(filepath: str) -> Optional[Dict[str, Any]]:
    """Parse text report into structured control list."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        filename = os.path.basename(filepath)
        is_ssh = "_ssh" in filename.lower()
        base_name = filename.replace("rapport_cis_", "").replace("_ssh", "").replace(".txt", "").upper()
        target_name = f"{base_name} [SSH]" if is_ssh else f"{base_name} [LOCAL]"

        score_match = re.search(r"Global Score\s*:\s*([\d\.]+)%", content)
        score = float(score_match.group(1)) if score_match else 0.0

        controls = []
        for block in re.split(r"-{50,}", content):
            block = block.strip()
            status_match = re.search(r"^\[(PASS|FAIL|MANUAL|ERROR|N/A)\]\s+([\d\.\-]+)\s+-\s+(.+)", block, re.MULTILINE)
            if not status_match:
                continue

            status, ctrl_id, ctrl_name = status_match.groups()
            cat_match = re.search(r"Category:\s*(.+)", block)
            out_match = re.search(r"Output:\s*(.*?)(?=\n\s*Remediation:|\Z)", block, re.DOTALL)
            rem_match = re.search(r"Remediation:\s*(.*)", block, re.DOTALL)

            controls.append({
                "status": status,
                "id": ctrl_id,
                "number": ctrl_id,
                "name": ctrl_name,
                "category": cat_match.group(1).strip() if cat_match else "General",
                "output": out_match.group(1).strip() if out_match else "",
                "remediation": rem_match.group(1).strip() if rem_match else "N/A"
            })

        return {"target": target_name, "filename": filename, "is_ssh": is_ssh, "score": score, "controls": controls}
    except Exception:
        return None


def generate_rca_html_dashboard(fleet_summaries: List[AuditDiagnosticSummary], total_controls: int, output_path: str) -> None:
    """Generates an HTML RCA Dashboard (PSL ONLY)."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_targets = len(fleet_summaries)
    total_clean = sum(s.clean_passes for s in fleet_summaries)
    total_sec_fail = sum(s.security_failures for s in fleet_summaries)
    total_manual = sum(s.manual_checks for s in fleet_summaries)
    total_env_err = sum(s.environment_errors for s in fleet_summaries)

    pct_pass = (total_clean / max(1, total_controls)) * 100.0
    pct_fail = (total_sec_fail / max(1, total_controls)) * 100.0
    pct_manual = (total_manual / max(1, total_controls)) * 100.0

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CIS Fleet RCA Dashboard</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 24px; }}
        .header {{ background: #1e293b; border-radius: 8px; padding: 20px; margin-bottom: 20px; border: 1px solid #334155; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 20px; }}
        .card {{ background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 16px; text-align: center; }}
        .val {{ font-size: 1.8rem; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 8px; overflow: hidden; }}
        th, td {{ padding: 10px 14px; text-align: left; border-bottom: 1px solid #334155; font-size: 0.9rem; }}
        th {{ background: #334155; color: #94a3b8; }}
        .pass {{ color: #10b981; }} .fail {{ color: #ef4444; }} .manual {{ color: #f59e0b; }} .env {{ color: #6366f1; }}
    </style>
</head>
<body>
    <div class="header">
        <h1 style="margin:0; color:#38bdf8;">🔍 CIS Benchmarks Fleet RCA Dashboard</h1>
        <p style="margin:4px 0 0 0; color:#94a3b8;">Generated: {now_str} | Targets: {total_targets} | Total Controls: {total_controls}</p>
    </div>
    <div class="grid">
        <div class="card"><div style="color:#94a3b8;">Targets</div><div class="val" style="color:#38bdf8;">{total_targets}</div></div>
        <div class="card"><div style="color:#94a3b8;">Pass ({pct_pass:.1f}%)</div><div class="val pass">{total_clean}</div></div>
        <div class="card"><div style="color:#94a3b8;">Security Fail ({pct_fail:.1f}%)</div><div class="val fail">{total_sec_fail}</div></div>
        <div class="card"><div style="color:#94a3b8;">Manual ({pct_manual:.1f}%)</div><div class="val manual">{total_manual}</div></div>
        <div class="card"><div style="color:#94a3b8;">Tooling Errors</div><div class="val env">{total_env_err}</div></div>
    </div>
    <table>
        <thead>
            <tr><th>Target</th><th>Controls</th><th>Pass</th><th>Fail</th><th>Manual</th><th>Tooling Errors</th></tr>
        </thead>
        <tbody>
"""
    for s in sorted(fleet_summaries, key=lambda x: x.target_name):
        html += f"            <tr><td><strong>{s.target_name}</strong></td><td>{s.total_checks}</td><td class='pass'>{s.clean_passes}</td><td class='fail'>{s.security_failures}</td><td class='manual'>{s.manual_checks}</td><td class='env'>{s.environment_errors}</td></tr>\n"

    html += """        </tbody>
    </table>
</body>
</html>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


def generate_fleet_rca_reports() -> Tuple[str, str, str]:
    """Scans reports/ and produces Markdown, JSON, and HTML RCA reports."""
    summaries: List[AuditDiagnosticSummary] = []
    total_controls = 0

    for tf in sorted(glob.glob(os.path.join(REPORTS_DIR, "rapport_cis_*.txt"))):
        parsed = parse_txt_report(tf)
        if not parsed:
            continue
        target_name = parsed["target"]
        summary = AuditDiagnosticSummary(target_name=target_name)
        for ctrl in parsed.get("controls", []):
            summary.add(CommandFailureClassifier.classify_control_result(ctrl, target_hint=target_name))
            total_controls += 1
        summaries.append(summary)

    md_path = os.path.join(REPORTS_DIR, "analyse_diagnostique_rca.md")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_targets = len(summaries)
    total_clean = sum(s.clean_passes for s in summaries)
    total_sec_fail = sum(s.security_failures for s in summaries)
    total_manual = sum(s.manual_checks for s in summaries)
    total_env_err = sum(s.environment_errors for s in summaries)

    lines = [
        "# 🔍 Fleet Root Cause Analysis (RCA) & Diagnostics Report",
        "",
        f"**Generated:** `{now_str}` | **Audited Targets:** `{total_targets}` | **Total Controls:** `{total_controls}`",
        "",
        "## 📊 Global Reliability & Compliance Matrix",
        "",
        "| Metric | Count | Percentage | Assessment |",
        "| :--- | :---: | :---: | :--- |",
        f"| **Total Assessed Controls** | `{total_controls}` | 100% | 🛡️ CIS Verified |",
        f"| 🟢 **Clean Compliant Passes** | `{total_clean}` | `{total_clean / max(1, total_controls) * 100:.1f}%` | Compliant Controls |",
        f"| 🔴 **Genuine Security Failures** | `{total_sec_fail}` | `{total_sec_fail / max(1, total_controls) * 100:.1f}%` | Non-Compliant Baseline |",
        f"| 🟡 **Manual Assessment Needed** | `{total_manual}` | `{total_manual / max(1, total_controls) * 100:.1f}%` | Human / Architecture Review |",
        f"| ⚠️ **Environmental / Tooling Errors** | `{total_env_err}` | `{total_env_err / max(1, total_controls) * 100:.1f}%` | {'✅ 0 Errors (100% Tooling Reliability)' if total_env_err == 0 else '⚠️ Infrastructure Issues'} |",
        "",
        "## 📋 Per-Target Diagnostic Breakdown",
        "",
        "| Target Product | Total Controls | Pass | Fail | Manual | Tooling Errors | Environment Reliability |",
        "| :--- | :---: | :---: | :---: | :---: | :--- |",
    ]

    for s in sorted(summaries, key=lambda x: x.target_name):
        rel_str = "✅ 100% Clean" if s.environment_errors == 0 else f"⚠️ {s.environment_errors} Tool Errors"
        lines.append(
            f"| `{s.target_name}` | `{s.total_checks}` | `{s.clean_passes}` | `{s.security_failures}` | `{s.manual_checks}` | `{s.environment_errors}` | {rel_str} |"
        )

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    json_path = os.path.join(REPORTS_DIR, "analyse_diagnostique_rca.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump([s.to_dict() for s in summaries], f, indent=2)

    html_path = os.path.join(REPORTS_DIR, "analyse_diagnostique_rca.html")
    generate_rca_html_dashboard(summaries, total_controls, html_path)
    return md_path, json_path, html_path


if __name__ == "__main__":
    generate_fleet_rca_reports()
