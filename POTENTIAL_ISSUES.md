# 🛠️ CIS Benchmarks Tools - Technical Backlog & Resolved Debt (v1.9.0)

This document tracks technical debt, active architectural backlog items (Target v2.0.0), security considerations, active quality controls, and resolved architectural backlog items.

---

## ⏳ Active Architectural Backlog (Target v2.0.0)

### 1. Plain-Text ASCII Summary Table Exporters (`--format txt`)
- **Problem**: Plain-text summary output lacks formatted ASCII summary tables and category breakdown ratios.
- **Planned Resolution**: Implement formatted ASCII summary table generator in `export_results()`.

### 2. Thematic Security Domain Metrics
- **Problem**: Compliance scores are grouped strictly by benchmark sections, lacking domain-level aggregation (Authentication, Access Control, Encryption, Network Isolation, Logging).
- **Planned Resolution**: Add thematic security tag aggregation in evaluation engine and report generators.

### 3. HTML Template Aesthetic & Functional Upgrade
- **Problem**: HTML report layout needs ultra-premium visual aesthetics, dark mode support, dynamic status badges, and enhanced responsive alignment.
- **Planned Resolution**: Upgrade `templates/report_template.html` and `templates/category_report_template.html`.

### 4. Rule Command Validation & Execution Safety
- **Problem**: Test procedure commands in JSON rules need pre-execution syntax validation and safety checks.
- **Planned Resolution**: Add command syntax validator and safety checker in `load_recommendations()`.

### 5. Check Automation Expansion (Minimize Manual Audits)
- **Problem**: Some controls currently require manual verification (`type: Manual`).
- **Planned Resolution**: Refactor manual checks into automated SQL queries and system commands to maximize automation.

### 6. Rule Exclusion & Skip Engine (`--exclude-rules` / `--skip-rule`)
- **Problem**: Users cannot exclude specific control IDs or categories during audit execution.
- **Planned Resolution**: Add `--exclude-rules` / `--skip-rule` CLI flags and JSON exclusion configuration handling.

### 7. Headless Browser Visual UI Validation in E2E Pipeline
- **Problem**: E2E test runner validates file size and HTML syntax, but does not visually verify browser rendering (layout overflow, misaligned tables, missing icons).
- **Planned Resolution**: Integrate headless browser visual QA runner in `scripts/run_e2e_tests.py` (`make test-e2e`).

---

## 🔒 Resolved Architectural Backlog

### 1. Dual Local & SSH Remote Execution Modes & DB Options (Resolved in v1.9.0 ✅)
- **Problem**: Audit scripts lacked uniform database connection parameters (`--db-host`, `--db-port`, `--db-user`, `--db-password`) and SSH connection options (`--ssh-port`, `--ssh-key`, `--sudo`), and E2E tests only validated local execution.
- **Resolution**: Standardized Local & SSH execution CLI options across all 18 audit scripts and `audit_cis.py`. Updated `scripts/run_e2e_tests.py` to validate report generation for BOTH Local Mode (`--mode local`) and SSH Remote Mode (`--mode ssh`).

### 2. Centralization of HTML Report Templates into `templates/` (Resolved in v1.8.0 ✅)
- **Problem**: HTML report template strings were duplicated across all 18 Python audit scripts, making UI maintenance tedious and prone to formatting drift.
- **Resolution**: Centralized HTML report templates into common template files `templates/report_template.html` and `templates/category_report_template.html`. Implemented dynamic template loaders (`load_html_template()`, `load_category_template()`) with inline PSL fallbacks across all audit scripts and `audit_cis.py`.

