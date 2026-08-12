# Workspace Rules for CIS Benchmarks Tools

## 1. Mandatory Core Architecture Rule

> [!IMPORTANT]
> **Utiliser uniquement les modules standards Python 3 (Python Standard Library - PSL ONLY).**
> - Aucun paquet externe tierce partie (`pip`, `jinja2`, `yaml`, `requests`, etc.) n'est autorisé.
> - L'ensemble des scripts d'audit, utilitaires, bundlers et moteurs doivent s'exécuter de manière 100% autonome sur n'importe quelle installation Python 3 standard.

---

## 2. Mandatory PR Diff Size & Atomic Commit Rules

> [!IMPORTANT]
> **Limite stricte de taille des Pull Requests : maximum 15 000 caractères diff (15K chars diff limit).**
> - Les outils de revue automatisée (ex: Sourcery AI) et les relecteurs humains bloquent les PR volumineuses (> 150 000 caractères diff, e.g. PR #17, #18, #19).
> - **Vérification obligatoire avant ouverture de PR** : Exécuter `git diff main...HEAD | wc -c` pour s'assurer que la taille totale du diff est **inférieure à 15 000 caractères**.
> - **Découpage atomique des PRs (Atomic PR Splitting)** :
>   - Si l'ajout ou la modification d'un script d'audit (ex: nouveau benchmark 50K-85K bytes) dépasse 15 000 caractères diff, la fonctionnalité doit être **découpée en plusieurs PRs atomiques et successives** (ex: PR 1: Dockerfile + enregistrement dans `audit_cis.py` + squelette ; PR 2: Structure des règles/contrôles ; PR 3: Implémentation complète et tests).
>   - Ne JAMAIS regrouper plusieurs scripts d'audit volumineux ou des gros bundles générés dans une seule PR.

---

## 3. Mandatory Git & Release Lifecycle for ALL Modifications

For EVERY modification (code change, script edit, refactoring, documentation update):

1. **GitHub Issue**:
   - Create a detailed GitHub Issue via `gh issue create` with clear title, description, tasks checklist, and label (`enhancement`, `bug`, `documentation`, etc.).
2. **Feature Branch**:
   - Create a new feature branch from `main`: `git checkout -b feat/<descriptive-name>`.
3. **Code Modification & Mandatory Synchronization**:
   - Write clean, maintainable code following **Python 3 Standard Library (PSL ONLY)** rule. No external packages allowed.
   - **Whenever Python code is modified**:
     - Increment version in `VERSION`.
     - Synchronize `ROADMAP.md` (Executive Progress Dashboard & Phase Task Items).
     - Synchronize `POTENTIAL_ISSUES.md` (Resolved Architectural Backlog & PR List).
   - Run `make pre-commit` to bundle `audit_cis.py` and run syntax, AST PSL, shell, and report integrity checks.
4. **Push Branch**:
   - `git push origin feat/<descriptive-name>`
5. **Pull Request & Diff Size Verification**:
   - Verify PR diff size: `git diff main...HEAD | wc -c` MUST be **< 15,000 characters**.
   - Create Pull Request via `gh pr create` pointing to `main` with detailed summary and referencing `closes #<IssueID>`.
6. **Merge & Sync**:
   - Merge PR via `gh pr merge <PR_ID> --merge --delete-branch`.
   - Sync local `main` via `git checkout main && git pull origin main`.
   - Provide complete summary to user with issue/PR links and validation status.
