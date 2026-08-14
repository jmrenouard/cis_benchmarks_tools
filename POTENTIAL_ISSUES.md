# 🛠️ CIS Benchmarks Tools - Technical Backlog & Resolved Debt (v2.1.0)

This document tracks technical debt, security considerations, active quality controls, and resolved architectural backlog items.

---

## 🔒 Resolved Architectural Backlog

### 1. Phase 11 Universal Product Hardening, Docker Auto-Routing & Info Maximization (Resolved in v2.3.0 ✅)
- **Problem**: Audit scripts across MySQL, PostgreSQL, MongoDB, Cassandra, and RHEL needed native Docker auto-routing, zero-error execution guarantees, maximized diagnostic output collection, and product justification reports.
- **Resolution**: Extended `detect_docker_container()` and `--docker` CLI parameter across all 18 audit scripts. Automated verifiable manual checks via CLI/SQL queries. Generated product-specific manual controls justification reports in `reports/` (MySQL, PostgreSQL, MongoDB, Cassandra, RHEL). Ensured all manual checks execute diagnostic inspection commands to collect maximum output details in audit reports. Added 52 automated unit tests in `tests/`.

### 2. Phase 10 MariaDB Zero-Error Engine, Docker Auto-Routing & Manual Automation (Resolved in v2.2.0 ✅)
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


