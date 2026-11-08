---
trigger: always_on
description: Core execution rules and constraints for the CIS Benchmark Tools project.
category: governance
---
# 03_execution_rules.md

## 🧠 Rationale
To ensure consistency, reliability, security, and smooth code review across all database and operating system auditing benchmarks. Strict adherence to these rules prevents broken tests, inconsistent naming, environment dependencies, and rejected Pull Requests.

## 🛠️ Implementation

### 1. Mandatory Testing & Quality Gates
- All code modifications MUST pass 100% of the unit test suite: `python -m unittest discover -s tests -v`.
- All modifications MUST pass the 8-step pre-commit verification: `python scripts/pre_commit_checks.py`.
- Any new or modified database audit script MUST have a corresponding Dockerfile in `docker/` (e.g., `docker/Dockerfile_mariadb106`) for containerized validation.

### 2. Standardized Naming Conventions
- Audit scripts: `audit_cis_<product>_<version>.py` (e.g., `audit_cis_mysql_80.py`, `audit_cis_rhel_8.py`).
- Rules specifications: `rules/<target_key>.json`.
- Test Dockerfiles: `docker/Dockerfile_<product><version>` or `docker/Dockerfile_<product>_<flavor>_<version>`.
- Generated Reports: `rapport_cis_<target_key>.<fmt>` or `cis_report_<target_key>.<fmt>`.

### 3. Dual-Mode Architecture & 100% PSL ONLY
- **100% Python Standard Library**: Runtime audit engines, CLI, transports, and orchestrator MUST depend exclusively on Python Standard Library. Zero third-party dependencies are permitted.
- **Standalone Portability**: Individual `audit_cis_*.py` scripts must retain standalone portability (fallback recommendation dictionaries and fallback inline SVG renderers).
- **Core Engine Integration**: Scripts integrate seamlessly with `cis_core_engine.py`, `execution_drivers.py`, and `audit_diagnostics.py` when executed within the repository suite.

### 4. 4-Tier Execution Contexts & Security
- Audits must support the 4 execution contexts: `Local`, `Remote SSH`, `Local Docker`, `Remote SSH Docker` via `execution_drivers.py`.
- Passwords MUST NOT be passed as CLI arguments (`ps aux` leak prevention). Passwords must use environment variables (`MYSQL_PWD`, `PGPASSWORD`, `CIS_DB_PASSWORD`) and be scrubbed via `SecretSanitizer`.

### 5. Pull Request Size & 9-Step Lifecycle
- Maximum PR diff size is strictly **15,000 characters** (`git diff main...HEAD | wc -c` < 15000). Larger additions must be split into atomic PRs.
- Every contribution must follow the 9-step GitHub workflow (`gh issue create` -> dedicated branch -> TDD -> action logbook & RCA register update -> commit -> PR < 15k chars -> merge -> issue close).

## ✅ Verification
- Run `python -m unittest discover -s tests -v` to verify 100% test pass.
- Run `python scripts/pre_commit_checks.py` to verify AST PSL compliance and rule integrity.
- Run `git diff main...HEAD | wc -c` to confirm PR diff size < 15,000 characters before submitting PR.