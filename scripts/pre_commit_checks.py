#!/usr/bin/env python3
"""
Pre-Commit Quality Assurance Routine for CIS Benchmarks Suite.
Validates PSL compliance, syntax, repository structure, report integrity, rules/ JSON integrity, and unit tests.
100% Python Standard Library (PSL ONLY).
"""

import ast
import glob
import json
import os
import py_compile
import subprocess
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

VERSION_FILE = os.path.join(REPO_ROOT, "VERSION")


def step_verify_and_sync_version():
    """Verify repository VERSION file exists and reads clean semantic version string."""
    print("🏷️ [1/8] Verifying repository VERSION file...")
    if not os.path.exists(VERSION_FILE):
        print(f"❌ Version file missing: {VERSION_FILE}", file=sys.stderr)
        sys.exit(1)
    with open(VERSION_FILE, "r", encoding="utf-8") as f:
        version = f.read().strip()
    print(f"  ✓ Repository Version: v{version}")


def step_concatenate_python_code():
    """Build audit_cis.py by calling bundle_audit_cis.py."""
    print("📦 [2/8] Concatenating & updating unified Python audit script (audit_cis.py)...")
    bundler_script = os.path.join(REPO_ROOT, "scripts", "bundle_audit_cis.py")
    try:
        subprocess.run([sys.executable, bundler_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to run script bundler {bundler_script}: {e}", file=sys.stderr)
        sys.exit(1)


def step_validate_python_syntax():
    """Check Python syntax for all .py files using py_compile."""
    print("🐍 [3/8] Validating Python syntax across all scripts (py_compile)...")
    py_files = sorted(glob.glob("**/*.py", recursive=True))
    for py in py_files:
        try:
            py_compile.compile(py, doraise=True)
            print(f"  ✓ {py}")
        except py_compile.PyCompileError as e:
            print(f"❌ Syntax error in {py}: {e}", file=sys.stderr)
            sys.exit(1)


def step_check_psl_compliance():
    """AST check to ensure NO third-party imports are used in audit_cis.py."""
    print("🔒 [4/8] Verifying Python Standard Library (PSL) compliance on audit_cis.py...")
    audit_script = os.path.join(REPO_ROOT, "audit_cis.py")
    with open(audit_script, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename="audit_cis.py")

    allowed_std_libs = {
        "argparse", "datetime", "json", "os", "subprocess", "sys", "re",
        "ast", "py_compile", "glob", "unittest", "html", "xml", "math"
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name.split('.')[0]
                if name not in allowed_std_libs:
                    print(f"❌ Forbidden non-PSL import '{name}' detected in audit_cis.py!", file=sys.stderr)
                    sys.exit(1)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                name = node.module.split('.')[0]
                if name not in allowed_std_libs:
                    print(f"❌ Forbidden non-PSL import '{name}' detected in audit_cis.py!", file=sys.stderr)
                    sys.exit(1)

    print("  ✓ audit_cis.py uses Python Standard Library ONLY!")


def step_check_shell_scripts():
    """Validate syntax of shell scripts using bash -n."""
    print("📜 [5/8] Validating Shell script syntax (bash -n)...")
    shell_files = sorted(glob.glob("scripts/*.sh"))
    for sh in shell_files:
        try:
            subprocess.run(["bash", "-n", sh], check=True)
            print(f"  ✓ {sh}")
        except subprocess.CalledProcessError:
            print(f"❌ Shell syntax error in {sh}", file=sys.stderr)
            sys.exit(1)


def step_validate_reports_and_structure():
    """Verify repository sub-directories, rules/ JSON specs, and report file integrity (> 1 KB)."""
    print("📁 [6/8] Validating repository structure, rules specs, and report integrity...")
    required_dirs = ["reports", "docker", "scripts", "CIS_DATA", "tests", "rules"]
    for d in required_dirs:
        if not os.path.isdir(d):
            print(f"❌ Required directory missing: {d}", file=sys.stderr)
            sys.exit(1)
        print(f"  ✓ Directory present: {d}/")

    rule_files = glob.glob("rules/*.json")
    for rfile in rule_files:
        try:
            with open(rfile, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list) or len(data) == 0:
                    print(f"❌ Rule file {rfile} is empty or not a valid JSON list", file=sys.stderr)
                    sys.exit(1)
        except Exception as e:
            print(f"❌ Invalid JSON rule file {rfile}: {e}", file=sys.stderr)
            sys.exit(1)
    print(f"  ✓ {len(rule_files)} JSON rule specification files validated in rules/")

    reports = glob.glob("reports/rapport_cis_*.html")
    valid_reports = 0
    for r in reports:
        size = os.path.getsize(r)
        if size < 1024:
            print(f"❌ Report file {r} is corrupt or empty ({size} bytes)", file=sys.stderr)
            sys.exit(1)
        valid_reports += 1
    print(f"  ✓ {valid_reports} HTML audit reports validated in reports/")


def step_validate_cisdata_and_permissions():
    """Verify CIS_DATA markdown specifications and script executable permissions."""
    print("🔒 [7/8] Validating CIS_DATA specs and executable permissions...")
    md_files = glob.glob("CIS_DATA/*.md")
    if not md_files:
        print("❌ No Markdown specification files found in CIS_DATA/", file=sys.stderr)
        sys.exit(1)

    for md in md_files:
        if os.path.getsize(md) == 0:
            print(f"❌ Empty specification file: {md}", file=sys.stderr)
            sys.exit(1)
    print(f"  ✓ {len(md_files)} Markdown specification files validated in CIS_DATA/")

    executable_scripts = ["audit_cis.py", "scripts/bundle_audit_cis.py", "scripts/pre_commit_checks.py", "scripts/pre-commit.sh"]
    for script in executable_scripts:
        if os.path.exists(script):
            os.chmod(script, 0o755)
            print(f"  ✓ Executable permission confirmed: {script}")


def step_run_unit_tests():
    """Run automated unit tests using unittest PSL module."""
    print("🧪 [8/8] Running automated unit test suite (unittest)...")
    suite = unittest.defaultTestLoader.discover(os.path.join(REPO_ROOT, "tests"))
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    if not result.wasSuccessful():
        print("❌ Unit test failures detected!", file=sys.stderr)
        sys.exit(1)
    print(f"  ✓ All {result.testsRun} unit tests PASSED successfully!")


def main():
    print("🔍 Running CIS Benchmarks Pre-Commit Routine (Python PSL)...")
    print("=" * 60)
    step_verify_and_sync_version()
    step_concatenate_python_code()
    step_validate_python_syntax()
    step_check_psl_compliance()
    step_check_shell_scripts()
    step_validate_reports_and_structure()
    step_validate_cisdata_and_permissions()
    step_run_unit_tests()
    print("=" * 60)
    print("🎉 All Pre-Commit Checks PASSED successfully!")


if __name__ == "__main__":
    main()
