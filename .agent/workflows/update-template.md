---
trigger: explicit_call
description: Workflow for updating the HTML/CSS template across all scripts simultaneously.
category: workflow
---
# Update HTML Template Workflow

## 🧠 Rationale
Because each script is self-contained, the `HTML_TEMPLATE` string is duplicated across all `audit_cis_*.py` files. Updates to the report UI must be synchronized.

## 🛠️ Implementation
When an update to the UI/HTML is requested:

1. **Modify One Script**: Implement and test the HTML/CSS changes in ONE script (e.g., `audit_cis_mysql_80.py`) using the `test-benchmark` workflow to verify rendering.
2. **Extract Template**: Extract the exact `HTML_TEMPLATE` and `CATEGORY_REPORT_TEMPLATE` multiline strings.
3. **Apply Globally**: Use search-and-replace tools (`replace_file_content` or `multi_replace`) to inject the updated strings into all other `audit_cis_*.py` files in the workspace.
4. **Validation**: Run a quick syntax check (e.g., `python3 -m py_compile`) on all modified scripts to ensure string boundaries weren't broken.

## ✅ Verification
- Run `grep_search` to confirm all scripts have the new template pattern.
- Python compilation passes for all modified scripts.