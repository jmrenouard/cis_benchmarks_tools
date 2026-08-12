#!/usr/bin/env python3
"""
Automated End-to-End (E2E) Test Runner & Quality Analysis Engine for CIS Benchmarks Suite.
Builds Docker images, runs containers, executes audit scripts across ALL report formats (html, json, xml, txt),
validates all report files in reports/, and performs post-execution integrity analysis.
100% Python Standard Library (PSL ONLY).
"""

import datetime
import json
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

E2E_TARGETS = [
    ("mariadb106", "docker/Dockerfile_mariadb106", "mariadb106-audit", "mariadb106-test", "audit_cis_mariadb_106.py", "rapport_cis_mariadb_106", 15),
    ("mariadb1011", "docker/Dockerfile_mariadb1011", "mariadb1011-audit", "mariadb1011-test", "audit_cis_mariadb_1011.py", "rapport_cis_mariadb_1011", 15),
    ("mysql80", "docker/Dockerfile_mysql80", "mysql80-audit", "mysql80-test", "audit_cis_mysql_80.py", "rapport_cis_mysql_8", 15),
    ("mysql-community84", "docker/Dockerfile_mysql_community_84", "mysql-community84-audit", "mysql-community84-test", "audit_cis_mysql_community_84.py", "rapport_cis_mysql_community_84", 15),
    ("mysql-enterprise84", "docker/Dockerfile_mysql_enterprise_84", "mysql-enterprise84-audit", "mysql-enterprise84-test", "audit_cis_mysql_enterprise_84.py", "rapport_cis_mysql_enterprise_84", 15),
    ("mysql-community97", "docker/Dockerfile_mysql_community_97", "mysql-community97-audit", "mysql-community97-test", "audit_cis_mysql_community_97.py", "rapport_cis_mysql_community_97", 15),
    ("mysql-enterprise97", "docker/Dockerfile_mysql_enterprise_97", "mysql-enterprise97-audit", "mysql-enterprise97-test", "audit_cis_mysql_enterprise_97.py", "rapport_cis_mysql_enterprise_97", 15),
    ("postgresql16", "docker/Dockerfile_postgresql16", "postgresql16-audit", "postgresql16-test", "audit_cis_postgresql_16.py", "rapport_cis_postgresql_16", 10),
    ("postgresql17", "docker/Dockerfile_postgresql17", "postgresql17-audit", "postgresql17-test", "audit_cis_postgresql_17.py", "rapport_cis_postgresql_17", 10),
    ("postgresql18", "docker/Dockerfile_postgresql18", "postgresql18-audit", "postgresql18-test", "audit_cis_postgresql_18.py", "rapport_cis_postgresql_18", 10),
    ("mongodb7", "docker/Dockerfile_mongodb7", "mongodb7-audit", "mongodb7-test", "audit_cis_mongodb_7.py", "rapport_cis_mongodb_7", 15),
    ("mongodb8", "docker/Dockerfile_mongodb8", "mongodb8-audit", "mongodb8-test", "audit_cis_mongodb_8.py", "rapport_cis_mongodb_8", 15),
    ("cassandra40", "docker/Dockerfile_cassandra40", "cassandra40-audit", "cassandra40-test", "audit_cis_cassandra_40.py", "rapport_cis_cassandra_40", 25),
    ("cassandra41", "docker/Dockerfile_cassandra41", "cassandra41-audit", "cassandra41-test", "audit_cis_cassandra_41.py", "rapport_cis_cassandra_41", 25),
    ("cassandra50", "docker/Dockerfile_cassandra50", "cassandra50-audit", "cassandra50-test", "audit_cis_cassandra_50.py", "rapport_cis_cassandra_50", 25),
]

FORMATS = ["html", "json", "xml", "txt"]


def analyze_report_integrity(filepath):
    """Analyze generated report file for size, structural integrity, visual UI components, and syntax (PSL ONLY)."""
    if not os.path.exists(filepath):
        return False, "File missing"

    size = os.path.getsize(filepath)
    if size < 50:
        return False, f"File too small ({size} bytes)"

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    if filepath.endswith(".html"):
        if "<html" not in content or "</html>" not in content:
            return False, "Malformed HTML structure"
        if "<svg" not in content:
            return False, "Missing Inline SVG charts"
        if "toggleDarkMode" not in content:
            return False, "Missing Dark Mode UI control"
        if "fa-" not in content:
            return False, "Missing FontAwesome visual icons"
    elif filepath.endswith(".json"):
        try:
            json.loads(content)
        except Exception as e:
            return False, f"Invalid JSON syntax: {e}"
    elif filepath.endswith(".xml"):
        try:
            ET.fromstring(content)
        except Exception as e:
            return False, f"Invalid XML syntax: {e}"
    elif filepath.endswith(".txt"):
        if "CIS BENCHMARK AUDIT REPORT" not in content and "Report Date" not in content:
            return False, "Malformed TXT report structure"
        if "CATEGORY BREAKDOWN & COMPLIANCE SUMMARY TABLE" not in content:
            return False, "Missing TXT ASCII Summary Table"

    return True, f"Valid ({size} bytes)"


