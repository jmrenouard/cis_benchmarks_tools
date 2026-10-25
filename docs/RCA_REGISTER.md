# RCA Register — Errors, Technical Dead-Ends, Approximations & Unimplemented Ideas

> **Governance Rule ([`AGENTS.md`](../AGENTS.md) §4 & [`.agents/rules/project-governance.md`](../.agents/rules/project-governance.md))**:
> This register guarantees full engineering traceability for the **CIS Benchmarks Tools Suite** project. It **MUST be systematically updated on every request, every change, and every result** across its four sections:
> 1. **Errors & Bugs Encountered (Root Cause Analysis — RCA)**
> 2. **Technical Dead-Ends & Abandoned Leads (`IMP`)**
> 3. **Current Approximations & Simplifying Assumptions (`APP`)**
> 4. **Unimplemented Ideas & Future Roadmap (`IDEA`)**

---

## 1. Errors & Bugs Encountered (Root Cause Analysis — RCA)

### RCA-001 — PostgreSQL Raw SQL Executed Without `psql` Wrapper (`returncode 127`)
- **Date / Linked Action**: `2026-08-18` (Phase 23 / Issue `#361` / PR `#362`)
- **Observed Symptom**: Raw `SELECT`/`SHOW` in `rules/postgresql_*.json` triggered `/bin/bash: SELECT: command not found`.
- **Root Cause Analysis**: SQL blocks extracted from CIS PDFs were passed directly to `/bin/bash -c` instead of `psql`.
- **Applied Change / Fix**: Wrapped SQL in `sudo -n -u postgres psql -t -A -c "..."` and added SQL auto-wrapping in `audit_cis_postgresql_*.py`.
- **Result & Non-Regression Test**: 0 command errors across 71 PostgreSQL controls (`tests/test_postgresql_command_safety.py`).

### RCA-002 — False-Positive Errors on Empty `path_command` and History File Loops
- **Date / Linked Action**: `2026-08-18` (Phase 20 / Issue `#352` / PR `#353`)
- **Observed Symptom**: Missing `.mysql_history`/`.psql_history` returned `returncode 1`, and empty `path_command` outputs were marked `Error`.
- **Root Cause Analysis**: Unmatched `find`/`grep` pipelines return non-zero without `; true`, and empty discovery outputs were treated as errors.
- **Applied Change / Fix**: Appended `; true` to history checks and returned `Not Applicable` on empty `path_command` with `returncode 0`.
- **Result & Non-Regression Test**: Verified in `tests/test_mariadb_audit_engine.py`.

### RCA-003 — Cross-Platform Windows Host Execution Discrepancies (`os.getuid`, `/bin/bash`, Missing `docker`)
- **Date / Linked Action**: `2026-10-21` (`ACT-004` & `ACT-006` / Issue `#438` & Issue `#442` / PR `#443`)
- **Observed Symptom**: Running `unittest` and `scripts/pre_commit_checks.py` on Windows raised `AttributeError: module 'os' has no attribute 'getuid'` in `execution_drivers.py`, `UNKNOWN_ERROR` instead of `MISSING_BINARY` when `/bin/bash` is missing, `FileNotFoundError` when `docker` is absent in `test_e2e_text_export_analysis.py`, and `UnicodeDecodeError` in `test_docker_e2e_engine.py`.
- **Root Cause Analysis**: `os.getuid()` is POSIX-only; `MISSING_BINARY_PATTERNS` lacked Windows command-not-found strings; `docker ps` lacked `FileNotFoundError` handling; `open(res_file, "r")` omitted `encoding="utf-8"`.
- **Applied Change / Fix**: Resolved in Issue `#442` via `getattr(os, "getuid", lambda: 1000)()`, Windows missing-binary regexes in `audit_diagnostics.py`, `FileNotFoundError` handling in `test_e2e_text_export_analysis.py`, explicit `encoding="utf-8"` in `test_docker_e2e_engine.py`, and UTF-8 / POSIX path normalization in `scripts/pre_commit_checks.py`.
- **Result & Non-Regression Test**: **193 / 193 unit tests and all 8 pre-commit checks pass at 100%**.

### RCA-004 — Target-Specific Rule Schema Heterogeneity (`number` vs `id`, `name` vs `title`)
- **Date / Linked Action**: `2026-10-21` (`ACT-007` / Issue `#450` / PR `#451`)
- **Observed Symptom**: Rule verification validator failed on database targets (`cassandra_*.json`, `mysql_*.json`, `mariadb_*.json`, `postgresql_*.json`, `mongodb_*.json`) reporting missing `id` and `title`.
- **Root Cause Analysis**: Database audit engines historically externalized rules using `number` and `name` keys, while OS benchmarks (RHEL) used `id` and `title`.
- **Applied Change / Fix**: Updated `audit_rules_engine` in `scripts/verify_benchmarks_and_reports.py` to accept polymorphic control keys (`id` or `number`, and `title` or `name`) with mandatory `category`.
- **Result & Non-Regression Test**: Verified by `tests/test_benchmark_sync_and_report_quality.py` (18/18 valid rule files and 887 controls verified).

