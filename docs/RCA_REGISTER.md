# RCA Register — Errors, Technical Dead-Ends, Approximations & Unimplemented Ideas

> **Governance Rule ([`AGENTS.md`](../AGENTS.md) §4 & [`.agents/rules/project-governance.md`](../.agents/rules/project-governance.md))**:
> This register guarantees full engineering traceability for the **CIS Benchmarks Tools Suite** project. It **MUST be systematically updated on every request, every change, and every result** across its four sections:
> 1. **Errors & Bugs Encountered (Root Cause Analysis — RCA)**
> 2. **Technical Dead-Ends & Abandoned Leads (`IMP`)**
> 3. **Current Approximations & Simplifying Assumptions (`APP`)**
> 4. **Unimplemented Ideas & Future Roadmap (`IDEA`)**

---

## 1. Errors & Bugs Encountered (Root Cause Analysis — RCA)

### RCA-022 — Unexcluded Archive Directory in Bandit SAST Scan & Script Governance Blind Spots
- **Date / Linked Action**: `2026-10-30` (`ACT-077` / Issue `#612`)
- **Observed Symptom**: GitHub Actions CI workflow `Security & Dependency Audit` failed on PR `#611` and `main` (Run `#41135860515`) on Bandit SAST scan step with exit code 1; Bandit detected 7 High-Severity CWE-78 issues in decommissioned `archive/scripts/generate_missing_reports.py`. Furthermore, `scripts/pre_commit_checks.py` used loose `"archive"` substring matching, and `tests/test_script_inventory_and_governance.py` omitted directory checking in `scripts/`.
- **Root Cause Analysis (5 Whys)**:
  1. *Why did Bandit scan fail on CI?* Bandit scanned `archive/scripts/generate_missing_reports.py` and flagged 7 High-Severity CWE-78 issues (`subprocess.run(..., shell=True)`).
  2. *Why was archive/ scanned?* In `.github/workflows/security.yml`, Bandit's exclusion flag was `-x ./tests,./scripts`, omitting `./archive`.
  3. *Why was ./archive omitted?* When 65 obsolete scripts were relocated from `scripts/` to `archive/scripts/` in PR `#609` and PR `#611` (`IMP-005`), the exclusion was added to `scripts/pre_commit_checks.py` for local `py_compile` but missed in GitHub Actions workflow.
  4. *Why did local tests pass?* Bandit is not installed or executed in the local PSL test environment; only GitHub Actions CI runs Bandit.
  5. *Why was PR #611 merged with failing CI?* Merged without verifying remote GitHub Actions checks, relying solely on local test passes.
- **Applied Change / Fix**:
  - Added `./archive` to Bandit exclusion in `.github/workflows/security.yml:38` (`-x ./tests,./scripts,./archive`).
  - Path-anchored archive exclusion in `scripts/pre_commit_checks.py:56` with modular predicate `should_skip_syntax_validation()`.
  - Hardened `tests/test_script_inventory_and_governance.py` with subdirectory whitelist checks, CI Bandit exclusion assertion, pre-commit check path anchoring verification, and exclusion logic unit tests.
- **Result & Non-Regression Test**: All 276 unit tests pass (100%); `scripts/pre_commit_checks.py` 8/8 pass; Bandit SAST scan in GitHub Actions CI passes cleanly with 0 high severity issues; PR diff strictly under 15,000 chars.

---

### RCA-021 — Unreachable Duplicate Subprocess Code in MariaDB Audit Engines (Finding 11)
- **Date / Linked Action**: `2026-10-30` (`ACT-059` / Issue `#576`)
- **Observed Symptom**: Static analysis detected 21 lines of unreachable dead code inside `run_command()` in `audit_cis_mariadb_106.py` and `audit_cis_mariadb_1011.py` located inside an `except Exception as e:` block following an unconditional return statement.
- **Root Cause Analysis (5 Whys)**:
  1. *Why was code unreachable?* The statements followed `return "", str(e), -1` inside the exception handler.
  2. *Why were statements placed after return?* During earlier refactoring of SSH/subprocess execution, an older duplicate block was left behind after the return statement instead of being replaced.
  3. *Why did it not raise a Python SyntaxError?* Python syntax permits statements after a return inside an exception block (they are simply never executed at runtime).
  4. *Why was it not detected during unit test execution?* Code coverage or dead code analyzers were not included in standard test discovery.
  5. *Why did other engines not have this issue?* The duplicate block was accidentally appended only to `audit_cis_mariadb_106.py` and `audit_cis_mariadb_1011.py`.
