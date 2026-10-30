#!/usr/bin/env python3
"""
Fix raw SQL test procedures in PostgreSQL rules specifications and audit engines (PSL ONLY).
"""

import json
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_DIR = os.path.join(REPO_ROOT, "rules")

pg_rule_files = ["postgresql_16.json", "postgresql_17.json", "postgresql_18.json"]

for rf in pg_rule_files:
    rpath = os.path.join(RULES_DIR, rf)
    with open(rpath, "r", encoding="utf-8") as f:
        rules = json.load(f)

    modified = 0
    for r in rules:
        tp = r.get("test_procedure", "")
        # Clean trailing french commentary from test procedure
        if "; doit être on" in tp:
            tp = re.sub(r";\s*doit être on.*$", "", tp).strip()
        if "; et vérifier la version" in tp:
            tp = re.sub(r";\s*et vérifier la version.*$", "", tp).strip()

        # Handle raw SQL commands that need psql wrapper
        if tp.startswith("SELECT ") or tp.startswith("SHOW "):
            # If multiple queries or chained with ||
            if " || " in tp:
                parts = [p.strip() for p in tp.split(" || ")]
                new_parts = []
                for p in parts:
                    if (p.startswith("SELECT ") or p.startswith("SHOW ")) and "psql" not in p:
                        clean_q = p.rstrip(";")
                        new_parts.append(f'sudo -n -u postgres psql -t -c "{clean_q};"')
                    else:
                        new_parts.append(p)
                tp = " || ".join(new_parts)
            elif "psql" not in tp:
                clean_q = tp.rstrip(";")
                tp = f'sudo -n -u postgres psql -t -c "{clean_q};"'

            r["test_procedure"] = tp
            modified += 1

    with open(rpath, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"✓ Updated {modified} test procedures in {rf}")

# Update audit engines to auto-wrap raw SQL queries
pg_scripts = ["audit_cis_postgresql_16.py", "audit_cis_postgresql_17.py", "audit_cis_postgresql_18.py"]

for ps in pg_scripts:
    pspath = os.path.join(REPO_ROOT, ps)
    with open(pspath, "r", encoding="utf-8") as f:
        content = f.read()

    # In perform_checks, before running cmd_to_run:
    old_block = """        if isinstance(cmd_to_run, str):
            stdout, stderr, returncode = run_command(cmd_to_run)"""
    new_block = """        if isinstance(cmd_to_run, str):
            clean_cmd = cmd_to_run.strip()
            if (clean_cmd.startswith("SELECT ") or clean_cmd.startswith("SHOW ")) and "psql" not in clean_cmd:
                cmd_to_run = f'sudo -n -u postgres psql -t -c "{clean_cmd.rstrip(\\";\\")};"'
            stdout, stderr, returncode = run_command(cmd_to_run)"""

    if old_block in content:
        content = content.replace(old_block, new_block)
        with open(pspath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Updated engine logic in {ps}")

print("PostgreSQL rules and engines fixed successfully.")
