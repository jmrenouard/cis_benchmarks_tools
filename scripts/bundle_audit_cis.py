#!/usr/bin/env python3
"""
Automated Bundler for CIS Benchmarks Suite.
Concatenates Python benchmark audit logic into unified `audit_cis.py` CLI script.
100% Python Standard Library (PSL ONLY).
"""

import os
import sys

os.environ.setdefault("PYTHONUTF8", "1")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

VERSION_FILE = os.path.join(REPO_ROOT, "VERSION")
if os.path.exists(VERSION_FILE):
    with open(VERSION_FILE, "r", encoding="utf-8") as f:
        VERSION = f.read().strip()
else:
    VERSION = "1.6.0"


def generate_unified_audit_script(target_file: str = None) -> bool:
    """Synchronizes __version__ in audit_cis.py from VERSION file via regex without overwriting content."""
    import re
    target = target_file or os.path.join(REPO_ROOT, "audit_cis.py")
    if not os.path.exists(target):
        print(f"❌ audit_cis.py not found at {target}", file=sys.stderr)
        sys.exit(1)

    print(f"📦 Synchronizing unified CIS audit script: {target} (v{VERSION})...")
    with open(target, "r", encoding="utf-8") as f:
        c = f.read()

    nc = re.sub(r'Unified CIS Benchmark Audit Engine v[0-9.]+', f'Unified CIS Benchmark Audit Engine v{VERSION}', c)
    nc = re.sub(r'(def _resolve_version\(\) -> str:[\s\S]*?return )["\'][0-9.]+["\']', rf'\g<1>"{VERSION}"', nc)
    nc = re.sub(r'__version__\s*=\s*["\'][0-9.]+["\']', f'__version__ = "{VERSION}"', nc)

    if nc != c:
        with open(target, "w", encoding="utf-8") as f:
            f.write(nc)
        print(f"✅ audit_cis.py successfully synchronized to v{VERSION}")
    else:
        print(f"✓ audit_cis.py already up-to-date (v{VERSION})")
    return True


update_unified_audit_script = generate_unified_audit_script


if __name__ == "__main__":
    generate_unified_audit_script()
