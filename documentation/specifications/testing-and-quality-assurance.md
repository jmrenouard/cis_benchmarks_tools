---
title: Testing & Quality Assurance Specification
date: 2026-11-08
category: specification
---

# Testing & Quality Assurance Specification

## 1. Quality Assurance Pipeline
Code quality and compliance are maintained through multi-tier automated validation:
1. **Unit Test Suite (`tests/`)**: 49 Python PSL `unittest` modules (295 unit tests) verifying CLI argument parsing, scoring logic, SVG generation, execution drivers, credential masking, target catalogs, and governance rules (`python -m unittest discover -s tests -v`).
2. **Pre-Commit Checks (`scripts/pre_commit_checks.py`)**: 8-step mandatory pre-commit verification routine:
   - Step 1: Verify and synchronize `VERSION`.
   - Step 2: Bundle and update unified script `audit_cis.py` via `scripts/bundle_audit_cis.py`.
   - Step 3: Validate Python syntax across all `.py` files using `py_compile`.
   - Step 4: Validate PSL-only imports via AST analysis (zero third-party imports).
   - Step 5: Validate Shell script syntax across `scripts/*.sh` using `bash -n`.
   - Step 6: Validate repository structure, rules specs (`rules/*.json`), and report integrity (`reports/*.html`).
   - Step 7: Validate `CIS_DATA/` Markdown specs and executable permissions.
   - Step 8: Execute full unit test suite (295 tests).
3. **Automated E2E Testing**: Validates audit execution against running Docker containers (`scripts/run_e2e_tests.py`).

## 2. Pull Request Diff Limit (< 15,000 characters)
- To ensure thorough human review and prevent automated AI review bot failures (Sourcery AI limit), every Pull Request diff MUST be strictly under 15,000 characters:
  ```bash
  git diff main...HEAD | wc -c
  ```
- Any feature or refactoring that exceeds 15,000 characters must be split into sequential, atomic PRs.

## 3. Tooling Inventory & Archiving Standard (`IMP-005`)
- Only the **13 essential production tools** are permitted in `scripts/`:
  `bundle_audit_cis.py`, `pre_commit_checks.py`, `pre-commit.sh`, `download_cis_benchmarks.py`, `verify_benchmarks_and_reports.py`, `clean_ssh_warnings_from_reports.py`, `run_e2e_tests.py`, `analyze_e2e_reports.py`, and the 5 container entrypoints `start_*.sh`.
- Historical one-off migration and patch scripts must reside in `archive/scripts/`.
- Enforced automatically by `tests/test_script_inventory_and_governance.py`.
