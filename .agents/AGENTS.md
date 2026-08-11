# Workspace Rules for CIS Benchmarks Tools

## Mandatory Git & Release Lifecycle for ALL Modifications

For EVERY modification (code change, script edit, refactoring, documentation update):

1. **GitHub Issue**:
   - Create a detailed GitHub Issue via `gh issue create` with clear title, description, tasks checklist, and label (`enhancement`, `bug`, `documentation`, etc.).
2. **Feature Branch**:
   - Create a new feature branch from `main`: `git checkout -b feat/<descriptive-name>`.
3. **Code Modification & Mandatory Synchronization**:
   - Write clean, maintainable code following **Python Standard Library (PSL ONLY)** rule. No external packages allowed.
   - **Whenever Python code is modified**:
     - Increment version in `VERSION`.
     - Update `ROADMAP.md` with new features/fixes.
     - Update `POTENTIAL_ISSUES.md` with resolved debt/issues.
   - Run `make pre-commit` to bundle `audit_cis.py` and run syntax, AST PSL, shell, and report integrity checks.
4. **Push Branch**:
   - `git push origin feat/<descriptive-name>`
5. **Pull Request**:
   - Create Pull Request via `gh pr create` pointing to `main` with detailed summary and referencing `closes #<IssueID>`.
6. **Merge & Sync**:
   - Merge PR via `gh pr merge <PR_ID> --merge --delete-branch`.
   - Sync local `main` via `git checkout main && git pull origin main`.
   - Provide complete summary to user with issue/PR links and validation status.
