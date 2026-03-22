---
title: Project Governance Specifications
date: 2026-03-22
---
# Project Governance

## 🧠 Rationale
To ensure the CIS Benchmark Tools project scales smoothly as more databases and versions are added. 

## 🛠️ Implementation
This project follows the `hey-agent` framework. The structure consists of:
- **Execution Rules**: Found in `03_execution_rules.md`. Focuses on mandatory testing, naming conventions, and self-containment.
- **Best Practices**: Found in `04_best_practices.md`. Focuses on automation, UI consistency, and security.
- **Workflows**: Stored in `.agent/workflows/`. Key workflows include `add-benchmark`, `test-benchmark`, and `update-template`.

Future structural changes should be routed through the `/hey-agent` trigger.