# Error, Failure Classifier, and Alert Matrix

Normative failure taxonomy in `audit_diagnostics.CommandFailureClassifier` (`audit_diagnostics.py`).

## 1. Priority Failure Classifier (`CommandFailureClassifier.classify`)

| Prio | `FailureCategory` | Env | Signals / Exit Codes | Runbook |
| :---: | :--- | :---: | :--- | :--- |
| 0 | `CLEAN_PASS` | `false` | `returncode == 0` | — |
| 1 | `TIMEOUT` | `true` | `rc == -1`, `timed out`, `TimeoutExpired` | [Triage](../../02-how-to-guides/incident-response/triage-audit-errors-and-auth-failures.md) |
| 2 | `MISSING_BINARY` | `true` | `rc == 127`, `command not found`, `WinError 2` | [Triage](../../02-how-to-guides/incident-response/triage-audit-errors-and-auth-failures.md) |
| 3 | `AUTH_FAILURE` | `true` | `password authentication failed`, `Access denied for user` | [Credentials](../../02-how-to-guides/security/protect-credentials-and-run-mcp-presets.md) |
| 4 | `CONNECTION_ERROR` | `true` | `Connection refused`, `Can't connect to`, `No route` | [Remote Audits](../../02-how-to-guides/deployment/run-remote-ssh-and-docker-audits.md) |
| 5 | `PERMISSION_DENIED` | `true` | `rc == 126`, `Permission denied`, `EACCES` | [Triage](../../02-how-to-guides/incident-response/triage-audit-errors-and-auth-failures.md) |
| 6 | `SYNTAX_ERROR` | `false` | `syntax error`, `unknown option`, `bad flag` | [SARIF CI](../../02-how-to-guides/operations/integrate-sarif-and-remediation-ci.md) |
| 7 | `UNKNOWN_ERROR` | `true` | Unmatched non-zero exit (`1`, `2`, `255`) | [Triage](../../02-how-to-guides/incident-response/triage-audit-errors-and-auth-failures.md) |

## 2. Control-Level Triage (`classify_control_result`)

| Status | Behavior | Category | Runbook |
| :--- | :--- | :--- | :--- |
| `PASS` / `SUCCESS` | Clean pass | `CLEAN_PASS` | — |
| `MANUAL` / `MANUEL` | Manual review | `MANUAL_ASSESSMENT_REQUIRED` | — |
| `ERROR` | Passes `output` to `classify()` | Env category | [Triage](../../02-how-to-guides/incident-response/triage-audit-errors-and-auth-failures.md) |
| `FAIL` / `FAILED` | Re-classifies env/auth patterns; else security | `SECURITY_NON_COMPLIANCE` or env | [Credentials](../../02-how-to-guides/security/protect-credentials-and-run-mcp-presets.md) |

## Related Documentation

- [CLI Flags & Exit Codes](../cli-and-scripts/cli-flags-and-exit-codes.md) · [Targets & Transport Matrix](../configuration/targets-and-transport-matrix.md)
- [Explanation Index](../../04-explanation/index.md)