- **Applied Change / Fix**: Removed all dead unreachable code in `audit_cis_mariadb_106.py` and `audit_cis_mariadb_1011.py`; added automated AST analysis regression test `test_no_unreachable_code_in_audit_engines` in `tests/test_benchmark_sync_and_report_quality.py` to prevent any unreachable statements across all 18 audit engines.
- **Result & Non-Regression Test**: 239/239 unit tests pass; `scripts/pre_commit_checks.py` 8/8 checks pass with 100% success; AST analysis verifies 0 unreachable statements.

### RCA-020 — SSH Audit Reports Syntax Corruption from Unbounded Host Warning Regex (Finding 8 Part B)
- **Date / Linked Action**: `2026-10-30` (`ACT-030` through `ACT-058` / Issues `#518` to `#574`)
- **Observed Symptom**: 12 SSH audit reports in `reports/` (2 XML and 10 JSON) suffered severe syntax breakage: XML reports had `</error></testcase>` tags swallowed; JSON reports contained unescaped quotes and missing commas (`\nStderr:\n\n      "error": "\n`), causing `json.loads` and `xml.etree.ElementTree` parsing failures.
- **Root Cause Analysis (5 Whys)**:
  1. *Why did JSON/XML reports fail to parse?* JSON parser raised `Invalid control character at line X column Y`; XML parser raised `mismatched tag: line 11 column 34`.
  2. *Why were closing tags and quotes missing?* An earlier warning cleaner script applied an unbounded regex `re.sub(r'Warning: Permanently added.*?to the list of known hosts\.\r?\n?', '', content)` across all report files.
  3. *Why did the regex match across line boundaries?* The non-greedy `.*?` matched beyond newline boundaries into the surrounding JSON structure and swallowed quotes, commas, and XML closing tags.
  4. *Why was this not caught immediately?* Pre-commit checks validated file size (> 1KB) on HTML reports but did not parse JSON or XML reports with `json.loads` or `ElementTree`.
  5. *Why was the cleaner script run without safeguards?* The script lacked post-cleaning syntax verification before overwriting files.
- **Applied Change / Fix**:
  - Restored clean XML structure in `reports/rapport_cis_mariadb_106_ssh.xml` and `reports/rapport_cis_mariadb_1011_ssh.xml` using bounded line-specific regex `re.compile(r'Warning: Permanently added [^\r\n]+ to the list of known hosts\.\r?\n?')`.
  - Replaced corrupted output/error syntax patterns across all 10 SSH JSON reports through sequential, atomic Pull Requests strictly respecting the `< 15,000` characters diff limit.
  - Added non-regression unit tests `test_mariadb_ssh_xml_reports_syntax` and `test_ssh_json_reports_syntax` in `tests/test_benchmark_sync_and_report_quality.py`.
- **Result & Non-Regression Test**: All 12 SSH reports pass syntax and quality checks (`python scripts/verify_benchmarks_and_reports.py --test-reports`); unit tests pass 238/238; pre-commit checks pass 8/8.

---

### RCA-019 — Windows Console Crashes on UTF-8 Output & Report Cleaning Syntax Breaks (Finding 8)
- **Date / Linked Action**: `2026-10-30` (`ACT-028` / Issue `#515`)
- **Observed Symptom**: Audit scripts crashed on Windows console with `UnicodeEncodeError: 'charmap'` when emitting emoji or accented text (e.g. `✓`, `❌`, `🚀`, `é`); legacy regex in `clean_ssh_warnings_from_reports.py` lacked validation and boundary containment.
- **Root Cause Analysis (5 Whys)**:
  1. *Why did print() crash on Windows?* Python on Windows defaults standard streams to OEM/ANSI codepages (e.g. cp1252) when not explicitly set to UTF-8.
  2. *Why were non-ASCII characters emitted?* CIS benchmarks rules and diagnostic summaries use French accents and unicode compliance badges.
  3. *Why did engines lack UTF-8 reconfigure?* UTF-8 stream reconfiguration was previously only present in RHEL engines and orchestrator, omitted from database engines.
  4. *Why did report cleaning corrupt files?* Regex replacements on structured files (JSON/XML) operated without post-substitution syntax validation.
