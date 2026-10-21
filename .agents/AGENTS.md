# Workspace Rules for CIS Benchmarks Tools

> See root [`AGENTS.md`](../AGENTS.md) and `.agents/rules/` (`git-workflow.md`, `github-workflow.md`, `project-governance.md`). All project files, rules, and registers **MUST** be in **English**.

## 1. Core Architecture & PR Diff Limit

> [!IMPORTANT]
> - **100% Python Standard Library (`PSL ONLY`)**: Zero external third-party packages (`pip`, `jinja2`, `yaml`, `requests`, `paramiko`) allowed in runtime/audit scripts.
> - **Strict PR Diff Limit (`< 15,000` chars)**: Run `git diff main...HEAD | wc -c` before opening any PR. Split larger changes into atomic PRs.

## 2. Mandatory Git, Registers & Release Lifecycle

For **every modification** (code, CI/CD, refactoring, documentation):
1. **GitHub Issue**: Open an issue via `gh issue create`.
2. **Dedicated Branch**: Create `<type>/issue-<id>-<slug>` from `main` (or `git worktree`).
3. **Implementation, Registers & Validation**:
   - Update [`docs/ACTION_LOGBOOK.md`](../docs/ACTION_LOGBOOK.md) and [`docs/RCA_REGISTER.md`](../docs/RCA_REGISTER.md) on every request, change, and result.
   - Synchronize `VERSION`, `ROADMAP.md`, and `POTENTIAL_ISSUES.md` when Python code changes; run `python scripts/pre_commit_checks.py` and `python -m unittest discover -s tests -v`.
4. **PR & Merge**: Push branch, verify diff `< 15,000` chars, open PR (`gh pr create`), merge (`gh pr merge --merge --delete-branch`), and sync `main`.
