#!/usr/bin/env python3
"""
Comprehensive fix for PostgreSQL rules and audit engines (PSL ONLY).
"""

import json
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_DIR = os.path.join(REPO_ROOT, "rules")

# 1. Clean JSON rules
for rfile in ["postgresql_16.json", "postgresql_17.json", "postgresql_18.json"]:
    rpath = os.path.join(RULES_DIR, rfile)
    with open(rpath, "r", encoding="utf-8") as f:
        rules = json.load(f)

    for r in rules:
        tp = r.get("test_procedure", "")
        # Remove trailing "|| SHOW ..." or "|| SELECT ..."
        if " || SHOW " in tp:
            tp = re.sub(r"\s*\|\|\s*SHOW\s+[^;]+;?", "", tp).strip()
        if " || SELECT " in tp:
            tp = re.sub(r"\s*\|\|\s*SELECT\s+[^;]+;?", "", tp).strip()
        r["test_procedure"] = tp

    with open(rpath, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"✓ Cleaned rules in {rfile}")

# 2. Update Python audit scripts
pg_scripts = ["audit_cis_postgresql_16.py", "audit_cis_postgresql_17.py", "audit_cis_postgresql_18.py"]
for sname in pg_scripts:
    spath = os.path.join(REPO_ROOT, sname)
    with open(spath, "r", encoding="utf-8") as f:
        content = f.read()

    # Clean RECOMMENDATIONS_DATA
    content = re.sub(r" \|\| SHOW [^'\";]+", "", content)
    content = re.sub(r" \|\| SELECT [^'\";]+", "", content)

    # Ensure all run_command inside perform_checks pass kwargs
    content = content.replace(
        "path_cmd_output, path_cmd_error, path_cmd_returncode = run_command(path_cmd, remote_host=remote_host)",
        "path_cmd_output, path_cmd_error, path_cmd_returncode = run_command(path_cmd, remote_host=remote_host, docker_container=docker_container, db_user=db_user, db_password=db_password, db_host=db_host, db_port=db_port, db_name=db_name, defaults_file=defaults_file, auth_db=auth_db)"
    )
    content = content.replace(
        "stdout, stderr, returncode = run_command(cmd_to_run, remote_host=remote_host)",
        "stdout, stderr, returncode = run_command(cmd_to_run, remote_host=remote_host, docker_container=docker_container, db_user=db_user, db_password=db_password, db_host=db_host, db_port=db_port, db_name=db_name, defaults_file=defaults_file, auth_db=auth_db)"
    )
    content = content.replace(
        "stdout, stderr, returncode = run_command(cmd, remote_host=remote_host)",
        "stdout, stderr, returncode = run_command(cmd, remote_host=remote_host, docker_container=docker_container, db_user=db_user, db_password=db_password, db_host=db_host, db_port=db_port, db_name=db_name, defaults_file=defaults_file, auth_db=auth_db)"
    )

    with open(spath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Updated engine logic in {sname}")

print("PostgreSQL comprehensive fix completed.")
