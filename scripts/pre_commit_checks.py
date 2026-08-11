#!/usr/bin/env python3
"""
Pre-Commit Validation Routine (Python Standard Library ONLY).
Concatenates Python benchmark code into `audit_cis.py` and runs syntax/PSL/version/structure/permissions integrity checks.
"""

import ast
import glob
import os
import py_compile
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
os.chdir(REPO_ROOT)


def step_verify_and_sync_version():
    """Verify VERSION file exists and synchronize version across unified script."""
    print("🏷️ [1/7] Verifying repository VERSION file...")
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
    print("📦 [2/7] Concatenating & updating unified Python audit script (audit_cis.py)...")
    from scripts.bundle_audit_cis import generate_unified_audit_script
    generate_unified_audit_script()


def step_validate_python_syntax():
    """Compile all python files to verify syntax using PSL py_compile."""
    print("🐍 [3/7] Validating Python syntax across all scripts (py_compile)...")
    py_files = sorted(glob.glob("*.py") + glob.glob("scripts/*.py"))
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
    print("🔒 [4/7] Verifying Python Standard Library (PSL) compliance on audit_cis.py...")
    with open("audit_cis.py", "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename="audit_cis.py")

    stdlib_modules = getattr(sys, 'stdlib_module_names', set([
        'argparse', 'ast', 'asyncio', 'base64', 'collections', 'contextlib',
        'csv', 'dataclasses', 'datetime', 'enum', 'functools', 'glob', 'html',
        'http', 'importlib', 'io', 'json', 'logging', 'math', 'os', 'pathlib',
        'platform', 're', 'shutil', 'socket', 'sqlite3', 'string', 'subprocess',
        'sys', 'time', 'typing', 'unittest', 'urllib', 'xml'
    ]))

    imported_modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported_modules.add(node.module.split('.')[0])

    non_psl = [m for m in imported_modules if m not in stdlib_modules and not m.startswith('audit_cis')]
    if non_psl:
        print(f"❌ Non-PSL imports detected in audit_cis.py: {non_psl}", file=sys.stderr)
        sys.exit(1)
    else:
        print("  ✓ audit_cis.py uses Python Standard Library ONLY!")


def step_check_shell_scripts():
    """Validate syntax of all shell scripts in scripts/ using bash -n."""
    print("📜 [5/7] Validating Shell script syntax (bash -n)...")
    sh_files = sorted(glob.glob("scripts/*.sh"))
    for sh_file in sh_files:
        try:
            subprocess.run(["bash", "-n", sh_file], check=True)
            print(f"  ✓ {sh_file}")
        except subprocess.CalledProcessError:
            print(f"  ❌ Shell syntax error in {sh_file}", file=sys.stderr)
            sys.exit(1)


def step_validate_reports_and_structure():
    """Verify repository sub-directories and report file integrity (> 1 KB)."""
    print("📁 [6/7] Validating repository structure and report integrity...")
    required_dirs = ["reports", "docker", "scripts", "CIS_DATA"]
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
    print("🔒 [7/7] Validating CIS_DATA specs and executable permissions...")
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
    print("=" * 60)
    print("🎉 All Pre-Commit Checks PASSED successfully!")


if __name__ == "__main__":
    main()
