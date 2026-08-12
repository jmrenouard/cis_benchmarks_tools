# 🗺️ CIS Benchmarks Tools - Strategic Roadmap & Backlog (v1.8.0)

This document outlines the strategic roadmap, architecture principles, and key milestones for the CIS Benchmarks Tools suite.

---

## 🔒 Mandatory Architecture & Release Standards

> [!IMPORTANT]
> 1. **Python Standard Library ONLY (PSL ONLY)**: All Python scripts (audit engine, `audit_cis_*.py` audit modules, unified CLI `audit_cis.py`, report generators, pre-commit scripts, unit tests, E2E runners) MUST use **EXCLUSIVELY the standard Python 3 library**. No external dependencies (`jinja2`, `yaml`, `requests`) are permitted.
> 2. **Automated Documentation Synchronization**: For every Python modification, the product version (`VERSION`), `ROADMAP.md`, and `POTENTIAL_ISSUES.md` are **automatically updated and validated**.
> 3. **Git Release Lifecycle & PR Diff Size Limit**: Version numbers MUST be embedded in Branch names (`feat/vX.Y.Z-...`), Issue titles (`[vX.Y.Z] ...`), and PR titles (`[vX.Y.Z] ...`). Total PR diff size MUST be **< 15,000 characters** (`git diff main...HEAD | wc -c` < 15000) to ensure review bot compatibility (Sourcery AI). Large benchmark additions must be split into atomic sub-15K PRs.
> 4. **Multi-Language Documentation**: `README.md` (English) and `README_fr.md` (French) MUST remain strictly synchronized 1:1.

---

## 📅 Milestones & Feature Phases

### Phase 1: Consolidation & Standardization (Completed ✅)
- [x] Support for 15 database benchmarks (MariaDB 10.6/10.11, MySQL 8.0/8.4/9.7, PostgreSQL 16/17/18, MongoDB 7/8, Cassandra 4.0/4.1/5.0).
- [x] Standardized Dockerfiles and startup scripts (`scripts/start_*.sh`).
- [x] Unified `Makefile` target (`make test-all`).
- [x] 15 HTML audit reports generated and checked into `reports/`.
- [x] Integration of 22 reference Markdown specifications into `CIS_DATA/`.

---

### Phase 2: Unified Audit Engine, PSL Modularization & Directory Structure (Completed ✅ - v1.2.5)

#### 1. Unified Audit Engine (`audit_cis.py`)
- [x] Centralized standalone execution CLI with version management (`python3 audit_cis.py --version`, `--target <target>`, `--all`, `--auto-detect`, `--list-targets`).
- [x] Native Python programmatic API (`from audit_cis import run_single_audit, list_targets, get_target_info, TARGET_MAP`).
- [x] Synthetic summary statistics display (887 audit controls across 18 targets).
- [x] Dynamic report directory creation for output HTML/JSON reports.
- [x] 100% PSL execution engine.

#### 2. Python Pre-Commit Validation Routine (`scripts/pre_commit_checks.py` & `make pre-commit`)
- [x] Automated Python script bundler (`scripts/bundle_audit_cis.py`) concatenating and synchronizing `audit_cis.py` on every commit.
- [x] Automated Python syntax validation (`py_compile`).
- [x] AST compliance verification to block non-PSL imports.
- [x] Shell script syntax validation (`bash -n`).
- [x] Project structure integrity checks (`reports/`, `docker/`, `scripts/`, `CIS_DATA/`) and HTML report size validation (> 1 KB).
- [x] Specification integrity checks for 22 Markdown files in `CIS_DATA/` and execution permission verification (`chmod +x`).

#### 3. Structured Directory Layout
- [x] `reports/`: Dedicated directory grouping all HTML audit reports.
- [x] `docker/`: Dedicated directory grouping all 16 Dockerfiles.
- [x] `scripts/`: Shell startup scripts (`start_*.sh`) and pre-commit validation routines.
- [x] `CIS_DATA/`: Contains all 22 reference Markdown benchmark specifications.

---

### Phase 3: Linux System Extensions, Multi-Language & Security (Completed ✅ - v1.5.0)

#### 1. System & OS Extensions (RHEL 8 / 9 / 10 & STIG)
- [x] Python PSL audit modules for Red Hat Enterprise Linux 8 (`audit_cis_rhel_8.py`), RHEL 9 (`audit_cis_rhel_9.py`), and RHEL 10 (`audit_cis_rhel_10.py`).
- [x] Native local execution and SSH remote server auditing via `--remote user@hostname` (zero external dependencies).

#### 2. Multi-Language Support (i18n) & Synchronized Documentation
- [x] Added `--lang {en,fr}` flag to CLI and HTML audit reports.
- [x] French translation of `README.md` (`README_fr.md`) 100% synchronized.

#### 3. Subprocess Command Injection Prevention (`shell=False`)
- [x] Migrated all system command calls to strict parameter lists (`shell=False`).

---

### Phase 4: Multi-Format Exporters, E2E Testing & CI/CD Pipeline (Completed ✅ - v1.6.0)

#### 1. Multi-Format Exporters (`--format html|json|xml|txt`)
- [x] Structured JSON compliance reports (`json` module).
- [x] STIG / JUnit XML formatted output (`xml.etree.ElementTree` module).
- [x] Plain-text TXT CLI summary logging.
- [x] Self-contained responsive HTML reports in `reports/`.

#### 2. Automated E2E Testing & CI/CD
- [x] GitHub Actions CI/CD pipeline (`.github/workflows/ci.yml`).
- [x] Automated PSL unit test suite (`tests/test_evaluate_condition.py`).
- [x] E2E test runner (`scripts/run_e2e_tests.py` / `make test-e2e`).

---

### Phase 5: Rule Spec Externalization & Offline SVG Charts Engine (Completed ✅ - v1.7.0)

#### 1. External Rule Specs Directory (`rules/*.json`)
- [x] Decoupled audit control specification rules from Python scripts into `rules/` directory (`rules/mariadb_106.json`, `rules/cassandra_40.json`, etc.).
- [x] Dynamic rule loader (`load_recommendations()`) in `audit_cis_*.py` and `audit_cis.py` with inline fallback.

#### 2. 100% Offline Pure Inline SVG Charts Engine
- [x] Self-contained Inline SVG Donut Chart showing global pass/fail ratios and center score percentage (zero JS library dependencies).
- [x] Responsive Category Stacked Bar Charts for visual compliance breakdown.
- [x] 100% Python Standard Library (PSL ONLY) compliance.


### 💬 GitHub PR Reviews & Feedback Summary

- **PR #1 (v1.5.1)**: Implemented initial CIS benchmarks automation tool and extensible audit check framework.
- **PR #17 – PR #26**: Added automated CIS audit implementations for MariaDB 10.6/10.11, MySQL 8.0/8.4/9.7, PostgreSQL 16/17/18, MongoDB 7/8, and Cassandra 4.0/4.1/5.0. Review bots (Sourcery AI) reported PR diff size warnings (> 150,000 characters).
- **PR (v1.7.1)**: Enforced mandatory PR diff size limit (< 15,000 characters) and atomic PR splitting strategy in agent workspace rules (`.agents/AGENTS.md` & `03_execution_rules.md`).

