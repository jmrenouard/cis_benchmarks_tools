#!/usr/bin/env python3
"""
Comment on and close resolved GitHub issues with clear status summaries in English (100% PSL ONLY).
"""

import json
import os
import urllib.request

TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Python-PSL"
}

RESOLUTIONS = {
    100: """### Status Update: Completed & Resolved in v2.0.0 Release ✅

- **Multi-Format Exporters**: Supported `--format html|json|xml|txt` across all 18 audit scripts, `audit_cis.py`, and `scripts/bundle_audit_cis.py`. Added formatted ASCII summary tables for `--format txt` in v2.0.0.
- **E2E Test Runner**: Implemented `scripts/run_e2e_tests.py` (`make test-e2e`) validating report generation for Local Mode & SSH Remote Mode.
- **Automated Testing Suite**: Implemented 100% PSL `unittest` suite (`tests/test_evaluate_condition.py`) integrated into `make pre-commit`.

This issue is closed as fully resolved in `main` (v2.0.0).""",

    101: """### Status Update: Completed & Resolved in v2.0.0 Release ✅

- **Local & SSH Execution Modes**: Standardized `-m / --mode {local,ssh}`, `-r / --remote / --ssh`, `--ssh-port`, `--ssh-key`, and `--sudo` CLI parameters across all 18 audit scripts and `audit_cis.py`.
- **Database Connection Parameters**: Added `--db-host / --host`, `--db-port / --port`, `--db-user / --user`, and `--db-password / --password` CLI arguments.
- **E2E Dual Mode Validation**: Updated `scripts/run_e2e_tests.py` to test and validate report generation for BOTH Local Mode and SSH Remote Mode.

This issue is closed as fully resolved in `main` (v2.0.0).""",

    102: """### Status Update: Completed & Resolved in v2.0.0 Release ✅

- **Rule Spec Externalization**: Externalized control specifications into 18 dedicated JSON files in `rules/*.json` loaded dynamically via `load_recommendations()`.
- **100% Offline SVG Chart Engine**: Replaced Chart.js CDN dependency with pure Python PSL inline SVG charts (`build_inline_svg_donut_chart()` and `build_inline_svg_category_chart()`). Works 100% offline.

This issue is closed as fully resolved in `main` (v2.0.0).""",

    104: """### Status Update: Completed & Resolved in v2.0.0 Release ✅

- **Automated Roadmap & Issues Synchronization**: Standardized Phase Executive Dashboard in `ROADMAP.md` and resolved technical backlog tracking in `POTENTIAL_ISSUES.md`.
- **Deduplication**: Streamlined workspace governance rules in `.agents/AGENTS.md` and cross-referenced in `ROADMAP.md`.
- **PR Review Integration**: Added PR review feedback summary table in `ROADMAP.md`.

This issue is closed as fully resolved in `main` (v2.0.0)."""
}


def close_issue(issue_num, comment):
    # 1. Post comment
    comment_url = f"https://api.github.com/repos/jmrenouard/cis_benchmarks_tools/issues/{issue_num}/comments"
    comment_data = json.dumps({"body": comment}).encode("utf-8")
    req_c = urllib.request.Request(comment_url, data=comment_data, headers=HEADERS, method="POST")
    with urllib.request.urlopen(req_c) as resp:
        print(f"  ✓ Comment posted to Issue #{issue_num}")

    # 2. Close issue
    issue_url = f"https://api.github.com/repos/jmrenouard/cis_benchmarks_tools/issues/{issue_num}"
    close_data = json.dumps({"state": "closed"}).encode("utf-8")
    req_i = urllib.request.Request(issue_url, data=close_data, headers=HEADERS, method="PATCH")
    with urllib.request.urlopen(req_i) as resp:
        print(f"  ✓ Issue #{issue_num} closed successfully!")


def main():
    print("Processing and closing resolved GitHub issues...")
    for num, comment in RESOLUTIONS.items():
        try:
            close_issue(num, comment)
        except Exception as e:
            print(f"❌ Error closing Issue #{num}: {e}")


if __name__ == "__main__":
    main()
