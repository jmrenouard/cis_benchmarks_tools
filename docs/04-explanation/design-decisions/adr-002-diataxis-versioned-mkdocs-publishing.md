# ADR-002: Diátaxis Documentation and Versioned MkDocs Publishing

| Attribute | Value |
| :--- | :--- |
| **Status** | Accepted (`2026-11-23`) |
| **Portal** | [https://cis-benchmarks.lightpath.fr/](https://cis-benchmarks.lightpath.fr/) |

## Context

Flat Markdown (`README.md`, `ROADMAP.md`, `documentation/specifications/*.md`) mixed genres, while tags
(`v2.9.0`, `v2.9.1`, `v2.10.0`) predated `mkdocs.yml` and Diátaxis directories.

## Multi-Version Publishing Pipeline

```mermaid
flowchart LR
    GIT["Tags + main"] --> BLD["build_versioned_docs.py"]
    BLD --> HK["mkdocs_hooks.py"]
    HK --> MK["mkdocs build --strict"]
    MK --> DIST["site_dist/ + .htaccess"]
    DIST --> SFTP["SFTP -> cis-benchmarks.lightpath.fr"]
```

## Options Considered and Trade-Offs

| Option | Genre Split | Tag Versioning | Hosting & Security | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **A: Flat Markdown** | Mixed genres | Single branch | No search/redirects | Rejected |
| **B: Unversioned MkDocs** | Medium | Drifts from tags | Missing `/latest/` | Rejected |
| **C: Diátaxis + Overlay** | 4 quadrants + STE | `git archive` overlay | `.htaccess` + guard | **Selected** |

## Decision

Adopt **Option C**: split `01-tutorials/`, `02-how-to-guides/` (STE), `03-reference/`, and `04-explanation/`.
`scripts/mkdocs_hooks.py` mounts virtual docs (`overview-en.md`, `overview-fr.md`, `ROADMAP.md`, `specs/*.md`) and
rewrites links. `scripts/build_versioned_docs.py` builds `/main/` (`/dev/`) and tags (`/latest/`) with
`assert_no_private_files`.

## Consequences

- Historical snapshots (`v2.9.0`–`v2.10.0`) and `/main/` share one `mike` switcher.
- CI enforces 40-char SHA pinning, `< 15,000` byte PR diffs, and pure-PSL tests.

## Related Documentation

- [CLI Flags & Exit Codes](../../03-reference/cli-and-scripts/cli-flags-and-exit-codes.md)
- [Integrate SARIF CI](../../02-how-to-guides/operations/integrate-sarif-and-remediation-ci.md) · [Four-Tier PSL Architecture](../architecture-overview/four-tier-psl-audit-architecture.md)
