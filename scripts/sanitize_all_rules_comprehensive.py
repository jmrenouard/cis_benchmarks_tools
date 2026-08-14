#!/usr/bin/env python3
"""
Comprehensive sanitization of all test_procedure entries across all 18 rules/*.json files (100% PSL ONLY).
"""

import glob
import json
import os
import re

known_commands = {
    "cat", "ls", "grep", "egrep", "fgrep", "find", "ps", "awk", "cut", "sed", "head", "tail",
    "echo", "getent", "crontab", "df", "stat", "test", "dpkg", "rpm", "systemctl", "service",
    "mysql", "mariadb", "psql", "cqlsh", "mongo", "mongosh", "python3", "python", "bash", "sh",
    "docker", "curl", "wget", "sshd", "which", "id", "whoami", "uname", "chmod", "chown", "su", "sudo", "pgbackrest"
}

def is_valid(tp):
    if not tp or not isinstance(tp, str):
        return False
    s = tp.strip()
    if not s:
        return False
    if s.startswith("!") or s.startswith("[") or s.startswith("(") or s.startswith("/") or s.startswith("."):
        return True
    first_word = s.split()[0].lower()
    if first_word in known_commands:
        return True
    if any(t in s for t in ["|", "&&", ";", ">", "||", "$"]):
        return True
    return False

print("Sanitizing all test_procedure entries across rules/*.json...")
for fpath in sorted(glob.glob("rules/*.json")):
    with open(fpath, "r", encoding="utf-8") as f:
        rules = json.load(f)

    for r in rules:
        num = str(r.get("number", ""))
        tp = r.get("test_procedure", "").strip()

        if not is_valid(tp):
            if "credentials de sauvegarde" in tp or num == "2.1.3" and "credentials" in tp:
                r["test_procedure"] = "ls -la /etc/mysql/ /etc/mariadb/ /root/.my.cnf /etc/my.cnf /var/lib/mysql/ 2>/dev/null || echo 'VERIF_CREDENTIALS_BACKUP'"
            elif "mongosh --quiet --eval \"print(db.version())\"" in tp or num == "1.1" and "mongo" in fpath:
                r["test_procedure"] = "mongosh --quiet --eval 'print(db.version())' 2>/dev/null || mongod --version 2>/dev/null || echo 'MONGODB_VERSION_CHECK'"
            elif "printjson(db.getUser())" in tp or num == "3.2" and "mongo" in fpath:
                r["test_procedure"] = "mongosh --quiet --eval 'printjson(db.getUser())' 2>/dev/null || echo 'MONGODB_USER_ROLE_CHECK'"
            elif "rolesInfo: 1" in tp or num == "3.4" and "mongo" in fpath:
                r["test_procedure"] = "mongosh --quiet --eval 'printjson(db.runCommand({rolesInfo: 1}))' 2>/dev/null || echo 'MONGODB_ROLES_CHECK'"
            elif "dbowner" in tp or num == "3.5" and "mongo" in fpath:
                r["test_procedure"] = "mongosh --quiet --eval 'printjson(db.runCommand({rolesInfo: \"dbOwner\"}))' 2>/dev/null || echo 'MONGODB_ADMIN_ROLES_CHECK'"
            elif "umask" in tp or num == "2.1" and "postgres" in fpath:
                r["test_procedure"] = "su - postgres -c umask 2>/dev/null || umask"
            elif "pg_proc" in tp or num == "4.5" and "postgres" in fpath:
                r["test_procedure"] = "psql -U postgres -t -A -c \"SELECT proname FROM pg_proc WHERE pronamespace = 'public'::regnamespace;\" 2>/dev/null || echo 'VERIF_PROC_PRIVILEGES'"
            elif "has_table_privilege" in tp or num == "4.6" and "postgres" in fpath:
                r["test_procedure"] = "psql -U postgres -t -A -c \"SELECT tablename FROM pg_tables WHERE schemaname = 'public';\" 2>/dev/null || echo 'VERIF_TABLE_PRIVILEGES'"
            elif "postgresql.conf" in tp or num == "6.1" and "postgres" in fpath:
                r["test_procedure"] = "cat /etc/postgresql/*/*/postgresql.conf /var/lib/postgresql/data/postgresql.conf 2>/dev/null | grep -v '^\\s*#' | head -n 30 || echo 'VERIF_RUNTIME_PARAMETERS'"
            elif "pgbackrest" in tp or num == "8.2" and "postgres" in fpath:
                r["test_procedure"] = "pgbackrest info 2>/dev/null || sudo -n pgbackrest info 2>/dev/null || echo 'PGBACKREST_CHECK'"
            else:
                # Safe fallback echo
                clean_tp = tp.replace("'", "").replace('"', "")
                r["test_procedure"] = f"echo 'Contrôle Manuel: {clean_tp[:60]}'"

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)

print("✅ All rules sanitized successfully!")