### 3. PR Diff Size Limit & Atomic Splitting Rules (Resolved in v1.7.1 ✅)
- **Problem**: Large Pull Requests (> 150,000 diff characters, e.g. PR #17, #18, #19) exceeded review limits of automated review bots (Sourcery AI) and hampered code review.
- **Resolution**: Updated `.agents/AGENTS.md` and `03_execution_rules.md` to enforce a strict **15,000 diff character limit per PR** (`git diff main...HEAD | wc -c` < 15000) and require atomic PR splitting for large benchmark script additions.

### 4. Externalization of Audit Rules into `rules/` Directory (Resolved in v1.7.0 ✅)
- **Problem**: Audit rule control specifications (`RECOMMENDATIONS_DATA`) were hardcoded inside Python script source files, mixing code logic with data specs.
- **Resolution**: Created top-level `rules/` directory containing 18 clean JSON specification files (`rules/mariadb_106.json`, `rules/cassandra_40.json`, `rules/rhel_8.json`, etc.). Created dynamic rule loader `load_recommendations()` in `audit_cis_*.py` and `audit_cis.py` with inline fallback.

### 5. Chart.js CDN Dependency & Missing Offline Charts (Resolved in v1.7.0 ✅)
- **Problem**: HTML audit reports depended on CDN-hosted Chart.js (`https://cdn.jsdelivr.net/npm/chart.js`), causing blank chart canvases when opened offline or behind firewalls.
- **Resolution**: Designed a 100% self-contained Inline SVG & HTML5 Donut and Stacked Bar Chart engine built in Python PSL (`build_inline_svg_donut_chart()` and `build_inline_svg_category_chart()`). Zero external JavaScript required. Works 100% offline.

### 6. Local & SSH Remote Execution Modes (Resolved in v1.6.0 ✅)
- **Problem**: Inability to select Local vs SSH execution mode explicitly across all benchmarks.
- **Resolution**: Standardized `-m / --mode {local,ssh}`, `-r / --remote / --ssh user@host`, and `--local` CLI options across all 18 audit scripts and `audit_cis.py`.

### 7. Subprocess Command Injection Prevention (Resolved in v1.5.0 ✅)
- **Problem**: Use of raw shell strings (`shell=True`) in `subprocess` calls posed command injection security risks.
- **Resolution**: Migrated all system command execution calls across all audit modules to strict parameter lists (`shell=False`).

---

## 📝 Active Quality Controls

- **PSL Compliance**: AST pre-commit checks (`scripts/pre_commit_checks.py`) verify zero external non-standard library imports.
- **Unit Tests**: 100% passing PSL `unittest` suite (`tests/test_evaluate_condition.py`).
- **Pre-Commit Routine**: 8-step automated checker (`make pre-commit`) enforcing syntax, permissions, structure, and test integrity.
- **PR Diff Size Limit**: Mandatory `< 15,000` diff character check (`git diff main...HEAD | wc -c`).

---

## 🔄 Resolved Pull Requests & Technical Improvements

- [x] **PR #1 (v1.5.1)**: Implement CIS benchmarks automation tool with extensible check framework.
- [x] **PR #17 (v1.6.0)**: CIS audit MariaDB 10.6 initial module.
- [x] **PR #18 (v1.6.0)**: CIS audit MariaDB 10.11 initial module.
- [x] **PR #19 (v1.6.0)**: CIS audit MySQL Enterprise 8.0 initial module.
- [x] **PR #20 (v1.6.0)**: CIS audit MySQL Community 8.4 initial module.
- [x] **PR #21 (v1.6.0)**: CIS audit MySQL Enterprise 8.4 initial module.
- [x] **PR #22 (v1.6.0)**: CIS audit MySQL Community 9.7 initial module.
- [x] **PR #23 (v1.6.0)**: CIS audit MySQL Enterprise 9.7 initial module.
- [x] **PR #24 (v1.6.0)**: CIS audit PostgreSQL 16 initial module.
- [x] **PR #25 (v1.6.0)**: CIS audit PostgreSQL 17 initial module.
- [x] **PR #26 (v1.6.0)**: CIS audit PostgreSQL 18 initial module.
- [x] **PR #106 (v1.7.1)**: Enforce PR diff size limit (< 15K chars) and atomic PR splitting in workspace rules.
- [x] **PR #107 (v1.8.0)**: Centralize HTML report templates in `templates/report_template.html` with PSL loader.
- [x] **PR #108 (v1.9.0)**: Standardize Local & SSH execution CLI parameters and dual-mode E2E test runner.
