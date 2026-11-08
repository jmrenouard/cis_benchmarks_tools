---
trigger: always_on
description: Best practices for coding, testing, and formatting in the CIS Benchmark Tools project.
category: governance
---
# 04_best_practices.md

## 🧠 Rationale
To maintain high code quality, standardized output formatting, zero-dependency security, and safe execution of auditing commands across diverse environments.

## 🛠️ Implementation

### 1. Automated vs. Manual Checks
- Prioritize `Automated` checks over `Manual` ones wherever technical verification is possible.
- Ensure robust error handling for OS commands in the test procedure:
  - Check return code explicitly.
  - Handle timeouts gracefully.
  - Never mask errors using destructive `2>/dev/null` redirection (`IMP-003`); preserve stderr for `CommandFailureClassifier`.

### 2. 100% Offline Inline SVG Reporting (No External CDNs)
- Maintain unified, responsive UI across all generated HTML reports.
- **Zero External JS/CSS CDNs for Visualizations**: In accordance with `IMP-002`, **Chart.js is permanently prohibited**. Charts MUST be rendered as 100% self-contained inline SVG (`build_inline_svg_donut_chart`, `build_inline_svg_category_chart`) generated directly in Python PSL.
- Respect the official **5-State Compliance Taxonomy**:
  - `Pass`: Conforms to benchmark (Green / `#DEF7EC`).
  - `Fail`: Non-compliant (Red / `#FDE8E8`).
  - `Error`: Execution failure (Orange / `#F3F4F6`).
  - `Manual`: Requires manual audit (Amber / `#FEF3C7`).
  - `Not Applicable`: Inactive / not relevant (Slate Gray / `#E5E7EB`).

### 3. Credential Security & Process Table Protection
- NEVER hardcode credentials (passwords, private keys, tokens) in scripts or Dockerfiles.
- NEVER pass passwords directly on the command line where they are visible in `ps aux` process tables (`RCA-006`).
- Always pass credentials via environment variables (`MYSQL_PWD`, `PGPASSWORD`, `CIS_DB_PASSWORD`) or client option files (`.my.cnf`).
- Ensure all execution transports sanitize command strings and error logs through `SecretSanitizer`.

### 4. Externalized JSON Rule Specifications
- Store recommendation definitions in `rules/<target_key>.json` so that benchmark updates do not require altering Python execution logic.
- Maintain embedded fallback data in standalone scripts for offline single-file portability.
- Always provide clear, actionable `remediation` instructions in the recommendation definitions.

## ✅ Verification
- Verify that generated HTML reports render clean donut and category bar charts completely offline without internet connectivity.
- Verify that `SecretSanitizer` redacts sensitive credentials in debug logs.
- Run `python scripts/pre_commit_checks.py` to confirm syntax, PSL compliance, and rules integrity.