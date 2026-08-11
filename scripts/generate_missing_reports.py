#!/usr/bin/env python3
"""
Generate Missing HTML Audit Reports (Python Standard Library ONLY).
Version: 1.4.1

Automates running audit scripts inside Docker containers for targets without reports,
then extracts the resulting HTML report files. Zero third-party dependencies.
"""

import os
import subprocess
import sys

DOCKER_MAPPING = [
    ("docker/Dockerfile.mariadb_106", "mariadb_106", "audit_cis_mariadb_106.py", "rapport_cis_mariadb_10.6.html", ""),
    ("docker/Dockerfile.mariadb_1011", "mariadb_1011", "audit_cis_mariadb_1011.py", "rapport_cis_mariadb_10.11.html", ""),
    ("docker/Dockerfile.mysql_80", "mysql_80", "audit_cis_mysql_80.py", "rapport_cis_mysql_enterprise_8.0.html", "-e MYSQL_ROOT_PASSWORD=rootpassword"),
    ("docker/Dockerfile.mysql_community_84", "mysql_community_84", "audit_cis_mysql_community_84.py", "rapport_cis_mysql_community_8.4.html", "-e MYSQL_ROOT_PASSWORD=rootpassword"),
    ("docker/Dockerfile.mysql_enterprise_84", "mysql_enterprise_84", "audit_cis_mysql_enterprise_84.py", "rapport_cis_mysql_enterprise_8.4.html", "-e MYSQL_ROOT_PASSWORD=rootpassword"),
    ("docker/Dockerfile.mysql_community_97", "mysql_community_97", "audit_cis_mysql_community_97.py", "rapport_cis_mysql_community_9.7.html", "-e MYSQL_ROOT_PASSWORD=rootpassword"),
    ("docker/Dockerfile.mysql_enterprise_97", "mysql_enterprise_97", "audit_cis_mysql_enterprise_97.py", "rapport_cis_mysql_enterprise_9.7.html", "-e MYSQL_ROOT_PASSWORD=rootpassword"),
    ("docker/Dockerfile.postgresql_16", "postgresql_16", "audit_cis_postgresql_16.py", "rapport_cis_postgresql_16.html", ""),
    ("docker/Dockerfile.postgresql_17", "postgresql_17", "audit_cis_postgresql_17.py", "rapport_cis_postgresql_17.html", ""),
    ("docker/Dockerfile.postgresql_18", "postgresql_18", "audit_cis_postgresql_18.py", "rapport_cis_postgresql_18.html", ""),
    ("docker/Dockerfile.mongodb_7", "mongodb_7", "audit_cis_mongodb_7.py", "rapport_cis_mongodb_7.html", ""),
    ("docker/Dockerfile.mongodb_8", "mongodb_8", "audit_cis_mongodb_8.py", "rapport_cis_mongodb_8.html", ""),
    ("docker/Dockerfile.cassandra_40", "cassandra_40", "audit_cis_cassandra_40.py", "rapport_cis_cassandra_4.0.html", ""),
    ("docker/Dockerfile.cassandra_41", "cassandra_41", "audit_cis_cassandra_41.py", "rapport_cis_cassandra_4.1.html", ""),
    ("docker/Dockerfile.cassandra_50", "cassandra_50", "audit_cis_cassandra_50.py", "rapport_cis_cassandra_5.0.html", ""),
]


def run_cmd(cmd_list, check=False):
    """Execute command as parameter list without shell=True for security."""
    return subprocess.run(cmd_list, check=check, capture_output=True, text=True)


def build_and_generate_report(df, tag, script, report, extra_args_str):
    """Build Docker container and run audit script to extract report."""
    print(f"🐳 Building Docker image for {tag}...")
    run_cmd(["docker", "build", "-f", df, "-t", f"{tag}:report", "."], check=True)

    run_cmd(["docker", "rm", "-f", f"{tag}_run"])

    extra_args = extra_args_str.split() if extra_args_str else []
    run_cmd_list = ["docker", "run", "-d"] + extra_args + ["--name", f"{tag}_run", f"{tag}:report"]
    print(f"🚀 Running container {tag}_run...")
    run_cmd(run_cmd_list, check=True)

    print(f"📊 Executing audit script inside container...")
    run_cmd(["docker", "exec", f"{tag}_run", "python3", f"/datas/{script}"])

    os.makedirs("reports", exist_ok=True)
    target_path = os.path.join("reports", report)

    print(f"📥 Copying generated report to {target_path}...")
    cp_res = run_cmd(["docker", "cp", f"{tag}_run:/datas/{report}", target_path])
    if cp_res.returncode != 0:
        with open(target_path, "w", encoding="utf-8") as out:
            exec_cat = run_cmd(["docker", "exec", f"{tag}_run", "cat", f"/datas/{report}"])
            out.write(exec_cat.stdout)

    run_cmd(["docker", "rm", "-f", f"{tag}_run"])
    print(f"✅ Generated report for {tag}: {target_path}")


def main():
    print("🔄 Generating missing HTML audit reports...")
    for df, tag, script, report, extra_args in DOCKER_MAPPING:
        report_path = os.path.join("reports", report)
        if not os.path.exists(report_path):
            print(f"⚡ Report missing for {tag}, generating...")
            try:
                build_and_generate_report(df, tag, script, report, extra_args)
            except Exception as e:
                print(f"❌ Failed to generate report for {tag}: {e}")
        else:
            print(f"✓ Report already exists: {report_path}")


if __name__ == "__main__":
    main()
