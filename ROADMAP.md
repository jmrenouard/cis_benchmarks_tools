# 🗺️ CIS Benchmarks Tools - Strategic Roadmap & Backlog (v1.8.0)

This document outlines the strategic roadmap, architecture principles, phase-level milestones, and task-level execution status for the CIS Benchmarks Tools suite.

---

## 🔒 Mandatory Architecture & Release Standards

> [!IMPORTANT]
> 1. **Python Standard Library ONLY (PSL ONLY)**: All Python scripts (audit engine, `audit_cis_*.py` audit modules, unified CLI `audit_cis.py`, report generators, pre-commit scripts, unit tests, E2E runners) MUST use **EXCLUSIVELY the standard Python 3 library**. No external dependencies (`jinja2`, `yaml`, `requests`) are permitted.
> 2. **Automated Documentation Synchronization**: For every Python modification, the product version (`VERSION`), `ROADMAP.md`, and `POTENTIAL_ISSUES.md` are **automatically updated and validated**.
> 3. **Git Release Lifecycle & PR Diff Size Limit**: Version numbers MUST be embedded in Branch names (`feat/vX.Y.Z-...`), Issue titles (`[vX.Y.Z] ...`), and PR titles (`[vX.Y.Z] ...`). Total PR diff size MUST be **< 15,000 characters** (`git diff main...HEAD | wc -c` < 15000) to ensure review bot compatibility (Sourcery AI). Large benchmark additions must be split into atomic sub-15K PRs.
> 4. **Multi-Language Documentation**: `README.md` (English) and `README_fr.md` (French) MUST remain strictly synchronized 1:1.

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

## 💬 GitHub PR Reviews & Feedback Summary

| PR ID | Target Version | Feature / Component | Status | Reviewer Feedback Summary |
| :---: | :---: | :--- | :---: | :--- |
| **PR #1** | `v1.5.1` | Baseline Automation Framework | `Merged ✅` | Implemented initial CIS benchmarks automation tool and check framework. |
| **PR #17 – #26** | `v1.6.0` | Initial Database Audit Implementations | `Merged ✅` | Added 15 database benchmark scripts. Review bots flagged large diff size (> 150K chars). |
| **PR #106** | `v1.7.1` | PR Diff Size Limit & Workspace Rules | `Merged ✅` | Enforced strict < 15K diff character limit and atomic PR splitting rules in `AGENTS.md`. |
| **PR #107** | `v1.8.0` | Centralized HTML Report Templates | `Merged ✅` | Extracted report templates into `templates/report_template.html` with PSL loader. |
