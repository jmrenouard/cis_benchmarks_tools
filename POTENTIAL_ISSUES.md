# 🛠️ CIS Benchmarks Tools - Technical Backlog & Resolved Debt (v2.1.0)

This document tracks technical debt, security considerations, active quality controls, and resolved architectural backlog items.

---

## 🔒 Resolved Architectural Backlog

### 1. Phase 10 MariaDB Zero-Error Engine, Docker Auto-Routing & Manual Automation (Resolved in v2.2.0 ✅)
- **Problem**: MariaDB audit scripts could produce raw execution error noise when services were stopped/unreachable, lacked native Docker container auto-routing, and contained manual checks that could be automated via SQL or system checks.
- **Resolution**: Enhanced `audit_cis_mariadb_106.py`, `audit_cis_mariadb_1011.py`, and rule specifications `rules/mariadb_106.json` and `rules/mariadb_1011.json`. Implemented `detect_docker_container()` and automatic Docker container command routing via `--docker` CLI parameter and `docker exec`. Automated verifiable manual checks via SQL queries (user reuse, socket plugin, password_reuse_check, privilege checks). Generated detailed justification report [mariadb_manual_controls_justification.md](file:///home/jmren/GIT_REPOS/cis_benchmarks_tools/reports/mariadb_manual_controls_justification.md) for controls requiring human policy review. Added 42 automated unit tests in `tests/test_mariadb_audit_engine.py`.

### 2. Phase 9 Verification Commands & Remediation Procedures in Reports (Resolved in v2.1.0 ✅)
- **Problem**: Audit test verification commands (`test_procedure` / `audit`) were omitted from TXT, XML, and RHEL HTML reports, and remediation procedures (`remediation`) were hidden for non-FAIL controls or missing in RHEL HTML report layouts.
- **Resolution**: Updated `scripts/add_multiformat_exporters.py` to systematically include test verification commands and remediation procedures across all export formats (TXT, JSON, XML, HTML). Updated RHEL audit scripts (`audit_cis_rhel_8.py`, `9.py`, `10.py`) to save test procedures and display `Commande de test` and `Procédure de remédiation` in HTML table reports.

### 2. Phase 8 Advanced Formatting, Exclusions & Visual UI Validation (Resolved in v2.0.0 ✅)
- **Problem**: Plain-text summary lacked ASCII tables, reports lacked thematic security metrics, HTML templates lacked dark mode, rules lacked pre-execution command safety validation, and E2E tests lacked visual UI checks.
- **Resolution**: Implemented formatted ASCII summary tables for `--format txt`, added thematic security metrics, upgraded `templates/report_template.html` with Dark Mode toggle and visual status icons, added rule command safety validator, added `--exclude-rules` / `--skip-rule` CLI flags, and enhanced E2E test runner for visual DOM validation.

### 2. Dual Local & SSH Remote Execution Modes & DB Options (Resolved in v1.9.0 ✅)
- **Problem**: Audit scripts lacked uniform database connection parameters (`--db-host`, `--db-port`, `--db-user`, `--db-password`) and SSH connection options (`--ssh-port`, `--ssh-key`, `--sudo`), and E2E tests only validated local execution.
- **Resolution**: Standardized Local & SSH execution CLI options across all 18 audit scripts and `audit_cis.py`. Updated `scripts/run_e2e_tests.py` to validate report generation for BOTH Local Mode (`--mode local`) and SSH Remote Mode (`--mode ssh`).

### 3. Centralization of HTML Report Templates into `templates/` (Resolved in v1.8.0 ✅)
- **Problem**: HTML report template strings were duplicated across all 18 Python audit scripts, making UI maintenance tedious and prone to formatting drift.
- **Resolution**: Centralized HTML report templates into common template files `templates/report_template.html` and `templates/category_report_template.html`. Implemented dynamic template loaders (`load_html_template()`, `load_category_template()`) with inline PSL fallbacks across all audit scripts and `audit_cis.py`.

### 4. PR Diff Size Limit & Atomic Splitting Rules (Resolved in v1.7.1 ✅)
- **Problem**: Large Pull Requests (> 150,000 diff characters, e.g. PR #17, #18, #19) exceeded review limits of automated review bots (Sourcery AI) and hampered code review.
- **Resolution**: Updated `.agents/AGENTS.md` and `03_execution_rules.md` to enforce a strict **15,000 diff character limit per PR** (`git diff main...HEAD | wc -c` < 15000) and require atomic PR splitting for large benchmark script additions.

### 5. Externalization of Audit Rules into `rules/` Directory (Resolved in v1.7.0 ✅)
- **Problem**: Audit rule control specifications (`RECOMMENDATIONS_DATA`) were hardcoded inside Python script source files, mixing code logic with data specs.
- **Resolution**: Created top-level `rules/` directory containing 18 clean JSON specification files (`rules/mariadb_106.json`, `rules/cassandra_40.json`, `rules/rhel_8.json`, etc.). Created dynamic rule loader `load_recommendations()` in `audit_cis_*.py` and `audit_cis.py` with inline fallback.

### 6. Chart.js CDN Dependency & Missing Offline Charts (Resolved in v1.7.0 ✅)
- **Problem**: HTML audit reports depended on CDN-hosted Chart.js (`https://cdn.jsdelivr.net/npm/chart.js`), causing blank chart canvases when opened offline or behind firewalls.
- **Resolution**: Designed a 100% self-contained Inline SVG & HTML5 Donut and Stacked Bar Chart engine built in Python PSL (`build_inline_svg_donut_chart()` and `build_inline_svg_category_chart()`). Zero external JavaScript required. Works 100% offline.

### 7. Local & SSH Remote Execution Modes (Resolved in v1.6.0 ✅)
- **Problem**: Inability to select Local vs SSH execution mode explicitly across all benchmarks.
- **Resolution**: Standardized `-m / --mode {local,ssh}`, `-r / --remote / --ssh user@host`, and `--local` CLI options across all 18 audit scripts and `audit_cis.py`.

### 8. Subprocess Command Injection Prevention (Resolved in v1.5.0 ✅)
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
- [x] **PR #109 (v2.0.0)**: Phase 8 Advanced Formatting, Rule Exclusions & Visual UI Validation release.
