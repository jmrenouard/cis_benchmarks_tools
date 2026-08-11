# Workspace Rules for CIS Benchmarks Tools

## Mandatory Core Architecture Rule

> [!IMPORTANT]
> **Use Python 3 Standard Library ONLY (PSL ONLY).**
> - No third-party external packages (`pip`, `jinja2`, `yaml`, `requests`, etc.) are allowed.
> - All audit scripts, utilities, bundlers, and execution engines must run 100% standalone on any standard Python 3 installation.

---

## Mandatory Documentation Synchronization Rule

> [!IMPORTANT]
> **Maintain strict synchronization between `README.md` (English) and `README_fr.md` (French).**
> - Whenever features, targets, CLI options, or documentation are updated, **both `README.md` and `README_fr.md` MUST be updated simultaneously** to preserve 1:1 structural consistency.

---

## Mandatory Git & Release Lifecycle for ALL Modifications

For EVERY modification (code change, script edit, refactoring, documentation update):

1. **Version Numbering & Mandatory Synchronization**:
   - Increment version in `VERSION` file (e.g., `1.5.0`).
   - Embed version number in **Branch name**, **Issue title**, and **PR title** (e.g., `feat/v1.5.0-descriptive-name`, `[v1.5.0] Title`).
   - Update `ROADMAP.md` and `POTENTIAL_ISSUES.md` with new features/fixes and version header.
   - Synchronize `README.md` (English) and `README_fr.md` (French).

2. **GitHub Issue**:
   - Create a detailed GitHub Issue via `gh issue create --title "[vX.Y.Z] Title"` with clear description, tasks checklist, and label in English.

3. **Feature Branch**:
   - Create a new feature branch from `main`: `git checkout -b feat/vX.Y.Z-<descriptive-name>`.

4. **Code Modification & Pre-Commit Routine**:
   - Write clean code following **Python 3 PSL ONLY** (zero third-party packages).
   - Support multi-language i18n (`--lang {en,fr}`).
   - Run `make pre-commit` to bundle `audit_cis.py` and run 7-step validation (syntax, AST PSL, shell, report & specs integrity).

5. **Push Branch**:
   - `git push origin feat/vX.Y.Z-<descriptive-name>`

6. **Pull Request & Merge**:
   - Create PR via `gh pr create --title "[vX.Y.Z] Title"` pointing to `main` referencing `closes #<IssueID>`.
   - Merge PR via `gh pr merge <PR_ID> --merge --delete-branch`.
   - Sync local `main` via `git checkout main && git pull origin main`.
   - Provide complete summary to user with issue/PR links and validation status.
