# 🗺️ CIS Benchmarks Tools - Strategic Roadmap & Backlog (v2.6.0)

This document outlines the strategic roadmap, architecture principles, phase-level milestones, and task-level execution status for the CIS Benchmarks Tools suite.

---

## 🔒 Governance & Core Standards

> [!NOTE]
> All development, git release lifecycles, PR size limits (< 15K diff chars), and Python Standard Library (PSL ONLY) enforcement rules strictly follow workspace governance defined in [.agents/AGENTS.md](file:///.agents/AGENTS.md).

---

## 📊 Executive Progress Dashboard (Phase Level)

| Phase        | Milestone Title                                                      | Target Version | Status        | Tasks | Progress |
| :-------------| :---------------------------------------------------------------------| :--------------:| :-------------:| :-----:| :--------:|
| **Phase 1**  | Consolidation & Baseline Standardization                             | `v1.0.0`       | `Completed ✅` | 5/5   | 100%     |
| **Phase 2**  | Unified Audit Engine & PSL Modularization                            | `v1.2.5`       | `Completed ✅` | 13/13 | 100%     |
| **Phase 3**  | Linux System Extensions, Multi-Language & Security                   | `v1.5.0`       | `Completed ✅` | 5/5   | 100%     |
| **Phase 4**  | Multi-Format Exporters, E2E Testing & CI/CD Pipeline                 | `v1.6.0`       | `Completed ✅` | 7/7   | 100%     |
| **Phase 5**  | Rule Spec Externalization & Offline SVG Charts Engine                | `v1.7.0`       | `Completed ✅` | 5/5   | 100%     |
| **Phase 6**  | PR Diff Size Limits & Centralized HTML Templates                     | `v1.8.0`       | `Completed ✅` | 4/4   | 100%     |
| **Phase 7**  | Dual Local/SSH Modes & Database Connection Parameters                | `v1.9.0`       | `Completed ✅` | 5/5   | 100%     |
| **Phase 8**  | Advanced Formatting, Rule Exclusions & Visual UI Validation          | `v2.0.0`       | `Completed ✅` | 7/7   | 100%     |
| **Phase 9**  | Verification Commands & Remediation Procedures in Reports            | `v2.1.0`       | `Completed ✅` | 4/4   | 100%     |
| **Phase 10** | MariaDB Zero-Error Engine, Docker Auto-Routing & Manual Automation   | `v2.2.0`       | `Completed ✅` | 5/5   | 100%     |
| **Phase 11** | Universal Product Hardening, Docker Auto-Routing & Info Maximization | `v2.3.0`       | `Completed ✅` | 6/6   | 100%     |
| **Phase 12** | Traçabilité Git Stricte, Revues Sourcery AI & Qualité Industrielle    | `v2.3.0`       | `Completed ✅` | 5/5   | 100%     |
| **Phase 13** | Universal Credential Injection, Multi-Distro Packages & Rule 1.5 Sync| `v2.4.0`       | `Completed ✅` | 5/5   | 100%     |
| **Phase 14** | 100% Deterministic Rule Automation & Expanded Test Suite Coverage    | `v2.4.1`       | `Completed ✅` | 6/6   | 100%     |
| **Phase 15** | Error Masking Elimination (`2>/dev/null`) & Engine Resilience        | `v2.4.2`       | `Completed ✅` | 6/6   | 100%     |
| **Phase 16** | Authentic CIS Spec Rule Sync & Zero Command Errors Guarantee         | `v2.5.0`       | `Completed ✅` | 6/6   | 100%     |
| **Phase 17** | Automated E2E Text Export Generation, Parsing & Real-Time Analysis   | `v2.6.0`       | `Completed ✅` | 6/6   | 100%     |
| **Phase 18** | Dedicated Docker Audit Execution & MySQL 8.0 Full Automation         | `v2.6.2`       | `Completed ✅` | 4/4   | 100%     |
| **Phase 19** | Context-Separated Execution & Systematic Audit Logging             | `v2.6.3`       | `Completed ✅` | 4/4   | 100%     |


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

### Phase 10: MariaDB Zero-Error Engine, Docker Auto-Routing & Manual Automation (`Completed ✅ - v2.2.0`)
**Summary**: Fix all syntax, command, and client errors in MariaDB audit scripts, implement automated Docker container detection and routing, and maximize automated information extraction for manual checks.

#### 10.1 MariaDB Command & SQL Fixes
- [x] **Dual Client Compatibility (`mariadb` / `mysql`)**: Support both binary clients with automatic fallback.
- [x] **Dynamic Path Resolution**: Resolve dynamic datadir and plugin directory paths via multi-command fallback chains.
- [x] **Single-Line Multi-Statement Handling**: Format SQL queries to avoid syntax errors in non-interactive batch mode.

#### 10.2 Docker Auto-Routing Engine
- [x] **Automatic Container Detection**: Auto-detect running database containers (`cis_mariadb_106`, `cis_mariadb_1011`, etc.) when executing audits in local mode.
- [x] **Transparent `docker exec` Execution**: Route host commands into target containers seamlessly without requiring manual `--docker` CLI arguments.

#### 10.3 Manual Checks Maximization & Automation
- [x] **Helper Command Ingestion**: Run OS and DB commands on manual review items to gather diagnostic data automatically for the auditor.
- [x] **Guidance Panel in Reports**: Display dedicated manual validation guides with step-by-step checklists in HTML reports.

---

### Phase 11: Universal Product Hardening, Docker Auto-Routing & Info Maximization (`Completed ✅ - v2.3.0`)
**Summary**: Propagate MariaDB engine enhancements, zero-error handling, and transparent container routing across all remaining target engines (MySQL, PostgreSQL, MongoDB, Cassandra).

#### 11.1 MySQL Suite Hardening (8.0, Community 8.4/9.7, Enterprise 8.4/9.7)
- [x] **MySQL Auto-Routing & Client Detection**: Implement automated container detection and socket error resilience.
- [x] **Command Precedence**: Ensure technical errors (`ERROR 1045`, `ERROR 2002`, `127`) are explicitly distinguished from security non-compliances.

#### 11.2 PostgreSQL Suite Hardening (16, 17, 18)
- [x] **PostgreSQL Socket & `psql` Execution**: Automate container-routed `psql` execution with `postgres` user credentials.
- [x] **Manual Privileges Inspection**: Convert manual role/RLS inspection items into diagnostic queries.

#### 11.3 NoSQL Suite Hardening (MongoDB 7/8 & Cassandra 4.0/4.1/5.0)
- [x] **MongoDB `mongosh` Routing**: Auto-detect MongoDB containers and route JavaScript evaluation commands.
- [x] **Cassandra `cqlsh` Routing**: Auto-detect Cassandra containers and route CQL queries.

---

### Phase 12: Traçabilité Git Stricte, Revues Sourcery AI & Suivi de la Qualité Industrielle (`Completed ✅ - v2.3.0`)
**Summary**: Intégrer les revues de code automatisées Sourcery AI, formaliser le cycle de vie des PRs à 6 étapes, assainir les spécifications de commandes, préserver la télémétrie `stderr` sans masquage et assurer la séparation complète des 4 contextes d'exécution.

#### 12.1 Cycle de Vie Git & Règle Obligatoire Issue-PR (Validé PR #110, #112)
- [x] **Cycle de vie strict à 6 étapes** : Issue (`gh issue create`) -> Feature Branch (`git checkout -b`) -> PR atomique < 15K diff (`gh pr create`) -> Merge (`gh pr merge`) -> Commentaire & Fermeture Issue (`gh issue comment/close`) -> Synchronisation locale.
- [x] **Automatisation du cycle de vie GitHub** : Création d'un script PSL d'automatisation des ouvertures, merges et résolutions d'issues via GitHub REST API (PR #110).
- [x] **Gouvernance d'équipe dans `.agents/AGENTS.md`** : Inscription formelle des règles de diff max (<15 000 caractères) et de l'architecture Python Standard Library ONLY (PR #112).

#### 12.2 Télémétrie Diagnostique & Préservation Intégrale de `stderr` (Validé PR #128)
- [x] **Élimination systématique de `2>/dev/null`** : Nettoyage de l'ensemble des 18 fichiers `rules/*.json` pour éliminer le masquage des erreurs système et autoriser l'affichage transparent des codes d'erreur.
- [x] **Exécution non bloquante en sous-processus** : Utilisation de `stdin=subprocess.DEVNULL` au niveau Python pour prévenir les blocages interactifs sans supprimer les flux d'erreur bruts.

#### 12.3 Classification des 4 Contextes & Taxonomie 5 États (Validé PR #114, #116, #118, #120)
- [x] **Moteur `detect_execution_context()`** : Catégorisation formelle en 4 contextes (`LOCAL_BAREMETAL`, `LOCAL_DOCKER`, `REMOTE_SSH_BAREMETAL`, `REMOTE_SSH_DOCKER`) avec suite de tests dédiés `tests/test_execution_context.py` (PR #116).
- [x] **Taxonomie des 5 états de contrôle** : Distinction formelle entre `Pass` (Conforme), `Fail` (Non-conforme), `Error` / `Erreur Commande` (Échec technique), `Manual` (Revue procédurale) et `Not Applicable` (PR #114, #118).
- [x] **Tableau de bord HTML à 5 cartes** : Ajout de la carte `Échecs d'exécution technique` (`border-l-orange-500`) et liaison de la variable `error_count` dans SafeDict (PR #120).

#### 12.4 Assainissement des Spécifications JSON & Garde Moteur (Validé PR #122, #124, #126)
- [x] **Garde d'exécution `is_valid_executable_command()`** : Validation dynamique empêchant l'exécution shell accidentelle de phrases descriptives en langage naturel (PR #124).
- [x] **Élimination des erreurs de syntaxe bash** : Élimination des apostrophes et textes non protégés provoquant des `unexpected EOF` dans les contrôles manuels (PR #124).
- [x] **Harmonisation des en-têtes & élimination des doublons** : Correction des titres produits (`Rapport d'Audit CIS - <Produit>`), contextualisation des badges avec icônes FontAwesome et élimination des versions dupliquées (PR #122).
- [x] **Résolution des imports datetime RHEL** : Harmonisation des imports sur RHEL 8, 9, 10 (PR #126).

#### 12.5 Validations & Évolutions Issues des Revues Sourcery AI (Validé PR #70-#132)
- [x] **Sécurisation des sous-processus (PR #80, #84, #90)** : Élimination de `shell=True` au profit de listes d'arguments typées et sécurisation des appels Docker/SSH.
- [x] **Internationalisation i18n & documentation (PR #92, #94, #96)** : Traduction intégrale en anglais avec miroir français `README_fr.md` et support `--lang {en,fr}`.
- [x] **Architecture modulaire & Graphiques SVG natifs (PR #103, #105, #108)** : Externalisation des règles JSON et moteur vectoriel 100% hors-ligne sans Chart.js.
- [x] **Validation continue de la suite de tests** : 60/60 tests unitaires passés avec succès sous Python Standard Library uniquement (PR #131, #132).

---

### Phase 13: Universal Credential Injection, Multi-Distro Packages & Rule 1.5 Sync (`Completed ✅ - v2.4.0`)
**Summary**: Normalize command-line parameter options, inject database credentials into runtime environments, adapt package query commands across Linux distributions (`apt`, `dnf`/`yum`, `apk`), and standardize executable version checks for Rule 1.5.

#### 13.1 CLI Standardization & Database Credential Injection (PR #144, #146, #152)
- [x] **Normalized CLI Parameters**: Unify `--db-user`, `--db-password`, `--db-host`, `--db-port`, and `--db-name` across all 18 database target engines.
- [x] **Target Engine Environment Injection**: Map credentials directly to native database client variables (`MYSQL_PWD`, `PGPASSWORD`, `CQLSH_HOST`, etc.) in `run_command` and Docker execution.
- [x] **Unified CLI Parsing**: Support both short (`-u`, `-p`, `-H`, `-P`, `-d`) and long option flags uniformly.

#### 13.2 Multi-Distribution Package Detection & Remediation (PR #148, #156)
- [x] **Cross-Distro Package Inquiries**: Reconcile Rule 1.2 package verification for Debian (`dpkg`), RHEL/Fedora (`rpm`), and Alpine (`apk`).
- [x] **Executable Rule 1.5 Version Check**: Standardize SQL-based `SHOW server_version` queries replacing natural language.
- [x] **Distribution-Agnostic Remediation Guidance**: Recommend appropriate package management commands in audit reports (`apt purge`, `dnf erase`, `apk del`).

---

### Phase 14: 100% Deterministic Rule Automation & Expanded Test Suite Coverage (`Completed ✅ - v2.4.1`)
**Summary**: Convert all remaining manual controls across all database benchmark rule files into deterministic automated controls, sanitize NoneType stderr evaluation and truthy path handling, and expand automated test suite to 70 tests.

#### 14.1 Complete Rule Automation Across All Targets (PR #168-#196)
- [x] **Cassandra 4.0, 4.1 & 5.0 Automation (PR #168, #170)**: 100% automated controls with deterministic CQL queries.
- [x] **MongoDB 7 & 8 Automation (PR #172, #174)**: 100% automated controls with deterministic `mongosh` queries.
- [x] **MariaDB 10.6 & 10.11 Automation (PR #176, #178)**: 100% automated controls with deterministic SQL queries.
- [x] **PostgreSQL 16, 17 & 18 Automation (PR #180, #182, #184, #186, #188, #190)**: 100% automated controls across all categories.
- [x] **MySQL 8.0, 8.4 & 9.7 Automation (PR #192, #194, #196)**: 100% automated controls with zero command errors.

#### 14.2 Engine Resilience & Test Suite Expansion (PR #158, #198-#218)
- [x] **NoneType-Safe Evaluation**: Guard `evaluate_condition` against `None` values for `stdout` and `stderr`.
- [x] **Truthy Path Command Handling**: Replace `"path_command" in rec` with `rec.get("path_command")` to eliminate `NoneType` iterable errors.
- [x] **Expanded Test Suite (PR #158)**: 70 unit and E2E tests covering credential injection, package queries, rule syntax, AST PSL conformity, and Docker audits.
- [x] **Zero Command Error Guarantee**: 0 command errors (`Status Error: 0`) and 0 manual controls across all 18 targets in Docker mode.

---

### Phase 15: Error Masking Elimination (`2>/dev/null`), POSIX Conditions & Multi-Engine Resilience (`Completed ✅ - v2.4.2`)
**Summary**: Completely eliminate the `2>/dev/null` anti-pattern across all 18 rule JSON specifications and Python engine audit scripts, replacing silent error suppression with robust POSIX conditionals (`test -f`, `test -d`, `for` loops) and transparent exit-code/stderr diagnostics.

#### 15.1 Rule Specification Sanitization (PR #224-#244)
- [x] **MySQL & MariaDB Rule Sanitization (PR #224, #226, #232, #234, #236)**: Replace `2>/dev/null` error-masking with explicit file/directory conditional checks across MySQL 8.0, 8.4, 9.7 and MariaDB 10.6, 10.11.
- [x] **PostgreSQL, MongoDB & Cassandra Rule Sanitization (PR #228, #238, #240, #242)**: Replace `2>/dev/null` with POSIX conditionals across PostgreSQL 16/17/18, MongoDB 7/8, and Cassandra 4.0/4.1/5.0.
- [x] **RHEL OS Rule Sanitization (PR #244)**: Eliminate `2>/dev/null` across RHEL 8, 9, and 10 benchmarks.

#### 15.2 Audit Engine Refactoring & E2E Validation (PR #230, #246-#274)
- [x] **MySQL & MariaDB Engine Refactoring (PR #246, #248, #250, #252, #254, #256, #258, #260, #262, #264, #266)**: Remove `2>/dev/null` and deduplicate context detection in MySQL and MariaDB engines.
- [x] **PostgreSQL, MongoDB, Cassandra & RHEL Engine Refactoring (PR #268, #270, #272, #274)**: Remove `2>/dev/null` error suppression across all database and OS audit scripts.
- [x] **Continuous Zero-Error Verification (PR #230)**: Automated test asserting 0 manual and 0 error controls across all 18 targets with 71 passing tests.

---

### Phase 16: Authentic CIS Benchmark Specification Synchronization & Zero Command Errors Guarantee (`Completed ✅ - v2.5.0`)
**Summary**: Perform a 100% complete synchronization of all 18 benchmark JSON rule files with the authentic CIS markdown specifications in `CIS_DATA/`. Restores the exact distribution of 564 Automated and 323 Manual controls across 887 total rules, with guaranteed 0 command errors (`Status: Error == 0`) across all targets in Docker execution mode.

#### 16.1 MySQL Benchmark Rules Synchronization (PR #278, #280, #282, #284, #286, #288, #290, #292, #294)
- [x] **MySQL 8.0 CIS Rules Sync (PR #278, #280)**: Synchronize `rules/mysql_80.json` with authentic CIS v1.5.0 spec (45 Automated, 25 Manual).
- [x] **MySQL Community 8.4 CIS Rules Sync (PR #282, #284)**: Synchronize `rules/mysql_community_84.json` with authentic CIS v1.1.0 spec (48 Automated, 31 Manual).
- [x] **MySQL Enterprise 8.4 CIS Rules Sync (PR #286, #288)**: Synchronize `rules/mysql_enterprise_84.json` with authentic CIS v1.1.0 spec (44 Automated, 26 Manual).
- [x] **MySQL Community 9.7 CIS Rules Sync (PR #290)**: Synchronize `rules/mysql_community_97.json` with authentic CIS v1.0.0 spec (45 Automated, 25 Manual).
- [x] **MySQL Enterprise 9.7 CIS Rules Sync (PR #292, #294)**: Synchronize `rules/mysql_enterprise_97.json` with authentic CIS v1.0.0 spec (44 Automated, 26 Manual).

#### 16.2 MariaDB, PostgreSQL, MongoDB & Cassandra Rules Synchronization (PR #296-#320)
- [x] **MariaDB 10.6 & 10.11 CIS Rules Sync (PR #296, #298, #300, #302)**: Synchronize `rules/mariadb_106.json` (45 Auto, 29 Manual) and `rules/mariadb_1011.json` (45 Auto, 30 Manual).
- [x] **PostgreSQL 16, 17 & 18 CIS Rules Sync (PR #304, #306, #308, #310, #312, #314)**: Synchronize `rules/postgresql_16.json` (42 Auto, 29 Manual), `rules/postgresql_17.json` (43 Auto, 28 Manual), and `rules/postgresql_18.json` (43 Auto, 28 Manual).
- [x] **MongoDB 7 & 8 CIS Rules Sync (PR #316)**: Synchronize `rules/mongodb_7.json` and `rules/mongodb_8.json` (12 Auto, 11 Manual each).
- [x] **Cassandra 4.0, 4.1 & 5.0 CIS Rules Sync (PR #318, #320)**: Synchronize `rules/cassandra_40.json`, `rules/cassandra_41.json`, `rules/cassandra_50.json` (12 Auto, 8 Manual each).

#### 16.3 Test Suite & Quality Assurance (PR #322)
- [x] **Zero Command Error & CIS Distribution Verification (PR #322)**: Update `test_zero_command_errors_and_automation.py` and `test_mariadb_audit_engine.py` to validate exact authentic CIS manual counts per target and assert 0 command errors.
- [x] **Unified Audit Bundling & Release v2.5.0 (PR #324)**: Re-bundle `audit_cis.py` (v2.5.0) and run full pre-commit validation.

---

### Phase 17: Automated E2E Text Export Generation, Parsing & Real-Time Error Analysis (`Completed ✅ - v2.6.0`)
**Summary**: Harmonize `.txt` text exporters across all 18 benchmark audit engines to include clean ASCII summary tables, formatted control blocks, and structured headers. Add automated text report parsing and real-time execution error detection on every E2E execution, guaranteeing continuous zero command execution errors (`Error == 0`).

#### 17.1 Text Exporters Harmonization Across 18 Audit Engines (PR #326, #328, #330, #332, #334, #336)
- [x] **MySQL Text Exporters (PR #326, #328)**: Harmonize text format exporter with ASCII summary tables across MySQL 8.0, Community 8.4, Enterprise 8.4, Community 9.7, Enterprise 9.7.
- [x] **MariaDB & PostgreSQL Text Exporters (PR #328, #330, #332)**: Harmonize text format exporter with ASCII summary tables across MariaDB 10.6, 10.11 and PostgreSQL 16, 17, 18.
- [x] **MongoDB, Cassandra & RHEL Text Exporters (PR #332, #334, #336)**: Harmonize text format exporter with ASCII summary tables across MongoDB 7, 8, Cassandra 4.0, 4.1, 5.0, and RHEL 8, 9, 10.

#### 17.2 Automated E2E Text Export Test Suite (PR #338)
- [x] **E2E Text Export Parsing & Verification Suite (PR #338)**: Implement `tests/test_e2e_text_export_analysis.py` validating that every audit engine generates valid `.txt` exports with header metrics, ASCII summary tables, 0 command errors, and authentic CIS manual distribution.
- [x] **Docker Integration Testing (PR #338)**: Add text format forwarding tests and live Docker execution tests in `tests/test_e2e_docker_audits.py`.

#### 17.3 E2E Test Runner & Real-Time Analysis Engine (PR #340, #342)
- [x] **Real-time Error Detection in E2E Runner (PR #340)**: Enhance `scripts/run_e2e_tests.py` with immediate text export parsing and zero-error verification upon report generation.
- [x] **Dynamic Versioning & Helper Scripts (PR #340)**: Update `scripts/analyze_e2e_reports.py` to dynamically load repository version from `VERSION` and add `scripts/enhance_txt_exporters.py`.
- [x] **Release v2.6.0 Finalization (PR #342)**: Bundle unified `audit_cis.py` (v2.6.0), synchronize documentation and release.

---

### Phase 18: Dedicated Docker Audit Execution & MySQL 8.0 Full Automation (`Completed ✅ - v2.6.2`)
**Summary**: Enhance MySQL 8.0 CIS audit execution when targeting Docker containers or local environments. Accurately detect execution context (`Local Docker (mysql80-test)`), forward database connection parameters (`db_user`, `db_password`, etc.) into all `run_command` invocations, harden `MYSQL_CMD` for container environments, clean dummy manual echoes in `rules/mysql_80.json`, and eliminate command execution errors.

#### 18.1 Rule Spec Sanitization & Minimal Environment Hardening (PR #344)
- [x] **Rule Spec Sanitization (PR #344)**: Clean dummy `echo 'Contrôle Manuel'` entries in `rules/mysql_80.json` (10 controls cleaned).
- [x] **Crontab Fallback Hardening (PR #344)**: Harden Rule 2.1.1 test procedure to check `/etc/crontab` and `ps -ef` gracefully when `crontab` binary is missing in minimal Docker containers (Part 1 of #343).

#### 18.2 Docker Execution Context & Database Parameter Routing (PR #345)
- [x] **Execution Context Detection & Reporting (PR #345)**: Call `detect_execution_context()` in `main()` and propagate context label (`Local Docker (mysql80-test)`) to HTML/JSON/XML report metadata.
- [x] **Database Parameter Forwarding (PR #345)**: Propagate `db_user`, `db_password`, `db_host`, `db_port`, `db_name`, `defaults_file`, and `auth_db` into all `run_command(...)` invocations within `perform_checks()`.
- [x] **Client Command Resilience & Fallbacks (PR #345)**: Harden `MYSQL_CMD` with `--defaults-extra-file=/root/.my.cnf` and root container credentials fallback (closes #343).


### Phase 19: Context-Separated Execution & Systematic Audit Logging (`Completed ✅ - v2.6.3`)
**Summary**: Separate command execution into 3 distinct contexts (Local/SSH/Docker) with dedicated command sets per rule, and add a systematic logging system that generates a `.log` companion file alongside each audit report.

#### 19.1 Context-Aware Command Selection Engine (PR #347)
- [x] **`get_context_command()` function (PR #347)**: Selects `test_procedure_docker` / `test_procedure_ssh` / `test_procedure` based on execution context type (LOCAL_DOCKER, REMOTE_SSH_BAREMETAL, etc.).
- [x] **`perform_checks()` context integration (PR #347)**: Updated to accept `exec_context` parameter and resolve `pre_condition`, `path_command`, `test_procedure_template`, and `test_procedure` through context-aware lookup.

#### 19.2 Docker-Specific OS Command Variants (PR #348)
- [x] **OS command Docker variants (PR #348)**: Added `test_procedure_docker` for rules 1.4 and 1.7 (systemctl → ps, /proc/*/environ → env). MySQL client swaps not needed since `run_command()` handles `docker exec` wrapping.

#### 19.3 Systematic Audit Logging (PR #350)
- [x] **PSL logging module (PR #350)**: `setup_audit_logger()` with FileHandler (DEBUG) + StreamHandler (INFO/DEBUG), credential masking via `_sanitize_log_cmd()`.
- [x] **`run_command()` instrumentation (PR #350)**: Logs every command (sanitized), stdout, stderr, return code, and execution duration.
- [x] **`perform_checks()` instrumentation (PR #350)**: WARNING for manual controls, ERROR for failures, DEBUG for pass/fail results.
- [x] **CLI `--verbose/-v` flag (PR #350)**: Enables DEBUG level on console for real-time command details (closes #349).

