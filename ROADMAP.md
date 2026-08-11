# 🗺️ CIS Benchmarks Tools - Strategic Roadmap & Backlog (v1.5.0)

This document outlines the strategic roadmap, architecture principles, and key milestones for the CIS Benchmarks Tools suite.

---

## 🔒 Mandatory Architecture & Release Standards

> [!IMPORTANT]
> 1. **Python Standard Library ONLY (PSL ONLY)**: All Python scripts (audit engine, `audit_cis_*.py` audit modules, unified CLI `audit_cis.py`, report generators, pre-commit scripts) MUST use **EXCLUSIVELY the standard Python 3 library**. No external dependencies (`jinja2`, `yaml`, `requests`) are permitted.
> 2. **Automated Documentation Synchronization**: For every Python modification, the product version (`VERSION`), `ROADMAP.md`, and `POTENTIAL_ISSUES.md` are **automatically updated and validated**.
> 3. **Git Release Lifecycle**: Version numbers MUST be embedded in Branch names (`feat/vX.Y.Z-...`), Issue titles (`[vX.Y.Z] ...`), and PR titles (`[vX.Y.Z] ...`).
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
- [x] Synchronized `README_fr.md` (French) with `README.md` (English) in 1:1 structure.

#### 3. Subprocess Security Migration (`shell=False` / Parameter Lists)
- [x] Migration of 100% of `subprocess.run` calls to strict parameter lists (`['/bin/bash', '-c', command]`, `['docker', ...]`).
- [x] Total elimination of `shell=True` across all Python files to prevent command injection risks.

---

### Phase 4: Multi-Format Exporters & CI/CD Pipeline (Backlog / Planned 🚀)

#### 1. Multi-Format Exporter Specification (`--format json|xml|html|txt`)
- [ ] Add `--format` / `-f` CLI option to export compliance audit results into multiple structured formats using Python Standard Library ONLY:
  - **HTML**: Self-contained visual report with Chart.js graphs and styling (`--format html`).
  - **JSON**: Machine-readable JSON output for SIEM / DevSecOps pipelines (`json` PSL module, `--format json`).
  - **XML**: STIG XCCDF / JUnit XML formatted output for CI/CD integration (`xml.etree.ElementTree` PSL module, `--format xml`).
  - **TXT**: Plain-text CLI output summary for terminal logging and email notifications (`--format txt`).

#### 2. CI/CD Pipeline & Automated Testing
- [ ] GitHub Actions CI/CD pipeline automating `make pre-commit` and `make test-all` on every Pull Request.
- [ ] Automated unit test suite based on Python `unittest` PSL module for `evaluate_condition` logic.
