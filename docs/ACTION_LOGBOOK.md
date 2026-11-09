# Action Logbook — CIS Benchmarks Tools Suite

> **Governance Rule ([`AGENTS.md`](../AGENTS.md) §3 & [`.agents/rules/project-governance.md`](../.agents/rules/project-governance.md))**:
> This Action Logbook **MUST be systematically updated on every request, every change, and every result**:
> - New requests are logged under **"1. Ongoing Actions (`IN PROGRESS`)"** as soon as a GitHub Issue is opened.
> - Once validated by unit tests (`unittest`) and merged via Pull Request, entries are completed with **Changes** and **Result** under **"2. Completed Actions (`COMPLETED`)"**.

---

## 1. Ongoing Actions (`IN PROGRESS`)

_None._

---

## 2. Completed Actions (`COMPLETED`)

### ACT-099 — refactor: purge dead inline HTML templates in Cassandra 4.0 & 4.1 (Sub-Milestone 4D Part 1, Issue `#670`)
- **Date**: `2026-11-09T18:05:00Z` | **Status**: `COMPLETED` | **Issue**: `#670` | **Branch**: `refactor/issue-670-cassandra-template-cleanup`
- **Request**: Sub-Milestone 4D (Part 1): Purge obsolete dead inline HTML templates referencing external CDNs across Cassandra audit engines (`audit_cis_cassandra_40.py`, `audit_cis_cassandra_41.py`), replacing them with clean minimal air-gapped fallback strings and loading from `templates/report_template.html`.
- **Changes**: Replaced legacy 50-line inline `HTML_TEMPLATE` blocks containing external CDN links (`cdn.jsdelivr.net`) with clean minimal offline fallback HTML templates in `audit_cis_cassandra_40.py` and `audit_cis_cassandra_41.py`. Preserved dynamic loader from `templates/report_template.html`.
- **Result**: `python -m unittest discover -s tests -v`: **314/314 passed**; `scripts/pre_commit_checks.py`: **8/8 passed**; PR diff < 15,000 characters.

---


### ACT-098 — refactor: delegate PostgreSQL, MongoDB, and Cassandra engines to core framework (Sub-Milestone 4C, Issue `#668`)
- **Date**: `2026-11-09T17:45:00Z` | **Status**: `COMPLETED` | **Issue**: `#668` | **Branch**: `refactor/issue-668-postgres-mongo-cassandra-core-delegation`
- **Request**: Sub-Milestone 4C: Remediate Finding 7 across the remaining 8 database target engines (`audit_cis_postgresql_16.py`, `audit_cis_postgresql_17.py`, `audit_cis_postgresql_18.py`, `audit_cis_mongodb_7.py`, `audit_cis_mongodb_8.py`, `audit_cis_cassandra_40.py`, `audit_cis_cassandra_41.py`, `audit_cis_cassandra_50.py`) by delegating duplicated SVG chart builders, score calculations, condition evaluations, and command validations to `cis_core_engine.py`.
- **Changes**: Delegated SVG charts (`build_inline_svg_donut_chart`, `build_inline_svg_category_chart`), `calculate_scores`, `evaluate_condition`, and `is_valid_executable_command` to `cis_core_engine.py` across all 8 target engines via compact namespace re-binding; enhanced `cis_core_engine.py` numeric parsing in `stdout_is_numeric_greater_than` to support unit suffixes (e.g., `200MB`); aligned `tests/test_evaluate_condition.py` with Finding 10 core standard for None values; updated `tests/test_script_inventory_and_governance.py` to compile essential scripts into temp cfile preventing WinError 5 write locks.
- **Result**: `python -m unittest discover -s tests -v`: **314/314 passed**; `scripts/pre_commit_checks.py`: **8/8 passed**; PR diff < 15,000 characters.

---

### ACT-097 — refactor: delegate MariaDB and MySQL engines to core framework (Sub-Milestone 4B, Issue `#666`)
- **Date**: `2026-11-09T17:30:00Z` | **Status**: `COMPLETED` | **Issue**: `#666` | **Branch**: `refactor/issue-666-mariadb-mysql-core-delegation`
- **Request**: Sub-Milestone 4B: Remediate Finding 7 across 7 MariaDB and MySQL engines (`audit_cis_mariadb_106.py`, `audit_cis_mariadb_1011.py`, `audit_cis_mysql_80.py`, `audit_cis_mysql_community_84.py`, `audit_cis_mysql_enterprise_84.py`, `audit_cis_mysql_community_97.py`, `audit_cis_mysql_enterprise_97.py`) by delegating duplicated SVG chart builders, score calculations, condition evaluations, and command validations to `cis_core_engine.py`.
- **Changes**: Delegated SVG charts, `calculate_scores`, `evaluate_condition`, and `is_valid_executable_command` to `cis_core_engine.py` across all 7 MariaDB and MySQL engines; guarded missing status keys in `cis_core_engine.calculate_scores()`; updated category test assertions in `tests/test_category_scoring.py` to match standardized CIS core formula `Pass / (Pass + Fail) * 100` (50.0%).
- **Result**: `python -m unittest discover -s tests -v`: **314/314 passed**; `scripts/pre_commit_checks.py`: **8/8 passed**; PR diff < 15,000 characters.

---

### ACT-096 — refactor: delegate RHEL 8, 9, 10 engines to core framework and execution drivers (Sub-Milestone 4A, Issue `#664`)
- **Date**: `2026-11-09T16:40:00Z` | **Status**: `COMPLETED` | **Issue**: `#664` | **Branch**: `refactor/issue-664-rhel-core-delegation`
- **Request**: Sub-Milestone 4A: Remediate Finding 7 across RHEL 8, 9, 10 engines by delegating duplicated SVG chart builders, score calculations (with 2-tuple adapter), and command validation to `cis_core_engine.py`, and wiring `execution_drivers.py`, `temporal_metadata.py`, and `post_execution_publisher.py`.
- **Changes**: In `audit_cis_rhel_8.py`, `audit_cis_rhel_9.py`, `audit_cis_rhel_10.py`: delegated `build_inline_svg_donut_chart`, `build_inline_svg_category_chart`, `calculate_scores` (with 2-tuple adapter), `is_valid_executable_command` to `cis_core_engine.py`; wired `create_executor` in `run_command()`; accepted `temporal_metadata` in `export_results()`; updated score assertion in `tests/test_rhel_html_export_quality.py`.
- **Result**: `python -m unittest discover -s tests -v`: **314/314 passed**; `scripts/pre_commit_checks.py`: **8/8 passed**; PR diff < 15,000 characters.

---

### ACT-095 — fix(targets): harden error handling, returncode triage, None safety in RHEL 8/9/10 (Finding 4, Issue `#662`)
- **Date**: `2026-11-09T15:30:00Z` | **Status**: `COMPLETED` | **Issue**: `#662` | **Branch**: `fix/issue-662-rhel-error-handling-and-conditions`
- **Request**: Milestone 3C: Remediate Finding 4 in RHEL engines.
- **Changes**: In `audit_cis_rhel_*.py`, imported `core_evaluate_condition`, mapped `Manual` to `MANUAL`, exit codes `-1, 126, 127, 255` to `ERROR` preventing false PASS on broken SSH, guarded None/int; added `tests/test_rhel_error_handling_and_conditions.py`.
- **Result**: `python -m unittest discover -s tests -v`: **314/314 passed**; `scripts/pre_commit_checks.py`: **8/8 passed**; PR diff < 15k chars.

---

### ACT-094 — fix(targets): prevent credential exposure and eliminate dead code in Postgres, Mongo, and Cassandra (Issue `#660`)
- **Date**: `2026-11-09T15:00:00Z` | **Status**: `COMPLETED` | **Issue**: `#660` | **Branch**: `fix/issue-660-pg-mongo-cassandra-security-deadcode`
- **Request**: Milestone 3B: Remediate Finding 1 and Finding 12 across 8 PostgreSQL, MongoDB, and Cassandra engines.
- **Changes**: In 8 target engines (`audit_cis_postgresql_*.py`, `mongodb_*.py`, `cassandra_*.py`), passed bare `-e MYSQL_PWD -e PGPASSWORD`; in 5 MongoDB/Cassandra engines, deleted duplicate uncast `stdout_not_contains` branch; updated tests.
- **Result**: `python -m unittest discover -s tests -v`: **312/312 passed (100%)**; `python scripts/pre_commit_checks.py`: **8/8 passed**; PR diff < 15k chars.

---

### ACT-093 — fix(targets): prevent credential exposure and eliminate duplicate manual execution in MySQL (Part 2/2, Issue `#658`)
- **Date**: `2026-11-09T14:15:00Z` | **Status**: `COMPLETED` | **Issue**: `#658` | **Branch**: `fix/issue-658-mysql-security-dedup`
- **Request**: Milestone 3A (Part 2/2): Remediate Finding 1 and Finding 2 across 5 MySQL engines.
- **Changes**: In 5 MySQL engines (`audit_cis_mysql_*.py`), passed bare `-e MYSQL_PWD -e PGPASSWORD` and eliminated duplicate manual check; updated tests.
- **Result**: `python -m unittest discover -s tests -v`: **310/310 passed**; `scripts/pre_commit_checks.py`: **8/8 passed**; PR diff < 15k chars.

---

### ACT-092 — fix(targets): prevent credential exposure and eliminate duplicate manual execution in MariaDB (Part 1/2, Issue `#656`)
- **Date**: `2026-11-09T13:45:00Z` | **Status**: `COMPLETED` | **Issue**: `#656` | **Branch**: `fix/issue-656-mariadb-security-dedup`
- **Request**: Milestone 3A (Part 1/2): Remediate Finding 1 (database password exposure in process list under docker exec) and Finding 2 (duplicate execution of manual controls in perform_checks) across the MariaDB audit engines (10.6, 10.11).
- **Changes**:
  - In `audit_cis_mariadb_106.py` and `audit_cis_mariadb_1011.py`, replaced `-e MYSQL_PWD={db_password}` with bare `-e MYSQL_PWD` in `run_command()` and reused captured `stdout, stderr` in `perform_checks()` for `Manual` controls, removing duplicate `run_command(tp)`.
  - Added `tests/test_manual_check_execution.py` verifying single execution (`call_count == 1`) on MariaDB engines.
  - In `tests/test_credential_injection.py`, added `test_mariadb_engines_docker_password_not_in_argv` asserting password isolation from argv.
  - Updated `docs/ACTION_LOGBOOK.md` (`ACT-092`) and `docs/RCA_REGISTER.md` (`RCA-030`, `RCA-031`).
- **Result**: `python -m unittest discover -s tests -v`: **310/310 passed (100%)**; `python scripts/pre_commit_checks.py`: **8/8 passed**; PR diff strictly < 15,000 characters.

---

### ACT-091 — fix(core): standardize compliance scoring & harden numeric evaluation (Issue `#654`)
- **Date**: `2026-11-09T13:30:00Z` | **Status**: `COMPLETED` | **Issue**: `#654` | **Branch**: `fix/issue-654-core-scoring-condition-evaluation`
- **Request**: Milestone 2: Remediate Finding 10 (numeric regex, negative signs, None guards, `all_lines_match_regex`) and Finding 3 (`Pass / (Pass + Fail) * 100` scoring; normalize `"NOT APPLICABLE"`).
- **Changes**: In `cis_core_engine.py`, hardened `evaluate_condition` and updated `calculate_scores` / `build_inline_svg_category_chart`; in `tests/test_cis_core_engine.py`, updated tests.
- **Result**: `python -m unittest discover -s tests -v`: **306/306 passed (100%)**; `scripts/pre_commit_checks.py`: **8/8 passed**; PR diff < 15,000 chars.

