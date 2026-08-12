#!/usr/bin/env python3
"""
Maximize information collection across ALL 18 CIS audit scripts and 18 JSON rule files.
Ensures that EVERY control (Automated or Manual) executes diagnostic CLI commands
to collect maximum system information, configuration details, and outputs into the report.
100% Python Standard Library (PSL ONLY).
"""

import glob
import json
import os
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
rule_files = sorted(glob.glob("rules/*.json"))

print(f"Maximizing information collection across {len(audit_files)} audit scripts and {len(rule_files)} rule specifications...")

# --- 1. Update JSON rules to ensure test_procedure has runnable inspection commands ---
for rf in rule_files:
    with open(rf, "r", encoding="utf-8") as f:
        rules = json.load(f)

    updated = False
    for r in rules:
        if r.get("type") == "Manual":
            proc = r.get("test_procedure", "")
            # Ensure proc is a runnable shell inspection command if it's currently descriptive prose
            if not proc or "Analyser les" in proc or "Examiner les" in proc or "Contrôler la" in proc or "Vérifier la" in proc:
                num = r.get("number", "")
                cat = r.get("category", "")
                if "2.1.2" in num:
                    r["test_procedure"] = "ls -la /var/backups/ /var/lib/mariadb/ /var/lib/mysql/ /var/lib/pgsql/ 2>/dev/null | head -n 20 || echo 'VÉRIFICATION_MANUELLE_REQUIS'"
                elif "2.1.3" in num:
                    r["test_procedure"] = "ls -la /etc/mysql/ /etc/pgsql/ /root/.my.cnf /root/.pgpass 2>/dev/null || echo 'VÉRIFICATION_PERMISSIONS_CREDENTIALS'"
                elif "2.1.4" in num:
                    r["test_procedure"] = "file /var/backups/* 2>/dev/null | head -n 10 || echo 'VÉRIFICATION_CHIFFREMENT_SAUVEGARDE'"
                elif "2.1.6" in num:
                    r["test_procedure"] = "ps -ef | grep -E 'replica|galera|patroni|barman|slave' | grep -v grep || echo 'VÉRIFICATION_REPLICATION_PCA'"
                elif "2.1.7" in num:
                    r["test_procedure"] = "ls -la /etc/mysql/mariadb.conf.d/ /etc/postgresql/ /etc/mongod.conf /etc/cassandra/ 2>/dev/null || echo 'VÉRIFICATION_CONFIG_SAUVEGARDE'"
                elif "2.2" in num:
                    r["test_procedure"] = "ps aux | grep -v -E 'root|systemd|ssh|grep' | head -n 20"
                elif "2.5" in num:
                    r["test_procedure"] = "ls -la /etc/ssl/certs/ /etc/mysql/ssl/ /etc/postgresql/*/main/ 2>/dev/null || echo 'VÉRIFICATION_MATÉRIEL_CRYPTO'"
                else:
                    r["test_procedure"] = f"echo 'INSPECTION MANUELLE DU CONTRÔLE {num} ({r.get('name')})' && ps -ef | head -n 10"
                updated = True

    if updated:
        with open(rf, "w", encoding="utf-8") as f:
            json.dump(rules, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Updated inspection commands in {rf}")


# --- 2. Update perform_checks() in all audit_cis_*.py files ---
for af in audit_files:
    with open(af, "r", encoding="utf-8") as f:
        content = f.read()

    # Modify Manual check condition to run test_procedure whenever non-empty
    old_pattern = r'elif rec\["type"\] == "Manual" and "test_procedure" in rec and \("mysql" in rec\["test_procedure"\].lower\(\).*?\):'
    new_pattern = r'elif rec["type"] == "Manual" and "test_procedure" in rec and rec["test_procedure"].strip():'

    if re.search(old_pattern, content):
        content = re.sub(old_pattern, new_pattern, content)
        with open(af, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ Updated perform_checks in {af}")

print("✅ Maximized information collection across all products and rules!")
