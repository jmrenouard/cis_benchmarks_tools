#!/usr/bin/env python3
"""
Link external HTML report templates in `templates/report_template.html` and `templates/category_report_template.html`
to all 18 CIS audit scripts with inline PSL fallbacks.
100% Python Standard Library (PSL ONLY).
"""

import glob
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(REPO_ROOT, "templates")

LOADER_FUNCTIONS = '''

def load_html_template():
    """Load common HTML report template from templates/ or fallback."""
    tmpl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "report_template.html")
    if os.path.exists(tmpl_path):
        try:
            with open(tmpl_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return HTML_TEMPLATE


def load_category_template():
    """Load common category report template from templates/ or fallback."""
    tmpl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "category_report_template.html")
    if os.path.exists(tmpl_path):
        try:
            with open(tmpl_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return CATEGORY_REPORT_TEMPLATE
'''


def process_audit_scripts():
    audit_files = sorted(glob.glob(os.path.join(REPO_ROOT, "audit_cis_*.py")))
    print(f"Linking external HTML templates to {len(audit_files)} audit scripts...")

    for file_path in audit_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "def load_html_template():" not in content:
            if "CATEGORY_REPORT_TEMPLATE = " in content:
                content = content.replace("CATEGORY_REPORT_TEMPLATE = ", LOADER_FUNCTIONS.strip() + "\n\nCATEGORY_REPORT_TEMPLATE = ")
            elif "def generate_html_report(" in content:
                content = content.replace("def generate_html_report(", LOADER_FUNCTIONS.strip() + "\n\ndef generate_html_report(")
            elif "def export_results(" in content:
                content = content.replace("def export_results(", LOADER_FUNCTIONS.strip() + "\n\ndef export_results(")

        content = content.replace("html_output = HTML_TEMPLATE.format(", "html_output = load_html_template().format(")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ Linked external template loader in {os.path.basename(file_path)}")


if __name__ == "__main__":
    process_audit_scripts()
