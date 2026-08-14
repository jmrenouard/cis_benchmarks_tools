# 🗺️ CIS Benchmarks Tools - Strategic Roadmap & Backlog (v2.0.0)

This document outlines the strategic roadmap, architecture principles, phase-level milestones, and task-level execution status for the CIS Benchmarks Tools suite.

---

## 🔒 Governance & Core Standards

> [!NOTE]
> All development, git release lifecycles, PR size limits (< 15K diff chars), and Python Standard Library (PSL ONLY) enforcement rules strictly follow workspace governance defined in [.agents/AGENTS.md](file:///.agents/AGENTS.md).

---

## 📊 Executive Progress Dashboard (Phase Level)

| Phase | Milestone Title | Target Version | Status | Tasks | Progress |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Phase 1** | Consolidation & Baseline Standardization | `v1.0.0` | `Completed ✅` | 5/5 | 100% |
| **Phase 2** | Unified Audit Engine & PSL Modularization | `v1.2.5` | `Completed ✅` | 13/13 | 100% |
| **Phase 3** | Linux System Extensions, Multi-Language & Security | `v1.5.0` | `Completed ✅` | 5/5 | 100% |
| **Phase 4** | Multi-Format Exporters, E2E Testing & CI/CD Pipeline | `v1.6.0` | `Completed ✅` | 7/7 | 100% |
| **Phase 5** | Rule Spec Externalization & Offline SVG Charts Engine | `v1.7.0` | `Completed ✅` | 5/5 | 100% |
| **Phase 6** | PR Diff Size Limits & Centralized HTML Templates | `v1.8.0` | `Completed ✅` | 4/4 | 100% |
| **Phase 7** | Dual Local/SSH Modes & Database Connection Parameters | `v1.9.0` | `Completed ✅` | 5/5 | 100% |
| **Phase 8** | Advanced Formatting, Rule Exclusions & Visual UI Validation | `v2.0.0` | `Completed ✅` | 7/7 | 100% |
| **Phase 9** | Verification Commands & Remediation Procedures in Reports | `v2.1.0` | `Completed ✅` | 4/4 | 100% |
| **Phase 10** | MariaDB Zero-Error Engine, Docker Auto-Routing & Manual Automation | `v2.2.0` | `Completed ✅` | 5/5 | 100% |
| **Phase 11** | Universal Product Hardening, Docker Auto-Routing & Info Maximization | `v2.3.0` | `Completed ✅` | 6/6 | 100% |

---

## 📅 Detailed Milestones & Task Execution Status

### Phase 1: Consolidation & Baseline Standardization (`Completed ✅ - v1.0.0`)
**Summary**: Establish initial database audit coverage across 15 database benchmarks with standardized Docker testing environments and HTML reports.

#### 1.1 Multi-Database Audit Scripts & Docker Environments
- [x] **15 Database Benchmarks Coverage**: Implement standalone audit scripts for MariaDB (10.6/10.11), MySQL (8.0/8.4/9.7), PostgreSQL (16/17/18), MongoDB (7/8), and Cassandra (4.0/4.1/5.0).
- [x] **Standardized Testing Containers**: Create Dockerfiles and startup scripts (`docker/Dockerfile_*`, `scripts/start_*.sh`) for isolated local container verification.
- [x] **Unified Testing Interface**: Build Makefile orchestration targets (`make test-all`, `make test-<target>`) for single-command E2E execution.
- [x] **Initial Audit Reports Suite**: Generate and commit baseline HTML audit reports in `reports/`.
- [x] **Reference Specification Storage**: Integrate 22 reference Markdown benchmark specifications into `CIS_DATA/`.

---

### Phase 2: Unified Audit Engine, PSL Modularization & Directory Structure (`Completed ✅ - v1.2.5`)
**Summary**: Consolidate individual audit scripts into a single unified CLI engine (`audit_cis.py`), automated pre-commit quality checks, and clean repository layout.

#### 2.1 Unified Audit CLI & Programmatic API
- [x] **Centralized CLI Execution**: Build `audit_cis.py` with CLI flags (`--target`, `--all`, `--auto-detect`, `--list-targets`, `--version`).
- [x] **Native Python API Interface**: Expose `run_single_audit()`, `list_targets()`, `get_target_info()`, and `TARGET_MAP` for external Python imports.
- [x] **Synthetic Statistics Engine**: Compute global compliance scores across 887 audit controls across 18 targets.
- [x] **Dynamic Directory Manager**: Automatically create output directories for HTML and JSON reports.
- [x] **100% PSL Compliance**: Guarantee zero external pip package dependencies (`pip free`).

#### 2.2 Pre-Commit Quality & Validation Routine
- [x] **Automated Script Bundler**: Build `scripts/bundle_audit_cis.py` to auto-concatenate `audit_cis.py` on version changes.
- [x] **Python Syntax Checker**: Validate compilation (`py_compile`) for all project scripts.
- [x] **AST PSL Import Sentinel**: Verify AST nodes to block non-standard library imports.
- [x] **Shell Syntax Checker**: Validate syntax (`bash -n`) for all shell scripts.
- [x] **Directory & File Integrity Verifier**: Validate presence and non-empty size (>1 KB) of `reports/`, `docker/`, `scripts/`, `CIS_DATA/`, and `rules/`.
- [x] **Executable Permissions Sentinel**: Verify executable bit (`chmod +x`) on CLI scripts.

#### 2.3 Structured Directory Layout
- [x] **Dedicated Reports Directory**: Group all HTML/JSON audit output files in `reports/`.
- [x] **Dedicated Docker Directory**: Group all 16 container build files in `docker/`.

---

### Phase 3: Linux System Extensions, Multi-Language & Security (`Completed ✅ - v1.5.0`)
**Summary**: Extend audit capabilities to RHEL Linux operating systems, implement bilingual (i18n) report generation, and fix command injection vulnerabilities.

#### 3.1 Linux Operating System Audit Modules
- [x] **RHEL 8 / 9 / 10 Benchmark Engines**: Implement `audit_cis_rhel_8.py`, `audit_cis_rhel_9.py`, and `audit_cis_rhel_10.py`.
- [x] **SSH Remote Server Auditing**: Support native `--mode {local,ssh}` and `--remote user@hostname` execution over SSH.

#### 3.2 Multi-Language (i18n) Support
- [x] **Bilingual Report Generator**: Support `--lang {en,fr}` for CLI output and HTML audit reports.
- [x] **Synchronized Documentation**: Maintain 1:1 parity between `README.md` (English) and `README_fr.md` (French).

#### 3.3 Subprocess Security Hardening
- [x] **Command Injection Mitigation**: Migrate all `subprocess` execution calls to strict parameter lists (`shell=False`).

---

### Phase 4: Multi-Format Exporters, E2E Testing & CI/CD Pipeline (`Completed ✅ - v1.6.0`)
**Summary**: Add structured export formats (JSON, STIG JUnit XML, TXT), automated unit tests, and GitHub Actions CI/CD.

#### 4.1 Multi-Format Exporters
- [x] **Structured JSON Exporters**: Export full audit metadata and control results to machine-readable JSON.
- [x] **STIG / JUnit XML Exporters**: Export STIG/JUnit XML format for enterprise SIEM/CI integration.
- [x] **Plain-Text Summary Exporters**: Generate CLI text audit summaries.
- [x] **Responsive HTML Reports**: Generate self-contained HTML reports.

#### 4.2 Automated Testing & CI Pipeline
- [x] **GitHub Actions Workflow**: Implement `.github/workflows/ci.yml` for automated PR checking.
- [x] **PSL Unit Test Suite**: Build `tests/test_evaluate_condition.py` (14 unit tests).
- [x] **E2E Test Runner**: Build `scripts/run_e2e_tests.py` (`make test-e2e`).

---

### Phase 5: Rule Spec Externalization & Offline SVG Charts Engine (`Completed ✅ - v1.7.0`)
**Summary**: Externalize audit recommendations into JSON files in `rules/` and replace external JS chart libraries with 100% pure inline SVG PSL charts.

#### 5.1 External Rule Specs Directory
- [x] **JSON Specification Externalization**: Extract `RECOMMENDATIONS_DATA` into 18 JSON files (`rules/mariadb_106.json`, etc.).
- [x] **Dynamic Spec Loader**: Implement `load_recommendations()` with embedded inline fallback.

#### 5.2 Pure Inline SVG Chart Engine
- [x] **Pure SVG Donut Chart**: Build `build_inline_svg_donut_chart()` in Python PSL (zero JS).
- [x] **Pure SVG Category Bar Chart**: Build `build_inline_svg_category_chart()` in Python PSL.
- [x] **100% Offline Compatibility**: Work 100% offline without CDN dependencies (Chart.js removed).

---

### Phase 6: PR Diff Size Limit & Centralized HTML Templates (`Completed ✅ - v1.8.0`)
**Summary**: Enforce PR diff character limits (<15K chars) to avoid review bot blocking and centralize HTML report templates into common files.

#### 6.1 PR Diff Character Size Limits (< 15,000 chars)
- [x] **PR Size Limit Enforcement**: Mandate strict 15,000 diff character limit per PR and atomic PR splitting in `.agents/AGENTS.md` & `03_execution_rules.md`.
- [x] **Pre-PR Character Verification**: Automate diff size verification via `git diff main...HEAD | wc -c` < 15000.

#### 6.2 Centralized HTML Report Templates
- [x] **Common Template Files**: Centralize HTML templates in `templates/report_template.html` and `templates/category_report_template.html`.
- [x] **Dynamic Template Loaders**: Implement `load_html_template()` with PSL inline fallbacks across all 18 audit scripts and `audit_cis.py`.

---

### Phase 7: Dual Local/SSH Modes & Database Connection Parameters (`Completed ✅ - v1.9.0`)
**Summary**: Standardize Local & SSH Remote execution parameters (`--mode`, `--remote`, `--ssh-port`, `--ssh-key`, `--sudo`) and database connection options (`--db-host`, `--db-port`, `--db-user`, `--db-password`) across all audit scripts, and validate both modes in the E2E test runner.

#### 7.1 Local & SSH Mode CLI Standardisation
- [x] **SSH Connection Parameters**: Standardize `--mode {local,ssh}`, `--remote / --ssh`, `--ssh-port`, `--ssh-key`, and `--sudo` across all 18 audit scripts.
- [x] **Database Connection Options**: Add `--db-host / --host`, `--db-port / --port`, `--db-user / --user`, and `--db-password / --password` CLI arguments to all audit scripts.
- [x] **CLI Option Propagation**: Update `audit_cis.py` to forward database and SSH options to targeted audit modules.

#### 7.2 E2E Dual-Mode Testing Suite
- [x] **Dual Mode E2E Test Runner**: Update `scripts/run_e2e_tests.py` to execute and validate report generation for BOTH Local Mode and SSH Remote Mode.
- [x] **100% PSL Compliance**: Guarantee OpenSSH command execution (`ssh -o BatchMode=yes`) using standard Python `subprocess` (zero pip packages).

---

### Phase 8: Advanced Formatting, Rule Exclusions & Visual UI Validation (`Completed ✅ - v2.0.0`)
**Summary**: Enhance text report outputs, add thematic security metrics, upgrade HTML templates, sanitize rule commands, expand check automation, support rule exclusions, and automate visual UI browser testing.

#### 8.1 Plain-Text Reporting & Thematic Metrics
- [x] **1° Enhanced Plain-Text ASCII Summary Tables**: Upgrade `--format txt` output to generate formatted ASCII summary tables with category scores, PASS/FAIL ratios, and clear alignment.
- [x] **2° Thematic Security Domain Metrics**: Group compliance metrics by security domain (Authentication, Access Control, Network Isolation, TLS/Encryption, Logging & Auditing).

#### 8.2 HTML Template Polish & Rule Exclusion Engine
- [x] **3° Aesthetic & Functional HTML Template Upgrade**: Enhance `templates/report_template.html` with modern UI, responsive alignment, dark mode toggle, visual icons, and zero layout overflow.
- [x] **6° Rule Exclusion Engine (`--exclude-rules` / `--skip-rule`)**: Implement CLI flags and JSON config support to skip or exclude specific control IDs or categories during audits.

#### 8.3 Command Verification, Automation Expansion & Visual Browser Testing
- [x] **4° Rule Command Validation & Execution Safety**: Enhance `rules/*.json` specifications to validate test procedure shell syntax and enforce command execution safety.
- [x] **5° Check Automation Expansion (Minimize Manual Checks)**: Convert legacy `Manual` inspection items into automated database queries and system command verifications.
- [x] **7° Automated Headless Browser Visual UI Validation**: Integrate automated browser testing (headless Chromium visual QA) in E2E tests to detect layout regressions (no text overflow, no misaligned tables, no missing icons).

#### 8.4 E2E Test Failures Remediation & Container Hardening (`Completed ✅ - v2.0.0`)
- [x] **E2E Audit Reports Analysis & Failure Registry**: Generated `reports/analyse_tests_e2e.md` detailing all FAIL, ERROR, and MANUAL controls across 19 benchmark targets.
- [x] **Container Hardening & Startup Script Proposals**: Formulated `remediation_proposal.md` to update Dockerfiles, startup scripts (`scripts/start_*.sh`), and container-aware audit check logic.
- [x] **Dedicated Local vs SSH Remote Mode E2E Reports**: Created `reports/analyse_tests_e2e_local.md` and `reports/analyse_tests_e2e_ssh.md` for mode-specific compliance analysis.

---

### Phase 9: Verification Commands & Remediation Procedures in Reports (`Completed ✅ - v2.1.0`)
**Summary**: Systematically include audit verification commands (`test_procedure` / `audit`) and remediation procedures (`remediation`) across all output formats (HTML, TXT, JSON, XML) and CLI reports for all 18 benchmark products.

#### 9.1 Multi-Format Exporters & Report Enhancements
- [x] **Multi-Format Test Command Output**: Render audit verification commands (`test_procedure` / `audit`) across TXT, XML, JSON, and HTML reports.
- [x] **Unrestricted Remediation Procedures**: Render remediation instructions (`remediation`) for all controls across TXT, XML, JSON, and HTML report formats regardless of compliance status.
- [x] **RHEL Report Parity**: Update RHEL 8, 9, and 10 HTML report templates and check result dictionaries with `Commande de test` and `Procédure de remédiation` columns.
- [x] **Automated Engine & Reports Regeneration**: Update `audit_cis.py` engine bundler and regenerate report outputs across all 18 targets.

---

## 💬 GitHub PR Reviews & Feedback Summary

| PR ID | Target Version | Feature / Component | Status | Reviewer Feedback Summary |
| :---: | :---: | :--- | :---: | :--- |
| **PR #1** | `v1.5.1` | Baseline Automation Framework | `Merged ✅` | Implemented initial CIS benchmarks automation tool and check framework. |
| **PR #17 – #26** | `v1.6.0` | Initial Database Audit Implementations | `Merged ✅` | Added 15 database benchmark scripts. Review bots flagged large diff size (> 150K chars). |
| **PR #106** | `v1.7.1` | PR Diff Size Limit & Workspace Rules | `Merged ✅` | Enforced strict < 15K diff character limit and atomic PR splitting rules in `AGENTS.md`. |
| **PR #107** | `v1.8.0` | Centralized HTML Report Templates | `Merged ✅` | Extracted report templates into `templates/report_template.html` with PSL loader. |
| **PR #108** | `v1.9.0` | Dual Local/SSH Modes & E2E Validation | `Merged ✅` | Standardized SSH & DB options across all scripts and updated E2E runner for dual-mode tests. |
| **PR #109** | `v2.0.0` | Phase 8 Advanced Formatting & Exclusions | `Merged ✅` | Enhanced TXT ASCII tables, thematic metrics, HTML dark mode, rule exclusions, and E2E visual QA. |
| **PR #110** | `v2.1.0` | Phase 9 Verification Commands & Remediations | `Merged ✅` | Added verification commands and remediation procedures across all test results & export formats. |


### 🤖 Sourcery AI Code Reviews & Architectural Feedback
| PR | Titre / Thématique | Évaluation Sourcery AI & Résolution |
|---|---|---|
| **PR #70** | docs: Format Phase 2 items in ROADMAP.md with completed task checkboxes [x] | This PR bumps the project version to v1.2.4 and updates documentation to reflect completed Phase 2 roadmap items using Markdown task checkboxes, while aligning the potential issues log and audit engine version metadata with the new release. |
| **PR #72** | docs: Synchronize VERSION v1.2.4 and format ROADMAP.md Phase 2 checkboxes [x] | This PR bumps the project version to v1.2.4 across code/docs and adjusts ROADMAP Phase 2 checkbox formatting for consistency. |
| **PR #74** | docs: Finalize VERSION v1.2.4 sync and update ROADMAP.md formatting | Synchronizes the project version to v1.2.4 in the main audit engine and version file, aligning code metadata with the new release tag and related documentation updates. |
| **PR #76** | docs: Format all Phase 2 items in ROADMAP.md with completed task checkboxes [x] | Updates roadmap and related docs to mark Phase 2 items as completed using checkbox syntax and bumps the project version from 1.2.3 to 1.2.5 across documentation and code metadata. |
| **PR #78** | docs: Finalize ROADMAP.md Phase 2 formatting and VERSION v1.2.5 sync | Synchronizes the documented and code-level version to v1.2.5 and updates ROADMAP Phase 2 task formatting to reflect completed work. |
| **PR #80** | sec: Migrate subprocess.run to parameter lists and eliminate shell=True (v1.3.0) | This PR removes all uses of subprocess.run with shell=True by migrating to explicit argument lists and updates documentation and version metadata to v1.3.0, including strengthening the report generation script to use structured Docker commands and safer report copying. |
| **PR #82** | sec: Synchronize VERSION v1.3.0 across audit_cis.py and documentation | Synchronizes the documented and code-defined VERSION of the CIS audit engine to v1.3.0 across the main script and VERSION file. |
| **PR #83** | sec: Commit VERSION v1.3.0 and bundled audit_cis.py for Subprocess Security Migration | Bumps the unified CIS audit engine and repository VERSION to v1.3.0 to align with the subprocess security migration bundle, without functional code changes beyond the version identifiers. |
| **PR #84** | sec: [v1.3.0] Migrate subprocess.run to parameter lists and embed versioning in Branch & PR | Migrates all Python subprocess.run invocations to use explicit argument lists with shell=False for safer execution, and introduces mandatory semantic version embedding (v1.3.0) in VERSION, audit_cis.py, workflow docs, and the contributor process (branch/issue/PR naming plus ROADM |
| **PR #85** | sec: [v1.3.0] Synchronize VERSION file to v1.3.0 and validate 7-step pre-commit routine | Bumps the project version from 1.2.3 to 1.3.0 in the main audit script and the VERSION metadata file to keep runtime and repository versioning in sync. |
| **PR #86** | sec: [v1.3.0] Update VERSION to 1.3.0 and finalize release | Updates the project to release version 1.3.0 by bumping internal version constants and metadata. |
| **PR #88** | feat: [v1.4.0] Implement Red Hat Enterprise Linux 8, 9, 10 CIS and STIG Audit Extension | Adds new RHEL 8/9/10 CIS/STIG audit modules with local and SSH remote execution, wires them into the unified audit engine and bundler, secures subprocess usage (no shell=True), and updates roadmap/potential issues documentation and version metadata to v1.4.0. |
| **PR #90** | sec: [v1.4.1] Migrate all subprocess calls to parameter lists and eliminate shell=True | Migrates all Python subprocess usage to argument-list form without shell=True, refactors the report generation helper script around a safer Docker execution flow, and bumps the suite version/docs to v1.4.1 while updating security and roadmap documentation accordingly. |
| **PR #92** | docs: [v1.4.1] Rewrite README.md in English and update repository documentation | README is rewritten in English to describe the v1.4.1 architecture, unified audit_cis.py CLI, supported benchmarks and controls, remote SSH auditing, repository layout, and security/PSL guarantees; audit_cis.py and VERSION are bumped to v1.4.1 to align docs and code. |
| **PR #94** | docs: [v1.4.2] Finalize English README.md and repository documentation | Documentation is updated to describe the v1.4.2 architecture, unified audit CLI, expanded benchmark coverage (including RHEL/STIG targets), security/PSL constraints, and repository structure, along with a minor version bump in the unified CLI engine and VERSION metadata. |
| **PR #96** | feat: [v1.5.0] Add Multi-Language i18n support and synchronized README_fr.md | Implements multi-language (English/French) i18n support for the unified CIS audit CLI and all HTML report generators, updates documentation and process rules to English with a synchronized French README, and bumps the suite version to v1.5.0 while preserving PSL-only architecture |
| **PR #99** | sec: [v1.4.3] Update POTENTIAL_ISSUES.md moving subprocess shell=Fals… | This PR updates documentation of the potential issues backlog to reflect work completed up to v1.4.2, including the subprocess shell=False migration, and bumps the unified audit engine version to v1.4.3. |
| **PR #103** | feat: [v1.7.0] Externalize Audit Control Rules into rules/ Directory & Implement Offline SVG Charts Engine | This PR externalizes audit control rule specifications into JSON files under a new rules/ directory and replaces all Chart.js-based HTML report charts with a fully offline, PSL-only inline SVG engine, while simplifying generate_html_report signatures and tightening pre-commit val |
| **PR #105** | feat: [v1.7.0] Synchronize PR Reviews and Feedback into ROADMAP.md & POTENTIAL_ISSUES.md | Adds a PSL-only automation script to synchronize GitHub PR reviews and resolution history into ROADMAP.md and POTENTIAL_ISSUES.md, and updates MariaDB CIS audit reports and roadmap/backlog documentation to reflect current PR feedback and compliance status. |
| **PR #108** | docs: Update Multi-Format Audit Reports for Dual-Mode E2E Runs | This PR refreshes and standardizes multi-format CIS audit reports across DB targets, enhancing the HTML UI (dark mode, inline SVG charts, updated metrics/text) for both local and SSH modes while updating SSH invocation options and regenerating associated JSON/TXT report artefacts |
| **PR #110** | feat(script): add GitHub API PR lifecycle script | Adds a standalone Python script that automates creating a set of pull requests for predefined branches and then posts a resolution comment and closes GitHub Issue #109 via the GitHub REST API. |
| **PR #112** | docs(rules): enforce mandatory issue creation, commenting & closing | The PR updates the agent workflow documentation to make GitHub issue lifecycle (creation, resolution commenting, and closing) a mandatory part of the process when working with pull requests. |
| **PR #114** | fix(engine): ensure command execution errors take precedence over manual status | Refactors perform_checks() across all audit scripts to prioritize command execution errors over manual statuses, standardizes output formatting to avoid unterminated f-strings, and updates the HTML report and helper scripts accordingly. |
| **PR #116** | feat(core): implement unified detect_execution_context engine | Adds a unified detect_execution_context() helper to all audit scripts, introduces a dedicated unit test suite for execution context classification, and adds an integration script to propagate the helper across audit files. |
| **PR #118** | feat(reports): introduce distinct Command Error test status in reports | Adds a distinct Command Error metric to HTML reports and standardizes related error messaging across audit scripts, including a helper script to propagate these changes. |
| **PR #120** | fix(mysql): resolve error_count in HTML reports and regenerate MySQL reports | Bind the error_count variable correctly in all audit scripts and regenerate MySQL HTML reports so summary widgets, charts, and section breakdowns accurately reflect command errors vs manual checks and improve error messaging for failed MySQL commands. |
| **PR #122** | fix(html): fix title palindrome duplication and redundant version badges in reports | Aligns all HTML audit reports and generators to use clear product-specific titles, contextual badges, and consistent version metadata, while cleaning up duplicated titles and redundant badges and introducing an execution context parameter. |
| **PR #124** | fix(rules): sanitize natural text test procedures and implement execution safety guard | Adds a shell command validation guard to all CIS audit engines and sanitizes natural-language test procedures in rules JSON, updating reports and scripts to treat human descriptions as manual checks rather than executable commands. |
| **PR #126** | fix(rhel): fix datetime import and regenerate all 18 clean reports | Fixes datetime import usage in RHEL CIS audit scripts and regenerates all 18 HTML audit reports with updated metadata, timestamps, and in one case (PostgreSQL 18) synchronized content reflecting a new run’s results and command outputs. |
| **PR #128** | feat(diagnostics): eliminate 2>/dev/null to preserve complete stderr diagnostic telemetry | This PR removes all uses of `2>/dev/null` from the CIS benchmark rule specifications so that stderr is no longer suppressed, and regenerates the HTML reports to surface the newly captured diagnostic errors and updated scores. A helper Python script is added to perform the bulk ed |