- **Applied Change / Fix**: Configured `os.environ.setdefault('PYTHONUTF8', '1')` and `sys.stdout/sys.stderr.reconfigure(encoding='utf-8', errors='replace')` across all 18 benchmark audit engines; in `scripts/clean_ssh_warnings_from_reports.py`, added post-cleaning syntax verification preventing corrupted files from being saved; added unit test `test_all_audit_engines_have_utf8_stream_reconfiguration` in `tests/test_benchmark_sync_and_report_quality.py`.
- **Result & Non-Regression Test**: `tests/test_benchmark_sync_and_report_quality.py` asserts all 18 engines reconfigure stdout and stderr; pre-commit checks pass 8/8; 235/235 tests pass with 100% success.

---

### RCA-018 — Fake Docker Container Synthesis on Bare-Metal Hosts (Finding 7)
- **Date / Linked Action**: `2026-10-30` (`ACT-027` / Issue `#513`)
- **Observed Symptom**: Bare-metal local audits executed via `audit_orchestrator.py` were routed through `docker exec <default_container>` even when Docker daemon was down or no containers existed, failing audits on bare-metal systems.
- **Root Cause Analysis (5 Whys)**:
  1. *Why did local bare-metal audits run docker exec?* `perform_checks` received a non-None `docker_container` argument (e.g. `mariadb106-prod`).
  2. *Why did orchestrator set active_container to default_container?* `execute_single_target` passed `self.docker_container or target_meta.get('default_container')` to `resolve_transport`.
  3. *Why did resolve_transport return TRANSPORT_CONTAINER_EXEC?* `docker_transport.py` had a fallback `or ContainerInfo(..., is_running=True)` when `inspect_container` failed.
  4. *Why did inspect_container fail?* The container did not exist on the bare-metal host.
  5. *Why was a synthetic is_running=True container created?* An over-optimistic fallback assumed specified containers were running without verifying with the Docker engine.
- **Applied Change / Fix**: In `audit_orchestrator.py`, passed `self.docker_container` directly to `resolve_transport` without falling back to `default_container`, and assigned `active_container = c_info.name if (c_info and c_info.is_running) else self.docker_container`; in `docker_transport.py`, removed `is_running=True` synthetic fallback and required `must_be_running=True` for product auto-discovery; added unit tests in `tests/test_audit_orchestrator.py` and `tests/test_docker_transport.py`.
- **Result & Non-Regression Test**: `test_baremetal_local_mode_does_not_synthesize_fake_container` verifies local bare-metal audit executes with `docker_container=None`; `test_transport_resolver_nonexistent_specified_container` verifies non-running status; 234/234 tests pass.

---

### RCA-017 — Database Passwords Exposed in Process Tables via CLI Args (Finding 6 Parts A & B)
- **Date / Linked Action**: `2026-10-30` (`ACT-024` & `ACT-025` / Issues `#508`, `#510`)
- **Observed Symptom**: Plaintext database passwords were visible to all OS users in `ps aux` and `/proc/<pid>/cmdline`: `DockerExecutor` and `RemoteSSHContainerExecutor` passed `-e MYSQL_PWD=<pass>` and `-e PGPASSWORD=<pass>` on the CLI; `audit_cis.py` passed `--db-password <password>` when invoking child benchmark scripts; Cassandra automated check 3.2 embedded `-p cassandra` directly in shell command line.
- **Root Cause Analysis (5 Whys)**:
  1. *Why were passwords visible in ps aux?* Secrets were passed as explicit command line arguments to `docker exec`, `python audit_cis_*.py`, and `cqlsh`.
  2. *Why does Docker expose -e KEY=VAL on CLI?* Passing `=VAL` on CLI stores the value in host `argv`, whereas passing bare `-e KEY` forwards the variable securely from the parent environment over the daemon socket.
  3. *Why did audit_cis.py pass --db-password?* The CLI runner converted parsed password arguments back into command line arguments rather than forwarding `CIS_DB_PASSWORD` via `env`.
  4. *Why did Cassandra check 3.2 embed -p cassandra?* The rule checked if the default password worked by explicitly attempting authentication on the CLI with `-p cassandra`.
