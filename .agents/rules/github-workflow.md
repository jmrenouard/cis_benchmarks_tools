---
trigger: always_on
description: Mandatory GitHub workflow: Issue -> Branch -> Tests -> Pull Request -> Merge for every request.
---

# Project Rule: Systematic GitHub Workflow (Issue + Branch + PR + Merge)

For every request made on the **CIS Benchmarks Tools Suite** project, you MUST systematically:

1. **Open a GitHub Issue** (`gh issue create`) in English describing the request and its acceptance criteria.
2. **Create a dedicated branch** (`<type>/issue-<id>-<slug>`) from `main` (use `git worktree` if other files are being modified in the workspace).
3. **Implement and run unit tests** (`python -m unittest discover -s tests -v`) and pre-commit checks (`python scripts/pre_commit_checks.py`) until full validation while respecting the `< 15,000` diff character limit per PR.
4. **Update `docs/ACTION_LOGBOOK.md` and `docs/RCA_REGISTER.md`** on every request, change, and result.
5. **Commit (Conventional Commits) and push the branch** to `origin`.
6. **Create a Pull Request** (`gh pr create`) referencing `Closes #<id>`.
7. **Merge the Pull Request** (`gh pr merge --merge --delete-branch`) and update `main`.
8. **Close the Issue with an explicit summary comment** (`gh issue comment <id> --body "..."` then `gh issue close <id>`).
