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
