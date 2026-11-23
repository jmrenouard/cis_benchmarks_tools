# ADR-001: 100% Python Standard Library (`PSL ONLY`) and Offline Inline SVG

| Attribute | Value |
| :--- | :--- |
| **Status** | Accepted (`2026-11-23`) |
| **Supersedes** | `IMP-001`, `IMP-002`, `IMP-003`, `IMP-006` (`docs/RCA_REGISTER.md`) |

## Context

Hardened servers forbid `pip install` (`requests`, `jinja2`, `pyyaml`, `paramiko`) and air-gapped networks block
CDNs (`Chart.js`). Operators still need CLI audits, SARIF output, and visual HTML reports.

## Options Considered and Trade-Offs

| Option | Portability | Supply-Chain Risk | Visual Reports | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **A: `pip` + CDN JS** | Fails offline | High external deps | Blank offline | Rejected |
| **B: Hybrid PSL + `pip`** | Divergent behavior | Medium | Splits templates | Rejected |
| **C: Strict PSL + SVG** | Any Python `3.8+` | Zero deps (`ast`) | Self-contained SVG | **Selected** |

## Decision

Restrict runtime modules to Python Standard Library (`PSL ONLY`), checked by `scripts/pre_commit_checks.py`. Render
charts via inline `<svg>` in `cis_core_engine.py`, preserve `stderr` without `2>/dev/null`, and inject secrets via
environment variables.

## Consequences

- `pyproject.toml` sets `dependencies = []`, and PSL `unittest` suites pass on bare CI runners.
- Tests and contributors must avoid third-party imports (`yaml`, `pytest`, `requests`).

## Related Documentation

- [Targets & Scoring](../../03-reference/configuration/targets-and-transport-matrix.md)
- [Protect Credentials](../../02-how-to-guides/security/protect-credentials-and-run-mcp-presets.md) · [Triage Errors](../../02-how-to-guides/incident-response/triage-audit-errors-and-auth-failures.md)