## 🔄 Historique Exhaustif des Pull Requests Résolues (Sourcery AI Validated)
- [x] **PR #72**: `docs: Synchronize VERSION v1.2.4 and format ROADMAP.md Phase 2 checkboxes [x]` — *This PR bumps the project version to v1.2.4 across code/docs and adjusts ROADMAP Phase 2 checkbox formatting for consistency.*
- [x] **PR #74**: `docs: Finalize VERSION v1.2.4 sync and update ROADMAP.md formatting` — *Synchronizes the project version to v1.2.4 in the main audit engine and version file, aligning code metadata with the new release tag and related documentation updates.*
- [x] **PR #76**: `docs: Format all Phase 2 items in ROADMAP.md with completed task checkboxes [x]` — *Updates roadmap and related docs to mark Phase 2 items as completed using checkbox syntax and bumps the project version from 1.2.3 to 1.2.5 across documentation and code metadata.*
- [x] **PR #78**: `docs: Finalize ROADMAP.md Phase 2 formatting and VERSION v1.2.5 sync` — *Synchronizes the documented and code-level version to v1.2.5 and updates ROADMAP Phase 2 task formatting to reflect completed work.*
- [x] **PR #80**: `sec: Migrate subprocess.run to parameter lists and eliminate shell=True (v1.3.0)` — *This PR removes all uses of subprocess.run with shell=True by migrating to explicit argument lists and updates documentation and version metadata to v1.3.0, including strengthening the report generation script to use structured Docker commands and safer report copying.*
- [x] **PR #82**: `sec: Synchronize VERSION v1.3.0 across audit_cis.py and documentation` — *Synchronizes the documented and code-defined VERSION of the CIS audit engine to v1.3.0 across the main script and VERSION file.*
- [x] **PR #83**: `sec: Commit VERSION v1.3.0 and bundled audit_cis.py for Subprocess Security Migration` — *Bumps the unified CIS audit engine and repository VERSION to v1.3.0 to align with the subprocess security migration bundle, without functional code changes beyond the version identifiers.*
- [x] **PR #84**: `sec: [v1.3.0] Migrate subprocess.run to parameter lists and embed versioning in Branch & PR` — *Migrates all Python subprocess.run invocations to use explicit argument lists with shell=False for safer execution, and introduces mandatory semantic version embedding (v1.3.0) in VERSION, audit_cis.py, workflow docs, and the contributor process (branch/issue/PR naming plus ROADM*
- [x] **PR #85**: `sec: [v1.3.0] Synchronize VERSION file to v1.3.0 and validate 7-step pre-commit routine` — *Bumps the project version from 1.2.3 to 1.3.0 in the main audit script and the VERSION metadata file to keep runtime and repository versioning in sync.*
- [x] **PR #86**: `sec: [v1.3.0] Update VERSION to 1.3.0 and finalize release` — *Updates the project to release version 1.3.0 by bumping internal version constants and metadata.*
- [x] **PR #88**: `feat: [v1.4.0] Implement Red Hat Enterprise Linux 8, 9, 10 CIS and STIG Audit Extension` — *Adds new RHEL 8/9/10 CIS/STIG audit modules with local and SSH remote execution, wires them into the unified audit engine and bundler, secures subprocess usage (no shell=True), and updates roadmap/potential issues documentation and version metadata to v1.4.0.*
- [x] **PR #90**: `sec: [v1.4.1] Migrate all subprocess calls to parameter lists and eliminate shell=True` — *Migrates all Python subprocess usage to argument-list form without shell=True, refactors the report generation helper script around a safer Docker execution flow, and bumps the suite version/docs to v1.4.1 while updating security and roadmap documentation accordingly.*
- [x] **PR #92**: `docs: [v1.4.1] Rewrite README.md in English and update repository documentation` — *README is rewritten in English to describe the v1.4.1 architecture, unified audit_cis.py CLI, supported benchmarks and controls, remote SSH auditing, repository layout, and security/PSL guarantees; audit_cis.py and VERSION are bumped to v1.4.1 to align docs and code.*
- [x] **PR #94**: `docs: [v1.4.2] Finalize English README.md and repository documentation` — *Documentation is updated to describe the v1.4.2 architecture, unified audit CLI, expanded benchmark coverage (including RHEL/STIG targets), security/PSL constraints, and repository structure, along with a minor version bump in the unified CLI engine and VERSION metadata.*
- [x] **PR #96**: `feat: [v1.5.0] Add Multi-Language i18n support and synchronized README_fr.md` — *Implements multi-language (English/French) i18n support for the unified CIS audit CLI and all HTML report generators, updates documentation and process rules to English with a synchronized French README, and bumps the suite version to v1.5.0 while preserving PSL-only architecture*
- [x] **PR #99**: `sec: [v1.4.3] Update POTENTIAL_ISSUES.md moving subprocess shell=Fals…` — *This PR updates documentation of the potential issues backlog to reflect work completed up to v1.4.2, including the subprocess shell=False migration, and bumps the unified audit engine version to v1.4.3.*
- [x] **PR #103**: `feat: [v1.7.0] Externalize Audit Control Rules into rules/ Directory & Implement Offline SVG Charts Engine` — *This PR externalizes audit control rule specifications into JSON files under a new rules/ directory and replaces all Chart.js-based HTML report charts with a fully offline, PSL-only inline SVG engine, while simplifying generate_html_report signatures and tightening pre-commit val*
- [x] **PR #105**: `feat: [v1.7.0] Synchronize PR Reviews and Feedback into ROADMAP.md & POTENTIAL_ISSUES.md` — *Adds a PSL-only automation script to synchronize GitHub PR reviews and resolution history into ROADMAP.md and POTENTIAL_ISSUES.md, and updates MariaDB CIS audit reports and roadmap/backlog documentation to reflect current PR feedback and compliance status.*
- [x] **PR #108**: `docs: Update Multi-Format Audit Reports for Dual-Mode E2E Runs` — *This PR refreshes and standardizes multi-format CIS audit reports across DB targets, enhancing the HTML UI (dark mode, inline SVG charts, updated metrics/text) for both local and SSH modes while updating SSH invocation options and regenerating associated JSON/TXT report artefacts*
- [x] **PR #110**: `feat(script): add GitHub API PR lifecycle script` — *Adds a standalone Python script that automates creating a set of pull requests for predefined branches and then posts a resolution comment and closes GitHub Issue #109 via the GitHub REST API.*
- [x] **PR #112**: `docs(rules): enforce mandatory issue creation, commenting & closing` — *The PR updates the agent workflow documentation to make GitHub issue lifecycle (creation, resolution commenting, and closing) a mandatory part of the process when working with pull requests.*
- [x] **PR #114**: `fix(engine): ensure command execution errors take precedence over manual status` — *Refactors perform_checks() across all audit scripts to prioritize command execution errors over manual statuses, standardizes output formatting to avoid unterminated f-strings, and updates the HTML report and helper scripts accordingly.*
- [x] **PR #116**: `feat(core): implement unified detect_execution_context engine` — *Adds a unified detect_execution_context() helper to all audit scripts, introduces a dedicated unit test suite for execution context classification, and adds an integration script to propagate the helper across audit files.*
- [x] **PR #118**: `feat(reports): introduce distinct Command Error test status in reports` — *Adds a distinct Command Error metric to HTML reports and standardizes related error messaging across audit scripts, including a helper script to propagate these changes.*
- [x] **PR #120**: `fix(mysql): resolve error_count in HTML reports and regenerate MySQL reports` — *Bind the error_count variable correctly in all audit scripts and regenerate MySQL HTML reports so summary widgets, charts, and section breakdowns accurately reflect command errors vs manual checks and improve error messaging for failed MySQL commands.*
- [x] **PR #122**: `fix(html): fix title palindrome duplication and redundant version badges in reports` — *Aligns all HTML audit reports and generators to use clear product-specific titles, contextual badges, and consistent version metadata, while cleaning up duplicated titles and redundant badges and introducing an execution context parameter.*
- [x] **PR #124**: `fix(rules): sanitize natural text test procedures and implement execution safety guard` — *Adds a shell command validation guard to all CIS audit engines and sanitizes natural-language test procedures in rules JSON, updating reports and scripts to treat human descriptions as manual checks rather than executable commands.*
- [x] **PR #126**: `fix(rhel): fix datetime import and regenerate all 18 clean reports` — *Fixes datetime import usage in RHEL CIS audit scripts and regenerates all 18 HTML audit reports with updated metadata, timestamps, and in one case (PostgreSQL 18) synchronized content reflecting a new run’s results and command outputs.*
- [x] **PR #128**: `feat(diagnostics): eliminate 2>/dev/null to preserve complete stderr diagnostic telemetry` — *This PR removes all uses of `2>/dev/null` from the CIS benchmark rule specifications so that stderr is no longer suppressed, and regenerates the HTML reports to surface the newly captured diagnostic errors and updated scores. A helper Python script is added to perform the bulk ed*
- [x] **PR #130**: `docs: synchronize Sourcery AI PR reviews into ROADMAP.md and POTENTIAL_ISSUES.md` — *This PR introduces a PSL-only helper script that extracts Sourcery AI review insights from recent GitHub PRs and uses it to keep ROADMAP.md and POTENTIAL_ISSUES.md synchronized with an up-to-date, structured history of Sourcery-validated pull requests and their summaries.*
- [x] **PR #132**: `docs: restructure ROADMAP.md with formal project phases from Sourcery AI reviews` — *Restructures ROADMAP.md to transform Sourcery AI code review insights into formal project phases (Phase 10, Phase 11, Phase 12) with task checklists and an executive dashboard.*
- [x] **PR #134**: `docs: finalize formal project phases in ROADMAP.md and synchronize POTENTIAL_ISSUES.md` — *Finalizes formal project phases in ROADMAP.md and closes GitHub Issue #133 with comprehensive checklist items.*
- [x] **PR #136**: `docs: synchronize README, README_fr, and documentation with v2.3.1 architectural evolutions` — *Updates README.md and README_fr.md with v2.3.1 specifications, 4-tier execution contexts, 5-state result taxonomy, zero-error engine guarantees, database credentials CLI options, and offline SVG charts.*
- [x] **PR #138**: `docs(readme_fr): update French documentation with v2.3.1 features and options` — *Synchronizes French documentation README_fr.md with v2.3.1 architecture, 4-tier execution contexts, 5-state result taxonomy, credentials CLI options, and offline SVG charts.*
- [x] **PR #140**: `docs(roadmap): synchronize ROADMAP.md and POTENTIAL_ISSUES.md with v2.3.1 releases` — *Synchronizes ROADMAP.md and POTENTIAL_ISSUES.md with v2.3.1 releases.*
- [x] **PR #142**: `fix(html): remove redundant suite version badge from report header` — *Removes the duplicate suite version badge from the report header across HTML templates and RHEL audit scripts, keeping only the CIS Benchmark version in the top header and the Suite version in the footer.*