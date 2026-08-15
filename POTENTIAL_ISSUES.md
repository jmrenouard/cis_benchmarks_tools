# 🛠️ CIS Benchmarks Tools - Technical Backlog & Resolved Debt (v2.6.0)

This document tracks technical debt, security considerations, active quality controls, and resolved architectural backlog items.

---

## 🔒 Resolved Architectural Backlog

### 1. Phase 17 Automated E2E Text Export Generation, Parsing & Real-Time Analysis (Resolved in v2.6.0 ✅)
- **Problem**: Text export (.txt) formatting varied across engines and was not systematically parsed for real-time error detection during automated E2E test runs.
- **Resolution**: Harmonized text exporter format across all 18 benchmark engines (PR #326-#336). Implemented comprehensive E2E text export testing suite in `tests/test_e2e_text_export_analysis.py` and `tests/test_e2e_docker_audits.py` (PR #338). Added real-time text parsing and zero-error verification in `scripts/run_e2e_tests.py` and dynamic versioning in `scripts/analyze_e2e_reports.py` (PR #340). Released v2.6.0 (PR #342).

### 2. Phase 16 Authentic CIS Spec Sync & Zero Command Errors Guarantee (Resolved in v2.5.0 ✅)
- **Problem**: Some CIS rules had drifted from official CIS benchmark specifications and could produce command execution errors in Docker environments.
- **Resolution**: Synchronized 100% of rule definitions across all 18 targets with authentic CIS specifications in `CIS_DATA/` (564 Automated, 323 Manual, 0 Command Errors).

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
- [x] **PR #144**: `feat(cli): normalize command-line parameters in audit_cis bundler and engine` — *Standardizes all CLI arguments, aliases, and credentials across the unified audit suite bundler and engine.*
- [x] **PR #146**: `feat(cli): standardize CLI parameters, credentials injection, and environment mapping across all 18 target audit engines` — *Standardizes CLI arguments, short/long aliases, and environment variable injections for database credentials across all target engines.*
- [x] **PR #148**: `fix(package): enhance package queries and remediations for multi-distribution environments (Debian, RHEL, Alpine)` — *Updates package checks and remediation recommendations to seamlessly support apt, dnf/yum, and apk across distributions.*
- [x] **PR #150**: `feat(engine): introduce deterministic execution contexts in perform_checks and fallback resolution` — *Adds robust execution context resolution and graceful fallback handling.*
- [x] **PR #152**: `refactor(engine): normalize argument parser flags across all database targets` — *Unifies argument parser flags and help messages across MySQL, MariaDB, PostgreSQL, MongoDB, Cassandra, and RHEL.*
- [x] **PR #154**: `fix(engine): resolve NoneType stdout/stderr formatting exceptions in report generation` — *Ensures stdout and stderr default to empty strings when evaluated in evaluate_condition to prevent TypeError exceptions.*
- [x] **PR #156**: `fix(postgresql): standardize rule 1.5 version check and multi-distro package remediation` — *Standardizes rule 1.5 executable SQL and cross-distro package remediations in PostgreSQL benchmarks.*
- [x] **PR #158**: `test(coverage): expand unit and end-to-end test suite coverage for credentials, distros, and zero command errors` — *Expands the automated test suite to 70 tests across 17 test modules covering credential injection, package queries, AST verification, and Docker CLI routing.*
- [x] **PR #168**: `feat(rules): convert manual controls to automated in Cassandra 4.0 and 4.1` — *Converts all manual checks in Cassandra 4.0 and 4.1 rule specifications to automated deterministic controls.*
- [x] **PR #170**: `feat(rules): convert manual controls to automated in Cassandra 5.0` — *Converts all manual checks in Cassandra 5.0 rule specifications to automated deterministic controls.*
- [x] **PR #172**: `feat(rules): convert manual controls to automated in MongoDB 7` — *Converts all manual checks in MongoDB 7 rule specifications to automated deterministic controls.*
- [x] **PR #174**: `feat(rules): convert manual controls to automated in MongoDB 8` — *Converts all manual checks in MongoDB 8 rule specifications to automated deterministic controls.*
- [x] **PR #176**: `feat(rules): convert manual controls to automated in MariaDB 10.6` — *Converts all manual checks in MariaDB 10.6 rule specifications to automated deterministic controls.*
- [x] **PR #178**: `feat(rules): convert manual controls to automated in MariaDB 10.11` — *Converts all manual checks in MariaDB 10.11 rule specifications to automated deterministic controls.*
- [x] **PR #180**: `feat(rules): convert manual controls to automated in PostgreSQL 16 (Part 1 - Cat 1 to 4)` — *Converts categories 1 to 4 manual checks in PostgreSQL 16 to automated deterministic controls.*
- [x] **PR #182**: `feat(rules): convert manual controls to automated in PostgreSQL 16 (Part 2 - Cat 5 to 8)` — *Converts categories 5 to 8 manual checks in PostgreSQL 16 to automated deterministic controls.*
- [x] **PR #184**: `feat(rules): convert manual controls to automated in PostgreSQL 17 (Part 1 - Cat 1 to 4)` — *Converts categories 1 to 4 manual checks in PostgreSQL 17 to automated deterministic controls.*
- [x] **PR #186**: `feat(rules): convert manual controls to automated in PostgreSQL 17 (Part 2 - Cat 5 to 8)` — *Converts categories 5 to 8 manual checks in PostgreSQL 17 to automated deterministic controls.*
- [x] **PR #188**: `feat(rules): convert manual controls to automated in PostgreSQL 18 (Part 1 - Cat 1 to 4)` — *Converts categories 1 to 4 manual checks in PostgreSQL 18 to automated deterministic controls.*
- [x] **PR #190**: `feat(rules): convert manual controls to automated in PostgreSQL 18 (Part 2 - Cat 5 to 8)` — *Converts categories 5 to 8 manual checks in PostgreSQL 18 to automated deterministic controls.*
- [x] **PR #192**: `feat(rules): convert manual controls to automated in MySQL Community 8.4` — *Converts manual checks in MySQL Community 8.4 rule specifications to automated deterministic controls.*
- [x] **PR #194**: `feat(rules): convert manual controls to automated in MySQL Enterprise 8.4 and MySQL 9.7` — *Converts manual checks in MySQL Enterprise 8.4, MySQL Community 9.7, and MySQL Enterprise 9.7 to automated deterministic controls.*
- [x] **PR #196**: `feat(mysql): convert manual controls to automated in MySQL 8.0 and update container hardening` — *Converts manual checks in MySQL 8.0 to automated deterministic controls and updates container startup hardening.*
- [x] **PR #198**: `feat(mysql): normalize CLI parameters, credentials injection, and truthy paths in MySQL Community 8.4` — *Normalizes CLI options, database credentials environment injection, and truthy path handling in MySQL Community 8.4.*
- [x] **PR #200**: `feat(mysql): normalize CLI parameters, credentials injection, and truthy paths in MySQL Enterprise 8.4` — *Normalizes CLI options, database credentials environment injection, and truthy path handling in MySQL Enterprise 8.4.*
- [x] **PR #202**: `feat(mysql): normalize CLI parameters, credentials injection, and truthy paths in MySQL Community 9.7` — *Normalizes CLI options, database credentials environment injection, and truthy path handling in MySQL Community 9.7.*
- [x] **PR #204**: `feat(mysql): normalize CLI parameters, credentials injection, and truthy paths in MySQL Enterprise 9.7` — *Normalizes CLI options, database credentials environment injection, and truthy path handling in MySQL Enterprise 9.7.*
- [x] **PR #206**: `feat(mongodb): normalize CLI parameters, credentials injection, and truthy paths in MongoDB 7` — *Normalizes CLI options, database credentials environment injection, and truthy path handling in MongoDB 7.*
- [x] **PR #208**: `feat(mongodb): normalize CLI parameters, credentials injection, and truthy paths in MongoDB 8` — *Normalizes CLI options, database credentials environment injection, and truthy path handling in MongoDB 8.*
- [x] **PR #210**: `feat(cassandra): normalize CLI parameters, credentials injection, and truthy paths in Cassandra 4.0` — *Normalizes CLI options, database credentials environment injection, and truthy path handling in Cassandra 4.0.*
- [x] **PR #212**: `feat(cassandra): normalize CLI parameters, credentials injection, and truthy paths in Cassandra 4.1` — *Normalizes CLI options, database credentials environment injection, and truthy path handling in Cassandra 4.1.*
- [x] **PR #214**: `feat(cassandra): normalize CLI parameters, credentials injection, and truthy paths in Cassandra 5.0` — *Normalizes CLI options, database credentials environment injection, and truthy path handling in Cassandra 5.0.*
- [x] **PR #216**: `feat(rhel): normalize CLI parameters, truthy paths, and safe evaluations in RHEL 8, 9, and 10` — *Normalizes CLI options, truthy path handling, and safe condition evaluation in RHEL 8, 9, and 10.*
- [x] **PR #218**: `feat(engines): update truthy path checks and safe stderr handling in MariaDB 10.6 and MySQL 8.0` — *Updates truthy path handling and safe stderr fallback in MariaDB 10.6 and MySQL 8.0.*
- [x] **PR #220**: `feat(engines): update truthy path checks and safe stderr handling in MariaDB 10.11 and PostgreSQL 16/17/18` — *Updates truthy path handling and safe stderr fallback in MariaDB 10.11 and PostgreSQL 16/17/18.*
- [x] **PR #222**: `feat(engines): update truthy path checks and safe stderr handling in MongoDB, Cassandra, and RHEL engines` — *Updates truthy path handling and safe stderr fallback across MongoDB 7/8, Cassandra 4.0/4.1/5.0, and RHEL 8/9/10 engines.*
- [x] **PR #224**: `fix(rules): adapt command environments and conditions in MySQL 8.0, Community 8.4, and Enterprise 8.4` — *Adapts shell commands and expected outputs to local and containerized environments for MySQL 8.0 and 8.4.*
- [x] **PR #226**: `fix(rules): adapt command environments and conditions in MySQL 9.7 and MariaDB 10.6/10.11` — *Adapts shell commands and expected outputs to local and containerized environments for MySQL 9.7 and MariaDB 10.6/10.11.*
- [x] **PR #228**: `fix(rules): adapt command environments and conditions in PostgreSQL, MongoDB, and Cassandra` — *Adapts shell commands and expected outputs for PostgreSQL 16/17/18, MongoDB 7/8, and Cassandra 4.0/4.1/5.0.*
- [x] **PR #230**: `test(e2e): add automated test asserting 0 manual and 0 error checks across all 18 targets in docker` — *Adds automated verification ensuring 100% automation and 0 error checks across all targets in Docker simulation.*
- [x] **PR #232**: `refactor(mysql): eliminate 2>/dev/null error masking from MySQL 8.0 and 8.4 rule specifications` — *Removes error masking redirects and replaces with explicit conditionals across MySQL 8.0, Community 8.4, and Enterprise 8.4 rules.*
- [x] **PR #234**: `refactor(mysql): eliminate 2>/dev/null error masking from MySQL Community 9.7 and Enterprise 9.7 rule specifications` — *Removes error masking redirects across MySQL Community 9.7 and Enterprise 9.7 rule specifications.*
- [x] **PR #236**: `refactor(mariadb): eliminate 2>/dev/null error masking from MariaDB 10.6 and 10.11 rule specifications` — *Removes error masking redirects across MariaDB 10.6 and 10.11 rule specifications.*
- [x] **PR #238**: `refactor(postgresql): eliminate 2>/dev/null error masking from PostgreSQL 16, 17, and 18 rule specifications` — *Removes error masking redirects across PostgreSQL 16, 17, and 18 rule specifications.*
- [x] **PR #240**: `refactor(mongodb): eliminate 2>/dev/null error masking from MongoDB 7 and 8 rule specifications` — *Removes error masking redirects across MongoDB 7 and 8 rule specifications.*
- [x] **PR #242**: `refactor(cassandra): eliminate 2>/dev/null error masking from Cassandra 4.0, 4.1, and 5.0 rule specifications` — *Removes error masking redirects across Cassandra 4.0, 4.1, and 5.0 rule specifications.*
- [x] **PR #244**: `refactor(rhel): eliminate 2>/dev/null error masking from RHEL 8, 9, and 10 rule specifications` — *Removes error masking redirects across RHEL 8, 9, and 10 rule specifications.*
- [x] **PR #246**: `refactor(mysql80): eliminate 2>/dev/null error masking from MySQL 8.0 audit engine` — *Removes error masking redirects from audit_cis_mysql_80.py.*
- [x] **PR #248**: `refactor(mysql84): eliminate 2>/dev/null error masking from MySQL Community 8.4 audit engine` — *Removes error masking redirects from audit_cis_mysql_community_84.py.*
- [x] **PR #250**: `refactor(mysql84): eliminate 2>/dev/null error masking from MySQL Enterprise 8.4 audit engine` — *Removes error masking redirects from audit_cis_mysql_enterprise_84.py.*
- [x] **PR #252**: `refactor(mysql97): eliminate 2>/dev/null error masking from MySQL Community 9.7 audit engine` — *Removes error masking redirects from audit_cis_mysql_community_97.py.*
- [x] **PR #254**: `refactor(mysql97): eliminate 2>/dev/null error masking from MySQL Enterprise 9.7 audit engine` — *Removes error masking redirects from audit_cis_mysql_enterprise_97.py.*
- [x] **PR #256**: `refactor(mariadb): deduplicate execution context and add sys import in MariaDB 10.6 audit engine` — *Deduplicates execution context functions in audit_cis_mariadb_106.py.*
- [x] **PR #258**: `refactor(mariadb106): eliminate 2>/dev/null in recommendation templates in MariaDB 10.6 audit engine` — *Removes error masking redirects from recommendations in audit_cis_mariadb_106.py.*
- [x] **PR #260**: `refactor(mariadb106): eliminate 2>/dev/null in execution commands in MariaDB 10.6 audit engine` — *Removes error masking redirects from execution functions in audit_cis_mariadb_106.py.*
- [x] **PR #262**: `refactor(mariadb): deduplicate execution context and add sys import in MariaDB 10.11 audit engine` — *Deduplicates execution context functions in audit_cis_mariadb_1011.py.*
- [x] **PR #264**: `refactor(mariadb1011): eliminate 2>/dev/null in recommendation templates in MariaDB 10.11 audit engine` — *Removes error masking redirects from recommendations in audit_cis_mariadb_1011.py.*
- [x] **PR #266**: `refactor(mariadb1011): eliminate 2>/dev/null in execution commands in MariaDB 10.11 audit engine` — *Removes error masking redirects from execution functions in audit_cis_mariadb_1011.py.*
- [x] **PR #268**: `refactor(postgresql): eliminate 2>/dev/null error masking in PostgreSQL 16 and 17 audit engines` — *Removes error masking redirects from audit_cis_postgresql_16.py and audit_cis_postgresql_17.py.*
- [x] **PR #270**: `refactor(engine): eliminate 2>/dev/null error masking in PostgreSQL 18 and MongoDB audit engines` — *Removes error masking redirects from audit_cis_postgresql_18.py, audit_cis_mongodb_7.py, and audit_cis_mongodb_8.py.*
- [x] **PR #272**: `refactor(cassandra): eliminate 2>/dev/null error masking in Cassandra 4.0 and 4.1 audit engines` — *Removes error masking redirects from audit_cis_cassandra_40.py and audit_cis_cassandra_41.py.*
- [x] **PR #274**: `refactor(engine): eliminate 2>/dev/null error masking in Cassandra 5.0 and RHEL audit engines` — *Removes error masking redirects from audit_cis_cassandra_50.py, audit_cis_rhel_8.py, audit_cis_rhel_9.py, and audit_cis_rhel_10.py.*
- [x] **PR #276**: `release(v2.4.2): eliminate 2>/dev/null error masking, enhance engine diagnostics & update roadmap` — *Released v2.4.2, synchronized Phase 15 in ROADMAP.md and POTENTIAL_ISSUES.md.*
- [x] **PR #278**: `fix(rules): restore authentic CIS manual assessment status in MySQL 8.0 (Part 1 - Cat 1 to 2)` — *Restored authentic CIS Benchmark v1.5.0 manual status for Category 1 and 2 in rules/mysql_80.json.*
- [x] **PR #280**: `fix(rules): restore authentic CIS manual assessment status in MySQL 8.0 (Part 2 - Cat 4 to 10)` — *Restored authentic CIS Benchmark v1.5.0 manual status for Category 4 to 10 in rules/mysql_80.json (45 Automated, 25 Manual).*
- [x] **PR #282**: `fix(rules): restore authentic CIS manual assessment status in MySQL Community 8.4 (Part 1 - Cat 1 to 3)` — *Restored authentic CIS Benchmark v1.1.0 manual status for Category 1 to 3 in rules/mysql_community_84.json.*
- [x] **PR #284**: `fix(rules): restore authentic CIS manual assessment status in MySQL Community 8.4 (Part 2 - Cat 4 to 10)` — *Restored authentic CIS Benchmark v1.1.0 manual status for Category 4 to 10 in rules/mysql_community_84.json (48 Automated, 31 Manual).*
- [x] **PR #286**: `fix(rules): restore authentic CIS manual assessment status in MySQL Enterprise 8.4 (Part 1 - Cat 1 to 3)` — *Restored authentic CIS Benchmark v1.1.0 manual status for Category 1 to 3 in rules/mysql_enterprise_84.json.*
- [x] **PR #288**: `fix(rules): restore authentic CIS manual assessment status in MySQL Enterprise 8.4 (Part 2 - Cat 4 to 10)` — *Restored authentic CIS Benchmark v1.1.0 manual status for Category 4 to 10 in rules/mysql_enterprise_84.json (44 Automated, 26 Manual).*
- [x] **PR #290**: `fix(rules): restore authentic CIS manual assessment status in MySQL Community 9.7` — *Restored authentic CIS Benchmark v1.0.0 manual status in rules/mysql_community_97.json (45 Automated, 25 Manual).*
- [x] **PR #292**: `fix(rules): restore authentic CIS manual assessment status in MySQL Enterprise 9.7 (Part 1 - Cat 1 to 3)` — *Restored authentic CIS Benchmark v1.0.0 manual status for Category 1 to 3 in rules/mysql_enterprise_97.json.*
- [x] **PR #294**: `fix(rules): restore authentic CIS manual assessment status in MySQL Enterprise 9.7 (Part 2 - Cat 4 to 10)` — *Restored authentic CIS Benchmark v1.0.0 manual status for Category 4 to 10 in rules/mysql_enterprise_97.json (44 Automated, 26 Manual).*
- [x] **PR #296**: `fix(rules): restore authentic CIS manual assessment status in MariaDB 10.6 (Part 1 - Cat 1 to 3)` — *Restored authentic CIS Benchmark v1.1.0 manual status for Category 1 to 3 in rules/mariadb_106.json.*
- [x] **PR #298**: `fix(rules): restore authentic CIS manual assessment status in MariaDB 10.6 (Part 2 - Cat 4 to 9)` — *Restored authentic CIS Benchmark v1.1.0 manual status for Category 4 to 9 in rules/mariadb_106.json (45 Automated, 29 Manual).*
- [x] **PR #300**: `fix(rules): restore authentic CIS manual assessment status in MariaDB 10.11 (Part 1 - Cat 1 to 3)` — *Restored authentic CIS Benchmark v1.0.0 manual status for Category 1 to 3 in rules/mariadb_1011.json.*
- [x] **PR #302**: `fix(rules): restore authentic CIS manual assessment status in MariaDB 10.11 (Part 2 - Cat 4 to 9)` — *Restored authentic CIS Benchmark v1.0.0 manual status for Category 4 to 9 in rules/mariadb_1011.json (45 Automated, 30 Manual).*
- [x] **PR #304**: `fix(rules): restore authentic CIS manual assessment status in PostgreSQL 16 (Part 1 - Cat 1 to 4)` — *Restored authentic CIS Benchmark v1.1.0 manual status for Category 1 to 4 in rules/postgresql_16.json.*
- [x] **PR #306**: `fix(rules): restore authentic CIS manual assessment status in PostgreSQL 16 (Part 2 - Cat 5 to 8)` — *Restored authentic CIS Benchmark v1.1.0 manual status for Category 5 to 8 in rules/postgresql_16.json (42 Automated, 29 Manual).*
- [x] **PR #308**: `fix(rules): restore authentic CIS manual assessment status in PostgreSQL 17 (Part 1 - Cat 1 to 4)` — *Restored authentic CIS Benchmark v1.1.0 manual status for Category 1 to 4 in rules/postgresql_17.json.*
- [x] **PR #310**: `fix(rules): restore authentic CIS manual assessment status in PostgreSQL 17 (Part 2 - Cat 5 to 8)` — *Restored authentic CIS Benchmark v1.1.0 manual status for Category 5 to 8 in rules/postgresql_17.json (43 Automated, 28 Manual).*
- [x] **PR #312**: `fix(rules): restore authentic CIS manual assessment status in PostgreSQL 18 (Part 1 - Cat 1 to 4)` — *Restored authentic CIS Benchmark v1.0.0 manual status for Category 1 to 4 in rules/postgresql_18.json.*
- [x] **PR #314**: `fix(rules): restore authentic CIS manual assessment status in PostgreSQL 18 (Part 2 - Cat 5 to 8)` — *Restored authentic CIS Benchmark v1.0.0 manual status for Category 5 to 8 in rules/postgresql_18.json (43 Automated, 28 Manual).*
- [x] **PR #316**: `fix(rules): restore authentic CIS manual assessment status in MongoDB 7 & 8` — *Restored authentic CIS Benchmark manual status in rules/mongodb_7.json and rules/mongodb_8.json (12 Automated, 11 Manual each).*
- [x] **PR #318**: `fix(rules): restore authentic CIS manual assessment status in Cassandra 4.0 & 4.1` — *Restored authentic CIS Benchmark manual status in rules/cassandra_40.json and rules/cassandra_41.json (12 Automated, 8 Manual each).*
- [x] **PR #320**: `fix(rules): restore authentic CIS manual assessment status in Cassandra 5.0` — *Restored authentic CIS Benchmark manual status in rules/cassandra_50.json (12 Automated, 8 Manual).*
- [x] **PR #322**: `test: update unit tests to validate authentic CIS spec distribution and zero command errors` — *Updated test suite to validate authentic CIS spec distribution (564 Automated, 323 Manual) and 0 command errors across all 18 targets.*