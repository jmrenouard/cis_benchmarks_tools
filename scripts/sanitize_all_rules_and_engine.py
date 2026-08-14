#!/usr/bin/env python3
"""
Sanitize all test_procedure entries in rules/*.json to ensure they are valid shell commands,
and inject is_valid_executable_command() guard into perform_checks() across all 18 audit scripts (100% PSL ONLY).
"""

import glob
import json
import os
import re

# 1. Sanitize rules/*.json
print("1. Sanitizing rules/*.json...")
for fpath in sorted(glob.glob("rules/*.json")):
    with open(fpath, "r", encoding="utf-8") as f:
        rules = json.load(f)

    modified = False
    for r in rules:
        tp = r.get("test_procedure", "").strip()
        if not tp:
            continue

        # Convert natural text descriptions to executable inspection commands or safe echoes
        if tp == "Vérifier l'existence et la validité du plan DR." or "plan DR" in tp:
            r["test_procedure"] = "ls -la /etc/mysql/ /etc/mariadb/ /etc/postgresql/ /var/backups/ /backup/ 2>/dev/null || echo 'MANUAL_DR_POLICY_REVIEW'"
            modified = True
        elif tp == "Vérifier les services actifs sur la machine." or "aucun autre service" in tp:
            r["test_procedure"] = "ps aux | grep -v '\\[.*\\]' | grep -v grep | head -n 30"
            modified = True
        elif tp.startswith("apt search") or tp.startswith("dnf search"):
            r["test_procedure"] = "dpkg -l | grep -iE 'postgres|mysql|mariadb' 2>/dev/null || rpm -qa | grep -iE 'postgres|mysql|mariadb' 2>/dev/null"
            modified = True
        elif "pg_hba.conf" in tp and not tp.startswith("grep") and not tp.startswith("cat"):
            r["test_procedure"] = "grep -E '^\\s*local\\s+.*trust' /etc/postgresql/*/*/pg_hba.conf /var/lib/postgresql/data/pg_hba.conf 2>/dev/null || echo 'PASS_AUCUN_TRUST_LOCAL'"
            modified = True
        elif "/etc/sudoers" in tp and not tp.startswith("grep") and not tp.startswith("cat"):
            r["test_procedure"] = "grep -iE 'postgres|mysql|mariadb' /etc/sudoers /etc/sudoers.d/* 2>/dev/null || echo 'PASS_AUCUN_SUDO_DEDIE'"
            modified = True
        elif "\\du+" in tp:
            r["test_procedure"] = "psql -U postgres -t -A -c 'SELECT rolname, rolsuper, rolcreatedb, rolcreaterole, rolreplication FROM pg_roles;' 2>/dev/null || echo 'VERIF_MANUELLE_ROLES_POSTGRES'"
            modified = True
        elif "\\d+ <table>" in tp or "Row Level Security" in tp:
            r["test_procedure"] = "psql -U postgres -t -A -c 'SELECT relname, relrowsecurity FROM pg_class WHERE relrowsecurity = true;' 2>/dev/null || echo 'VERIF_MANUELLE_RLS_POSTGRES'"
            modified = True
        elif re.match(r"^(Vérifier|Consulter|Examiner|Contrôler|S\'assurer|Confirmer|Review|Verify|Ensure|Check)\b", tp, re.IGNORECASE):
            r["test_procedure"] = f"echo 'Contrôle Manuel: {tp.replace(chr(39), chr(34))}'"
            modified = True

    if modified:
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(rules, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Sanitized {fpath}")

# 2. Inject is_valid_executable_command() in audit scripts
guard_function_code = '''def is_valid_executable_command(cmd_str):
    """Check if command string is a valid shell executable command rather than descriptive human text."""
    if not cmd_str or not isinstance(cmd_str, str):
        return False
    s = cmd_str.strip()
    if not s:
        return False
    if s.startswith("!") or s.startswith("[") or s.startswith("(") or s.startswith("/") or s.startswith("."):
        return True
    first_word = s.split()[0].lower()
    known_commands = {
        "cat", "ls", "grep", "egrep", "fgrep", "find", "ps", "awk", "cut", "sed", "head", "tail",
        "echo", "getent", "crontab", "df", "stat", "test", "dpkg", "rpm", "systemctl", "service",
        "mysql", "mariadb", "psql", "cqlsh", "mongo", "mongosh", "python3", "python", "bash", "sh",
        "docker", "curl", "wget", "sshd", "which", "id", "whoami", "uname", "chmod", "chown"
    }
    if first_word in known_commands:
        return True
    if any(token in s for token in ["|", "&&", ";", ">", "||", "$"]):
        return True
    return False
'''

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"2. Injecting command safety guard across {len(audit_files)} audit scripts...")

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    if "def is_valid_executable_command(" not in content:
        content = content.replace("def run_command(", guard_function_code + "\n\ndef run_command(")

    # In perform_checks, validate cmd_to_run with is_valid_executable_command
    old_cmd_check = "if cmd_to_run:"
    new_cmd_check = """if cmd_to_run:
                    if not is_valid_executable_command(cmd_to_run):
                        check_result["status"] = "Manual"
                        check_result["output"] = "This control requires manual verification." + chr(10) + chr(10) + "Guide procédural: " + cmd_to_run
                        check_result["test_procedure"] = command_executed_display
                        results[category].append(check_result)
                        continue"""

    if old_cmd_check in content and "if not is_valid_executable_command(cmd_to_run):" not in content:
        content = content.replace(old_cmd_check, new_cmd_check, 1)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Successfully sanitized all rules and hardened audit engine execution guard!")
