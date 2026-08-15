#!/usr/bin/env python3
"""
Harmonize .txt export formatter across all 18 CIS audit engines and unified runner (PSL ONLY).
"""

import glob
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


NEW_TXT_BLOCK = """    elif fmt == "txt":
        pass_cnt = sum(1 for r in flat_results if r.get("status") in ["PASS", "Pass"])
        fail_cnt = sum(1 for r in flat_results if r.get("status") in ["FAIL", "Fail"])
        manual_cnt = sum(1 for r in flat_results if r.get("status") in ["MANUAL", "Manual"])
        error_cnt = sum(1 for r in flat_results if r.get("status") in ["ERROR", "Error"])
        lines = [
            "=" * 90,
            f"               CIS BENCHMARK AUDIT REPORT - {target_name.upper()}",
            "=" * 90,
            f"Report Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Global Score  : {overall_score:.1f}%",
            f"Total Controls: {len(flat_results)} (Passed: {pass_cnt}, Failed: {fail_cnt}, Manual: {manual_cnt}, Error: {error_cnt})",
            "-" * 90,
            " CATEGORY BREAKDOWN & COMPLIANCE SUMMARY TABLE",
            "-" * 90,
            f"  {'ID':<6} {'Category Name':<45} {'Pass':<6} {'Fail':<6} {'Manual':<8} {'Score':<8}",
            f"  {'-'*6} {'-'*45} {'-'*6} {'-'*6} {'-'*8} {'-'*8}",
        ]
        if isinstance(categories_scores, dict):
            for cat_id, data in categories_scores.items():
                raw_name = str(data.get("name", cat_id)).strip()
                m = re.match(r"^(\\d+[\\.\\d]*)\\s*[-.:]?\\s*(.*)$", raw_name)
                if m:
                    cid, cname = m.group(1), m.group(2)
                else:
                    cid, cname = str(cat_id)[:6], raw_name
                cname_trunc = cname[:44] if cname else raw_name[:44]
                p = data.get("passed_automated", 0)
                f = data.get("failed_automated", 0)
                m_cnt = data.get("manual_checks", 0)
                sc = data.get("score", 0.0)
                lines.append(f"  {cid:<6} {cname_trunc:<45} {p:<6} {f:<6} {m_cnt:<8} {sc:>6.1f}%")
        lines.extend([
            "=" * 90,
            " DETAILED CONTROL RESULTS",
            "=" * 90,
            ""
        ])
        for r in flat_results:
            status = r.get("status", "")
            if status in ["PASS", "Pass"]:
                status_icon = "[PASS]"
            elif status in ["FAIL", "Fail"]:
                status_icon = "[FAIL]"
            elif status in ["ERROR", "Error"]:
                status_icon = "[ERROR]"
            elif status in ["N/A", "Not Applicable"]:
                status_icon = "[N/A]"
            else:
                status_icon = "[MANUAL]"
            rec_id = r.get("number", r.get("id", ""))
            rec_name = r.get("name", r.get("title", ""))
            lines.append(f"{status_icon} {rec_id} - {rec_name}")
            lines.append(f"  Category: {r.get('category')}")
            test_proc = r.get("test_procedure", r.get("audit", ""))
            if test_proc:
                lines.append(f"  Commande de test: {str(test_proc).strip()}")
            out = r.get("output", r.get("stdout", ""))
            if out:
                lines.append(f"  Output: {str(out).strip()}")
            rem = r.get("remediation", "")
            if rem:
                lines.append(f"  Procédure de remédiation: {str(rem).strip()}")
            lines.append("-" * 90)"""


def process_file(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    start_idx = content.find('    elif fmt == "txt":')
    if start_idx == -1:
        return False

    end_idx = content.find('        with open(filename, "w", encoding="utf-8") as f:', start_idx)
    if end_idx == -1:
        return False

    new_content = content[:start_idx] + NEW_TXT_BLOCK + "\n" + content[end_idx:]
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


def main():
    target_files = sorted(glob.glob(os.path.join(REPO_ROOT, "audit_cis_*.py")))
    updated = 0
    for fpath in target_files:
        if process_file(fpath):
            print(f"✓ Updated txt exporter in {os.path.basename(fpath)}")
            updated += 1
    print(f"Total updated files: {updated}")


if __name__ == "__main__":
    main()
