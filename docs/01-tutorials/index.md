# Tutorials

> [!NOTE]
> Practice CIS audits inside `/tmp/cis-*` before auditing production systems.

| Lesson | Outcome | Commands |
| :--- | :--- | :--- |
| [1. First Local & Docker Audit](01-first-local-and-docker-audit.md) | List 18 targets, run local JSON audit, audit container, verify SVG | `audit_cis.py --local`, `--docker` |
| [2. SARIF & Dry-Run Remediation Lab](02-sarif-and-dry-run-remediation-lab.md) | Export SARIF v2.1.0, generate dry-run `diff`/`sql`/`json` | `sarif_exporter.py`, `--remediate-dry-run` |

## Next Steps

- [How-To Guides](../02-how-to-guides/index.md) · [Reference](../03-reference/index.md)
- [Explanation](../04-explanation/index.md) · [Portal](../index.md)
