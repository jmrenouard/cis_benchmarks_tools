# 🛠️ CIS Benchmarks Tools - Resolved Debt & Technical Backlog (v1.8.0)

This document tracks technical debt, security considerations, and resolved architectural backlog items.

---

## 🔒 Resolved Architectural Backlog

### 1. Centralization of HTML Report Templates into `templates/` (Resolved in v1.8.0 ✅)
- **Problem**: HTML report template strings were duplicated across all 18 Python audit scripts, making UI maintenance tedious.
- **Resolution**: Centralized HTML report templates into common template files `templates/report_template.html` and `templates/category_report_template.html`. Implemented dynamic loader `load_html_template()` with inline PSL fallbacks across all audit scripts and `audit_cis.py`.

### 2. Externalization of Audit Rules into `rules/` Directory (Resolved in v1.7.0 ✅)
- **Problem**: Audit rule control specifications (`RECOMMENDATIONS_DATA`) were hardcoded inside Python script source files, mixing code logic with data specs.
- **Resolution**: Created top-level `rules/` directory containing 18 clean JSON specification files (`rules/mariadb_106.json`, `rules/cassandra_40.json`, `rules/rhel_8.json`, etc.). Created dynamic rule loader `load_recommendations()` in `audit_cis_*.py` and `audit_cis.py` with inline fallback.

### 2. Chart.js CDN Dependency & Missing Offline Charts (Resolved in v1.7.0 ✅)
- **Problem**: HTML audit reports depended on CDN-hosted Chart.js (`https://cdn.jsdelivr.net/npm/chart.js`), causing blank chart canvases when opened offline or behind firewalls.
- **Resolution**: Designed a 100% self-contained Inline SVG & HTML5 Donut and Stacked Bar Chart engine built in Python PSL (`build_inline_svg_donut_chart()` and `build_inline_svg_category_chart()`). Zero external JavaScript required. Works 100% offline.

### 3. Local & SSH Remote Execution Modes (Resolved in v1.6.0 ✅)
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
- [x] **PR #27: CIS audit MongoDB 7**
- [x] **PR #28: CIS audit MongoDB 8**
- [x] **PR #29: CIS audit Cassandra 4.0**
- [x] **PR #30: CIS audit Cassandra 4.1**
- [x] **PR #31: CIS audit Cassandra 5.0**
- [x] **PR #33: Add missing HTML audit reports for PostgreSQL, MongoDB, and Cassandra**
- [x] **PR #35: Fix PostgreSQL docker run in Makefile and add report generator utility**
- [x] **PR #37: Add CIS Benchmark Markdown specification source files in CIS_DATA/**
- [x] **PR #39: Add POTENTIAL_ISSUES.md and ROADMAP.md for backlog tracking**
- [x] **PR #41: Add PSL-only unified audit script audit_cis.py and pre-commit routine**
- [x] **PR #43: Refactor pre-commit routine to use Python script for code concatenation and PSL validation**
- [x] **PR #45: Refactor pre-commit routine to concatenate Python code via Python PSL script**
- [x] **PR #47: Enhance unified audit_cis.py CLI engine with rule metadata and pre-commit auto-bundling**
- [x] **PR #49: Implement centralized versioning system (v1.1.0) across scripts and repository**
- [x] **PR #51: Organize HTML audit reports into dedicated reports/ directory**
- [x] **PR #53: Organize Dockerfiles into dedicated docker/ directory**
- [x] **PR #55: Update VERSION to v1.2.0, ROADMAP.md, and POTENTIAL_ISSUES.md**
- [x] **PR #57: Enhance audit_cis.py CLI and Python PSL programmatic API**
- [x] **PR #59: Update ROADMAP.md with Python PSL programmatic API details**
- [x] **PR #61: Enhance pre-commit checks with report integrity and repository structure validation**
- [x] **PR #63: Bump version to v1.2.1 and update ROADMAP.md & POTENTIAL_ISSUES.md**
- [x] **PR #65: Add workspace AGENTS.md enforcing strict Git release lifecycle**
- [x] **PR #67: Explicitly specify Python 3 Standard Library ONLY constraint in AGENTS.md**
- [x] **PR #69: Enhance pre-commit checks with executable permissions and CIS_DATA Markdown integrity checks**
- [x] **PR #70: Format Phase 2 items in ROADMAP.md with completed task checkboxes [x]**
- [x] **PR #72: Synchronize VERSION v1.2.4 and format ROADMAP.md Phase 2 checkboxes [x]**
- [x] **PR #74: Finalize VERSION v1.2.4 sync and update ROADMAP.md formatting**
- [x] **PR #76: Format all Phase 2 items in ROADMAP.md with completed task checkboxes [x]**
- [x] **PR #78: Finalize ROADMAP.md Phase 2 formatting and VERSION v1.2.5 sync**
- [x] **PR #80: sec: Migrate subprocess.run to parameter lists and eliminate shell=True (v1.3.0)**
- [x] **PR #82: sec: Synchronize VERSION v1.3.0 across audit_cis.py and documentation**
- [x] **PR #83: sec: Commit VERSION v1.3.0 and bundled audit_cis.py for Subprocess Security Migration**
- [x] **PR #84: sec: [v1.3.0] Migrate subprocess.run to parameter lists and embed versioning in Branch & PR**
- [x] **PR #85: sec: [v1.3.0] Synchronize VERSION file to v1.3.0 and validate 7-step pre-commit routine**
- [x] **PR #86: sec: [v1.3.0] Update VERSION to 1.3.0 and finalize release**
- [x] **PR #88: [v1.4.0] Implement Red Hat Enterprise Linux 8, 9, 10 CIS and STIG Audit Extension**
- [x] **PR #90: sec: [v1.4.1] Migrate all subprocess calls to parameter lists and eliminate shell=True**
- [x] **PR #92: [v1.4.1] Rewrite README.md in English and update repository documentation**
- [x] **PR #94: [v1.4.2] Finalize English README.md and repository documentation**
- [x] **PR #96: [v1.5.0] Add Multi-Language i18n support and synchronized README_fr.md**
- [x] **PR #99: sec: [v1.4.3] Update POTENTIAL_ISSUES.md moving subprocess shell=Fals…**
- [x] **PR #103: [v1.7.0] Externalize Audit Control Rules into rules/ Directory & Implement Offline SVG Charts Engine**
