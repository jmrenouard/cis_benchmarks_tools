#!/usr/bin/env python3
"""
Unified CIS Benchmark Audit Engine v2.4.2
Automated security audit suite for databases and Linux operating systems (Local & SSH Remote Modes).
100% Python Standard Library (PSL ONLY).
"""

import argparse
import datetime
import json
import os
import subprocess
import sys

__version__ = "2.4.2"

TARGET_MAP = {
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
}


def list_targets():
    """List all supported CIS audit targets."""
    print(f"\n📋 [v{__version__}] Supported CIS Audit Targets ({len(TARGET_MAP)} Benchmarks / 887 Controls):\n")
    print(f"  {'Target Key':<22} {'Name':<30} {'Controls':<10} {'Script File'}")
    print(f"  {'-'*22} {'-'*30} {'-'*10} {'-'*30}")
    for key, (script, name, count) in TARGET_MAP.items():
        print(f"  {key:<22} {name:<30} {count:<10} {script}")
    print()


def run_single_audit(target_key, output_file=None, fmt="html", lang="en", mode="local", remote_host=None, ssh_port=22, ssh_key=None, docker_container=None, db_host=None, db_port=None, db_user=None, db_password=None, db_name=None, defaults_file=None, auth_db=None, use_sudo=False):
    """Run audit for a single target in Local, SSH Remote, or Docker mode."""
    if target_key not in TARGET_MAP:
        print(f"❌ Unknown target '{target_key}'. Use --list-targets to view valid keys.", file=sys.stderr)
        return False

    script_file, label, count = TARGET_MAP[target_key]
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_file)

    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}", file=sys.stderr)
        return False

    mode_label = f"SSH Remote Mode ({remote_host})" if (mode == "ssh" or remote_host) else "Local Mode"
    if docker_container:
        mode_label += f" [Docker: {docker_container}]"
    print(f"\n🚀 [v{__version__}] Running CIS Audit for {label} [{mode_label}] ({count} controls, {script_file})...")
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
        cmd.extend(["--db-host", db_host])
    if db_port:
        cmd.extend(["--db-port", str(db_port)])
    if db_user:
        cmd.extend(["--db-user", db_user])
    if db_password:
        cmd.extend(["--db-password", db_password])
    if db_name:
        cmd.extend(["--db-name", db_name])
    if defaults_file:
        cmd.extend(["--defaults-file", defaults_file])
    if auth_db:
        cmd.extend(["--auth-db", auth_db])
    if use_sudo:
        cmd.append("--sudo")
    if output_file:
        cmd.extend(["--output", output_file])

    try:
        subprocess.run(cmd, check=True)
        elapsed = (datetime.datetime.now() - start_time).total_seconds()
        print(f"✅ {label} CIS Audit completed successfully in {elapsed:.2f}s")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ CIS Audit for {label} failed with exit code {e.returncode}", file=sys.stderr)
        return False


def auto_detect_and_run():
    """Programmatic API & CLI: Detect running database containers and execute audits."""
    print(f"🔍 [v{__version__}] Auto-detecting active database containers...")
    detected = []

    try:
        ps_out = subprocess.check_output(["docker", "ps", "--format", "{{.Names}} {{.Image}}"], text=True)
        for line in ps_out.splitlines():
            line_lower = line.lower()
            for key in TARGET_MAP:
                if key.replace("-", "") in line_lower or key.split("-")[0] in line_lower:
                    if key not in detected:
                        detected.append(key)
    except Exception as e:
        print(f"⚠️ Docker auto-detection note: {e}")

    if not detected:
        print("ℹ️ No specific containers auto-detected. Listing available targets.")
        list_targets()
        return

    print(f"🎯 Auto-detected targets: {', '.join(detected)}")
    for target in detected:
        run_single_audit(target)


