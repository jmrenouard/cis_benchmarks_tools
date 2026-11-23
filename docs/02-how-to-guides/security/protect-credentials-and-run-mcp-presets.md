# Protect Credentials and Run Read-Only MCP Presets

Read [Reference Index](../../03-reference/index.md) before you start.

## Prerequisites

1. Make sure that `conf/mcp_api_executor_presets.json` exists in the repository.
2. Store database credentials in a vault or `0600` option file.

## Safety Instructions

**WARNING:** Never pass `-p` or `--db-password` inside CLI arguments or MCP calls.
Command arguments expose plaintext passwords in `ps aux` and `/proc`.

**CAUTION:** Never use `--all`, `--auto-detect`, `--sync-cis`, or `--force` inside MCP presets.
Forbidden flags break the read-only `cis.mcp.contract.v1` boundary.

## Procedure

1. Export the password strictly via `CIS_DB_PASSWORD`:

   ```bash
   export CIS_DB_PASSWORD="$(vault_fetch_secret)"
   ```

2. Or pass a `0600` option file for MySQL, MariaDB, or PostgreSQL:

   ```bash
   chmod 0600 ~/.my.cnf
   python3 audit_cis.py -t mariadb106 --defaults-file ~/.my.cnf -f json -o reports/m106.json
   ```

3. Run only the four read-only presets from `conf/mcp_api_executor_presets.json`:

   ```bash
   python3 audit_cis.py --list-targets
   python3 audit_cis.py -t postgresql16 -f sarif -l en -m local -o reports/pg16.sarif
   python3 audit_cis.py --remediate-dry-run --from-report reports/pg16.json --remediation-format diff --remediation-output reports/pg16.diff
   ```

4. Unset `CIS_DB_PASSWORD` immediately after audit execution finishes:

   ```bash
   unset CIS_DB_PASSWORD
   ```

**NOTE:** `SecretSanitizer` masks passwords and tokens with `***` in logs and SARIF outputs.

## Verification

1. Run the contract and credential tests:

   ```bash
   python3 -m unittest tests/test_mcp_contract.py tests/test_credential_injection.py -v
   ```

2. Confirm zero plaintext passwords inside generated JSON and SARIF files.

## Rollback

1. Unset `CIS_DB_PASSWORD`.
2. Clear shell history (`history -c`).
3. Rotate any exposed database password immediately.
4. Delete log and report files from that session.

## Related Documentation

- [Reference Index](../../03-reference/index.md) · [Explanation Index](../../04-explanation/index.md)
