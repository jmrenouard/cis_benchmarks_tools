# 🛠️ CIS Benchmarks Tools - Resolved Debt & Technical Backlog (v1.8.0)

This document tracks technical debt, security considerations, and resolved architectural backlog items.

---

## 🔒 Resolved Architectural Backlog

### 1. Centralization of HTML Report Templates into `templates/` (Resolved in v1.8.0 ✅)
- **Problem**: HTML report template strings were duplicated across all 18 Python audit scripts, making UI maintenance tedious.
- **Resolution**: Centralized HTML report templates into common template files `templates/report_template.html` and `templates/category_report_template.html`. Implemented dynamic loader `load_html_template()` with inline PSL fallbacks across all audit scripts and `audit_cis.py`.

### 2. PR Diff Size Limit & Atomic Splitting Rules (Resolved in v1.7.1 ✅)
- **Problem**: Large Pull Requests (> 150,000 diff characters, e.g. PR #17, #18, #19) exceeded review limits of automated review bots (Sourcery AI) and hampered code review.
- **Resolution**: Updated `.agents/AGENTS.md` and `03_execution_rules.md` to enforce a strict **15,000 diff character limit per PR** (`git diff main...HEAD | wc -c` < 15000) and require atomic PR splitting for large benchmark script additions.

### 3. Externalization of Audit Rules into `rules/` Directory (Resolved in v1.7.0 ✅)
- **Problem**: Audit rule control specifications (`RECOMMENDATIONS_DATA`) were hardcoded inside Python script source files, mixing code logic with data specs.
- **Resolution**: Created top-level `rules/` directory containing 18 clean JSON specification files (`rules/mariadb_106.json`, `rules/cassandra_40.json`, `rules/rhel_8.json`, etc.). Created dynamic rule loader `load_recommendations()` in `audit_cis_*.py` and `audit_cis.py` with inline fallback.

### 4. Chart.js CDN Dependency & Missing Offline Charts (Resolved in v1.7.0 ✅)
- **Problem**: HTML audit reports depended on CDN-hosted Chart.js (`https://cdn.jsdelivr.net/npm/chart.js`), causing blank chart canvases when opened offline or behind firewalls.
- **Resolution**: Designed a 100% self-contained Inline SVG & HTML5 Donut and Stacked Bar Chart engine built in Python PSL (`build_inline_svg_donut_chart()` and `build_inline_svg_category_chart()`). Zero external JavaScript required. Works 100% offline.

### 5. Local & SSH Remote Execution Modes (Resolved in v1.6.0 ✅)
- **Problem**: Inability to select Local vs SSH execution mode explicitly across all benchmarks.
- **Resolution**: Standardized `-m / --mode {local,ssh}`, `-r / --remote / --ssh user@host`, and `--local` CLI options across all 18 audit scripts and `audit_cis.py`.

---

## 📝 Active Quality Controls
- **PSL Compliance**: AST pre-commit checks block non-PSL imports.
- **Unit Tests**: 100% passing PSL `unittest` suite (`tests/test_evaluate_condition.py`).
- **Pre-Commit Checks**: 8-step quality checker (`make pre-commit`).


## 🔄 Resolved Pull Requests & Technical Improvements
- [x] **PR #1: Implement CIS benchmarks automation tool with extensible check framework**
- [x] **PR #17: CIS audit MariaDB 10.6**
- [x] **PR #18: CIS audit MariaDB 10.11**
- [x] **PR #19: CIS audit MySQL Enterprise 8.0**
- [x] **PR #20: CIS audit MySQL Community 8.4**
- [x] **PR #21: CIS audit MySQL Enterprise 8.4**
- [x] **PR #22: CIS audit MySQL Community 9.7**
- [x] **PR #23: CIS audit MySQL Enterprise 9.7**
- [x] **PR #24: CIS audit PostgreSQL 16**
- [x] **PR #25: CIS audit PostgreSQL 17**
- [x] **PR #26: CIS audit PostgreSQL 18**
