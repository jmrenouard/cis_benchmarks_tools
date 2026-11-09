# Release Notes — CIS Benchmarks Tools Suite v2.10.0

**Release Tag:** `v2.10.0` | **Date:** November 2026 | **Stability:** Production / Enterprise Stable  
**Target Coverage:** 18 Benchmarks · 887 Audit Rules · 6 DB & OS Families · 4 Transport Tiers

---

## Executive Summary

CIS Benchmarks Tools Suite **v2.10.0** delivers enterprise readiness across the codebase (35 Python modules, ~25,600 lines, 100% PSL ONLY). Remediates all **12 Ponytail audit findings**, standardizes compliance scoring across 18 targets, eliminates credentials from process tables, purges dead CDN templates for offline inline SVG reports, and certifies test readiness with **314 passing unit tests**.

---

## Key Highlights & Remediations

- **1. Process Credential Protection (`Finding 1`)**: Database passwords are passed via child environment dictionaries (`MYSQL_PWD`, `PGPASSWORD`, `CIS_DB_PASSWORD`), preventing leakage in host `ps aux`.
- **2. Standardized Compliance Scoring (`Finding 3`)**: Harmonized all 18 targets to the official standard formula:

$$
\text{Score} = \frac{\text{Pass}}{\text{Pass} + \text{Fail}} \times 100
$$

Excludes `Manual`, `N/A`, and `Error` controls from denominator, preventing artificial score inflation.
- **3. Unified Execution Drivers & SSH (`Findings 5 & 11`)**: `SSHExecutor` applies `cwd`; sudo routes via `as_user="root"`; batched 4 container inspection probes into 1 round-trip.
- **4. Accurate RHEL Error Taxonomy (`Finding 4`)**: Exit codes `-1`, `126`, `127` classify as `ERROR` instead of false `FAIL`; manual checks evaluate to `MANUAL`; `None`-safe checks.
- **5. Manual Control Deduplication (`Finding 2`)**: Eliminated redundant execution of manual checks in MariaDB and MySQL engines, halving SSH/Docker round-trips.
- **6. Portable Dashboards & Explicit Accounting (`Finding 6`)**: Replaced `file://` links with relative paths (`os.path.relpath`); tallies `N/A` explicitly.
- **7. Clean Bundling & Timeouts (`Findings 8 & 9`)**: Non-destructive version injection in `bundle_audit_cis.py`; timeouts require explicit `returncode == -1`.
- **8. Numeric Safety & Dead Code Cleanup (`Findings 10 & 12`)**: Anchored numeric regex checks (`^\s*(-?\d+)\s*$`); purged duplicate uncast branches in NoSQL engines.
- **9. 100% Offline SVG Reports (`Finding 7`)**: Purged dead CDN templates across all 18 engines; reports render offline inline SVG.

---

## Verification & Test Metrics
- **Automated Unit Tests:** **314 passed**, 0 failed, 1 skipped (live Docker probe optional per APP-001).
- **Pre-Commit Routine:** **8/8 validation checks PASSED** via `scripts/pre_commit_checks.py`.
- **PSL Compliance:** **100% Python Standard Library ONLY** (Zero external dependencies).
- **Certification:** Documented in `TEST_READY.md`.
