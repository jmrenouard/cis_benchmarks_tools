---
trigger: explicit_call
description: Workflow for updating the HTML/CSS template across all scripts simultaneously.
category: workflow
---
# Update HTML Template Workflow

## 🧠 Rationale
HTML report templates are centralized in the common template file `templates/report_template.html` and `templates/category_report_template.html`. All `audit_cis_*.py` scripts and `audit_cis.py` load templates dynamically via `load_html_template()` with inline PSL fallbacks.

## 🛠️ Implementation
When an update to the UI/HTML is requested:

1. **Modify Central Template**: Edit `templates/report_template.html` (or `templates/category_report_template.html`).
2. **Verify Rendering**: Test report generation on any script (e.g. `python3 audit_cis_mysql_80.py`) or run `python3 scripts/generate_all_reports.py`.
3. **Validation**: Run `make pre-commit` to re-bundle `audit_cis.py` and validate syntax, AST PSL rules, executable permissions, and unit tests.

## ✅ Verification
- Generated HTML reports render correctly in modern browsers.
- `make pre-commit` completes successfully.