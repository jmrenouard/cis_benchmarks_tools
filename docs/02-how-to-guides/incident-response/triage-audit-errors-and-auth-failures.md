# Triage Audit Errors and Authentication Failures

Read [Reference Index](../../03-reference/index.md) before you start.

## Prerequisites

1. Make sure that you have shell access on the controller.
2. Collect the target key, transport mode, and `Error` message.

## Safety Instructions

**CAUTION:** Never add `2>/dev/null` to hide `stderr` streams.
Masked `stderr` hides `MISSING_BINARY` and `PERMISSION_DENIED` faults.

## Procedure

1. Classify each `Error` or `Fail` entry with `CommandFailureClassifier`:

   ```bash
   python3 -c "import json; from audit_diagnostics import CommandFailureClassifier as C; r=json.load(open('reports/audit.json')); rows=r['results'] if isinstance(r['results'],list) else sum(r['results'].values(),[]); print([(x.get('number') or x.get('id'), C.classify_control_result(x).category) for x in rows if str(x.get('status','')).upper() in ('ERROR','FAIL')])"
   ```

2. If the classifier reports `MISSING_BINARY` or code `127`, install the client binary.
3. If the classifier reports `PERMISSION_DENIED` or code `126`, add `--sudo`.
4. If the classifier reports `AUTH_FAILURE`, verify `CIS_DB_PASSWORD`, `--db-user`, or `--defaults-file`.
5. If the classifier reports `CONNECTION_ERROR`, verify the database host and port.
6. If the classifier reports `TIMEOUT` or code `-1`, verify network latency and host load.
7. Re-run the failed target audit:

   ```bash
   python3 audit_cis.py -t mariadb106 --local -f json -o reports/m106_check.json
   ```

**NOTE:** The score engine excludes `Error`, `Manual`, and `Not Applicable` checks from percentages.

## Verification

1. Confirm zero `Error` entries inside the refreshed JSON report.
2. Confirm that `audit_cis.py` exits with code `0`.

## Rollback

1. Restore previous `--defaults-file` or `sudoers` settings.
2. Delete temporary diagnostic reports from `reports/`.
3. Escalate persistent outages to the database administrator.

## Related Documentation

- [Reference Index](../../03-reference/index.md) · [Explanation Index](../../04-explanation/index.md)