- **Applied Change / Fix**:
  - Part A: In `execution_drivers.py`, updated `DockerExecutor.execute` to pass bare `-e MYSQL_PWD` / `-e PGPASSWORD` flags on CLI and pass passwords in `env=cmd_env`; updated `RemoteSSHContainerExecutor` to export variables in remote subshell; updated unit tests in `tests/test_credential_injection.py` and `tests/test_execution_drivers.py`.
  - Part B: In `scripts/bundle_audit_cis.py` and `audit_cis.py`, passed `CIS_DB_PASSWORD` in `cmd_env` to `subprocess.run` instead of appending `--db-password` to CLI argv; defaulted CLI `--db-password` to `os.environ.get('CIS_DB_PASSWORD')`; removed hardcoded `-p cassandra` from automated control 3.2 in `audit_cis_cassandra_40.py`, `41.py`, `50.py`, and JSON rules `rules/cassandra_40.json`, `41.json`, `50.json`; updated unit tests in `tests/test_audit_cis_cli.py` and `tests/test_e2e_docker_audits.py`.
- **Result & Non-Regression Test**: `tests/test_audit_cis_cli.py`, `tests/test_e2e_docker_audits.py`, `tests/test_credential_injection.py`, and `tests/test_execution_drivers.py` assert zero secret strings in `called_cmd` argv and successful environment forwarding; 233/233 tests pass.

---

### RCA-016 — Shell Injection and Host Variable Expansion in Execution Drivers (Finding 5)
- **Date / Linked Action**: `2026-10-30` (`ACT-023` / Issue `#506`)
- **Observed Symptom**: DockerExecutor invoked host `/bin/bash -c` wrapping `docker exec` with `json.dumps(command)`, causing host shell variable expansion (`$VAR`, `$(...)`, backticks) and shell injection, and failing on Windows hosts lacking `/bin/bash`; RemoteSSHContainerExecutor evaluated commands inside double quotes on remote host before container entry; SSHExecutor and LocalExecutor did not quote `as_user` or `cmd_str` with `shlex.quote`.
- **Root Cause Analysis (5 Whys)**:
  1. *Why did host variable expansion occur?* `DockerExecutor` passed command arguments to host `/bin/bash -c` which evaluated them before starting the container.
  2. *Why was host `/bin/bash` invoked?* The executor stringified the docker exec command line instead of invoking `subprocess.run(parts, ...)` directly.
  3. *Why did remote SSH container execution leak variables?* Container command was double-quoted in `remote_docker_cmd` without single-quote protection.
- **Applied Change / Fix**: In `execution_drivers.py`, updated `DockerExecutor.execute` to pass `parts` argument list directly to `subprocess.run(parts, ...)`, bypassing host shell completely; updated `RemoteSSHContainerExecutor` to use `shlex.quote` for container CLI, container name, flags, and command; quoted `as_user` in `SSHExecutor`; replaced `json.dumps` with `shlex.quote` in `LocalExecutor`; added dedicated security unit tests in `tests/test_execution_drivers.py`.
- **Result & Non-Regression Test**: `tests/test_execution_drivers.py` verifies host shell bypass, absence of `/bin/bash` on host CLI, and safe quoting across all drivers; 231/231 tests pass with 100% success.

---

### RCA-015 — MariaDB Sudo Drop and Orchestrator Export Mismatch
- **Date / Linked Action**: `2026-10-30` (`ACT-022` / Issue `#504`)
- **Observed Symptom**: MariaDB 10.6/10.11 dropped `sudo=True` commands without `sudo -n`; `audit_orchestrator.py` raised `TypeError` on 15 targets lacking `execution_context` in `export_results`; orchestrator CLI rejected DB args.
- **Root Cause Analysis (5 Whys)**:
  1. *Why was sudo dropped?* `create_executor` omitted sudo and executed commands before reaching fallback.
  2. *Why did export fail?* `export_fn` fallback retained `execution_context`, unsupported by 15 targets.
  3. *Why did CLI reject DB args?* `argparse` parser omitted DB credentials arguments.
