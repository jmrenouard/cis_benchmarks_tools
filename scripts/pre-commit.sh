#!/bin/bash
# Pre-Commit Routine Script for CIS Benchmarks Tools Suite
# Enforces Python Standard Library (PSL) compliance & syntax integrity.

set -e

echo "🔍 Running CIS Benchmarks Pre-Commit Checks..."
echo "=================================================="

# 1. Check Python syntax on all audit scripts using Python Standard Library py_compile
echo "🐍 [1/4] Validating Python syntax (py_compile)..."
python3 -c "
import glob, py_compile, sys

py_files = sorted(glob.glob('*.py') + glob.glob('scripts/*.py'))
failed = False
for f in py_files:
    try:
        py_compile.compile(f, doraise=True)
        print(f'  ✓ {f}')
    except Exception as e:
        print(f'  ✗ Syntax error in {f}: {e}', file=sys.stderr)
        failed = True

if failed:
    sys.exit(1)
"

# 2. Enforce Python Standard Library (PSL) ONLY rule on audit_cis.py
echo "🔒 [2/4] Verifying Python Standard Library (PSL) compliance on audit_cis.py..."
python3 -c "
import ast, sys, modulefinder

with open('audit_cis.py', 'r') as f:
    tree = ast.parse(f.read(), filename='audit_cis.py')

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
    print(f'❌ Non-PSL imports detected in audit_cis.py: {non_psl}', file=sys.stderr)
    sys.exit(1)
else:
    print('  ✓ audit_cis.py uses Python Standard Library ONLY!')
"

# 3. Check Bash script syntax
echo "📜 [3/4] Validating Shell script syntax (bash -n)..."
for sh_file in scripts/*.sh; do
    if [ -f "$sh_file" ]; then
        bash -n "$sh_file"
        echo "  ✓ $sh_file"
    fi
done

# 4. Verify main executable script audit_cis.py
echo "🚀 [4/4] Testing unified script CLI help (--help)..."
python3 audit_cis.py --help > /dev/null
echo "  ✓ audit_cis.py CLI interface operational!"

echo "=================================================="
echo "🎉 All Pre-Commit Checks PASSED successfully!"
