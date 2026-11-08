---
title: System Architecture Specification
date: 2026-11-08
category: specification
---

# System Architecture Specification

## 1. Architectural Philosophy
The CIS Benchmarks Tools Suite is engineered on the principle of **Zero-Dependency Security Auditing**. Security tools must be portable, verifiable, auditable, and incapable of introducing supply-chain vulnerabilities.

## 2. 100% Python Standard Library (`PSL ONLY`)
- The suite requires Python 3.8+ and relies **exclusively** on modules from the Python Standard Library (`os`, `sys`, `json`, `subprocess`, `re`, `shlex`, `html`, `xml.etree.ElementTree`, `datetime`, `argparse`, `unittest`, `ast`, etc.).
- Third-party packages (`requests`, `jinja2`, `yaml`, `paramiko`, `cryptography`, `pandas`) are strictly forbidden.
- Compliance is mechanically verified in `scripts/pre_commit_checks.py` via Abstract Syntax Tree (AST) inspection of import nodes.

## 3. Dual-Mode Architecture: Standalone Portability & Unified Orchestration
The codebase operates under a dual-mode pattern:
1. **Standalone Portability**:
   - Each of the 18 audit scripts (`audit_cis_<target>.py`) is capable of executing as a single, self-contained file on target systems where network access, local packages, or extra repository files are unavailable.
   - Scripts embed fallback recommendation dictionaries and self-contained inline SVG renderers.
2. **Modular Orchestration Core**:
   - When executed within the repository, audit scripts dynamically leverage shared core components:
     - `cis_core_engine.py`: Shared rule loading, command execution, scoring, SVG chart rendering, and multi-format exporters.
     - `execution_drivers.py`: Polymorphic execution transports (Local, Docker, SSH, Remote Docker) with credential sanitization.
     - `audit_diagnostics.py`: Root-cause failure classification and diagnostic summaries.
     - `audit_orchestrator.py`: Multi-product audit scheduling, discovery, container resolution, and parallel execution.
     - `audit_cis.py`: Unified entry point CLI.
     - `rules/<target_key>.json`: Decoupled, schema-validated CIS benchmark rule specifications.

## 4. Component Interaction Diagram

```
+-------------------------------------------------------------------+
|                        audit_cis.py (Unified CLI)                 |
+---------------------------------+---------------------------------+
                                  |
               +------------------+------------------+
               |                                     |
               v                                     v
+-----------------------------+       +-----------------------------+
|    audit_orchestrator.py    |       |  18 Standalone Scripts       |
|    (Multi-target / Pipeline)|       |  (audit_cis_<target>.py)     |
+--------------+--------------+       +--------------+--------------+
               |                                     |
               +------------------+------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                   cis_core_engine.py (Core Engine)                |
|  - load_recommendations()       - run_command()                   |
|  - evaluate_condition()         - calculate_scores()              |
|  - build_inline_svg_*()         - export_results()                |
+---------------------------------+---------------------------------+
                                  |
               +------------------+------------------+
               |                                     |
               v                                     v
+-----------------------------+       +-----------------------------+
|    execution_drivers.py     |       |    audit_diagnostics.py     |
|  - LocalExecutor            |       |  - CommandFailureClassifier |
|  - DockerExecutor           |       |  - FailureCategory          |
|  - SSHExecutor              |       |  - FailureDiagnostic        |
|  - RemoteSSHContainerExec   |       +-----------------------------+
|  - SecretSanitizer          |
+-----------------------------+
               |
               v
+-------------------------------------------------------------------+
|       Target Systems: Bare-Metal / Docker / Remote SSH / Hybrid   |
+-------------------------------------------------------------------+
```