### RCA-005 — Windows Cloud Sync (Dropbox) File Locking during In-Tree Wheel Builds
- **Date / Linked Action**: `2026-10-25` (`ACT-009` / Issue `#456` / PR `#457`)
- **Observed Symptom**: `PermissionError: [WinError 32]` or `[WinError 5]` during setuptools temporary folder removal when running `python -m build` in the local Windows Dropbox folder.
- **Root Cause Analysis**: Background sync daemons immediately acquire read locks on newly created build files (`build/`, `*.egg-info`), causing setuptools' immediate cleanup step to fail on Windows.
- **Applied Change / Fix**: Implemented packaging validation in `tests/test_pypi_packaging.py` validating `pyproject.toml`, metadata, and modules without requiring in-tree temporary builds, and verified that out-of-tree builds in `$env:TEMP` succeed cleanly.
- **Result & Non-Regression Test**: 4/4 packaging unit tests passed (`tests/test_pypi_packaging.py`); CI workflow runs on isolated Linux runners.

### RCA-006 — CI Lint F821 Undefined Names, Gitignored Benchmark PDF Inventory, and PyPI OIDC Exchange Failure
- **Date / Linked Action**: `2026-10-25` (`ACT-011` / Issue `#460`)
- **Observed Symptom**: CI failed on lint (22 Ruff F821 undefined variable errors), benchmark inventory test in CI (`0 < 15`), and PyPI workflow (`invalid-publisher`).
- **Root Cause Analysis**: Missing `import sys`/`os` and uninitialized `env`; `audit_benchmark_documents()` only scanned `*.pdf` (gitignored in CI); and `pypi-publish.yml` defaulted to OIDC without registered publisher.
- **Applied Change / Fix**: Fixed imports and initialized `env = os.environ.copy()`; scanned both `*.pdf` and `*.md` with stem deduplication; added resilient preflight in `pypi-publish.yml`.
- **Result & Non-Regression Test**: `ruff check` 0 errors; `pre_commit_checks.py` 8/8 checks and 199/199 unit tests pass; `.md`-only scan validates 22/22 documents.

### RCA-007 — Mypy Type Analysis Var-Annotated Failures on Unpacked Dynamic Return Values
- **Date / Linked Action**: `2026-10-25` (`ACT-012` / Issue `#462`)
- **Observed Symptom**: CI failed in `Mypy Type Check (Python 3.12)` with `Need type annotation for "results"` and `Need type annotation for "categories_scores"`.
- **Root Cause Analysis**: Mypy requires explicit type annotations when empty collections are assigned from untyped callable return unpacking (`results, overall_score, categories_scores, *extra = audit_func()`).
- **Applied Change / Fix**: Explicitly annotated `results: Dict[str, Any] = {}`, `categories_scores: Dict[str, Any] = {}`, `captured_exc: Optional[Exception] = None`, and `extra: List[Any] = ...` in `post_execution_publisher.py`.
- **Result & Non-Regression Test**: Unit test suite passes 100% (199/199); pre-commit checks 8/8 pass.

### RCA-008 — Release v2.9.0 Asset Pipeline Failure Due to Untagged Post-Fix State and OIDC Token Secret Shadowing
- **Date / Linked Action**: `2026-10-25` (`ACT-013` / Issue `#464`)
- **Observed Symptom**: GitHub Release `v2.9.0` workflow failed in CI during pre-commit checks (`test_audit_benchmark_documents_inventory`), leaving the release with 0 attached artifacts and formatted notes with ASCII bell characters (`\a`). Moreover, in `pypi-publish.yml`, passing empty `password:` to `pypa/gh-action-pypi-publish` in OIDC mode shadowed native OIDC minting.
- **Root Cause Analysis**: `v2.9.0` tag was cut at commit `e3ebf9c` prior to PR `#461` and PR `#463` fixes. Additionally, `pypa/gh-action-pypi-publish` treats the presence of `password:` as a signal to use token authentication rather than OIDC exchange.
- **Applied Change / Fix**: Bumped version to `v2.9.1`, removed conflicting `password:` argument in the OIDC publish step, expanded `tests/test_pypi_packaging.py` to verify wheel structure and entrypoints, and released `v2.9.1` with full distribution assets attached.
- **Result & Non-Regression Test**: 202/202 unit tests pass; 8/8 pre-commit checks pass; clean wheel and sdist builds verified.


---

## 2. Technical Dead-Ends & Abandoned Leads (`IMP`)

### IMP-001 — Third-Party Python Dependencies (`requests`, `jinja2`, `pyyaml`, `paramiko`)
- **Why It Is a Dead-End**: Air-gapped production database servers prohibit installing external `pip` packages on audited hosts.
- **Adopted Decision**: Enforce **100% Python Standard Library (`PSL ONLY`)**, verified by AST checks in `scripts/pre_commit_checks.py`.

