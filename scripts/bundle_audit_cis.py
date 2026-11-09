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

# DEPRECATED: Unused legacy template string (Phase 1 retirement, Refs #646; removed in #647)
_DEPRECATED_TEMPLATE = f'''#!/usr/bin/env python3
"""
Unified CIS Benchmark Audit Engine v{VERSION}
Automated security audit suite for databases and Linux operating systems (Local & SSH Remote Modes).
100% Python Standard Library (PSL ONLY).
"""

import argparse
import datetime
import json
import os
import subprocess
import sys

os.environ.setdefault("PYTHONUTF8", "1")

if hasattr(sys.stdout, "reconfigure"):

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

if hasattr(sys.stderr, "reconfigure"):

    sys.stderr.reconfigure(encoding="utf-8", errors="replace")



__version__ = "{VERSION}"

TARGET_MAP = {{
    "mariadb106": ("audit_cis_mariadb_106.py", "MariaDB 10.6", 74),
    "mariadb1011": ("audit_cis_mariadb_1011.py", "MariaDB 10.11", 75),
    "mysql80": ("audit_cis_mysql_80.py", "MySQL Enterprise 8.0", 70),
    "mysql-community84": ("audit_cis_mysql_community_84.py", "MySQL Community 8.4 LTS", 79),
    "mysql-enterprise84": ("audit_cis_mysql_enterprise_84.py", "MySQL Enterprise 8.4 LTS", 70),
    "mysql-community97": ("audit_cis_mysql_community_97.py", "MySQL Community 9.7", 70),
    "mysql-enterprise97": ("audit_cis_mysql_enterprise_97.py", "MySQL Enterprise 9.7", 70),
    "postgresql16": ("audit_cis_postgresql_16.py", "PostgreSQL 16", 71),
    "postgresql17": ("audit_cis_postgresql_17.py", "PostgreSQL 17", 71),
    "postgresql18": ("audit_cis_postgresql_18.py", "PostgreSQL 18", 71),
    "mongodb7": ("audit_cis_mongodb_7.py", "MongoDB 7.0", 23),
    "mongodb8": ("audit_cis_mongodb_8.py", "MongoDB 8.0", 23),
    "cassandra40": ("audit_cis_cassandra_40.py", "Apache Cassandra 4.0", 20),
    "cassandra41": ("audit_cis_cassandra_41.py", "Apache Cassandra 4.1", 20),
    "cassandra50": ("audit_cis_cassandra_50.py", "Apache Cassandra 5.0", 20),
    "rhel8": ("audit_cis_rhel_8.py", "Red Hat Enterprise Linux 8", 20),
    "rhel9": ("audit_cis_rhel_9.py", "Red Hat Enterprise Linux 9", 20),
    "rhel10": ("audit_cis_rhel_10.py", "Red Hat Enterprise Linux 10", 20),
}}


def list_targets():
    """List all supported CIS audit targets."""
    print(f"\\n📋 [v{{__version__}}] Supported CIS Audit Targets ({{len(TARGET_MAP)}} Benchmarks / 887 Controls):\\n")
    print(f"  {{'Target Key':<22}} {{'Name':<30}} {{'Controls':<10}} {{'Script File'}}")
    print(f"  {{'-'*22}} {{'-'*30}} {{'-'*10}} {{'-'*30}}")
    for key, (script, name, count) in TARGET_MAP.items():
        print(f"  {{key:<22}} {{name:<30}} {{count:<10}} {{script}}")
    print()


def run_single_audit(target_key, output_file=None, fmt="html", lang="en", mode="local", remote_host=None, ssh_port=22, ssh_key=None, docker_container=None, db_host=None, db_port=None, db_user=None, db_password=None, db_name=None, defaults_file=None, auth_db=None, use_sudo=False):
    """Run audit for a single target in Local, SSH Remote, or Docker mode."""
    if target_key not in TARGET_MAP:
        print(f"❌ Unknown target '{{target_key}}'. Use --list-targets to view valid keys.", file=sys.stderr)
        return False

    script_file, label, count = TARGET_MAP[target_key]
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_file)

    if not os.path.exists(script_path):
        print(f"❌ Script not found: {{script_path}}", file=sys.stderr)
        return False

    mode_label = f"SSH Remote Mode ({{remote_host}})" if (mode == "ssh" or remote_host) else "Local Mode"
    if docker_container:
        mode_label += f" [Docker: {{docker_container}}]"
    print(f"\\n🚀 [v{{__version__}}] Running CIS Audit for {{label}} [{{mode_label}}] ({{count}} controls, {{script_file}})...")
    start_time = datetime.datetime.now()

    cmd = [sys.executable, script_path, "--format", fmt, "--lang", lang, "--mode", mode]
    if docker_container:
        cmd.extend(["--docker", docker_container])
    if remote_host:
        cmd.extend(["--remote", remote_host])
    if ssh_port and int(ssh_port) != 22:
        cmd.extend(["--ssh-port", str(ssh_port)])
    if ssh_key:
        cmd.extend(["--ssh-key", ssh_key])
    if db_host:
'''


if __name__ == '__main__':
    generate_unified_audit_script()