- **Applied Change / Fix**: Updated MariaDB engines to bypass `create_executor` on `sudo=True`; added standard 7-arg `export_fn` fallback and UTF-8 stdout streams; added DB options to `build_cli_parser()`; added tests in `tests/test_mariadb_sudo_and_orchestrator_export.py`.
- **Result & Non-Regression Test**: `tests/test_mariadb_sudo_and_orchestrator_export.py` passes 6/6 tests; test suite passes 234/234 tests with 100% success.

---

### RCA-013 — Database Credentials and SSH Flags Dropped Across Engines and Orchestrator (Finding 3)
- **Date / Linked Action**: `2026-10-30` (`ACT-021` / Issue `#484`)
- **Observed Symptom**: CLI arguments `-u/--db-user`, `-p/--db-password`, `-H/--db-host`, `-P/--db-port`, `-D/--db-name`, `--defaults-file`, `--auth-db` had no effect on 12 database engines, and `--ssh-port`, `-i/--ssh-key`, `--sudo` were not propagated in orchestrator and engines.
- **Root Cause Analysis (5 Whys)**:
  1. *Why had arguments no effect?* `__main__` called `perform_checks(rules_data, remote_host=remote_target, docker_container=docker_target)` omitting parsed `args.db_*`.
  2. *Why were SSH flags dropped?* `audit_orchestrator.py` omitted `ssh_port`, `ssh_key`, `sudo` from check invocation; engines did not propagate `ssh_port`, `ssh_key`, `sudo` to `run_command`.
- **Applied Change / Fix**: Updated `__main__` across all 12 database engines to pass `db_*` kwargs; added `check_kwargs` property and forwarded `ssh_port`, `ssh_key`, `sudo` across `audit_orchestrator.py` and all 15 audit engines (`rhel_8/9/10`, `postgresql_16/17/18`, `mariadb_106/1011`, `mysql_80`, `mysql_community_84/97`, `mysql_enterprise_84/97`, `cassandra_40/41/50`, `mongodb_7/8`); added non-regression tests in `tests/test_credential_and_flag_propagation.py`.
- **Result & Non-Regression Test**: `tests/test_credential_and_flag_propagation.py` verifies all 15 database engines pass `db_*` kwargs in `__main__`, and verifies SSH flag propagation in orchestrator, RHEL, and database engines.

---

### RCA-012 — Automated Checks Omitting `docker_container` in PostgreSQL, MongoDB, and Cassandra (Finding 2)
- **Date / Linked Action**: `2026-10-30` (`ACT-020` / Issue `#481`)
- **Observed Symptom**: Auditing containerized instances of PostgreSQL (16, 17, 18), MongoDB (7, 8), and Cassandra (4.0, 4.1, 5.0) via `audit_cis.py --docker <name>` executed commands on the local host rather than inside the specified container, resulting in `returncode 127` (`psql: command not found` / `cqlsh: command not found`).
- **Root Cause Analysis (5 Whys)**:
  1. *Why were commands executed on host?* `perform_checks()` in those 8 engine scripts invoked `run_command(cmd, remote_host=remote_host)` without passing the `docker_container` keyword argument.
  2. *Why was `docker_container` omitted?* Internal loops across automated rules extracted commands from JSON rule specs and called `run_command` forwarding only `remote_host`.
- **Applied Change / Fix**: Updated `perform_checks()` across PostgreSQL, MongoDB, and Cassandra audit engines to explicitly forward `docker_container=docker_container` to `run_command()`.
- **Result & Non-Regression Test**: Verified via `tests/test_container_parameter_forwarding.py` asserting that mocked `run_command` receives `docker_container` across all 8 targets.

---

