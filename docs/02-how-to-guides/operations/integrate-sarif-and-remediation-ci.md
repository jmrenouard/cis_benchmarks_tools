# Integrate SARIF and Dry-Run Remediation in CI

Read [Reference Index](../../03-reference/index.md) before you start.

## Prerequisites

1. Make sure that Python `3.8+` exists on the CI runner.
2. Confirm `security-events: write` permission for SARIF upload.

## Safety Instructions

**CAUTION:** Review dry-run diffs and SQL before production runs.
Unchecked edits can restart services or lock administrative accounts.

## Procedure

1. Run an audit with `--format sarif`:

   ```bash
   python3 audit_cis.py -t rhel9 --local -f sarif -o reports/rhel9.sarif
   ```

2. Validate the SARIF v2.1.0 output:

   ```bash
   python3 -c "import json, sarif_exporter as s; ok, m = s.validate_sarif_document(json.load(open('reports/rhel9.sarif'))); print(m); assert ok"
   ```

3. Generate a JSON report for dry-run remediation:

   ```bash
   python3 audit_cis.py -t postgresql16 --local -f json -o reports/pg16.json
   ```

4. Generate deterministic dry-run remediation diffs or Ansible tasks:

   ```bash
   python3 audit_cis.py --remediate-dry-run --from-report reports/pg16.json --remediation-format diff --remediation-output reports/pg16.diff
   python3 audit_cis.py --remediate-dry-run --from-report reports/pg16.json --remediation-format ansible --remediation-output reports/pg16.yml
   ```

5. Upload `reports/rhel9.sarif` in GitHub Actions with `github/codeql-action/upload-sarif`.

**NOTE:** `--remediate-dry-run` runs zero OS commands and zero SQL queries.

## Verification

1. Confirm that `validate_sarif_document` prints `Valid SARIF v2.1.0`.
2. Confirm that JSON dry-run output sets `"dry_run": true`:

   ```bash
   python3 audit_cis.py --remediate-dry-run --from-report reports/pg16.json --remediation-format json | head -n 5
   ```

## Rollback

1. Disable the SARIF upload step.
2. Delete stale `.sarif` and `.diff` files from `reports/`.
3. Run `python3 -m unittest tests/test_sarif_exporter.py -v`.

## Related Documentation

- [Reference Index](../../03-reference/index.md) · [Explanation Index](../../04-explanation/index.md)