def run_e2e_for_target(target):
    key, dockerfile, img_name, container_name, script, report_prefix, wait_sec = target
    print(f"\n============================================================")
    print(f"🚀 [E2E Test & Multi-Format Analysis] Starting cycle for: {key}")
    print(f"============================================================")

    # 1. Clean container if exists
    subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)

    # 2. Build Docker Image
    print(f"🐳 [1/5] Building Docker image '{img_name}' from {dockerfile}...")
    b_res = subprocess.run(["docker", "build", "-f", dockerfile, "-t", img_name, "."], capture_output=True, text=True)
    if b_res.returncode != 0:
        print(f"❌ Docker build failed for {key}: {b_res.stderr.strip()}", file=sys.stderr)
        return False, "Docker Build Failure", {}

    # 3. Run Container
    print(f"📦 [2/5] Starting container '{container_name}'...")
    env_args = ["-e", "POSTGRES_PASSWORD=rootpass"] if "postgresql" in key else []
    r_res = subprocess.run(["docker", "run", "-d"] + env_args + ["--name", container_name, img_name], capture_output=True, text=True)
    if r_res.returncode != 0:
        print(f"❌ Container start failed for {key}: {r_res.stderr.strip()}", file=sys.stderr)
        return False, "Container Startup Failure", {}

    print(f"⏳ Waiting {wait_sec}s for service initialization...")
    time.sleep(wait_sec)

    fmt_results = {}
    all_formats_valid = True

    # 4. Execute Audit Script for Local & SSH Remote Modes across ALL Formats
    print(f"🐍 [3/5] Executing audit script '/datas/{script}' in BOTH Local Mode & SSH Remote Mode ({', '.join(FORMATS)})...")
    
    # Test Local Mode
    for fmt in FORMATS:
        report_file = f"{report_prefix}.{fmt}"
        cmd = ["docker", "exec", container_name, "python3", f"/datas/{script}", "-m", "local", "-f", fmt, "-o", f"/datas/{report_file}"]
        exec_res = subprocess.run(cmd, capture_output=True, text=True)
        
        # Copy report from container to reports/
        subprocess.run(["docker", "cp", f"{container_name}:/datas/{report_file}", "reports/"], capture_output=True, text=True)

        dest_path = os.path.join("reports", report_file)
        valid, note = analyze_report_integrity(dest_path)
        fmt_results[fmt] = (valid, note, os.path.getsize(dest_path) if os.path.exists(dest_path) else 0)
        if not valid:
            all_formats_valid = False
            print(f"  ❌ Format '{fmt}' (Local Mode) failed validation: {note}", file=sys.stderr)
        else:
            print(f"  ✓ Format '{fmt}' (Local Mode) validated: {dest_path}")

    # Test SSH Remote Mode execution handling
    for fmt in ["json", "html"]:
        ssh_report = f"{report_prefix}_ssh.{fmt}"
        cmd_ssh = ["docker", "exec", container_name, "python3", f"/datas/{script}", "-m", "ssh", "-r", "127.0.0.1", "-f", fmt, "-o", f"/datas/{ssh_report}"]
        exec_ssh = subprocess.run(cmd_ssh, capture_output=True, text=True)
        subprocess.run(["docker", "cp", f"{container_name}:/datas/{ssh_report}", "reports/"], capture_output=True, text=True)
        ssh_dest = os.path.join("reports", ssh_report)
        ssh_valid, ssh_note = analyze_report_integrity(ssh_dest)
        if ssh_valid:
            print(f"  ✓ Format '{fmt}' (SSH Remote Mode) validated: {ssh_dest}")

    # 5. Cleanup Container
    print(f"🧹 [5/5] Cleaning up container '{container_name}'...")
    subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)

    summary_note = "All 4 formats valid" if all_formats_valid else "Some formats failed"
    return all_formats_valid, summary_note, fmt_results


def main():
    print("🌟 Executing Automated E2E Test Suite for ALL Report Formats (HTML, JSON, XML, TXT)...")
    start_time = datetime.datetime.now()
    analysis_results = {}

    for target in E2E_TARGETS:
        key = target[0]
        success, note, fmt_data = run_e2e_for_target(target)
        analysis_results[key] = {
            "success": success,
            "note": note,
            "formats": fmt_data
        }

    elapsed = (datetime.datetime.now() - start_time).total_seconds()

    print("\n" + "=" * 70)
    print("📊 E2E Test Suite & Multi-Format Report Integrity Summary")
    print("=" * 70)
    print(f"  {'Target':<22} {'Status':<10} {'HTML':<10} {'JSON':<10} {'XML':<10} {'TXT':<10}")
    print(f"  {'-'*22} {'-'*10} {'-'*10} {'-'*10} {'-'*10} {'-'*10}")
    passed_count = 0
    for key, data in analysis_results.items():
        status_str = "PASS ✅" if data["success"] else "FAIL ❌"
        fmts = data.get("formats", {})
        h_str = "OK" if fmts.get("html", (False,))[0] else "FAIL"
        j_str = "OK" if fmts.get("json", (False,))[0] else "FAIL"
        x_str = "OK" if fmts.get("xml", (False,))[0] else "FAIL"
        t_str = "OK" if fmts.get("txt", (False,))[0] else "FAIL"
        print(f"  {key:<22} {status_str:<10} {h_str:<10} {j_str:<10} {x_str:<10} {t_str:<10}")
        if data["success"]:
            passed_count += 1

    print(f"\n🎉 Multi-Format E2E Analysis Complete: {passed_count}/{len(E2E_TARGETS)} targets passed in {elapsed:.2f}s!")
    sys.exit(0 if passed_count == len(E2E_TARGETS) else 1)


if __name__ == "__main__":
    main()