### RCA-011 — RHEL 8, 9, 10 HTML Report Exporter Crash & Unpopulated Category Scores (Finding 1)
- **Date / Linked Action**: `2026-10-30` (`ACT-019` / Issue `#479`)
- **Observed Symptom**: When running `audit_cis_rhel_8.py`, `audit_cis_rhel_9.py`, or `audit_cis_rhel_10.py` with `--format html`, execution crashed with `TypeError: build_inline_svg_category_chart() takes 1 positional argument but 5 were given`, and the HTML category breakdown section displayed empty/NaN score metrics.
- **Root Cause Analysis (5 Whys)**:
  1. *Why did HTML export crash?* RHEL audit scripts called `build_inline_svg_category_chart(cat_scores, total, passed, failed, manual)` instead of passing a dictionary `categories_scores`.
  2. *Why was the signature mismatched?* The inline SVG chart generator had been refactored in database scripts to take a single structured dictionary, but RHEL scripts retained legacy multi-argument invocation signatures.
  3. *Why were category scores unpopulated?* RHEL's `calculate_scores()` returned an empty dictionary `{}`, leaving category statistics uncalculated.
- **Applied Change / Fix**: Standardized `calculate_scores()` across `audit_cis_rhel_8.py`, `audit_cis_rhel_9.py`, and `audit_cis_rhel_10.py` to populate category metrics dictionary; updated `generate_html_report()` to pass `categories_scores` dict to `build_inline_svg_category_chart()`; added unit tests in `tests/test_rhel_html_export_quality.py`.
- **Result & Non-Regression Test**: Unit test `tests/test_rhel_html_export_quality.py` passes 100%; HTML reports generate valid inline SVGs with category breakdowns.

---

### RCA-014 — Orchestrator `ModuleNotFoundError` on RHEL Targets Caused by Missing Underscores (Finding 4)
- **Date / Linked Action**: `2026-10-30` (`ACT-018` / Issue `#477`)
- **Observed Symptom**: Running `audit_orchestrator.py` against `rhel8`, `rhel9`, or `rhel10` failed immediately with `ModuleNotFoundError: No module named 'audit_cis_rhel8'`.
- **Root Cause Analysis (5 Whys)**:
  1. *Why did import fail?* `CANONICAL_TARGETS` in `audit_orchestrator.py` mapped RHEL keys to `"module": "audit_cis_rhel8"`, `"audit_cis_rhel9"`, and `"audit_cis_rhel10"`.
  2. *Why did that filename not exist?* The actual script files on disk were created with underscores: `audit_cis_rhel_8.py`, `audit_cis_rhel_9.py`, and `audit_cis_rhel_10.py`.
  3. *Why did unit tests not catch this?* `test_canonical_targets_catalog_completeness` only checked dictionary keys, never attempting to import the referenced module.
- **Applied Change / Fix**: Corrected module and rule specification names in `audit_orchestrator.py` to `audit_cis_rhel_8`, `audit_cis_rhel_9`, `audit_cis_rhel_10` (and `rhel_8`, `rhel_9`, `rhel_10`); added inspect-based signature adaptation and fallback normalization; updated unit tests to assert module importability and rule file presence for all 18 canonical targets.
- **Result & Non-Regression Test**: `tests/test_audit_orchestrator.py` dynamically verifies that `importlib.import_module()` succeeds and rule files exist for all 18 canonical targets.

---

### RCA-010 — Windows CP1252 UnicodeEncodeError & RHEL HTML Exporter Regression
- **Date / Linked Action**: `2026-10-30` (`ACT-017` / Issue `#453`)
- **Observed Symptom**: `verify_benchmarks_and_reports.py` and RHEL engines failed on Windows with `UnicodeEncodeError: 'charmap'`; RHEL `generate_html_report` crashed with `TypeError` and `KeyError`; `clean_ssh_warnings_from_reports.py` regex truncated quotes/tags.
- **Root Cause Analysis**: Missing `sys.stdout.reconfigure(encoding="utf-8")`; RHEL engines passed 5 args to 1-arg `build_inline_svg_category_chart` and used `.format()` without SafeDict; SSH regex matched `[^\n\r]+` past delimiters.
- **Applied Change / Fix**: Added UTF-8 stdout reconfiguration; fixed RHEL category scores and HTML generation using SafeDict; safe-guarded SSH warnings regex; added regression tests in `test_benchmark_sync_and_report_quality.py`.
- **Result & Non-Regression Test**: `verify_benchmarks_and_reports.py --all` passes; 216/216 unit tests and 8/8 pre-commit checks pass.

---