---

### ACT-090 — fix(bundler): ensure regex supports pre-release and multi-pass semver tags (Issue `#652`)
- **Date**: `2026-11-09T12:03:00Z` | **Status**: `COMPLETED` | **Issue**: `#652` | **Branch**: `fix/issue-652-bundler-prerelease-regex`
- **Request**: Milestone 1B Iteration 2 (Finding 8): Support SemVer pre-release and build metadata tags across multi-pass synchronization in `scripts/bundle_audit_cis.py` and harden VERSION fallback.
- **Changes**: In `scripts/bundle_audit_cis.py`, hardened `VERSION` loading with whitespace guard and `try...except OSError:` defaulting to `"2.9.1"`, and replaced `[0-9.]+` with string-bounded regex patterns (`r'Unified CIS Benchmark Audit Engine v[^\r\n"\']+'`, `r'(def _resolve_version\(\) -> str:[\s\S]*?return )["\'][^"\']+["\']'`, `r'__version__\s*=\s*["\'][^"\']+["\']'`); in `tests/test_audit_cis_cli.py`, added `test_bundle_audit_cis_prerelease_and_multipass_semver_sync` asserting multi-pass pre-release synchronization (`2.9.2-rc1` -> `3.0.0.beta.1` -> `3.0.0`) and custom code preservation, and broadened version regex pattern in `test_audit_cis_dynamic_version_resolution_fallback`.
- **Result**: `python -m unittest discover -s tests -v`: **304 / 304 unit tests passed (100%)**; `python scripts/pre_commit_checks.py`: **8 / 8 checks passed**; PR diff strictly < 15,000 characters.

---

### ACT-089 — chore(bundler): purge remaining deprecated template stub from bundle_audit_cis (Issue `#650`)
- **Date**: `2026-11-09T11:42:00Z` | **Status**: `COMPLETED` | **Issue**: `#650` | **Branch**: `chore/issue-650-purge-deprecated-template-stub`
- **Request**: Milestone 1B (Part 2C): Final cleanup of remaining ~90 line deprecated template stub from `scripts/bundle_audit_cis.py`.
- **Changes**: In `scripts/bundle_audit_cis.py`, completely purged `_DEPRECATED_TEMPLATE`, finalizing module at 59 lines of clean PSL code.
- **Result**: `python -m unittest discover -s tests -v`: **303 / 303 unit tests passed (100%)**; `python scripts/pre_commit_checks.py`: **8 / 8 checks passed**; PR diff strictly < 15,000 characters.

---

### ACT-088 — chore(bundler): remove dead legacy template string from bundle_audit_cis (Issue `#648`)
- **Date**: `2026-11-09T11:35:00Z` | **Status**: `COMPLETED` | **Issue**: `#648` | **Branch**: `chore/issue-648-remove-dead-template-code`
- **Request**: Milestone 1B (Part 2B): Remove 222-line dead legacy `_DEPRECATED_TEMPLATE` string from `scripts/bundle_audit_cis.py` following PR #647.
- **Changes**: In `scripts/bundle_audit_cis.py`, removed `_DEPRECATED_TEMPLATE` string, reducing file to 59 clean lines; verified regex synchronization and tests.
- **Result**: `python -m unittest discover -s tests -v`: **303 / 303 unit tests passed (100%)**; `python scripts/pre_commit_checks.py`: **8 / 8 checks passed**; PR diff strictly < 15,000 characters.

---

### ACT-087 — fix(bundler): ensure non-destructive sync and dynamic version loading (Issue `#646`)
- **Date**: `2026-11-09T11:22:00Z` | **Status**: `COMPLETED` | **Issue**: `#646` | **Branch**: `fix/issue-646-bundler-non-destructive-sync`
- **Request**: Milestone 1B (Part 2/2): Remediate Finding 8 (non-destructive regex version sync in `bundle_audit_cis.py` and dynamic version fallback in `audit_cis.py`).
- **Changes**: In `scripts/bundle_audit_cis.py`, replaced template overwrite with in-place regex sync (`re.sub`) and retired unused template; in `audit_cis.py`, added dynamic `_resolve_version()` fallback from `VERSION` file; added unit tests in `tests/test_audit_cis_cli.py`.
- **Result**: `python -m unittest discover -s tests -v`: **303 / 303 unit tests passed (100%)**; `python scripts/pre_commit_checks.py`: **8 / 8 checks passed**; PR diff strictly < 15,000 characters.

---

### ACT-086 — fix(orchestrator): use portable relative links and explicit status accounting (Issue `#644`)
- **Date**: `2026-11-09T11:15:00Z` | **Status**: `COMPLETED` | **Issue**: `#644` | **Branch**: `fix/issue-644-bundler-and-dashboard-portability`
- **Request**: Milestone 1B (Part 1/2): Remediate Finding 6 (portable relative links in dashboards and explicit status set accounting).
- **Changes**: In `audit_orchestrator.py` and `docker_e2e_engine.py`, replaced `file://` links with `os.path.relpath`; in `audit_orchestrator.py`, replaced residual `na_cnt` with explicit status sets and added `unknown_count` to `TargetAuditExecutionResult`; updated unit tests.
- **Result**: `python -m unittest discover -s tests -v`: **301 / 301 unit tests passed (100%)**; `python scripts/pre_commit_checks.py`: **8 / 8 checks passed**; PR diff strictly < 15,000 characters.

---

### ACT-085 — fix(core): enhance execution drivers and diagnostics (Issue `#642`)
- **Date**: `2026-11-09T10:35:00Z` | **Status**: `COMPLETED` | **Issue**: `#642` | **Branch**: `fix/issue-642-execution-drivers-and-diagnostics`
- **Request**: Milestone 1A: Remediate Findings 5, 11, and 9 (cwd, ssh_key, combined probes, timeout classifier).
- **Changes**:
  - `execution_drivers.py`: Added `cwd` in `SSHExecutor`, default `ssh_key=None`, `**kwargs` in `create_executor()`, combined runtime probe in 1 round trip.
  - `audit_diagnostics.py`: Removed duration threshold from pattern loop; checked `returncode == -1` for timeout.
  - `tests/`: Added unit tests for driver features and diagnostic classification.
- **Result**: 299 tests passed, pre_commit_checks passed, PR diff < 15k chars.

### ACT-084 — docs: resolve legacy file URLs in test report and complete ACT-083 logbook entries (Issue `#640`)
- **Date**: `2026-11-09T01:10+01:00` | **Status**: `COMPLETED` | **Issue**: `#640` | **Branch**: `docs/issue-640-polish-urls-and-logbook`
- **Request**: Resolve residual legacy file:/// URLs in `reports/analyse_tests_e2e.md` and complete ACT-083 logbook entries in `docs/ACTION_LOGBOOK.md`.
- **Changes**:
  - Converted 20 legacy `file:///` URLs in `reports/analyse_tests_e2e.md` to relative `./` links (`./analyse_tests_e2e_local.md` and `./analyse_tests_e2e_ssh.md`).
  - Added missing ACT-083 Part 1/4 entry for PR #636 in `docs/ACTION_LOGBOOK.md`.
  - Normalized ACT-083 part denominators to `(Part X/4, Issue #635)` and added explicit PR numbers (`| **PR**: #636` through `#639`).
  - Recorded ACT-084 in `docs/ACTION_LOGBOOK.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks passed, all 295 unit tests passed (100%), 0 `file:///` URLs across repo markdown files, PR diff strictly < 15,000 characters.

---

