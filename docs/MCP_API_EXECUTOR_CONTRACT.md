# Read-Only CLI JSON/SARIF Contract for `api_executor` MCP Integration

**Contract Version:** `cis.mcp.contract.v1` | **Preset Catalog:** [`conf/mcp_api_executor_presets.json`](../conf/mcp_api_executor_presets.json) | **Runtime:** 100% PSL ONLY

## 1. Strict Read-Only Guarantee
- Every MCP preset MUST enforce `"read_only": true` and `"mutating": false`.
- Allowed presets: `cis_list_targets`, `cis_audit_json`, `cis_audit_sarif`, `cis_remediate_dry_run`.
- Forbidden flags: `-p`, `--password`, `--db-password`, `--apply`, `--allow-ephemeral-apply`, `--force`, `--sync-cis`, `--all`, `--auto-detect`.
- `cis_remediate_dry_run` runs `remediation_generator.py` with `dry_run=True` and executes zero system or database commands.

## 2. CLI Invocation, Targets & Exit Codes
- **Entrypoint:** `python3 audit_cis.py ...` (or console script `audit-cis ...`).
- **Exit Codes:** `0` = success, `1` = audit/runtime error, `2` = invalid CLI arguments.
- **18 Canonical Targets (887 Controls):** `mariadb106`, `mariadb1011`, `mysql80`, `mysql-community84`, `mysql-enterprise84`, `mysql-community97`, `mysql-enterprise97`, `postgresql16`, `postgresql17`, `postgresql18`, `mongodb7`, `mongodb8`, `cassandra40`, `cassandra41`, `cassandra50`, `rhel8`, `rhel9`, `rhel10`.
- **Preset Commands:**
  1. `audit-cis --list-targets`
  2. `audit-cis --target <target> --format json --lang <en|fr> --mode <local|ssh> --output <path.json>`
  3. `audit-cis --target <target> --format sarif --lang <en|fr> --mode <local|ssh> --output <path.sarif>`
  4. `audit-cis --remediate-dry-run --from-report <report.json> --remediation-format <diff|sql|shell|ansible|json> --remediation-output <out_path>`
- **Optional Connection Flags:** `--docker`, `--remote`, `--ssh-port`, `--ssh-key`, `--db-host`, `--db-port`, `--db-user`, `--db-name`, `--defaults-file`, `--auth-db`, `--sudo`.

## 3. Output Schemas & 5-State Taxonomy
- **5-State Compliance Taxonomy:** `Pass`, `Fail`, `Error`, `Manual`, `Not Applicable`.
- **JSON Report (`--format json`):** Top-level `benchmark` (and `target` on MariaDB), `report_date`, `overall_score`, `total_checks`, `results`. Per `RCA-004`, MariaDB emits `results` as `dict[category, list[control]]`, whereas MySQL/PostgreSQL/MongoDB/Cassandra/RHEL emit a flat `list[control]` (normalize with `sarif_exporter.normalize_control_results`).
- **SARIF v2.1.0 (`--format sarif`):** Schema `https://json.schemastore.org/sarif-2.1.0.json`, `version: "2.1.0"`, `runs[0].tool.driver.name: "cis-benchmarks-tools"`, `rules[]` (`CIS-<RULE_SPEC>-<ID>`), `results[]` (`ruleId`, `kind`, `level`, `message.text`, `locations[0].physicalLocation.artifactLocation.uri`, SHA-256 `partialFingerprints.cisControlFingerprint/v1`, `properties.complianceState`), and `runs[0].properties` (`target`, `ruleSpec`, `overallScore`, `counts`, `executionContext`). Validate via `sarif_exporter.validate_sarif_document(doc)`.
- **Dry-Run Remediation JSON (`--remediation-format json`):** `dry_run: true`, `target`, `rule_spec`, `family`, `total_items`, `items[]` (`control_id`, `compliance_state`, `action_type`, `requires_restart`, `risk_level`, `config_file`, `sql`, `shell`, `diff`, `verification_command`, optional `manual_guidance`).

## 4. Credential & Redaction Boundary
- Inject database passwords strictly via the `CIS_DB_PASSWORD` environment variable; never pass credentials in argv.
- All report strings from untrusted outputs are redacted by `SecretSanitizer`.
- `api_executor` traces should record preset name, sanitized args, exit code, and SHA-256 digest of generated output files.
