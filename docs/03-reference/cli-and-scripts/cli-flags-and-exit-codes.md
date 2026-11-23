# CLI Flags, Scripts, Environment Variables, and Exit Codes

Normative CLI and exit-code contract for **CIS Benchmarks Tools Suite** `v2.10.0` (`audit_cis.py`).

## 1. Unified CLI Options (`audit_cis.py` / `audit-cis`)

| Flags | Arg / Choices | Default | Behavior |
| :--- | :--- | :--- | :--- |
| `-t`, `--target` | 18 target keys | `None` | Benchmark target to audit. |
| `-c`, `--docker`, `--container` | `<NAME\|ID>` | `None` | Target Docker container. |
| `-m`, `--mode` / `--local` | `local\|ssh` | `local` | Transport mode (`--local` forces local). |
| `-r`, `--remote`, `--ssh` | `<USER@HOST>` | `None` | Remote SSH host (implies `ssh`). |
| `--ssh-port`, `-i`/`--ssh-key`, `--sudo` | `<PORT>`, `<PATH>`, switch | `22`, `None`, `false` | SSH port, key, and `sudo -n`. |
| `-H`/`--host`/`--db-host`, `-P`/`--port`/`--db-port` | `<HOST>`, `<PORT>` | `localhost`, `None` | DB host and TCP port. |
| `-u`/`--user`/`--db-user`, `-p`/`--password`/`--db-password` | `<USER>`, `<PASS>` | `None`, `$CIS_DB_PASSWORD` | DB auth (`CIS_DB_PASSWORD` preferred). |
| `-D`/`-d`/`--database`/`--db-name`, `--auth-db` | `<DB>` | `None` | DB name / MongoDB auth DB. |
| `--defaults-file`, `--config-file` | `<PATH>` | `None` | Option file (`.my.cnf`, `.pgpass`, `cqlshrc`). |
| `-f`, `--format` | `html\|json\|xml\|txt\|sarif` | `html` | Report export format. |
| `-l`, `--lang` | `en\|fr` | `en` | Report and CLI language. |
| `-o`/`--output`, `-j`/`--output-json` | `<PATH>` | `None` | Output / JSON summary path. |
| `--list-targets`, `-a`/`--all`, `--auto-detect` | switches | `false` | List targets, run all 18, or auto-detect. |
| `--sync-cis`, `--verify-cis`, `--cis-types`, `--types`, `--force`, `--dry-run`, `--base-url` | sync options | `false` / `None` | Sync or verify `CIS_DATA/` manifest. |
| `--remediate-dry-run`, `--remediation-format`, `--remediation-output`, `--from-report` | `diff\|sql\|shell\|ansible\|json` | `false`, `diff` | Dry-run remediation (zero mutations). |
| `-v`/`--version`, `-h`/`--help` | switches | — | Print suite version or usage help. |

## 2. Companion Modules & Environment Variables

- `audit_orchestrator.py`: `-j/--parallel <N>`, `-f FORMATS`, `-o/--output-dir`.
- `remediation_generator.py`: `--from-report`, `-t/--target`, `-f/--format`, `-o/--output`.
- Env: `CIS_DB_PASSWORD`, `MYSQL_PWD`, `PGPASSWORD`, `PYTHONUTF8`, `CIS_LIVE_DOCKER_E2E`, `CIS_DOCS_REF`, `CIS_DOCS_SITE_URL`.

## 3. Process & Subprocess Exit Codes

| Code | Scope | Condition |
| :---: | :--- | :--- |
| `0` | CLI / Subprocess | Audit, `--list-targets`, `--auto-detect`, or dry-run passed. |
| `1` | CLI / Subprocess | Missing script, failed check, `--all` failure, runtime error. |
| `2` | CLI (`argparse`) | Invalid args or `--remediate-dry-run` missing report/target. |
| `126` | Subprocess | Permission denied (`CommandFailureClassifier.PERMISSION_DENIED`). |
| `127` | Subprocess | Missing binary (`CommandFailureClassifier.MISSING_BINARY`). |
| `-1` | Subprocess | Timeout expiration or driver exception (`TIMEOUT`). |

## Related Documentation

- [Targets & Transport Matrix](../configuration/targets-and-transport-matrix.md)
- [Error & Alert Matrix](../troubleshooting-codes/error-and-alert-matrix.md)
- [Remote SSH & Docker Audits](../../02-how-to-guides/deployment/run-remote-ssh-and-docker-audits.md)