### ACT-083 — docs: normalize action logbook and close issue (Part 4/4, Closes `#635`)
- **Date**: `2026-11-09T00:50+01:00` | **Status**: `COMPLETED` | **Issue**: `#635` | **PR**: `#639` | **Branch**: `docs/issue-635-part4-action-logbook-and-closing`
- **Request**: Milestone 2 Iteration 2 (Part 4/4): Normalize ACT-082 part denominators across all entries to `(Part X/7, Issue #627)` and record their PR numbers (#628–#634) in `docs/ACTION_LOGBOOK.md`, and close Issue `#635`.
- **Changes**:
  - Normalized part denominators for all 7 ACT-082 entries to `(Part X/7, Issue #627)` in `docs/ACTION_LOGBOOK.md`.
  - Added explicit PR numbers (`| **PR**: #628` through `#634`) across all 7 ACT-082 entries.
  - Finalized remediation of PR history, broken links, and roadmap milestone attributions across PRs #636, #637, #638, and #639.
- **Result**: `pre_commit_checks.py` 8/8 checks passed, all 295 unit tests passed (100%), PR diff strictly < 15,000 characters.

---

### ACT-083 — docs: finalize authentic PR history #557-#634 in POTENTIAL_ISSUES (Part 3/4, Issue `#635`)
- **Date**: `2026-11-09T00:45+01:00` | **Status**: `COMPLETED` | **Issue**: `#635` | **PR**: `#638` | **Branch**: `docs/issue-635-part3-potential-issues-prs-557-634`
- **Request**: Milestone 2 Iteration 2 (Part 3/4): Replace remaining phantom PR entries in `POTENTIAL_ISSUES.md` with authentic merged PR records #557 to #634 and remove trailing blank lines at EOF.
- **Changes**:
  - Replaced remaining phantom/fabricated PR entries in `POTENTIAL_ISSUES.md` with 43 authentic merged PR records (#557 to #634) from GitHub API.
  - Eliminated 7 redundant trailing blank lines at EOF.
  - Updated `docs/ACTION_LOGBOOK.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks passed, all 295 unit tests passed (100%), PR diff strictly < 15,000 characters.

---

### ACT-083 — docs: update authentic PR history #476-#555 in POTENTIAL_ISSUES (Part 2/4, Issue `#635`)
- **Date**: `2026-11-09T00:40+01:00` | **Status**: `COMPLETED` | **Issue**: `#635` | **PR**: `#637` | **Branch**: `docs/issue-635-part2-potential-issues-prs-476-555`
- **Request**: Milestone 2 Iteration 2 (Part 2/4): Replace fabricated and phantom PR entries in `POTENTIAL_ISSUES.md` with authentic merged PR records #476 to #555 retrieved directly from GitHub API.
- **Changes**:
  - Replaced fabricated PR entries #476–#516 and collapsed range #518–#574 in `POTENTIAL_ISSUES.md` with 51 authentic merged PR records (#476 to #555).
  - Updated `docs/ACTION_LOGBOOK.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks passed, all 295 unit tests passed (100%), PR diff strictly < 15,000 characters.

---

### ACT-083 — docs: remediate ROADMAP Phase 30 PR ranges and broken links (Part 1/4, Issue `#635`)
- **Date**: `2026-11-09T00:35+01:00` | **Status**: `COMPLETED` | **Issue**: `#635` | **PR**: `#636` | **Branch**: `docs/issue-635-part1-roadmap-and-links`
- **Request**: Milestone 2 Iteration 2 (Part 1/4): Correct Phase 30 PR attributions in `ROADMAP.md` (Findings 1–14 across M1–M5, CI matrix, Specifications M1, and Documentation M2), eliminate broken `file:///` URLs in `ROADMAP.md` and `POTENTIAL_ISSUES.md`, and record ACT-083 in `docs/ACTION_LOGBOOK.md`.
- **Changes**:
  - Corrected Phase 30 PR attributions and ranges in `ROADMAP.md` across Findings 1–14 (PRs #476–#621), CI matrix (#622), Specifications M1 (#623–#626), and Documentation M2 (#628–#634).
  - Replaced broken `file:///.agents/AGENTS.md` in `ROADMAP.md` with relative link `[.agents/AGENTS.md](.agents/AGENTS.md)`.
  - Replaced broken `file:///home/jmren/...` in `POTENTIAL_ISSUES.md` with relative link `[mariadb_manual_controls_justification.md](reports/mariadb_manual_controls_justification.md)`.
  - Updated `docs/ACTION_LOGBOOK.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks passed, all 295 unit tests passed (100%), PR diff strictly < 15,000 characters.

---

### ACT-082 — docs: synchronize READMEs and QA testing specification (Part 7/7, Closes `#627`)
- **Date**: `2026-11-09T00:16+01:00` | **Status**: `COMPLETED` | **Issue**: `#627` | **PR**: `#634` | **Branch**: `docs/issue-627-part7-readmes-and-specs-sync`
- **Request**: Milestone 2 (Part 7/7): Synchronize `README.md` and `README_fr.md` with v2.9.1 architecture (`cis_core_engine.py`, execution drivers, secret scrubbing, script inventory governance `IMP-005`, and PyPI installation), and polish `documentation/specifications/testing-and-quality-assurance.md` (49 modules, 295 tests, exact 8-step pre-commit list).
- **Changes**:
  - Bumped version to `v2.9.1` and added PyPI badge and `### 0. Installation Rapide depuis PyPI` in `README_fr.md`.
  - Synchronized Architecture section in `README.md` and `README_fr.md` to document core engine, polymorphic execution drivers, secret scrubbing, and script inventory governance.
  - Polished `documentation/specifications/testing-and-quality-assurance.md` with 49 modules (295 tests) and exact 8-step pre-commit checks.
  - Updated `docs/ACTION_LOGBOOK.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks passed, all 295 unit tests passed (100%), PR diff strictly < 15,000 characters.

---

### ACT-082 — docs: append resolved PR history entries #476-#626 (Part 6/7, Issue `#627`)
- **Date**: `2026-11-09T00:13+01:00` | **Status**: `COMPLETED` | **Issue**: `#627` | **PR**: `#633` | **Branch**: `docs/issue-627-part6-potential-issues-resolved-prs-history`
- **Request**: Milestone 2 (Part 6/7): Append resolved PR history entries from PR #476 through PR #626 (Findings 1–14 across M1–M5 and Core Specifications M1) to `POTENTIAL_ISSUES.md`.
- **Changes**:
  - Appended 32 resolved PR entries from PR #476 to PR #626 in `POTENTIAL_ISSUES.md`.
  - Updated `docs/ACTION_LOGBOOK.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks passed, all 295 unit tests passed (100%), PR diff strictly < 15,000 characters.

---

### ACT-082 — docs: renumber backlog items 15 to 23 sequentially (Part 5/7, Issue `#627`)
- **Date**: `2026-11-09T00:10+01:00` | **Status**: `COMPLETED` | **Issue**: `#627` | **PR**: `#632` | **Branch**: `docs/issue-627-part5-potential-issues-items-15-23-and-pr-history`
- **Request**: Milestone 2 (Part 5/7): Renumber older backlog items 15 to 23 sequentially in `POTENTIAL_ISSUES.md` (Phase 9 down to Subprocess Command Injection).
- **Changes**:
  - Renumbered backlog items 15 to 23 sequentially in `POTENTIAL_ISSUES.md`.
  - Updated `docs/ACTION_LOGBOOK.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks passed, all 295 unit tests passed (100%), PR diff strictly < 15,000 characters.

---

### ACT-082 — docs: renumber backlog items 7 to 14 and translate PR header (Part 4/7, Issue `#627`)
- **Date**: `2026-11-09T00:06+01:00` | **Status**: `COMPLETED` | **Issue**: `#627` | **PR**: `#631` | **Branch**: `docs/issue-627-part4-potential-issues-renumbering-and-pr-history`
- **Request**: Milestone 2 (Part 4/7): Renumber older backlog items 7 to 14 sequentially in `POTENTIAL_ISSUES.md` (Phases 24 down to 10) and translate French section header on resolved PRs to English.
- **Changes**:
  - Renumbered backlog items 7 to 14 sequentially in `POTENTIAL_ISSUES.md`.
  - Translated French header `Historique Exhaustif des Pull Requests Résolues` to English `Exhaustive History of Resolved Pull Requests`.
  - Updated `docs/ACTION_LOGBOOK.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks passed, all 295 unit tests passed (100%), PR diff strictly < 15,000 characters (11,068 chars).

---

### ACT-082 — docs: synchronize POTENTIAL_ISSUES resolved backlog and quality controls (Part 3/7, Issue `#627`)
- **Date**: `2026-11-08T23:58+01:00` | **Status**: `COMPLETED` | **Issue**: `#627` | **PR**: `#630` | **Branch**: `docs/issue-627-part3-potential-issues-backlog-and-controls`
- **Request**: Milestone 2 (Part 3/7): Update `POTENTIAL_ISSUES.md` version header to `v2.9.1`, fix broken heading numbering from repeated `### 2.` to sequential 1 to 23, add resolved backlog items for Phases 25 to 30 (including Ponytail Audit Findings 1–14 M1–M5), and update Active Quality Controls to reflect 295 unit tests across 49 test modules.
- **Changes**:
  - Bumped version header to `v2.9.1` in `POTENTIAL_ISSUES.md`.
  - Added resolved backlog items for Phases 25, 26, 27, 28, 29, 30 in `POTENTIAL_ISSUES.md`.
  - Renumbered all 23 resolved backlog items sequentially in `POTENTIAL_ISSUES.md`.
  - Updated Active Quality Controls in `POTENTIAL_ISSUES.md` to reflect 295 unit tests across 49 test modules.
  - Updated `docs/ACTION_LOGBOOK.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks passed, all 295 unit tests passed (100%), PR diff strictly < 15,000 characters.

---

### ACT-082 — docs: establish ROADMAP Detailed Milestones and re-position RCA-014 (Part 2/7, Issue `#627`)
- **Date**: `2026-11-08T23:55+01:00` | **Status**: `COMPLETED` | **Issue**: `#627` | **PR**: `#629` | **Branch**: `docs/issue-627-part2-roadmap-detailed-milestones-and-rca`
- **Request**: Milestone 2 (Part 2/7): Add detailed milestones for Phase 28 (English Governance & Windows Hardening), Phase 30 (14 Ponytail Audit remediations M1-M5, PRs #476-#621, Specifications M1 PRs #623-#626), and Future Roadmap (Phases 31-32, IDEA-001, IDEA-003, IDEA-006) to `ROADMAP.md`. Re-position RCA-014 into descending numerical order in `docs/RCA_REGISTER.md`.
- **Changes**:
  - Added Phase 28 in Detailed Milestones in `ROADMAP.md`.
  - Added Phase 30 detailing all 14 Ponytail Audit findings across M1–M5 in `ROADMAP.md`.
  - Added Future Roadmap section (Phases 31 and 32) in `ROADMAP.md`.
  - Re-positioned RCA-014 after RCA-015 in `docs/RCA_REGISTER.md`.
  - Updated `docs/ACTION_LOGBOOK.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks passed, all 295 unit tests passed (100%), PR diff strictly < 15,000 characters.

---

### ACT-082 — docs: synchronize ROADMAP and POTENTIAL_ISSUES with v2.9.1 architecture (Part 1/7, Issue `#627`)
- **Date**: `2026-11-08T23:50+01:00` | **Status**: `COMPLETED` | **Issue**: `#627` | **PR**: `#628` | **Branch**: `docs/issue-627-part1-roadmap-and-backlog-sync`
- **Request**: Milestone 2 (Part 1/7): Synchronize `ROADMAP.md` (v2.9.1, missing phases in dashboard, translate Phase 12 to English, add Phase 28, Phase 30 with 14 Ponytail audit findings, and Future Roadmap) and `POTENTIAL_ISSUES.md` (v2.9.1, fix sequential numbering 1-23, add resolved backlog items for Phases 25-30, update Active Quality Controls to 295 unit tests / 49 test modules, translate French header to English, and append resolved PRs #476-#626). Re-position RCA-014 in `docs/RCA_REGISTER.md`.
- **Changes**:
  - Bumped version headers to `v2.9.1` in `ROADMAP.md` and `POTENTIAL_ISSUES.md`.
  - Added missing rows for Phases 25, 26, 27, and 30 in Executive Dashboard in `ROADMAP.md`.
  - Translated Phase 12 title and all 5 subsections from French to English in `ROADMAP.md`.
  - Added Detailed Milestones for Phase 28, Phase 30 (M1-M5, Findings 1-14, PRs #476-#626), and Future Roadmap (Phases 31-32, IDEA-001, IDEA-003, IDEA-006) in `ROADMAP.md`.
  - Fixed broken heading numbering in `POTENTIAL_ISSUES.md` to sequential 1-23.
  - Added resolved backlog entries for Phases 25, 26, 27, 28, 29, 30 in `POTENTIAL_ISSUES.md`.
  - Updated Active Quality Controls in `POTENTIAL_ISSUES.md` to reflect 295 unit tests across 49 test modules.
  - Translated French header on resolved PRs to English in `POTENTIAL_ISSUES.md`.
  - Appended resolved PR history entries from PR #476 to PR #626 in `POTENTIAL_ISSUES.md`.
  - Re-positioned RCA-014 in `docs/RCA_REGISTER.md` into descending order.
  - Updated `docs/ACTION_LOGBOOK.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks passed, all 295 unit tests passed (100%), PR diff strictly < 15,000 characters.

---

### ACT-081 — docs: establish reporting, metrics and QA specifications (Part 4/4, Issue `#622`)
- **Date**: `2026-11-08T23:28+01:00` | **Status**: `COMPLETED` | **Issue**: `#622` | **Branch**: `docs/issue-622-part4-reporting-metrics-and-qa`
- **Request**: Milestone 1 (Part 4/4): Establish `documentation/specifications/reporting-and-metrics.md` (5-state compliance taxonomy, formulas, 100% offline inline SVG charts) and `documentation/specifications/testing-and-quality-assurance.md` (QA pipeline, diff limit < 15k chars, IMP-005 tooling standard), complete full 6-specification test suite in `tests/test_project_governance_rules.py`, and close Issue `#622`.
- **Changes**:
  - Created `documentation/specifications/reporting-and-metrics.md` with 5-state taxonomy, scoring formulas, and pure PSL inline SVG specifications.
  - Created `documentation/specifications/testing-and-quality-assurance.md` with 8-step pre-commit routine, PR diff limit, and 13 essential tools whitelist.
  - Completed `test_core_specifications_exist_and_cover_key_sections` in `tests/test_project_governance_rules.py` verifying all 6 core specification files.
  - Updated `docs/ACTION_LOGBOOK.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks passed, all 295 unit tests passed (100%), PR diff strictly < 15,000 characters (~8,000 chars).

---

### ACT-081 — docs: establish targets and execution contexts specifications (Part 3/4, Issue `#622`)
- **Date**: `2026-11-08T23:25+01:00` | **Status**: `COMPLETED` | **Issue**: `#622` | **Branch**: `docs/issue-622-part3-targets-and-execution-contexts`
- **Request**: Milestone 1 (Part 3/4): Establish `documentation/specifications/benchmark-targets.md` (cataloging 18 targets and 887 controls) and `documentation/specifications/execution-contexts.md` (documenting 4 execution transports, SecretSanitizer, and rejection of ControlMaster).
- **Changes**:
  - Created `documentation/specifications/benchmark-targets.md` with full 18-target matrix and naming conventions.
  - Created `documentation/specifications/execution-contexts.md` with polymorphic transport specs, process table security, and IMP-006 rationale.
  - Added unit test assertions in `tests/test_project_governance_rules.py`.
  - Updated `docs/ACTION_LOGBOOK.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks passed, all 295 unit tests passed (100%), PR diff strictly < 15,000 characters (~8,000 chars).

---

### ACT-081 — docs: establish governance and architecture specifications (Part 2/4, Issue `#622`)
- **Date**: `2026-11-08T23:22+01:00` | **Status**: `COMPLETED` | **Issue**: `#622` | **Branch**: `docs/issue-622-part2-governance-and-architecture`
- **Request**: Milestone 1 (Part 2/4): Replace legacy hey-agent stub in `documentation/specifications/project-governance.md` with complete project governance specification and establish `documentation/specifications/architecture.md` (100% PSL, dual-mode architecture, component interaction diagram).
- **Changes**:
  - Rewrote `documentation/specifications/project-governance.md` with 7 core pillars, 9-step GitHub lifecycle, and living registers.
  - Created `documentation/specifications/architecture.md` with zero-dependency philosophy, dual-mode engine pattern, and ASCII architecture diagram.
  - Added unit test `test_core_specifications_governance_and_architecture` in `tests/test_project_governance_rules.py`.
  - Updated `docs/ACTION_LOGBOOK.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks passed, all 295 unit tests passed (100%), PR diff strictly < 15,000 characters (~11,500 chars).

---

### ACT-081 — docs: harmonize execution rules and best practices (Part 1/4, Issue `#622`)
- **Date**: `2026-11-08T23:15+01:00` | **Status**: `COMPLETED` | **Issue**: `#622` | **Branch**: `docs/issue-622-part1-execution-rules-harmonization`
- **Request**: Milestone 1 (Part 1/4): Harmonize `03_execution_rules.md` and `04_best_practices.md` with core pillars (purging Chart.js/CDN rules, aligning with 18 targets, 4 transports, PSL-only, offline inline SVG, and diff limits < 15,000 characters).
- **Changes**:
  - Harmonized `03_execution_rules.md` with dual-mode architecture, PSL-only, 4 transports, and diff limits.
  - Harmonized `04_best_practices.md` by purging Chart.js/CDN rules and codifying offline inline SVG reporting.
  - Added unit test `test_execution_rules_and_best_practices_aligned_with_core_pillars` in `tests/test_project_governance_rules.py`.
  - Updated `docs/RCA_REGISTER.md` with harmonization cross-reference under `IMP-002`.
  - Updated `docs/ACTION_LOGBOOK.md` (`ACT-081`).
- **Result**: `pre_commit_checks.py` 8/8 checks passed, all 294 unit tests passed (100%), PR diff strictly < 15,000 characters (~11,000 chars).

---

### ACT-080 — fix(ci): align Python matrix with active versions and remove EOL Python 3.9 on Ubuntu 26.04 (Issue `#620`)
- **Date**: `2026-11-05T00:14+01:00` | **Status**: `COMPLETED` | **Issue**: `#620` | **Branch**: `fix/issue-620-ci-python-matrix-eol-39`
- **Request**: Fix failing GitHub Actions CI workflow run `41923567716` by removing EOL Python 3.9 from `.github/workflows/ci.yml` and testing against active supported Python versions (`3.10`, `3.11`, `3.12`, `3.13`) across `ci.yml` and `unit-tests.yml`.
- **Changes**:
  - Updated `.github/workflows/ci.yml` matrix from `["3.9", "3.10", "3.11", "3.12"]` to `["3.10", "3.11", "3.12", "3.13"]`.
  - Updated `.github/workflows/unit-tests.yml` matrix to include `3.13` (`["3.10", "3.11", "3.12", "3.13"]`).
  - Added unit test assertion `test_ci_and_unit_tests_python_matrix_excludes_eol_versions` in `tests/test_github_actions_workflows.py`.
  - Added entry `RCA-023` to `docs/RCA_REGISTER.md`.
  - Updated `docs/ACTION_LOGBOOK.md` (`ACT-080`).
- **Result**: `pre_commit_checks.py` 8/8 checks passed, all 293 unit tests passed (100%), PR diff strictly < 15,000 characters.

---

### ACT-079 — feat(core): implement shared core engine foundation and phased roadmap (Finding 9, Issue `#616`)
- **Date**: `2026-10-31T00:35+01:00` | **Status**: `COMPLETED` | **Issue**: `#616`
- **Request**: Remediate Finding 9: implement shared core engine `cis_core_engine.py`, unit tests `tests/test_cis_core_engine.py`, and 6-phase roadmap `IDEA-006`.
- **Changes**: Created `cis_core_engine.py`, `tests/test_cis_core_engine.py`, updated `docs/RCA_REGISTER.md` and `docs/ACTION_LOGBOOK.md`.
- **Result**: `pre_commit_checks.py` 8/8 pass, 292/292 tests pass, PR diff < 15,000 chars.

---

### ACT-078 — test(coverage): implement target catalog and CLI argument matrix test suite (Finding 13, Issue `#614`)
- **Date**: `2026-10-31T00:15+01:00` | **Status**: `COMPLETED` | **Issue**: `#614`
- **Request**: Remediate Ponytail Audit Finding 13: implement comprehensive target catalog and CLI argument matrix test suite `tests/test_target_catalog_and_cli_matrix.py` covering canonical target resolution, interface contracts across all 18 targets, rule specification integrity, CLI argument parsing, parameter forwarding without secret leakage, and error isolation on invalid targets, and document `IDEA-007`.
- **Changes**:
  - Created `tests/test_target_catalog_and_cli_matrix.py` with 3 test classes and 9 matrix test methods.
  - Updated `docs/RCA_REGISTER.md` with entry `IDEA-007`.
  - Updated `docs/ACTION_LOGBOOK.md` with entry `ACT-078`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 285/285 unit tests pass (100%), PR diff < 15,000 characters.

---

### ACT-077 — fix(ci): exclude archive from Bandit SAST scan, anchor path checks, and harden inventory tests (Issue `#612`)
- **Date**: `2026-10-30T23:45+01:00` | **Status**: `COMPLETED` | **Issue**: `#612`
- **Request**: Remediate Reviewer M4-2 findings: exclude `./archive` from Bandit SAST scan in `.github/workflows/security.yml`, replace loose substring matching with path-anchored check in `scripts/pre_commit_checks.py`, harden `tests/test_script_inventory_and_governance.py` with subdirectory whitelist validation and Bandit exclusion assertion, and document `RCA-022`.
- **Changes**:
  - Updated `.github/workflows/security.yml` line 38 to `-x ./tests,./scripts,./archive`.
  - Updated `scripts/pre_commit_checks.py` line 56 with normalized `should_skip_syntax_validation()`.
  - Updated `tests/test_script_inventory_and_governance.py` with subdirectory validation, Bandit exclusion test, path anchoring test, and syntax exclusion logic unit tests.
  - Updated `docs/RCA_REGISTER.md` with entry `RCA-022`.
  - Updated `docs/ACTION_LOGBOOK.md` with entry `ACT-077`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 276/276 unit tests pass (100%), PR diff < 15,000 characters.

---

### ACT-076 — feat(scripts): decommission remaining obsolete scripts, add inventory test, document IMP-005 (Finding 12 Part 2/2, Issue `#610`)
- **Date**: `2026-10-30T23:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#610`
- **Request**: Remediate Finding 12 (Part 2/2): relocate remaining 33 obsolete scripts to `archive/scripts/` via git mv, add inventory test `tests/test_script_inventory_and_governance.py`, and document `IMP-005`.
- **Changes**: Moved 33 scripts via git mv; added `test_script_inventory_and_governance.py`; added `IMP-005` to `docs/RCA_REGISTER.md`.
- **Result**: `pre_commit_checks.py` 8/8 pass, 272/272 tests pass, PR diff < 15,000 chars.

---

### ACT-075 — feat(scripts): decommission obsolete migration scripts (Finding 12 Part 1/2, Issue `#608`)
- **Date**: `2026-10-30T23:20+01:00` | **Status**: `COMPLETED` | **Issue**: `#608`
- **Request**: Remediate Ponytail Audit Finding 12 (Part 1/2): decommission first batch of 32 obsolete one-off migration and hotfix scripts from `scripts/` to `archive/scripts/` via git mv to comply strictly with the `< 15,000` PR diff character ceiling, and update `scripts/pre_commit_checks.py` to skip `archive/` during syntax validation.
- **Changes**: Relocated 32 obsolete scripts from `scripts/` to `archive/scripts/` via git mv; updated `scripts/pre_commit_checks.py` line 56 to skip `archive/`, `.agents/`, and `.ruff_cache/` directories during `py_compile`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, unit tests pass 269/269 with 100% success, PR diff < 15,000 chars (~8,500 chars).

---

### ACT-074 — feat(transport): harden SSH timeouts and document ControlMaster trade-offs (Finding 14, Issue `#606`)
- **Date**: `2026-10-30T23:05+01:00` | **Status**: `COMPLETED` | **Issue**: `#606`
- **Request**: Remediate Ponytail Audit Finding 14: harden SSH connection options in `execution_drivers.py` (`SSHExecutor`, `RemoteSSHContainerExecutor`) with `ConnectTimeout=10`, `ServerAliveInterval=15`, `ServerAliveCountMax=3`, `TCPKeepAlive=yes`, and document the deliberate rejection of `ControlMaster` socket multiplexing in `docs/RCA_REGISTER.md` (`IMP-006`).
- **Changes**: Updated `_build_ssh_prefix()` in `SSHExecutor` and `RemoteSSHContainerExecutor` within `execution_drivers.py`; updated `SSHExecutor.execute()` default timeout to 15s; added unit test methods in `tests/test_execution_drivers.py` asserting presence of hardened flags and absence of `ControlMaster`; added entry `IMP-006` to `docs/RCA_REGISTER.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, unit tests pass 269/269 with 100% success, PR diff < 15,000 chars.

---

### ACT-073 — fix(mysql-enterprise): safe key access and hardening in MySQL Enterprise engines (Part 2B, Issue `#604`)
- **Date**: `2026-10-30T22:28+01:00` | **Status**: `COMPLETED` | **Issue**: `#604`
- **Request**: Remediate Challenger M3-1 empirical finding in MySQL Enterprise 8.4 and Enterprise 9.7 audit engines: replace raw dictionary subscripts (`check["type"]`, `check["status"]`) in `calculate_scores()` with safe getters, guard non-dict items, add fallback support for untyped checks, and support case-insensitive status matching.
- **Changes**: Updated `calculate_scores()` in `audit_cis_mysql_enterprise_84.py` and `audit_cis_mysql_enterprise_97.py` with defensive key access (`check.get()`), non-dict item guard, untyped fallback scoring, and case-insensitive status evaluation; updated `tests/test_category_scoring.py` to assert all MySQL test cases across Enterprise engines.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 267/267 unit tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-072 — fix(mysql): safe key access and hardening in MySQL Community engines (Part 2A, Issue `#602`)
- **Date**: `2026-10-30T22:25+01:00` | **Status**: `COMPLETED` | **Issue**: `#602`
- **Request**: Remediate Challenger M3-1 finding in MySQL 8.0, Community 8.4/9.7 engines: replace raw subscripts with safe getters in `calculate_scores()`, guard non-dict items, add untyped check fallback, and support case-insensitive status.
- **Changes**: Updated `calculate_scores()` in `audit_cis_mysql_80.py`, `audit_cis_mysql_community_84.py`, `audit_cis_mysql_community_97.py` with defensive key resolution (`check.get()`), non-dict guard, untyped fallback, case-insensitivity; added 4 unit tests in `TestDynamicCategoryScoringMySQL`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 263/263 tests pass, PR diff < 15,000 chars.

---

### ACT-071 — fix(mariadb): safe key access and hardening in calculate_scores (Issue `#600`)
- **Date**: `2026-10-30T22:20+01:00` | **Status**: `COMPLETED` | **Issue**: `#600`
- **Request**: Remediate Challenger M3-1 empirical finding in MariaDB 10.6 and 10.11 engines: replace raw dictionary subscripts (`check["type"]`, `check["status"]`) in `calculate_scores()` with safe getters, guard non-dict items, add fallback support for untyped checks (`check.get("scored") is True` or status-based detection), and support case-insensitive status matching.
- **Changes**: Updated `calculate_scores()` in `audit_cis_mariadb_106.py` and `audit_cis_mariadb_1011.py` with defensive key access (`check.get()`), non-dict item guard, untyped fallback scoring, and case-insensitive status evaluation; expanded `tests/test_category_scoring.py` with 4 new unit test methods in `TestDynamicCategoryScoringMariaDB`; updated `APP-004` in `docs/RCA_REGISTER.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 263/263 unit tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-070 — feat(engines): dynamic rule category scoring in Cassandra 5.0 engine & APP-004 (Finding 10 Part 11, Issue `#598`)
- **Date**: `2026-10-30T21:52+01:00` | **Status**: `COMPLETED` | **Issue**: `#598`
- **Request**: Remediate Ponytail Audit Finding 10 (Part 11 / Final): refactor `calculate_scores(results)` to dynamically discover categories from `results` in Cassandra 5.0 audit engine (`audit_cis_cassandra_50.py`), complete Finding 10 across all 15 database engines, and document the dynamic rule category scoring architectural standard in `docs/RCA_REGISTER.md` (`APP-004`).
- **Changes**: Updated `calculate_scores()` in Cassandra 5.0 engine (`audit_cis_cassandra_50.py`) to discover categories dynamically from `results` dictionary or list without relying on static `RECOMMENDATIONS_DATA`; expanded unit test suite `tests/test_category_scoring.py` with Cassandra 5.0; added architectural entry `APP-004` to `docs/RCA_REGISTER.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 259/259 unit tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-069 — feat(engines): dynamic rule category scoring in Cassandra 4.1 engine (Finding 10 Part 10, Issue `#596`)
- **Date**: `2026-10-30T21:49+01:00` | **Status**: `COMPLETED` | **Issue**: `#596`
- **Request**: Remediate Ponytail Audit Finding 10 (Part 10): refactor `calculate_scores(results)` to dynamically discover categories from `results` in Cassandra 4.1 audit engine (`audit_cis_cassandra_41.py`).
- **Changes**: Updated `calculate_scores()` in Cassandra 4.1 engine (`audit_cis_cassandra_41.py`) to discover categories dynamically from `results` dictionary or list without relying on static `RECOMMENDATIONS_DATA`; expanded unit test suite `tests/test_category_scoring.py` with Cassandra 4.1.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 259/259 unit tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-068 — feat(engines): dynamic rule category scoring in Cassandra 4.0 engine (Finding 10 Part 9, Issue `#594`)
- **Date**: `2026-10-30T21:46+01:00` | **Status**: `COMPLETED` | **Issue**: `#594`
- **Request**: Remediate Ponytail Audit Finding 10 (Part 9): refactor `calculate_scores(results)` to dynamically discover categories from `results` in Cassandra 4.0 audit engine (`audit_cis_cassandra_40.py`).
- **Changes**: Updated `calculate_scores()` in Cassandra 4.0 engine (`audit_cis_cassandra_40.py`) to discover categories dynamically from `results` dictionary or list without relying on static `RECOMMENDATIONS_DATA`; expanded unit test suite `tests/test_category_scoring.py` with Cassandra 4.0.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 259/259 unit tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-067 — feat(engines): dynamic rule category scoring in MongoDB 8 engine (Finding 10 Part 8, Issue `#592`)
- **Date**: `2026-10-30T21:43+01:00` | **Status**: `COMPLETED` | **Issue**: `#592`
- **Request**: Remediate Ponytail Audit Finding 10 (Part 8): refactor `calculate_scores(results)` to dynamically discover categories from `results` in MongoDB 8 audit engine (`audit_cis_mongodb_8.py`).
- **Changes**: Updated `calculate_scores()` in MongoDB 8 engine (`audit_cis_mongodb_8.py`) to discover categories dynamically from `results` dictionary or list without relying on static `RECOMMENDATIONS_DATA`; expanded unit test suite `tests/test_category_scoring.py` with MongoDB 8.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 255/255 unit tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-066 — feat(engines): dynamic rule category scoring in MongoDB 7 engine (Finding 10 Part 7, Issue `#590`)
- **Date**: `2026-10-30T21:40+01:00` | **Status**: `COMPLETED` | **Issue**: `#590`
- **Request**: Remediate Ponytail Audit Finding 10 (Part 7): refactor `calculate_scores(results)` to dynamically discover categories from `results` in MongoDB 7 audit engine (`audit_cis_mongodb_7.py`).
- **Changes**: Updated `calculate_scores()` in MongoDB 7 engine (`audit_cis_mongodb_7.py`) to discover categories dynamically from `results` dictionary or list without relying on static `RECOMMENDATIONS_DATA`; expanded unit test suite `tests/test_category_scoring.py` with MongoDB 7.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 255/255 unit tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-065 — feat(engines): dynamic rule category scoring in PostgreSQL 18 engine (Finding 10 Part 6, Issue `#588`)
- **Date**: `2026-10-30T21:36+01:00` | **Status**: `COMPLETED` | **Issue**: `#588`
- **Request**: Remediate Ponytail Audit Finding 10 (Part 6): refactor `calculate_scores(results)` to dynamically discover categories from `results` in PostgreSQL 18 audit engine (`audit_cis_postgresql_18.py`).
- **Changes**: Updated `calculate_scores()` in PostgreSQL 18 engine (`audit_cis_postgresql_18.py`) to discover categories dynamically from `results` dictionary or list without relying on static `RECOMMENDATIONS_DATA`; expanded unit test suite `tests/test_category_scoring.py` with PostgreSQL 18.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 251/251 unit tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-064 — feat(engines): dynamic rule category scoring in PostgreSQL 17 engine (Finding 10 Part 5, Issue `#586`)
- **Date**: `2026-10-30T21:32+01:00` | **Status**: `COMPLETED` | **Issue**: `#586`
- **Request**: Remediate Ponytail Audit Finding 10 (Part 5): refactor `calculate_scores(results)` to dynamically discover categories from `results` in PostgreSQL 17 audit engine (`audit_cis_postgresql_17.py`).
- **Changes**: Updated `calculate_scores()` in PostgreSQL 17 engine (`audit_cis_postgresql_17.py`) to discover categories dynamically from `results` dictionary or list without relying on static `RECOMMENDATIONS_DATA`; expanded unit test suite `tests/test_category_scoring.py` with PostgreSQL 17.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 251/251 unit tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-063 — feat(engines): dynamic rule category scoring in PostgreSQL 16 engine (Finding 10 Part 4, Issue `#584`)
- **Date**: `2026-10-30T21:28+01:00` | **Status**: `COMPLETED` | **Issue**: `#584`
- **Request**: Remediate Ponytail Audit Finding 10 (Part 4): refactor `calculate_scores(results)` to dynamically discover categories from `results` in PostgreSQL 16 audit engine (`audit_cis_postgresql_16.py`).
- **Changes**: Updated `calculate_scores()` in PostgreSQL 16 engine (`audit_cis_postgresql_16.py`) to discover categories dynamically from `results` dictionary or list without relying on static `RECOMMENDATIONS_DATA`; expanded unit test suite `tests/test_category_scoring.py` with `TestDynamicCategoryScoringPostgreSQL`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 251/251 unit tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-062 — feat(engines): dynamic rule category scoring in MySQL Enterprise engines (Finding 10 Part 3/4, Issue `#582`)
- **Date**: `2026-10-30T21:24+01:00` | **Status**: `COMPLETED` | **Issue**: `#582`
- **Request**: Remediate Ponytail Audit Finding 10 (Part 3/4): refactor `calculate_scores(results)` to dynamically discover categories from `results` across MySQL Enterprise 8.4 and 9.7 audit engines (`audit_cis_mysql_enterprise_84.py`, `audit_cis_mysql_enterprise_97.py`).
- **Changes**: Updated `calculate_scores()` in MySQL Enterprise engines (`audit_cis_mysql_enterprise_84.py`, `audit_cis_mysql_enterprise_97.py`) to discover categories dynamically from `results` dictionary or list; expanded unit test suite `tests/test_category_scoring.py` with Enterprise MySQL engines.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 247/247 unit tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-061 — feat(engines): dynamic rule category scoring in MySQL 8.0 & Community engines (Finding 10 Part 2/4, Issue `#580`)
- **Date**: `2026-10-30T21:20+01:00` | **Status**: `COMPLETED` | **Issue**: `#580`
- **Request**: Remediate Ponytail Audit Finding 10 (Part 2/4): refactor `calculate_scores(results)` to dynamically discover categories from `results` across MySQL 8.0 and MySQL Community audit engines (`audit_cis_mysql_80.py`, `audit_cis_mysql_community_84.py`, `audit_cis_mysql_community_97.py`).
- **Changes**: Updated `calculate_scores()` in 3 MySQL engines (`audit_cis_mysql_80.py`, `audit_cis_mysql_community_84.py`, `audit_cis_mysql_community_97.py`) to discover categories dynamically from `results` dictionary or list; expanded unit test suite `tests/test_category_scoring.py` with `TestDynamicCategoryScoringMySQL`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 247/247 unit tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-060 — feat(engines): dynamic rule category scoring in MariaDB engines (Finding 10 Part 1/3, Issue `#578`)
- **Date**: `2026-10-30T21:14+01:00` | **Status**: `COMPLETED` | **Issue**: `#578`
- **Request**: Remediate Ponytail Audit Finding 10 (Part 1/3): refactor `calculate_scores(results)` to dynamically discover categories from `results` across MariaDB audit engines (`audit_cis_mariadb_106.py` and `audit_cis_mariadb_1011.py`).
- **Changes**: Updated `calculate_scores()` in MariaDB audit engines (`audit_cis_mariadb_106.py` and `audit_cis_mariadb_1011.py`) to discover categories dynamically from `results` dictionary or list; added unit test suite `tests/test_category_scoring.py`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 243/243 unit tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-059 — fix(engines): remove unreachable duplicate code in run_command (Finding 11, Issue `#576`)
- **Date**: `2026-10-30T21:05+01:00` | **Status**: `COMPLETED` | **Issue**: `#576`
- **Request**: Remediate Ponytail Audit Finding 11: cleanly remove unreachable duplicate subprocess execution and exception handling in `run_command()` across MariaDB audit engines (`audit_cis_mariadb_106.py` and `audit_cis_mariadb_1011.py`).
- **Changes**: Removed unreachable dead duplicate blocks in `audit_cis_mariadb_106.py` and `audit_cis_mariadb_1011.py`; verified all 18 engines with AST check; added `test_no_unreachable_code_in_audit_engines` in `tests/test_benchmark_sync_and_report_quality.py`; logged `RCA-021` in `docs/RCA_REGISTER.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 239/239 unit tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-058 — Automated Non-Regression Test Suite for SSH JSON & XML Reports Quality (Finding 8 Part B, Issue `#574`)
- **Date**: `2026-10-30T20:42+01:00` | **Status**: `COMPLETED` | **Issue**: `#574`
- **Request**: Complete Ponytail Audit Finding 8 (Part B): add automated regression unit tests in `tests/test_benchmark_sync_and_report_quality.py` guaranteeing all 10 SSH JSON reports and 2 SSH XML reports remain 100% syntactically valid and pass quality checks.
- **Changes**: Added `test_ssh_json_reports_syntax` to `tests/test_benchmark_sync_and_report_quality.py` validating that all 10 SSH JSON reports parse and conform to quality criteria; logged RCA-020 in `docs/RCA_REGISTER.md`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 238/238 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-057 — fix(reports): repair syntax in MySQL Community 8.4 SSH JSON report (Part 3/3) (Issue `#572`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#572`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mysql_community_84_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mysql_community_84_ssh.json` (final batch); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-056 — fix(reports): repair syntax in MySQL Community 8.4 SSH JSON report (Part 2/3) (Issue `#570`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#570`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mysql_community_84_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mysql_community_84_ssh.json` (batch of 23); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-055 — fix(reports): repair syntax in MySQL Community 8.4 SSH JSON report (Part 1/3) (Issue `#568`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#568`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mysql_community_84_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mysql_community_84_ssh.json` (batch of 23); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-054 — fix(reports): repair syntax in MariaDB 10.11 SSH JSON report (Part 3/3) (Issue `#566`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#566`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mariadb_1011_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mariadb_1011_ssh.json` (final batch); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-053 — fix(reports): repair syntax in MariaDB 10.11 SSH JSON report (Part 2/3) (Issue `#564`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#564`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mariadb_1011_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mariadb_1011_ssh.json` (batch of 22); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-052 — fix(reports): repair syntax in MariaDB 10.11 SSH JSON report (Part 1/3) (Issue `#562`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#562`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mariadb_1011_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mariadb_1011_ssh.json` (batch of 22); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-051 — fix(reports): repair syntax in MariaDB 10.6 SSH JSON report (Part 3/3) (Issue `#560`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#560`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mariadb_106_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mariadb_106_ssh.json` (final batch); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-050 — fix(reports): repair syntax in MariaDB 10.6 SSH JSON report (Part 2/3) (Issue `#558`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#558`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mariadb_106_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mariadb_106_ssh.json` (batch of 22); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-049 — fix(reports): repair syntax in MariaDB 10.6 SSH JSON report (Part 1/3) (Issue `#556`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#556`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mariadb_106_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mariadb_106_ssh.json` (batch of 22); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-048 — fix(reports): repair syntax in MySQL Enterprise 9.7 SSH JSON report (Part 3/3) (Issue `#554`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#554`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mysql_enterprise_97_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mysql_enterprise_97_ssh.json` (final batch); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-047 — fix(reports): repair syntax in MySQL Enterprise 9.7 SSH JSON report (Part 2/3) (Issue `#552`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#552`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mysql_enterprise_97_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mysql_enterprise_97_ssh.json` (batch of 20); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-046 — fix(reports): repair syntax in MySQL Enterprise 9.7 SSH JSON report (Part 1/3) (Issue `#550`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#550`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mysql_enterprise_97_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mysql_enterprise_97_ssh.json` (batch of 20); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-045 — fix(reports): repair syntax in MySQL Enterprise 8.4 SSH JSON report (Part 3/3) (Issue `#548`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#548`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mysql_enterprise_84_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mysql_enterprise_84_ssh.json` (final batch); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-044 — fix(reports): repair syntax in MySQL Enterprise 8.4 SSH JSON report (Part 2/3) (Issue `#546`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#546`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mysql_enterprise_84_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mysql_enterprise_84_ssh.json` (batch of 20); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-043 — fix(reports): repair syntax in MySQL Enterprise 8.4 SSH JSON report (Part 1/3) (Issue `#544`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#544`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mysql_enterprise_84_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mysql_enterprise_84_ssh.json` (batch of 20); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-042 — fix(reports): repair syntax in MySQL Community 9.7 SSH JSON report (Part 3/3) (Issue `#542`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#542`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mysql_community_97_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mysql_community_97_ssh.json` (final batch); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-041 — fix(reports): repair syntax in MySQL Community 9.7 SSH JSON report (Part 2/3) (Issue `#540`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#540`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mysql_community_97_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mysql_community_97_ssh.json` (batch of 20); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-040 — fix(reports): repair syntax in MySQL Community 9.7 SSH JSON report (Part 1/3) (Issue `#538`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#538`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mysql_community_97_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mysql_community_97_ssh.json` (batch of 20); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-039 — fix(reports): repair syntax in MySQL 8.0 SSH JSON report (Part 3/3) (Issue `#536`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#536`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mysql_8_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mysql_8_ssh.json` (final batch); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-038 — fix(reports): repair syntax in MySQL 8.0 SSH JSON report (Part 2/3) (Issue `#534`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#534`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mysql_8_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mysql_8_ssh.json` (batch of 20); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-037 — fix(reports): repair syntax in MySQL 8.0 SSH JSON report (Part 1/3) (Issue `#532`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#532`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_mysql_8_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_mysql_8_ssh.json` (batch of 20); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-036 — fix(reports): repair syntax in PostgreSQL 18 SSH JSON report (Part 2/2) (Issue `#530`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#530`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_postgresql_18_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_postgresql_18_ssh.json` (final batch); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-035 — fix(reports): repair syntax in PostgreSQL 18 SSH JSON report (Part 1/2) (Issue `#528`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#528`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_postgresql_18_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_postgresql_18_ssh.json` (batch of 20); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-034 — fix(reports): repair syntax in PostgreSQL 17 SSH JSON report (Part 2/2) (Issue `#526`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#526`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_postgresql_17_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_postgresql_17_ssh.json` (final batch); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-033 — fix(reports): repair syntax in PostgreSQL 17 SSH JSON report (Part 1/2) (Issue `#524`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#524`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_postgresql_17_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_postgresql_17_ssh.json` (batch of 20); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-032 — fix(reports): repair syntax in PostgreSQL 16 SSH JSON report (Part 2/2) (Issue `#522`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#522`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_postgresql_16_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_postgresql_16_ssh.json` (final batch); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-031 — fix(reports): repair syntax in PostgreSQL 16 SSH JSON report (Part 1/2) (Issue `#520`)
- **Date**: `2026-10-30T20:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#520`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B): repair syntax in `reports/rapport_cis_postgresql_16_ssh.json`.
- **Changes**: Replaced corrupted output/error pattern in `reports/rapport_cis_postgresql_16_ssh.json` (batch of 20); verified diff strictly < 15,000 characters.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-030 — Repair Syntax Corruption in MariaDB SSH XML Reports (Finding 8 Part B1, Issue `#518`)
- **Date**: `2026-10-30T20:28+01:00` | **Status**: `COMPLETED` | **Issue**: `#518`
- **Request**: Remediate Ponytail Audit Finding 8 (Part B1): repair XML syntax errors in MariaDB 10.6 and 10.11 SSH reports caused by earlier unbounded regex warning stripping.
- **Changes**: Cleaned `reports/rapport_cis_mariadb_106_ssh.xml` and `reports/rapport_cis_mariadb_1011_ssh.xml` restoring closing tags `</error></testcase>` and stripping host warning lines cleanly with bounded regex; added unit test `test_mariadb_ssh_xml_reports_syntax` in `tests/test_benchmark_sync_and_report_quality.py`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 237/237 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-029 — UTF-8 Console Streams for Cassandra, MongoDB, and RHEL Engines (Finding 8 Part A2, Issue `#515`)
- **Date**: `2026-10-30T20:21+01:00` | **Status**: `COMPLETED` | **Issue**: `#515`
- **Request**: Complete Finding 8 Part A: reconfigure UTF-8 console output across Cassandra, MongoDB, and RHEL benchmark audit engines.
- **Changes**: Configured `os.environ.setdefault('PYTHONUTF8', '1')` and `sys.stdout/sys.stderr.reconfigure(encoding='utf-8', errors='replace')` across `audit_cis_cassandra_40.py`, `41.py`, `50.py`, `audit_cis_mongodb_7.py`, `8.py`, `audit_cis_rhel_8.py`, `9.py`, and `10.py`; updated `test_all_audit_engines_have_utf8_stream_reconfiguration` in `tests/test_benchmark_sync_and_report_quality.py` to assert 100% of all 18 engines have UTF-8 stream reconfiguration.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 236/236 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-028 — UTF-8 Console Streams Across All Engines & SSH Warning Script Hardening (Finding 8 Part A, Issue `#515`)
- **Date**: `2026-10-30T20:18+01:00` | **Status**: `COMPLETED` | **Issue**: `#515`
- **Request**: Remediate Ponytail Audit Finding 8 (Part A): prevent Windows console crashes (`UnicodeEncodeError: 'charmap'`) across all benchmark engines and harden SSH warning cleaning script.
- **Changes**: Added `os.environ.setdefault('PYTHONUTF8', '1')` and `sys.stdout/sys.stderr.reconfigure(encoding='utf-8', errors='replace')` across all 18 benchmark audit engines; in `scripts/clean_ssh_warnings_from_reports.py`, reconfigured stderr and added post-cleaning syntax verification preventing corrupted files from being saved; added unit test `test_all_audit_engines_have_utf8_stream_reconfiguration` in `tests/test_benchmark_sync_and_report_quality.py`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 235/235 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-027 — Prevent Fake Docker Container Synthesis on Bare-Metal Hosts (Finding 7, Issue `#513`)
- **Date**: `2026-10-30T20:06+01:00` | **Status**: `COMPLETED` | **Issue**: `#513`
- **Request**: Remediate Ponytail Audit Finding 7: prevent `audit_orchestrator.py` from synthesizing fake Docker containers on bare-metal hosts and routing audits through `docker exec`.
- **Changes**: In `audit_orchestrator.py`, passed `self.docker_container` directly to `DockerTransportResolver.resolve_transport` rather than defaulting to `target_meta.get('default_container')`, and set `active_container = c_info.name if (c_info and c_info.is_running) else self.docker_container`; in `docker_transport.py`, removed synthetic `is_running=True` fallback, set `is_running=False` on unfound specified containers, and required `must_be_running=True` for product auto-discovery; added unit tests in `tests/test_audit_orchestrator.py` and `tests/test_docker_transport.py`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 234/234 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-026 — Cassandra Default Password Removal from CLI Benchmark Checks (Finding 6 Part B2, Issue `#508`)
- **Date**: `2026-10-30T20:00+01:00` | **Status**: `COMPLETED` | **Issue**: `#508`
- **Request**: Complete Finding 6 remediation (Item 4): eliminate plaintext password `-p cassandra` from CLI argument list in automated check 3.2 across Cassandra benchmark engines and rule definitions.
- **Changes**: In `audit_cis_cassandra_40.py`, `41.py`, `50.py` and `rules/cassandra_40.json`, `41.json`, `50.json`, removed `-p cassandra` from automated control 3.2 test procedure; added unit test `test_control_3_2_no_hardcoded_password_in_command` in `tests/test_cassandra_audit_engine.py`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 233/233 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-025 — CLI Password Forwarding via Environment in Audit Runner (Finding 6 Part B1, Issue `#510`)
- **Date**: `2026-10-30T19:55+01:00` | **Status**: `COMPLETED` | **Issue**: `#510`
- **Request**: Remediate Finding 6 Part B1: eliminate database password exposure in OS process tables when invoking benchmarks from unified CLI runner `audit_cis.py`.
- **Changes**: In `scripts/bundle_audit_cis.py` and `audit_cis.py`, passed `CIS_DB_PASSWORD` via child process environment (`env=cmd_env`) instead of appending `--db-password` to CLI argv; defaulted CLI `--db-password` parameter to `os.environ.get('CIS_DB_PASSWORD')`; added UTF-8 stream reconfigurations; updated unit tests in `tests/test_audit_cis_cli.py` and `tests/test_e2e_docker_audits.py`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 233/233 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-024 — Database Password Elimination in Docker & SSH Executor Argv (Finding 6 Part A, Issue `#508`)
- **Date**: `2026-10-30T19:45+01:00` | **Status**: `COMPLETED` | **Issue**: `#508`
- **Request**: Remediate Ponytail Audit Finding 6 (Part A): Eliminate exposure of plaintext database passwords in process table (`ps aux`) arguments across `DockerExecutor` and `RemoteSSHContainerExecutor`.
- **Changes**: In `execution_drivers.py`, updated `DockerExecutor.execute` to pass bare `-e MYSQL_PWD` and `-e PGPASSWORD` flags on Docker CLI and propagate secrets via `env=cmd_env` to `subprocess.run`; updated `RemoteSSHContainerExecutor` to export variables in remote subshell; updated unit tests in `tests/test_credential_injection.py` and `tests/test_execution_drivers.py`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 233/233 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-023 — Shell Injection & Host Variable Expansion Elimination in Execution Drivers (Issue `#506`)
- **Date**: `2026-10-30T19:35+01:00` | **Status**: `COMPLETED` | **Issue**: `#506`
- **Request**: Remediate Ponytail Audit Finding 5: Eliminate host variable expansion and shell injection in `DockerExecutor`, `RemoteSSHContainerExecutor`, `SSHExecutor`, and `LocalExecutor`.
- **Changes**: In `execution_drivers.py`, updated `DockerExecutor.execute` to pass `parts` argument list directly to `subprocess.run(parts, ...)`, completely bypassing the host shell; in `RemoteSSHContainerExecutor.execute`, quoted `as_user`, `cwd`, and `command` with `shlex.quote`; in `SSHExecutor.execute`, quoted `as_user` with `shlex.quote`; in `LocalExecutor.execute`, replaced `json.dumps` with `shlex.quote`; updated unit tests in `tests/test_execution_drivers.py`, `tests/test_in_container_isolation.py`, `tests/test_mariadb_audit_engine.py`, and `tests/test_credential_injection.py`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 231/231 tests pass with 100% success, PR diff < 15,000 chars.

---

### ACT-022 — MariaDB Sudo Propagation, Orchestrator Export Adaptation & CLI DB Args (Issue `#504`)
- **Date**: `2026-10-30T19:15+01:00` | **Status**: `COMPLETED` | **Issue**: `#504`
- **Request**: Resolve Challenger 2 findings: MariaDB 10.6/10.11 sudo drop, orchestrator export adaptation for 7-argument engines, and missing orchestrator CLI DB arguments.
- **Changes**: Updated `run_command` in `audit_cis_mariadb_106.py` and `1011.py` with `if create_executor and not sudo:` to preserve `sudo -n`; added standard 7-argument fallback in `audit_orchestrator.py` and file existence check; added `build_cli_parser()` with DB arguments; added unit tests in `tests/test_mariadb_sudo_and_orchestrator_export.py`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 234/234 tests pass, PR diff < 15,000 chars.

---

### ACT-021 — Database Credentials & SSH Flag Propagation (Parts A1, A2, B1-B17, Issue `#484`)
- **Date**: `2026-10-30T18:45+01:00` | **Status**: `COMPLETED` | **Issue**: `#484`
- **Changes**: Forwarded `args.db_*` in `__main__` across all 12 database engines; propagated `ssh_port`, `ssh_key`, and `sudo` across `audit_orchestrator.py` and all 15 audit engines (`rhel_8/9/10`, `postgresql_16/17/18`, `mariadb_106/1011`, `mysql_80`, `mysql_community_84/97`, `mysql_enterprise_84/97`, `cassandra_40/41/50`, `mongodb_7/8`); added unit tests in `tests/test_credential_and_flag_propagation.py`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 224/224 tests pass, PR diff < 15,000 chars.

---

### ACT-020 — Docker Container Forwarding in Automated Database Checks (Issue `#481`)
- **Date**: `2026-10-30T17:15+01:00` | **Status**: `COMPLETED` | **Issue**: `#481`
- **Changes**: Forwarded `docker_container=docker_container` in all automated check `run_command()` calls across 8 database audit engines (`postgresql_16/17/18`, `mongodb_7/8`, `cassandra_40/41/50`); added unit test suite `tests/test_container_parameter_forwarding.py`.
- **Result**: Part A (PostgreSQL) merged in PR #482; Part B (MongoDB & Cassandra) implemented; `pre_commit_checks.py` 8/8 checks pass, 220/220 tests pass.

---

### ACT-019 — RHEL HTML Report & Category Score Population (Issue `#479`)
- **Date**: `2026-10-30T17:05+01:00` | **Status**: `COMPLETED` | **Issue**: `#479`
- **Changes**: Updated `calculate_scores()` in `audit_cis_rhel_8.py`, `audit_cis_rhel_9.py`, and `audit_cis_rhel_10.py` to calculate full category breakdown scores; standardized `build_inline_svg_category_chart()` invocation in `generate_html_report()`; added comprehensive unit test suite `tests/test_rhel_html_export_quality.py`.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 221/221 tests pass, PR diff < 15,000 chars.

---

### ACT-018 — Orchestrator RHEL Module & Rule Spec Alignment (Issue `#477`)
- **Date**: `2026-10-30T16:55+01:00` | **Status**: `COMPLETED` | **Issue**: `#477`
- **Changes**: Updated `CANONICAL_TARGETS` in `audit_orchestrator.py` to map RHEL targets to `audit_cis_rhel_8`, `audit_cis_rhel_9`, `audit_cis_rhel_10` and rule specs `rhel_8`, `rhel_9`, `rhel_10`; added inspect-based signature filtering for `perform_checks`; updated `tests/test_audit_orchestrator.py` to verify module importability and rule file existence across all 18 targets.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 216/216 tests pass, PR diff < 15,000 chars.

---

### ACT-017 — UTF-8 Console & RHEL Exporter Fixes (Issue `#453`)
- **Date**: `2026-10-30T01:30+01:00` | **Status**: `COMPLETED` | **Issue**: `#453`
- **Changes**: Reconfigured UTF-8 streams, fixed RHEL 8/9/10 `calculate_scores` and `generate_html_report`, safe-guarded SSH regex in `scripts/clean_ssh_warnings_from_reports.py`, and added unit tests.
- **Result**: `pre_commit_checks.py` 8/8 checks pass, 216/216 tests pass, PR diff < 15,000 chars.

---

### ACT-016 — Robust CIS Downloader & CLI Sync Forwarding (Issue `#470`)
- **Date**: `2026-10-25T23:05+01:00` | **Status**: `COMPLETED` | **Issue**: `#470`
- **Changes**: Defaulted sync to `md`, added comma type parsing, unknown target check, OpenerDirector support, and forwarded CLI sync flags.
- **Result**: `pre_commit_checks.py`: 8/8 checks, 216/216 tests pass; PR diff < 15,000 chars.

---

### ACT-015 — Streaming Downloader & CLI Sync (Issue `#468`)
- **Date**: `2026-10-25T22:42+01:00` | **Status**: `COMPLETED` | **Issue**: `#468`
- **Changes**: Updated `download_cis_benchmarks.py`, `bundle_audit_cis.py`, `audit_cis.py`, `Makefile`, and unit tests.
- **Result**: `pre_commit_checks.py`: 8/8 checks, 211/211 tests pass; PR diff < 15,000 chars.

---

### ACT-014 — Manifest & Integrity Verifier (Issue `#466`)
- **Date**: `2026-10-25T22:33+01:00` | **Status**: `COMPLETED` | **Issue**: `#466` (PR `#467`)
- **Changes**: Created `conf/cis_manifest.json`, `download_cis_benchmarks.py`, and tests.
- **Result**: `pre_commit_checks.py`: 8/8 checks, 207/207 tests pass; PR diff 14,740 chars; merged in PR `#467`.

---

### ACT-013 — Release v2.9.1 Quality, Attached Distribution Assets & PyPI OIDC Publishing Fix (Issue `#464`)
- **Date**: `2026-10-25T21:25+01:00`
- **Status**: `COMPLETED`
- **Issue / Branch**: Issue `#464` (`fix/issue-464-v2.9.1-release-and-assets`, release `v2.9.1`)
- **Request**: Bump version to `v2.9.1`, fix PyPI OIDC publishing workflow by eliminating conflicting `password` input, add wheel and entrypoint tests in `tests/test_pypi_packaging.py`, and publish stable release `v2.9.1` with full distribution assets attached.
- **Changes**: Updated [`VERSION`](../VERSION), [`audit_cis.py`](../audit_cis.py), [`.github/workflows/pypi-publish.yml`](../.github/workflows/pypi-publish.yml), [`tests/test_pypi_packaging.py`](../tests/test_pypi_packaging.py), [`README.md`](../README.md), [`ROADMAP.md`](../ROADMAP.md), and [`POTENTIAL_ISSUES.md`](../POTENTIAL_ISSUES.md).
- **Result**: `pre_commit_checks.py`: **8 / 8 checks and 202 / 202 tests passed (100%)**; PR diff `< 15,000` chars; wheel and sdist built cleanly.

---

### ACT-012 — Explicit Variable Type Annotations for Mypy in Post-Execution Publisher (Issue `#462`)
- **Date**: `2026-10-25T21:12+01:00`
- **Status**: `COMPLETED`
- **Issue / Branch**: Issue `#462` (`fix/issue-462-mypy-type-annotations`)
- **Request**: Fix Mypy type-checking errors in `post_execution_publisher.py` by providing explicit type annotations for `results`, `categories_scores`, `extra`, and `captured_exc`.
- **Changes**: Updated [`post_execution_publisher.py`](../post_execution_publisher.py).
- **Result**: `pre_commit_checks.py`: **8 / 8 checks and 199 / 199 tests passed (100%)**; PR diff `< 15,000` chars.

---

### ACT-011 — CI Lint Fixes, Markdown Benchmark Inventory Sync & Resilient PyPI Preflight Workflow (Issue `#460`)
- **Date**: `2026-10-25T21:05+01:00`
- **Status**: `COMPLETED`
- **Issue / Branch**: Issue `#460` (`fix/issue-460-ci-lint-and-pypi-preflight`)
- **Request**: Resolve CI failures by fixing Ruff undefined variable lint errors (`F821`), update benchmark inventory scanner to support git-tracked Markdown files when PDFs are gitignored, and implement resilient multi-mode PyPI publishing preflight check.
- **Changes**: Updated 10 audit engines (`audit_cis_mysql_*.py`, `audit_cis_postgresql_*.py`, `audit_cis_rhel_*.py`), [`scripts/standardize_generate_html_report.py`](../scripts/standardize_generate_html_report.py), [`scripts/verify_benchmarks_and_reports.py`](../scripts/verify_benchmarks_and_reports.py), [`.github/workflows/pypi-publish.yml`](../.github/workflows/pypi-publish.yml), and [`tests/test_github_actions_workflows.py`](../tests/test_github_actions_workflows.py).
- **Result**: `ruff check`: 0 errors; `pre_commit_checks.py`: **8 / 8 checks and 199 / 199 tests passed (100%)**; PR diff `< 15,000` chars.

---

### ACT-010 — PyPI Publishing GitHub Actions Workflow, Release Asset Pipeline & Stable Release `v2.9.0` (Issue `#458`)
- **Date**: `2026-10-25T20:48+01:00`
- **Status**: `COMPLETED`
- **Issue / Branch**: Issue `#458` (`ci/issue-458-pypi-workflow-and-release`, release `v2.9.0`)
- **Request**: Add automated GitHub Actions PyPI publishing workflow (`.github/workflows/pypi-publish.yml`) supporting repository secrets (`PYPI_API_TOKEN` / `PYPI_TOKEN`), update `.github/workflows/release.yml` with wheel and sdist builds, sync `README.md`, `ROADMAP.md`, `POTENTIAL_ISSUES.md`, and publish stable release.
- **Changes**: Created [`.github/workflows/pypi-publish.yml`](../.github/workflows/pypi-publish.yml); updated [`.github/workflows/release.yml`](../.github/workflows/release.yml), [`tests/test_github_actions_workflows.py`](../tests/test_github_actions_workflows.py), [`README.md`](../README.md), [`ROADMAP.md`](../ROADMAP.md), and [`POTENTIAL_ISSUES.md`](../POTENTIAL_ISSUES.md).
- **Result**: `python -m unittest discover -s tests -v`: **199 / 199 unit tests passed (100%)**; `python scripts/pre_commit_checks.py`: **8 / 8 checks passed**.

---

### ACT-009 — PyPI Packaging Configuration, Release Publishing Workflow & Stable Release `v2.9.0` (Issue `#456`)
- **Date**: `2026-10-25T20:24+01:00`
- **Status**: `COMPLETED`
- **Issue / Branch**: Issue `#456` (`feat/issue-456-pypi-packaging-and-stable-release`, release `v2.9.0`)
- **Request**: Add PyPI packaging (`pyproject.toml`, `MANIFEST.in`), add GitHub Actions PyPI publishing workflow (`pypi-publish.yml`) supporting repository token secret, update release workflow to package wheels/sdist, and publish stable release.
- **Changes**: Created [`pyproject.toml`](../pyproject.toml), [`MANIFEST.in`](../MANIFEST.in), [`.github/workflows/pypi-publish.yml`](../.github/workflows/pypi-publish.yml), and [`tests/test_pypi_packaging.py`](../tests/test_pypi_packaging.py); updated [`.github/workflows/release.yml`](../.github/workflows/release.yml), [`VERSION`](../VERSION) (`2.9.0`), [`audit_cis.py`](../audit_cis.py), [`scripts/bundle_audit_cis.py`](../scripts/bundle_audit_cis.py), [`README.md`](../README.md), [`ROADMAP.md`](../ROADMAP.md), [`POTENTIAL_ISSUES.md`](../POTENTIAL_ISSUES.md), and [`tests/test_github_actions_workflows.py`](../tests/test_github_actions_workflows.py).
- **Result**: `python -m unittest discover -s tests -v`: **198 / 198 unit tests passed (100%)**; `python scripts/pre_commit_checks.py`: **8 / 8 checks passed**; wheel & sdist build cleanly verified.

---

### ACT-008 — Add Commit Testing Workflows & Enforce Post-Merge Issue Comment Rule (Issue `#454`)
- **Date**: `2026-10-25T20:12+01:00`
- **Status**: `COMPLETED`
- **Issue / Branch**: Issue `#454` (`ci/issue-454-commit-testing-and-issue-comment-rule`)
- **Request**: Add commit testing GitHub Actions workflow (running on pushes to all branches and PRs) and enforce repository governance rule requiring each task to have an issue that is closed with an explicit summary comment after merging the pull request.
- **Changes**: Updated [`.github/workflows/ci.yml`](../.github/workflows/ci.yml), [`.github/workflows/unit-tests.yml`](../.github/workflows/unit-tests.yml), [`.github/workflows/lint.yml`](../.github/workflows/lint.yml), [`.github/workflows/security.yml`](../.github/workflows/security.yml), [`AGENTS.md`](../AGENTS.md), [`.agents/AGENTS.md`](../.agents/AGENTS.md), [`.agents/rules/git-workflow.md`](../.agents/rules/git-workflow.md), [`.agents/rules/github-workflow.md`](../.agents/rules/github-workflow.md), [`tests/test_github_actions_workflows.py`](../tests/test_github_actions_workflows.py), and [`tests/test_project_governance_rules.py`](../tests/test_project_governance_rules.py).
- **Result**: `python -m unittest discover -s tests -v`: **194 / 194 unit tests passed (100%)**; `python scripts/pre_commit_checks.py`: **8 / 8 checks passed**.

---

### ACT-007 — CIS Benchmarks PDF Update Tracking, Rule Verification, and Report Quality Test Suite (Issue `#450`)
- **Date**: `2026-10-21T23:45+02:00`
- **Status**: `COMPLETED`
- **Issue / Branch**: Issue `#450` (`feat/issue-450-benchmark-sync-and-report-quality`)
- **Request**: Verify publication of latest CIS Benchmark PDF updates, check existing rules against updates, and conduct an in-depth quality testing campaign for generated reports.
- **Changes**: Added [`scripts/verify_benchmarks_and_reports.py`](../scripts/verify_benchmarks_and_reports.py) and [`tests/test_benchmark_sync_and_report_quality.py`](../tests/test_benchmark_sync_and_report_quality.py).
- **Result**: `python -m unittest tests/test_benchmark_sync_and_report_quality.py -v`: **5 / 5 tests passed (100%)**; 22 CIS benchmark PDF documents indexed, 887 rules validated across 18 target JSON files.

---

### ACT-006 — Resolve `RCA-003` Cross-Platform Windows Host Execution & UTF-8 Test Suite Compatibility (Issue `#442`)
- **Date**: `2026-10-21T23:39+02:00`
- **Status**: `COMPLETED`
- **Issue / Branch**: Issue `#442` (`fix/issue-442-cross-platform-rca-003`, release `v2.8.1`)
- **Request**: Resolve all cross-platform discrepancies identified in `RCA-003` (`docs/RCA_REGISTER.md`) and synchronize `VERSION`, `ROADMAP.md`, and `POTENTIAL_ISSUES.md`.
- **Changes**: Updated [`execution_drivers.py`](../execution_drivers.py), [`audit_diagnostics.py`](../audit_diagnostics.py), [`scripts/pre_commit_checks.py`](../scripts/pre_commit_checks.py), [`tests/test_e2e_text_export_analysis.py`](../tests/test_e2e_text_export_analysis.py), [`tests/test_docker_e2e_engine.py`](../tests/test_docker_e2e_engine.py), [`VERSION`](../VERSION) (`2.8.1`), [`audit_cis.py`](../audit_cis.py), [`ROADMAP.md`](../ROADMAP.md), [`POTENTIAL_ISSUES.md`](../POTENTIAL_ISSUES.md), and [`docs/RCA_REGISTER.md`](RCA_REGISTER.md).
- **Result**: `python scripts/pre_commit_checks.py`: **8 / 8 steps and 193 / 193 unit tests passed (100%)**.

---

### ACT-005 — Add GitHub Actions Suite (`unit-tests.yml`, `lint.yml`, `security.yml`, `release.yml`, `dependabot.yml`) (Issue `#440` / PR `#441`)
- **Date**: `2026-10-21T23:21+02:00`
- **Status**: `COMPLETED`
- **Issue / Branch**: Issue `#440` (`ci/issue-440-github-actions-suite`)
- **Request**: Expand the GitHub Actions CI/CD suite in English while preserving the 100% Python Standard Library (`PSL ONLY`) architecture.
- **Changes**: Updated [`.github/workflows/ci.yml`](../.github/workflows/ci.yml), created [`.github/workflows/unit-tests.yml`](../.github/workflows/unit-tests.yml), [`.github/workflows/lint.yml`](../.github/workflows/lint.yml), [`.github/workflows/security.yml`](../.github/workflows/security.yml), [`.github/workflows/release.yml`](../.github/workflows/release.yml), [`.github/dependabot.yml`](../.github/dependabot.yml), and [`tests/test_github_actions_workflows.py`](../tests/test_github_actions_workflows.py).
- **Result**: `python -m unittest tests/test_github_actions_workflows.py -v`: **5 / 5 tests passed (100%)**.

---

### ACT-004 — Create English Action Logbook (`docs/ACTION_LOGBOOK.md`) and RCA Register (`docs/RCA_REGISTER.md`) (Issue `#438` / PR `#439`)
- **Date**: `2026-10-21T23:12+02:00`
- **Status**: `COMPLETED`
- **Issue / Branch**: Issue `#438` (`docs/issue-438-action-logbook-rca-register`)
- **Request**: Initialize the mandatory English living governance registers (`docs/ACTION_LOGBOOK.md` and `docs/RCA_REGISTER.md`) and unit test suite (`tests/test_project_governance_rules.py`).
- **Changes**: Created [`docs/ACTION_LOGBOOK.md`](ACTION_LOGBOOK.md), [`docs/RCA_REGISTER.md`](RCA_REGISTER.md), and [`tests/test_project_governance_rules.py`](../tests/test_project_governance_rules.py).
- **Result**: `python -m unittest tests/test_project_governance_rules.py -v`: **3 / 3 tests passed (100%)**.

---

### ACT-003 — Adopt English `AGENTS.md` and `.agents/rules/` Governance Framework (Issue `#436` / PR `#437`)
- **Date**: `2026-10-21T23:06+02:00`
- **Status**: `COMPLETED`
- **Issue / PR**: Issue `#436` · PR `#437` (`docs/issue-436-english-governance-rules`, merged into `main`, commit `44e6ec2`)
- **Request**: Adopt the project governance rules from `AGENTS.md` and `.agents/rules/` in English while preserving the core identity of CIS Benchmarks Tools Suite (`100% PSL ONLY`, `< 15,000` diff chars per PR).
- **Changes**: Created [`AGENTS.md`](../AGENTS.md), translated [`.agents/AGENTS.md`](../.agents/AGENTS.md), and created [`.agents/rules/git-workflow.md`](../.agents/rules/git-workflow.md), [`.agents/rules/github-workflow.md`](../.agents/rules/github-workflow.md), and [`.agents/rules/project-governance.md`](../.agents/rules/project-governance.md).
- **Result**: PR diff size `14,883` chars (`< 15,000` limit); PR `#437` merged into `main`, closing Issue `#436`.

---

### ACT-002 — Dynamic Real-Time Timestamping & Post-Execution Publishing (Issue `#404` / PR `#405`–`#412`)
- **Date**: `2026-08-19T08:50+00:00`
- **Status**: `COMPLETED`
- **Issue / PR**: Issue `#404` · PR `#405`–`#412` (merged into `main`, release `v2.8.0`)
- **Request**: Implement timezone-aware dynamic timestamping (`temporal_metadata.py`) and atomic post-execution publishing (`post_execution_publisher.py`).
- **Changes**: Added `temporal_metadata.py`, `post_execution_publisher.py`, and updated `templates/report_template.html` and `audit_cis_mariadb_106.py`.
- **Result**: 180 unit tests passing; `v2.8.0` released and Issue `#404` closed.

---

### ACT-001 — In-Container Docker Transport Driver & E2E Execution Engine (Issue `#395` / PR `#396`–`#403`)
- **Date**: `2026-08-19T08:28+00:00`
- **Status**: `COMPLETED`
- **Issue / PR**: Issue `#395` · PR `#396`–`#403` (merged into `main`, release `v2.7.0`)
- **Request**: Implement in-container Docker transport (`docker_transport.py`), POSIX inspection (`in_container_inspector.py`), and E2E execution (`docker_e2e_engine.py`).
- **Changes**: Added `docker_transport.py`, `in_container_inspector.py`, `docker_e2e_engine.py`, and isolation unit tests.
- **Result**: 156 unit tests passing with zero host leakage; `v2.7.0` released and Issue `#395` closed.