def main():
    parser = argparse.ArgumentParser(
        description=f"Unified CIS Benchmark Audit Suite v{__version__} (Local & SSH Remote Modes, PSL ONLY)",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-t", "--target", choices=list(TARGET_MAP.keys()), help="Target database benchmark to audit")
    parser.add_argument("-c", "--docker", "--container", dest="docker_container", default=None, help="Target Docker container name or ID")
    parser.add_argument("-m", "--mode", choices=["local", "ssh"], default="local", help="Audit execution mode (local or ssh)")
    parser.add_argument("-r", "--remote", "--ssh", dest="remote_host", default=None, help="Remote SSH server target (e.g. user@hostname)")
    parser.add_argument("--ssh-port", type=int, default=22, help="SSH port for remote execution (default: 22)")
    parser.add_argument("-i", "--ssh-key", dest="ssh_key", default=None, help="Path to SSH private key file")
    parser.add_argument("--sudo", action="store_true", help="Execute remote/local commands with sudo privileges")
    parser.add_argument("-H", "--host", "--db-host", dest="db_host", default="localhost", help="Database host address (default: localhost)")
    parser.add_argument("-P", "--port", "--db-port", dest="db_port", type=int, default=None, help="Database port number")
    parser.add_argument("-u", "--user", "--db-user", dest="db_user", default=None, help="Database username")
    parser.add_argument("-p", "--password", "--db-password", dest="db_password", default=None, help="Database password")
    parser.add_argument("-D", "-d", "--database", "--db-name", dest="db_name", default=None, help="Database name")
    parser.add_argument("--defaults-file", "--config-file", dest="defaults_file", default=None, help="Path to database option/configuration file (.my.cnf, .pgpass, cqlshrc)")
    parser.add_argument("--auth-db", dest="auth_db", default=None, help="Authentication database (MongoDB)")
    parser.add_argument("--local", action="store_true", help="Force local audit execution mode")
    parser.add_argument("-f", "--format", choices=["html", "json", "xml", "txt"], default="html", help="Report output format (html/json/xml/txt)")
    parser.add_argument("-l", "--lang", choices=["en", "fr"], default="en", help="Language for report and CLI output (en/fr)")
    parser.add_argument("-o", "--output", dest="output", default=None, help="Path to save report output")
    parser.add_argument("-j", "--output-json", help="Path to save JSON summary report")
    parser.add_argument("--list-targets", action="store_true", help="List all supported database targets")
    parser.add_argument("-a", "--all", action="store_true", help="Run CIS audits for ALL targets sequentially")
    parser.add_argument("--auto-detect", action="store_true", help="Auto-detect running database containers and execute audits")
    parser.add_argument("-v", "--version", action="version", version=f"CIS Benchmarks Suite v{__version__}")

    args = parser.parse_args()

    if args.list_targets:
        list_targets()
        sys.exit(0)

    if args.auto_detect:
        auto_detect_and_run()
        sys.exit(0)

    exec_mode = "ssh" if (args.mode == "ssh" or args.remote_host) else "local"

    if args.all:
        print(f"🌟 [v{__version__}] Executing CIS Audit for ALL targets [Mode: {exec_mode}]...")
        success_count = 0
        for target_key in TARGET_MAP:
            if run_single_audit(target_key, fmt=args.format, lang=args.lang, mode=exec_mode, remote_host=args.remote_host, ssh_port=args.ssh_port, ssh_key=args.ssh_key, docker_container=args.docker_container, db_host=args.db_host, db_port=args.db_port, db_user=args.db_user, db_password=args.db_password, db_name=args.db_name, defaults_file=args.defaults_file, auth_db=args.auth_db, use_sudo=args.sudo):
                success_count += 1
        print(f"\n🎉 Completed: {success_count}/{len(TARGET_MAP)} CIS audits succeeded.")
        sys.exit(0 if success_count == len(TARGET_MAP) else 1)

    if args.target:
        out = args.output or args.output_json
        fmt = "json" if args.output_json and not args.output else args.format
        success = run_single_audit(args.target, output_file=out, fmt=fmt, lang=args.lang, mode=exec_mode, remote_host=args.remote_host, ssh_port=args.ssh_port, ssh_key=args.ssh_key, docker_container=args.docker_container, db_host=args.db_host, db_port=args.db_port, db_user=args.db_user, db_password=args.db_password, db_name=args.db_name, defaults_file=args.defaults_file, auth_db=args.auth_db, use_sudo=args.sudo)
        sys.exit(0 if success else 1)

    parser.print_help()


if __name__ == "__main__":
    main()
