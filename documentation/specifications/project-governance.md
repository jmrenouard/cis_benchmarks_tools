---
title: Project Governance Specifications
date: 2026-11-08
category: governance
---

# Project Governance Specification

## 1. Overview & Rationale
The **CIS Benchmarks Tools Suite** (`jmrenouard/cis_benchmarks_tools`) is an automated, enterprise-grade compliance auditing engine for databases and Linux operating systems. To maintain absolute security, determinism, and high code quality across 18 official benchmark targets (887 controls), this document establishes the binding governance standards for development, contribution, and automated agent workflows.

## 2. Core Architectural Pillars
All work within this repository must strictly adhere to seven non-negotiable architectural pillars:
1. **100% Python Standard Library (`PSL ONLY`)**: Exclusively PSL modules are permitted across all audit engines (`audit_cis_*.py`), unified CLI (`audit_cis.py`), execution transports (`execution_drivers.py`), orchestrator (`audit_orchestrator.py`), and diagnostics (`audit_diagnostics.py`). Zero third-party packages (`pip`, `requests`, `jinja2`, `yaml`, `paramiko`) are allowed.
2. **Strict PR Diff Size Limit (`< 15,000` characters)**: Every Pull Request diff (`git diff main...HEAD | wc -c`) must remain strictly under 15,000 characters to pass automated review bots and human review.
3. **18 Official CIS Benchmarks & DISA STIG Targets**: Comprehensive coverage of 887 controls across MariaDB, MySQL, PostgreSQL, MongoDB, Cassandra, and RHEL 8/9/10.
4. **4-Tier Execution Context**: Polymorphic execution transports (`Local`, `Remote SSH`, `Local Docker`, `Remote SSH Docker`) handled seamlessly by `execution_drivers.py`.
5. **5-State Compliance Taxonomy**: Unified result states (`Pass`, `Fail`, `Error`, `Manual`, `Not Applicable`).
6. **100% Offline Inline SVG Reporting**: Zero external CDN dependencies for visualizations; charts are rendered via native inline SVG (`build_inline_svg_donut_chart`, `build_inline_svg_category_chart`).
7. **Living Governance Registers**: Continuous logging in `docs/ACTION_LOGBOOK.md` and `docs/RCA_REGISTER.md` on every request, change, and result.

## 3. Mandatory 9-Step GitHub Lifecycle
Every task, bug fix, feature, or refactoring must follow this 9-step workflow in English:
0. **Issue Creation (`gh issue create`)**: Create a GitHub issue with structured context, objectives, and acceptance criteria.
1. **Dedicated Branch**: Branch off `main` as `<type>/issue-<id>-<slug>` (use `git worktree` when needed).
2. **Pre-commit Test Pass**: Pass 100% of unit tests (`python -m unittest discover -s tests -v`) and pre-commit checks (`python scripts/pre_commit_checks.py`).
3. **Rigorous Staging (`git add`)**: Stage only tracked files; exclude temporary files, caches, or dumps.
4. **Structured Commit (`git commit`)**: Use Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`) referencing `Refs #<id>` or `Closes #<id>`.
5. **Branch Push**: Push to remote (`git push -u origin <branch>`).
6. **Pull Request (`gh pr create`)**: Open a PR targeting `main` referencing `Closes #<id>`, verifying diff < 15,000 chars.
7. **PR Merge (`gh pr merge`)**: Merge via `gh pr merge <pr-id> --merge --delete-branch` and fast-forward `main`.
8. **Issue Closure (`gh issue close --comment "..."`)**: Close the issue with a detailed summary comment referencing the merged PR.

## 4. Mandatory Living Registers
- **Action Logbook (`docs/ACTION_LOGBOOK.md`)**: Records every action under Ongoing Actions (`IN PROGRESS`) and moves it to Completed Actions (`COMPLETED`) with PR number, diff size, and test results.
- **RCA Register (`docs/RCA_REGISTER.md`)**: Tracks 4 transparent categories:
  1. *Errors & Bugs Encountered (`RCA-XXX`)*: 5 Whys analysis, fix, and non-regression tests.
  2. *Technical Dead-Ends & Abandoned Leads (`IMP-XXX`)*: Explored and rejected approaches (e.g., non-PSL deps, Chart.js, SSH ControlMaster).
  3. *Current Approximations & Simplifying Assumptions (`APP-XXX`)*: Active heuristics or simplifications.
  4. *Unimplemented Ideas & Future Roadmap (`IDEA-XXX`)*: Backlog of prospective improvements.

## 5. Strict English-Only Policy
All GitHub issues, pull requests, commit messages, code comments, docstrings, and governance registers must be strictly written in English. Zero French is permitted on GitHub or within code files.