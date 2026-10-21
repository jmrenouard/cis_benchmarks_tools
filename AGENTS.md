# CIS Benchmarks Tools Suite Project Rules (AGENTS.md)

These rules apply **without exception** to every session and every agent working on the **CIS Benchmarks Tools Suite** (`jmrenouard/cis_benchmarks_tools`) repository. All project documentation, rules, governance registers, commit messages, issues, and Pull Requests **MUST** be written in **English**.

---

## 1. Core Architecture & PR Diff Constraints

1. **100% Python Standard Library (`PSL ONLY`)**:
   - Use **exclusively** Python 3 Standard Library modules across all audit engines (`audit_cis_*.py`), unified CLI (`audit_cis.py`), execution drivers (`execution_drivers.py`), orchestrators (`audit_orchestrator.py`), and diagnostics (`audit_diagnostics.py`). Zero external packages (`pip`, `requests`, `jinja2`, `yaml`, `paramiko`) are allowed.
2. **Strict Pull Request Diff Size Limit (`< 15,000` characters)**:
   - Every Pull Request diff (`git diff main...HEAD | wc -c`) **MUST** remain under **15,000 characters**. Split larger changes into sequential, atomic Issues and Pull Requests.
3. **Preservation of Core Project Identity**:
   - Preserve the 18 official CIS Benchmarks / DISA STIG targets (887 controls across MariaDB, MySQL, PostgreSQL, MongoDB, Cassandra, and RHEL 8/9/10), 4-tier execution context (`Local`, `Remote SSH`, `Local Docker`, `Remote SSH Docker`), 5-state compliance taxonomy (`Pass`, `Fail`, `Error`, `Manual`, `Not Applicable`), and 100% offline inline SVG reporting.

---

## 2. Mandatory GitHub Workflow (Required for Every Request)

For **every user request** (new feature, bug fix, CI/CD, documentation, or refactoring), the agent **MUST systematically** execute the complete GitHub lifecycle below:

1. **Open a GitHub Issue**:
   - Create an issue using `gh issue create --title "<type>: <title>" --body "<context, objectives, and acceptance criteria>"` and retrieve `#<id>`.
2. **Create a Dedicated Branch**:
   - Create `<type>/issue-<id>-<slug>` from `main` (use `git worktree` when parallel work exists in the main working directory).
3. **TDD Implementation & Unit Tests**:
   - Write or update unit tests in `tests/` and verify that `python -m unittest discover -s tests -v` and `python scripts/pre_commit_checks.py` pass locally.
4. **Update Governance Registers (`docs/ACTION_LOGBOOK.md` & `docs/RCA_REGISTER.md`)**:
   - Systematically update `docs/ACTION_LOGBOOK.md` and `docs/RCA_REGISTER.md` before committing (see Sections 3 and 4 below).
5. **Commit & Push**:
   - Make atomic Conventional Commits (`feat:`, `fix:`, `ci:`, `docs:`, `test:`, `chore:`) referencing `Refs #<id>` or `Closes #<id>`, keeping PR diff `< 15,000` characters, and push (`git push -u origin <branch>`).
6. **Create a Pull Request (PR)**:
   - Open a PR targeting `main` via `gh pr create --base main --head <branch> --title "<type>: <title> (#<id>)" --body "Closes #<id> ..."`.
7. **Merge the Pull Request & Close**:
   - Merge into `main` via `gh pr merge <pr-id> --merge --delete-branch` and synchronize `main` (`git pull --ff-only origin main`).

---

## 3. Ongoing / Completed Action Logbook (`docs/ACTION_LOGBOOK.md`)

The agent **MUST systematically update** [`docs/ACTION_LOGBOOK.md`](docs/ACTION_LOGBOOK.md) **on every request, every change, and every result**:

1. **Upon receiving a request (`IN PROGRESS` / `Ongoing Actions`)**:
   - Add an entry with identifier (`ACT-XXX`), ISO timestamp, GitHub Issue (`#<id>`), and exact **Request**.
2. **During and after implementation (`CHANGES & RESULT`)**:
   - Document created/modified files (**Changes**) and verification metrics (**Result**: passing unit tests, `pre_commit_checks.py`, PR number, and merge commit).
3. **Upon completion (`COMPLETED` / `Completed Actions`)**:
   - Move the action to the completed actions section once tests and the Pull Request are validated.

---

## 4. RCA Register of Errors, Dead-Ends, Approximations, and Unimplemented Ideas (`docs/RCA_REGISTER.md`)

The agent **MUST systematically update** [`docs/RCA_REGISTER.md`](docs/RCA_REGISTER.md) **on every request, every change, and every result** whenever any of the following four events occurs:

1. **Errors & Bugs Encountered (`RCA-XXX`)**:
   - Log every runtime error, test failure, platform discrepancy, or CI/CD conflict with: *Observed Symptom*, *Root Cause Analysis (5 Whys)*, *Applied Change / Fix*, and *Result / Non-Regression Test*.
2. **Technical Dead-Ends & Abandoned Leads (`IMP-XXX`)**:
   - Record every explored and rejected approach (non-PSL dependencies, CDN reliance, `2>/dev/null` masking, oversized PRs) so no session repeats the same dead-end.
3. **Current Approximations & Simplifying Assumptions (`APP-XXX`)**:
   - Declare every simplification compared to live production environments or official CIS Benchmarks / DISA STIG specifications with its impact and removal condition.
4. **Unimplemented Ideas & Future Roadmap (`IDEA-XXX`)**:
   - Log every feature, optimization, or extension identified outside the immediate scope with its priority and target module.