### RCA-009 — CIS Downloader 404 Remote PDFs, Silent Skips & Opener Crash
- **Date / Linked Action**: `2026-10-25` (`ACT-016` / Issue `#470`)
- **Observed Symptom**: Sync defaulted to 404 remote PDFs; comma-types and unknown targets silently skipped; `OpenerDirector` crashed.
- **Root Cause Analysis**: Default sync type was `"all"`; no comma-parsing or target manifest check; direct callable call on `OpenerDirector`.
- **Applied Change / Fix**: Defaulted sync to `md`; added `parse_file_types` and unknown target check; supported `opener.open()`; forwarded CLI flags.
- **Result & Non-Regression Test**: 216/216 unit tests and 8/8 pre-commit checks pass.

---

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

### IMP-005 — Retention of One-Off Migration and Hotfix Scripts in Production Tooling (Finding 12)
- **Observed Finding / Debt**: Finding 12 of the Ponytail Audit identified 65 historical one-off migration and hotfix scripts (~289 KB) accumulated in `scripts/`.
- **Why It Is a Dead-End**:
  1. *CI Lint Bloat*: Compiling 65 dead files during pre-commit checks adds unnecessary overhead.
  2. *Maintenance Confusion*: Unclear distinction between 13 active production tools and historical artifacts.
  3. *Bitrot Hazard*: Outdated schemas in one-off scripts risk corrupting current rules if accidentally re-run.
  4. *Diff Limit Hazard*: Pure deletion (`git rm`) produces ~305,000 diff chars; single files like `build_full_roadmap_phases.py` (20,805 bytes) exceed the 15,000-char PR diff limit (`IMP-004`).
- **Adopted Decision & Archiving Standard**:
  1. **Decommissioning via Archiving**: Relocated all 65 obsolete scripts to `archive/scripts/` via `git mv`, leveraging Git rename detection to keep PR diffs under 15,000 chars.
  2. **Preservation of 13 Essential Tools**: Whitelisted active tooling in `scripts/`: `bundle_audit_cis.py`, `pre_commit_checks.py`, `pre-commit.sh`, `download_cis_benchmarks.py`, `verify_benchmarks_and_reports.py`, `clean_ssh_warnings_from_reports.py`, `run_e2e_tests.py`, `analyze_e2e_reports.py`, and the 5 container entrypoints `start_*.sh`.
  3. **Automated Inventory Governance Test**: Enforced in `tests/test_script_inventory_and_governance.py` that only the 13 essential tools exist in `scripts/` and compile cleanly.

### IMP-006 — OpenSSH `ControlMaster` Connection Multiplexing for Remote Audits (Finding 14)
- **Observed Finding / Proposed Optimization**: Finding 14 of the Ponytail Audit highlighted the connection overhead of establishing separate SSH connections for each of the 70+ (or up to 180+) individual CIS control checks per audit target, proposing OpenSSH connection multiplexing (`ControlMaster auto`, `ControlPath /tmp/ssh_mux_%h_%p_%r`, `ControlPersist 10m`) to reuse a single persistent TCP connection.
- **Why It Is a Dead-End**:
  1. *Cross-Platform Windows Host Incompatibility*: The test harness and orchestrator run interchangeably on Linux and Windows. On Windows hosts, OpenSSH (`ssh.exe`) lacks stable Unix Domain Socket (`AF_UNIX`) emulation for `ControlPath`, named pipes cannot be bound as control sockets transparently, and user path lengths (`%TEMP%`, `AppData`) frequently exceed the 108-character POSIX `sockaddr_un.sun_path` buffer limit, causing immediate crashes (`unix_listener: path ... too long for Unix domain socket`). Furthermore, Windows NTFS permissions cannot satisfy OpenSSH's strict 0600 file ownership verification.
  2. *Orphaned Control Sockets and Unrecoverable Hangs*: If a remote target host, container, or network link bounces or freezes mid-audit, the local control socket file remains orphaned on disk. Subsequent child `ssh` commands connect to the stale socket and hang indefinitely waiting for an unresponsive master process, or crash with `mux_client_hello_exchange: write packet: Broken pipe`. Recovering requires external process reaping and socket unlinking (`ssh -O stop` / `rm -f`), which is brittle and prone to deadlock in automated headless CI/CD runs.
  3. *Concurrency & Head-of-Line Blocking*: When `audit_orchestrator.py` executes concurrent checks across multiple worker threads (`parallel_workers > 1`), multiplexing all concurrent streams over a single TCP connection and single-threaded SSH crypto process causes Head-of-Line (HOL) blocking whenever a heavy command (such as a recursive filesystem scan or database dump) executes. Additionally, simultaneous initial connections trigger socket binding race conditions (`bind(): Address already in use`).
  4. *PSL-Only Architectural Mandate*: Rule 1 and `IMP-001` strictly forbid external SSH libraries with native in-process multiplexing (such as `paramiko` or `asyncssh`). Implementing OpenSSH master daemon lifecycle management, signal trapping, cross-platform socket cleanup, and zombie process reaping in pure Python Standard Library introduces hundreds of lines of fragile scaffolding that violates the repository's KISS and YAGNI architectural standards.