### IMP-002 — External CDN JavaScript (`Chart.js`) for HTML Compliance Charts
- **Why It Is a Dead-End**: Offline security workstations block external CDNs, leaving blank charts.
- **Adopted Decision**: Generate **100% Pure Inline SVG Donut and Category Bar Charts** directly in Python PSL.

### IMP-003 — Destructive `2>/dev/null` Error Masking in CIS Rule Checks
- **Why It Is a Dead-End**: Masks root causes (`Permission denied`, `command not found`), conflating tooling errors with security outcomes.
- **Adopted Decision**: Preserve `stderr` diagnostics and classify failures via `CommandFailureClassifier` (`audit_diagnostics.py`).

### IMP-004 — Monolithic Pull Requests Exceeding 15,000 Diff Characters
- **Why It Is a Dead-End**: Automated review gates (Sourcery AI) and human reviewers reject oversized PRs (`> 15,000` diff chars).
- **Adopted Decision**: Enforce `< 15,000` diff characters per PR (`git diff main...HEAD | wc -c`) via atomic PR splitting.

---

## 3. Current Approximations & Simplifying Assumptions (`APP`)

### APP-001 — Simulated Docker Command Execution in Fast Unit Tests
- **Target Files**: `tests/test_zero_command_errors_and_automation.py` and `tests/test_e2e_docker_audits.py`
- **Nature & Justification**: Fast `unittest` runs simulate container command responses using deterministic mocks when live database containers are not running, executing 180+ tests in `< 2s` in CI.
- **Removal Condition**: Run `make test-all` or `python3 scripts/run_e2e_tests.py` on a Docker host for live container audits.

### APP-002 — Regex Heuristic Matching in `CommandFailureClassifier`
- **Target File**: `audit_diagnostics.py` (`CommandFailureClassifier.classify`)
- **Nature & Justification**: Classifies failures (`MISSING_BINARY`, `PERMISSION_DENIED`, `AUTH_FAILURE`, `CONNECTION_ERROR`, `TIMEOUT`, `SYNTAX_ERROR`) using priority-ordered regexes in `< 0.1 ms` with zero external dependencies.
- **Removal Condition**: Extend pattern catalogs when new localized OS/DB CLI messages appear.

### APP-003 — Local SHA-256 Benchmark Integrity Manifest Validation
- **Target Files**: `conf/cis_manifest.json` & `scripts/download_cis_benchmarks.py`
- **Nature & Justification**: Benchmark specifications mapped in `conf/cis_manifest.json` with SHA-256 digests. Verification runs in `< 0.1s` PSL-only.
- **Removal Condition**: Streaming remote sync and CLI integrated in Part 2 (Issue `#468`).




---

## 4. Unimplemented Ideas & Future Roadmap (`IDEA`)

### IDEA-001 — CIS GitHub Benchmark v1.2.0 Automated Audit Engine (`audit_cis_github.py`)
- **Priority / Target**: `High` · `audit_cis_github.py` & `rules/github_120.json`
- **Description**: Use `CIS_DATA/CIS_GitHub_Benchmark_v1.2.0_PDF.md` to build a 100% PSL audit engine auditing GitHub repository security settings via `gh api`.

### IDEA-002 — CIS Apache Cassandra 3.11 Legacy Archive Target Support
- **Priority / Target**: `Low` · `audit_cis_cassandra_311.py` & `rules/cassandra_311.json`
- **Description**: Optional legacy audit target based on `CIS_DATA/CIS_APACHE_CASSANDRA_3.11_Benchmark_v1.1.0_ARCHIVE.md`.

### IDEA-003 — SARIF v2.1.0 Exporter for GitHub Code Scanning (`--format sarif`)
- **Priority / Target**: `Medium` · `audit_cis.py` & `audit_cis_*.py`
- **Description**: Native PSL `--format sarif` exporter for uploading CIS Benchmark findings to GitHub Security.

### IDEA-004 — PyPI Distribution Pipeline with Trusted Publishing or API Token
- **Priority / Target**: `Completed ✅` · `pyproject.toml`, `.github/workflows/pypi-publish.yml`, and `release.yml`
- **Description**: Standard `pyproject.toml` packaging with console entrypoints (`audit-cis`, `audit_cis`) and automated GitHub Actions PyPI publishing workflow triggered on stable release creation (implemented in v2.9.0, ACT-009, ACT-010).

### IDEA-005 — Automated GitHub Actions Issue Closure with PR Merge Summary Comment
- **Priority / Target**: `Medium` · `.github/workflows/ci.yml` & `.agents/rules/`
- **Description**: Enforcement of the rule requiring every task to be tracked by an issue closed with an explicit summary comment upon PR merge.
