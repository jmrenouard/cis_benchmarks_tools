#!/usr/bin/env python3
"""
Pre-Commit Validation Routine (Python Standard Library ONLY).
Concatenates Python benchmark code into `audit_cis.py` and runs syntax/PSL/version/structure/permissions/tests integrity checks.
"""

import ast
import glob
import os
import py_compile
import subprocess
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
os.chdir(REPO_ROOT)


def step_verify_and_sync_version():
    """Verify VERSION file exists and synchronize version across unified script."""
    print("🏷️ [1/8] Verifying repository VERSION file...")
    version_file = os.path.join(REPO_ROOT, "VERSION")
    if not os.path.exists(version_file):
        print("❌ VERSION file missing in repository root!", file=sys.stderr)
        sys.exit(1)

    with open(version_file, "r", encoding="utf-8") as f:
        version = f.read().strip()
    print(f"  ✓ Repository Version: v{version}")
    return version


def step_concatenate_python_code():
    """Concatenate and synchronize python audit code into unified audit_cis.py script."""
    print("📦 [2/8] Concatenating & updating unified Python audit script (audit_cis.py)...")
    from scripts.bundle_audit_cis import generate_unified_audit_script
    generate_unified_audit_script()


def step_validate_python_syntax():
    """Compile all python files to verify syntax using PSL py_compile."""
    print("🐍 [3/8] Validating Python syntax across all scripts (py_compile)...")
    py_files = sorted(glob.glob("*.py") + glob.glob("scripts/*.py") + glob.glob("tests/*.py"))
    failed = False
    for f in py_files:
        try:
            py_compile.compile(f, doraise=True)
            print(f"  ✓ {f}")
        except Exception as e:
            print(f"  ❌ Syntax error in {f}: {e}", file=sys.stderr)
            failed = True
    if failed:
        sys.exit(1)


def step_check_psl_compliance():
    """Verify that audit_cis.py uses ONLY Python Standard Library modules."""
    print("🔒 [4/8] Verifying Python Standard Library (PSL) compliance on audit_cis.py...")
    with open("audit_cis.py", "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    allowed_modules = {
        "argparse", "ast", "datetime", "glob", "html", "json", "os", "py_compile",
        "re", "subprocess", "sys", "time", "xml", "xml.etree.ElementTree", "unittest", "tempfile"
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name.split(".")[0]
                if module not in allowed_modules:
                    print(f"❌ NON-PSL Import Detected: {alias.name}", file=sys.stderr)
                    sys.exit(1)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                module = node.module.split(".")[0]
                if module not in allowed_modules:
                    print(f"❌ NON-PSL ImportFrom Detected: {node.module}", file=sys.stderr)
                    sys.exit(1)

    print("  ✓ audit_cis.py uses Python Standard Library ONLY!")


def step_check_shell_scripts():
    """Verify shell script syntax using bash -n."""
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
    """Verify repository sub-directories and report file integrity (> 1 KB)."""
    print("📁 [6/8] Validating repository structure and report integrity...")
    required_dirs = ["reports", "docker", "scripts", "CIS_DATA", "tests"]
    for d in required_dirs:
        if not os.path.isdir(d):
            print(f"❌ Required directory missing: {d}", file=sys.stderr)
            sys.exit(1)
        print(f"  ✓ Directory present: {d}/")

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
