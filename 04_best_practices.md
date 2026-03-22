---
trigger: always_on
description: Best practices for coding, testing, and formatting in the CIS Benchmark Tools project.
category: governance
---
# 04_best_practices.md

## 🧠 Rationale
To maintain high code quality, standardized output formatting, and safe execution of OS-level commands during the auditing process.

## 🛠️ Implementation

### 1. Automated vs. Manual Checks
- Prioritize `Automated` checks over `Manual` ones wherever possible.
- Ensure robust error handling for OS commands in the `test_procedure`:
  - Check for `returncode`.
  - Handle `timeout` gracefully.
  - Handle "command not found" errors.

### 2. HTML Consistency
- Maintain a unified UI across all generated HTML reports.
- Use Tailwind CSS via CDN and Chart.js as currently implemented in the `HTML_TEMPLATE` block of existing scripts.
- Ensure responsive design and clear color-coding (Pass=Green, Fail=Red, Manual=Yellow, Error=Gray).

### 3. Security
- NEVER hardcode sensitive credentials (passwords, API keys) in the Python scripts or Dockerfiles.
- Use environment variables, configuration files (e.g., `.my.cnf`), or secure initialization modes (like `--initialize-insecure`) specifically designated for isolated testing environments only.

### 4. Remediation Instructions
- Always provide clear, actionable `remediation` instructions in the `RECOMMENDATIONS_DATA` for any failing check.

## ✅ Verification
- Run a manual code review to check for hardcoded secrets.
- Verify that the HTML report renders correctly in a modern browser and uses Tailwind classes.