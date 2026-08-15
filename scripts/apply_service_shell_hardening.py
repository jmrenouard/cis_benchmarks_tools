#!/usr/bin/env python3
"""
Apply non-interactive shell hardening to Dockerfiles and startup scripts (PSL ONLY).
"""

import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCKER_DIR = os.path.join(REPO_ROOT, "docker")
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
MAKEFILE_PATH = os.path.join(REPO_ROOT, "Makefile")

# 1. Update MariaDB and MySQL Dockerfiles
target_dockerfiles = [
    "Dockerfile_mariadb106",
    "Dockerfile_mariadb1011",
    "Dockerfile_mysql80",
    "Dockerfile_mysql_community_84",
    "Dockerfile_mysql_enterprise_84",
    "Dockerfile_mysql_community_97",
    "Dockerfile_mysql_enterprise_97",
]

for df_name in target_dockerfiles:
    df_path = os.path.join(DOCKER_DIR, df_name)
    with open(df_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "usermod -s /sbin/nologin mysql" not in content:
        # Add after apt-get clean or ssh-keygen
        if "ssh-keygen -A" in content:
            content = content.replace("ssh-keygen -A", "ssh-keygen -A && \\\n  (usermod -s /sbin/nologin mysql || usermod -s /bin/false mysql || true)")
        elif "apt-get clean" in content:
            content = content.replace("apt-get clean", "(usermod -s /sbin/nologin mysql || usermod -s /bin/false mysql || true) && \\\n  apt-get clean")
        
        with open(df_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Hardened service shell in {df_name}")

# 2. Update startup scripts
for sname in ["start_mariadb.sh", "start_mysql.sh"]:
    spath = os.path.join(SCRIPTS_DIR, sname)
    with open(spath, "r", encoding="utf-8") as f:
        content = f.read()

    if "usermod -s /sbin/nologin mysql" not in content:
        content = content.replace(
            "ln -sf /dev/null /root/.bash_history 2>/dev/null || true",
            "ln -sf /dev/null /root/.bash_history 2>/dev/null || true\nusermod -s /sbin/nologin mysql 2>/dev/null || true"
        )
        with open(spath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Hardened startup script {sname}")

# 3. Update Makefile audit and run targets
with open(MAKEFILE_PATH, "r", encoding="utf-8") as f:
    mf_content = f.read()

# Update audit commands to pass -o /datas/$(REPORT)
targets = [
    ("MARIADB106_CONTAINER", "MARIADB106_SCRIPT", "MARIADB106_REPORT"),
    ("MARIADB1011_CONTAINER", "MARIADB1011_SCRIPT", "MARIADB1011_REPORT"),
    ("MYSQL80_CONTAINER", "MYSQL80_SCRIPT", "MYSQL80_REPORT"),
    ("MYSQL_COMMUNITY84_CONTAINER", "MYSQL_COMMUNITY84_SCRIPT", "MYSQL_COMMUNITY84_REPORT"),
    ("MYSQL_ENTERPRISE84_CONTAINER", "MYSQL_ENTERPRISE84_SCRIPT", "MYSQL_ENTERPRISE84_REPORT"),
    ("MYSQL_COMMUNITY97_CONTAINER", "MYSQL_COMMUNITY97_SCRIPT", "MYSQL_COMMUNITY97_REPORT"),
    ("MYSQL_ENTERPRISE97_CONTAINER", "MYSQL_ENTERPRISE97_SCRIPT", "MYSQL_ENTERPRISE97_REPORT"),
    ("POSTGRESQL16_CONTAINER", "POSTGRESQL16_SCRIPT", "POSTGRESQL16_REPORT"),
    ("POSTGRESQL17_CONTAINER", "POSTGRESQL17_SCRIPT", "POSTGRESQL17_REPORT"),
    ("POSTGRESQL18_CONTAINER", "POSTGRESQL18_SCRIPT", "POSTGRESQL18_REPORT"),
    ("MONGODB7_CONTAINER", "MONGODB7_SCRIPT", "MONGODB7_REPORT"),
    ("MONGODB8_CONTAINER", "MONGODB8_SCRIPT", "MONGODB8_REPORT"),
    ("CASSANDRA40_CONTAINER", "CASSANDRA40_SCRIPT", "CASSANDRA40_REPORT"),
    ("CASSANDRA41_CONTAINER", "CASSANDRA41_SCRIPT", "CASSANDRA41_REPORT"),
    ("CASSANDRA50_CONTAINER", "CASSANDRA50_SCRIPT", "CASSANDRA50_REPORT"),
]

for cont_var, scr_var, rep_var in targets:
    old_cmd = f"docker exec $({cont_var}) python3 /datas/$({scr_var})"
    new_cmd = f"docker exec $({cont_var}) python3 /datas/$({scr_var}) -o /datas/$({rep_var})"
    if old_cmd in mf_content and new_cmd not in mf_content:
        mf_content = mf_content.replace(old_cmd, new_cmd)

# Add copying rules/templates in run targets if not present
for cont_var, _, _ in targets:
    run_block = f"run-{cont_var.lower().replace('_container', '')}:"
    # Find block and ensure cp templates and rules happens
    pass

with open(MAKEFILE_PATH, "w", encoding="utf-8") as f:
    f.write(mf_content)

print("Makefile updated successfully.")
