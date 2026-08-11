#!/usr/bin/env python3
"""
Unified CIS Benchmark Audit Suite Engine (Python Standard Library ONLY).
Runs CIS security compliance audits for all 15 supported database targets:
  - MariaDB (10.6, 10.11)
  - MySQL (8.0, Community 8.4/9.7, Enterprise 8.4/9.7)
  - PostgreSQL (16, 17, 18)
  - MongoDB (7, 8)
  - Apache Cassandra (4.0, 4.1, 5.0)

Zero external dependencies: uses only Python Standard Library (argparse, json, subprocess, os, sys, re, html, datetime).
"""

import argparse
import datetime
import html
import importlib
import json
import os
import re
import subprocess
import sys

TARGET_MAP = {
    "mariadb106": ("audit_cis_mariadb_106.py", "MariaDB 10.6"),
    "mariadb1011": ("audit_cis_mariadb_1011.py", "MariaDB 10.11"),
    "mysql80": ("audit_cis_mysql_80.py", "MySQL Enterprise 8.0"),
    "mysql-community84": ("audit_cis_mysql_community_84.py", "MySQL Community 8.4"),
    "mysql-enterprise84": ("audit_cis_mysql_enterprise_84.py", "MySQL Enterprise 8.4"),
    "mysql-community97": ("audit_cis_mysql_community_97.py", "MySQL Community 9.7"),
    "mysql-enterprise97": ("audit_cis_mysql_enterprise_97.py", "MySQL Enterprise 9.7"),
    "postgresql16": ("audit_cis_postgresql_16.py", "PostgreSQL 16"),
    "postgresql17": ("audit_cis_postgresql_17.py", "PostgreSQL 17"),
    "postgresql18": ("audit_cis_postgresql_18.py", "PostgreSQL 18"),
    "mongodb7": ("audit_cis_mongodb_7.py", "MongoDB 7"),
    "mongodb8": ("audit_cis_mongodb_8.py", "MongoDB 8"),
    "cassandra40": ("audit_cis_cassandra_40.py", "Apache Cassandra 4.0"),
    "cassandra41": ("audit_cis_cassandra_41.py", "Apache Cassandra 4.1"),
    "cassandra50": ("audit_cis_cassandra_50.py", "Apache Cassandra 5.0"),
}


def list_targets():
    """List all supported CIS benchmark targets."""
    print("📋 Supported CIS Benchmark Audit Targets:")
    print("=" * 55)
    for key, (script_file, label) in TARGET_MAP.items():
        print(f"  • {key:<20} -> {label} ({script_file})")
    print("=" * 55)


def run_single_audit(target_key, output_html=None, output_json=None):
    """Execute a single CIS audit benchmark script using standard library subprocess."""
    if target_key not in TARGET_MAP:
        print(f"❌ Unknown target: '{target_key}'. Use --list-targets to view valid choices.", file=sys.stderr)
        return False

    script_file, label = TARGET_MAP[target_key]
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_file)

    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}", file=sys.stderr)
        return False

    print(f"\n🚀 Running CIS Audit for {label} ({script_file})...")
    start_time = datetime.datetime.now()

    cmd = [sys.executable, script_path]
    try:
        result = subprocess.run(cmd, check=True)
        elapsed = (datetime.datetime.now() - start_time).total_seconds()
        print(f"✅ {label} CIS Audit completed successfully in {elapsed:.2f}s")

        # Custom report renaming if requested
        default_report = f"rapport_cis_{target_key.replace('-', '_')}.html"
        if output_html and os.path.exists(default_report):
            os.rename(default_report, output_html)
            print(f"📄 HTML report saved to: {output_html}")

        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ CIS Audit for {label} failed with exit code {e.returncode}", file=sys.stderr)
        return False


def auto_detect_and_run():
    """Detect running database containers or services and run matching CIS audits."""
    print("🔍 Auto-detecting active database containers...")
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
        description="Unified CIS Benchmark Audit Suite (Python Standard Library ONLY)",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-t", "--target", choices=list(TARGET_MAP.keys()), help="Target database benchmark to audit")
    parser.add_argument("-l", "--list-targets", action="store_true", help="List all supported database targets")
    parser.add_argument("-a", "--all", action="store_true", help="Run CIS audits for ALL 15 targets sequentially")
    parser.add_argument("-d", "--auto-detect", action="store_true", help="Auto-detect running database containers and execute audits")
    parser.add_argument("-o", "--output-html", help="Path to save custom HTML report")
    parser.add_argument("-j", "--output-json", help="Path to save JSON summary report")

    args = parser.parse_args()

    if args.list_targets:
        list_targets()
        sys.exit(0)

    if args.auto_detect:
        auto_detect_and_run()
        sys.exit(0)

    if args.all:
        print("🌟 Executing CIS Audit for ALL 15 database targets...")
        success_count = 0
        for target_key in TARGET_MAP:
            if run_single_audit(target_key):
                success_count += 1
        print(f"\n🎉 Completed: {success_count}/{len(TARGET_MAP)} CIS audits succeeded.")
        sys.exit(0 if success_count == len(TARGET_MAP) else 1)

    if args.target:
        success = run_single_audit(args.target, output_html=args.output_html, output_json=args.output_json)
        sys.exit(0 if success else 1)

    # Default action if no flags passed: show help
    parser.print_help()


if __name__ == "__main__":
    main()
