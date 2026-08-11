#!/usr/bin/env python3
"""
Automated End-to-End (E2E) Test Runner & Quality Analysis Engine for CIS Benchmarks Suite.
Builds Docker images, runs containers, executes audit scripts, validates reports, and performs post-execution integrity analysis.
100% Python Standard Library (PSL ONLY).
"""

import datetime
import json
import os
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

E2E_TARGETS = [
    ("mariadb106", "docker/Dockerfile_mariadb106", "mariadb106-audit", "mariadb106-test", "audit_cis_mariadb_106.py", "rapport_cis_mariadb_106.html", 15),
    ("mariadb1011", "docker/Dockerfile_mariadb1011", "mariadb1011-audit", "mariadb1011-test", "audit_cis_mariadb_1011.py", "rapport_cis_mariadb_1011.html", 15),
    ("mysql80", "docker/Dockerfile_mysql80", "mysql80-audit", "mysql80-test", "audit_cis_mysql_80.py", "rapport_cis_mysql_8.html", 15),
    ("mysql-community84", "docker/Dockerfile_mysql_community_84", "mysql-community84-audit", "mysql-community84-test", "audit_cis_mysql_community_84.py", "rapport_cis_mysql_community_84.html", 15),
    ("mysql-enterprise84", "docker/Dockerfile_mysql_enterprise_84", "mysql-enterprise84-audit", "mysql-enterprise84-test", "audit_cis_mysql_enterprise_84.py", "rapport_cis_mysql_enterprise_84.html", 15),
    ("mysql-community97", "docker/Dockerfile_mysql_community_97", "mysql-community97-audit", "mysql-community97-test", "audit_cis_mysql_community_97.py", "rapport_cis_mysql_community_97.html", 15),
    ("mysql-enterprise97", "docker/Dockerfile_mysql_enterprise_97", "mysql-enterprise97-audit", "mysql-enterprise97-test", "audit_cis_mysql_enterprise_97.py", "rapport_cis_mysql_enterprise_97.html", 15),
    ("postgresql16", "docker/Dockerfile_postgresql16", "postgresql16-audit", "postgresql16-test", "audit_cis_postgresql_16.py", "rapport_cis_postgresql_16.html", 10),
    ("postgresql17", "docker/Dockerfile_postgresql17", "postgresql17-audit", "postgresql17-test", "audit_cis_postgresql_17.py", "rapport_cis_postgresql_17.html", 10),
    ("postgresql18", "docker/Dockerfile_postgresql18", "postgresql18-audit", "postgresql18-test", "audit_cis_postgresql_18.py", "rapport_cis_postgresql_18.html", 10),
    ("mongodb7", "docker/Dockerfile_mongodb7", "mongodb7-audit", "mongodb7-test", "audit_cis_mongodb_7.py", "rapport_cis_mongodb_7.html", 15),
    ("mongodb8", "docker/Dockerfile_mongodb8", "mongodb8-audit", "mongodb8-test", "audit_cis_mongodb_8.py", "rapport_cis_mongodb_8.html", 15),
    ("cassandra40", "docker/Dockerfile_cassandra40", "cassandra40-audit", "cassandra40-test", "audit_cis_cassandra_40.py", "rapport_cis_cassandra_40.html", 25),
    ("cassandra41", "docker/Dockerfile_cassandra41", "cassandra41-audit", "cassandra41-test", "audit_cis_cassandra_41.py", "rapport_cis_cassandra_41.html", 25),
    ("cassandra50", "docker/Dockerfile_cassandra50", "cassandra50-audit", "cassandra50-test", "audit_cis_cassandra_50.py", "rapport_cis_cassandra_50.html", 25),
]


def analyze_report_integrity(filepath):
    """Analyze generated report file for size, structural integrity, and syntax."""
    if not os.path.exists(filepath):
        return False, "File missing"

    size = os.path.getsize(filepath)
    if size < 1024:
        return False, f"File too small ({size} bytes)"

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    if filepath.endswith(".html"):
        if "<html" not in content or "</html>" not in content:
            return False, "Malformed HTML structure"
        if "<table>" not in content and "class=" not in content:
            return False, "Missing HTML report content table"
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

    return True, f"Valid ({size} bytes)"


