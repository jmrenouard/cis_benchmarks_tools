# Workspace Rules for CIS Benchmarks Tools

## Mandatory Core Architecture Rule

> [!IMPORTANT]
> **Utiliser uniquement les modules standards Python 3 (Python Standard Library - PSL ONLY).**
> - Aucun paquet externe tierce partie (`pip`, `jinja2`, `yaml`, `requests`, etc.) n'est autorisé.
> - L'ensemble des scripts d'audit, utilitaires, bundlers et moteurs doivent s'exécuter de manière 100% autonome sur n'importe quelle installation Python 3 standard.

---

## Mandatory Git & Release Lifecycle for ALL Modifications

For EVERY modification (code change, script edit, refactoring, documentation update):

1. **Version Numbering & Mandatory Synchronization**:
   - Increment version in `VERSION` file (e.g. `1.3.0`).
   - Embed version number in **Branch name**, **Issue title**, and **PR title** (e.g., `feat/v1.3.0-descriptive-name`, `[v1.3.0] Title`).
   - Update `ROADMAP.md` and `POTENTIAL_ISSUES.md` with new features/fixes and version header.

2. **GitHub Issue**:
   - Create a detailed GitHub Issue via `gh issue create --title "[vX.Y.Z] Title"` with clear description, tasks checklist, and label.

3. **Feature Branch**:
   - Create a new feature branch from `main`: `git checkout -b feat/vX.Y.Z-<descriptive-name>`.

4. **Code Modification & Pre-Commit Routine**:
   - Write clean code following **Python 3 PSL ONLY** (zero third-party packages).
   - Run `make pre-commit` to bundle `audit_cis.py` and run 7-step validation (syntax, AST PSL, shell, report & specs integrity).

5. **Push Branch**:
   - `git push origin feat/vX.Y.Z-<descriptive-name>`

6. **Pull Request & Merge**:
   - Create PR via `gh pr create --title "[vX.Y.Z] Title"` pointing to `main` referencing `closes #<IssueID>`.
   - Merge PR via `gh pr merge <PR_ID> --merge --delete-branch`.
   - Sync local `main` via `git checkout main && git pull origin main`.
   - Provide complete summary to user with issue/PR links and validation status.