- **Adopted Decision & Hardened Alternative**:
  1. **Deliberate Rejection of `ControlMaster`**: Maintain completely stateless, independent, decoupled SSH invocations per command to guarantee total cross-platform isolation and zero-hang guarantees.
  2. **Connection Resiliency Hardening**: Standardize connection parameters across `SSHExecutor` and `RemoteSSHContainerExecutor` in `execution_drivers.py` with:
     - `ConnectTimeout=10`: Allows reliable connection establishment on high-latency WAN/VPN/cloud links while failing fast (10s) when hosts are down.
     - `BatchMode=yes`: Strictly suppresses password/passphrase/hostkey prompts on `stdin`, preventing hanging interactive prompts.
     - `ServerAliveInterval=15` and `ServerAliveCountMax=3`: Sends encrypted keepalive packets every 15s, keeping stateful NAT/firewalls open during long checks and terminating dead sessions within 45s instead of standard 2-hour OS TCP timeouts.
     - `StrictHostKeyChecking=no` and `UserKnownHostsFile=/dev/null`: Eliminates host key collision errors across ephemeral containers and avoids polluting `~/.ssh/known_hosts`.
     - `TCPKeepAlive=yes`: Ensures OS-level TCP socket heartbeat.
  3. **Non-Regression Verification**: Assert in `tests/test_execution_drivers.py` that hardened timeout and keepalive flags are systematically constructed in SSH command arguments and that no `ControlMaster` options are present.

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

### APP-004 — Dynamic Rule Category Discovery & Safe Key Access in Database Audit Engines (Finding 10)
- **Target Files**: All 15 database audit engines (`audit_cis_mariadb_106.py`, `audit_cis_mariadb_1011.py`, `audit_cis_mysql_80.py`, `audit_cis_mysql_community_84.py`, `audit_cis_mysql_community_97.py`, `audit_cis_mysql_enterprise_84.py`, `audit_cis_mysql_enterprise_97.py`, `audit_cis_postgresql_16.py`, `audit_cis_postgresql_17.py`, `audit_cis_postgresql_18.py`, `audit_cis_mongodb_7.py`, `audit_cis_mongodb_8.py`, `audit_cis_cassandra_40.py`, `audit_cis_cassandra_41.py`, `audit_cis_cassandra_50.py`).
- **Nature & Justification**: All 15 database engines dynamically discover categories from `results` (supporting dict/list, arbitrary order, and filtered subsets) without hardcoded rule dependencies. In M3 Iter2, MariaDB 10.6/10.11 engines were hardened with defensive key access (`check.get()`), non-dict item guards, untyped fallback detection (`check.get("scored") is True` or automated status), and case-insensitive status evaluation.
- **Removal Condition**: Permanent architectural standard across all audit engines and report exporters.

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

### IDEA-007 — Canonical Target Catalog & CLI Argument Forwarding Matrix Test Coverage (Finding 13)
- **Priority / Target**: `Completed ✅` · `tests/test_target_catalog_and_cli_matrix.py`, `audit_cis.py`, & `audit_orchestrator.py`
- **Description**: Exhaustive matrix test suite validating canonical target resolution across all 18 targets (`CANONICAL_TARGETS` vs `TARGET_MAP`), rule specification presence in `rules/`, interface contracts (`perform_checks`, `calculate_scores`, `build_inline_svg_category_chart`, `build_inline_svg_donut_chart`, `export_results`), CLI parsing, and argument forwarding without secret leakage (implemented in ACT-078).