def run_e2e_for_target(target):
    key, dockerfile, img_name, container_name, script, report_name, wait_sec = target
    print(f"\n============================================================")
    print(f"🚀 [E2E Test & Analysis] Starting cycle for: {key}")
    print(f"============================================================")

    # 1. Clean container if exists
    subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)

    # 2. Build Docker Image
    print(f"🐳 [1/5] Building Docker image '{img_name}' from {dockerfile}...")
    b_res = subprocess.run(["docker", "build", "-f", dockerfile, "-t", img_name, "."], capture_output=True, text=True)
    if b_res.returncode != 0:
        print(f"❌ Docker build failed for {key}: {b_res.stderr.strip()}", file=sys.stderr)
        return False, "Docker Build Failure", 0

    # 3. Run Container
    print(f"📦 [2/5] Starting container '{container_name}'...")
    env_args = ["-e", "POSTGRES_PASSWORD=rootpass"] if "postgresql" in key else []
    r_res = subprocess.run(["docker", "run", "-d"] + env_args + ["--name", container_name, img_name], capture_output=True, text=True)
    if r_res.returncode != 0:
        print(f"❌ Container start failed for {key}: {r_res.stderr.strip()}", file=sys.stderr)
        return False, "Container Startup Failure", 0

    print(f"⏳ Waiting {wait_sec}s for service initialization...")
    time.sleep(wait_sec)

    # 4. Execute Audit Script Inside Container
    print(f"🐍 [3/5] Executing audit script '/datas/{script}' in container...")
    exec_res = subprocess.run(["docker", "exec", container_name, "python3", f"/datas/{script}"], capture_output=True, text=True)
    print(exec_res.stdout)

    # 5. Copy and Validate Report
    print(f"📄 [4/5] Copying report '/datas/{report_name}' to reports/...")
    subprocess.run(["docker", "cp", f"{container_name}:/datas/{report_name}", "reports/"], capture_output=True, text=True)

    dest_report = os.path.join("reports", report_name)
    valid, note = analyze_report_integrity(dest_report)

    # 6. Cleanup Container
    print(f"🧹 [5/5] Cleaning up container '{container_name}'...")
    subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)

    if not valid:
        print(f"❌ Post-Execution Integrity Analysis Failed for {key}: {note}", file=sys.stderr)
        return False, f"Report Validation Failure: {note}", os.path.getsize(dest_report) if os.path.exists(dest_report) else 0

    print(f"✅ E2E Analysis Passed for {key}! Analysis Note: {note}")
    return True, note, os.path.getsize(dest_report)


def main():
    print("🌟 Executing Automated E2E Test Suite & Post-Execution Analysis...")
    start_time = datetime.datetime.now()
    analysis_results = {}

    for target in E2E_TARGETS:
        key = target[0]
        success, note, size = run_e2e_for_target(target)
        analysis_results[key] = {
            "success": success,
            "note": note,
            "size": size
        }

    elapsed = (datetime.datetime.now() - start_time).total_seconds()

    print("\n" + "=" * 70)
    print("📊 E2E Test Suite & Post-Execution Analysis Summary")
    print("=" * 70)
    print(f"  {'Target':<22} {'Status':<10} {'Report Size':<15} {'Analysis Note'}")
    print(f"  {'-'*22} {'-'*10} {'-'*15} {'-'*20}")
    passed_count = 0
    for key, data in analysis_results.items():
        status_str = "PASS ✅" if data["success"] else "FAIL ❌"
        size_str = f"{data['size']} bytes" if data["size"] > 0 else "0 bytes"
        print(f"  {key:<22} {status_str:<10} {size_str:<15} {data['note']}")
        if data["success"]:
            passed_count += 1

    print(f"\n🎉 Post-Execution Analysis Complete: {passed_count}/{len(E2E_TARGETS)} targets passed in {elapsed:.2f}s!")
    sys.exit(0 if passed_count == len(E2E_TARGETS) else 1)


if __name__ == "__main__":
    main()
