#!/usr/bin/env python3
"""
Fix history test procedures and empty path_command handling across rules and audit engines (PSL ONLY).
"""

import glob
import json
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_DIR = os.path.join(REPO_ROOT, "rules")

# 1. Update rules/*.json
for fname in sorted(os.listdir(RULES_DIR)):
    if not fname.endswith(".json"):
        continue
    fpath = os.path.join(RULES_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        rules = json.load(f)

    modified = False
    for r in rules:
        tp = r.get("test_procedure", "")
        if "for h in /root /home/*; do [ -f \"$h/.mysql_history\" ] && echo \"$h/.mysql_history\"; done" in tp and not tp.endswith("; true"):
            r["test_procedure"] = tp.rstrip() + "; true"
            modified = True
        elif "for h in /root /home/* /var/lib/postgresql; do [ -f \"$h/.psql_history\" ] && echo \"$h/.psql_history\"; done" in tp and not tp.endswith("; true"):
            r["test_procedure"] = tp.rstrip() + "; true"
            modified = True

    if modified:
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(rules, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"✓ Updated history test procedure in {fname}")

# 2. Update audit_cis_*.py
audit_files = sorted(glob.glob(os.path.join(REPO_ROOT, "audit_cis_*.py")))
for afile in audit_files:
    with open(afile, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace path_returncode handling
    old_target = """                    if path_returncode != 0 or not path_stdout:
                        if "Unknown system variable" in path_stderr or "ERROR 1193" in path_stderr:
                             check_result["status"] = "Not Applicable"
                             check_result["output"] = "Variable/Plugin non disponible (N/A)." + chr(10) + "Stderr:" + chr(10) + path_stderr
                        else:
                             check_result["status"] = "Error"
                             err_detail = path_stderr if path_stderr else "Impossible d'exécuter la commande client MariaDB/MySQL (vérifier si le service est démarré ou conteneur Docker actif). [Erreur d'Exécution de Commande - Non-conformité de sécurité non évaluée]"
                             check_result["output"] = "Error lors de l'obtention du chemin via:" + chr(10) + f"`{path_cmd}`" + chr(10) + "Output:" + chr(10) + err_detail
                             check_result["error"] = err_detail
                        results[category].append(check_result)
                        continue"""

    new_target = """                    if path_returncode != 0 or not path_stdout:
                        if "Unknown system variable" in path_stderr or "ERROR 1193" in path_stderr:
                             check_result["status"] = "Not Applicable"
                             check_result["output"] = "Variable/Plugin non disponible (N/A)." + chr(10) + "Stderr:" + chr(10) + path_stderr
                        elif path_returncode == 0 and not path_stdout:
                             check_result["status"] = "Not Applicable"
                             check_result["output"] = "Variable/Journal non configuré(e) ou désactivé(e) (N/A)." + chr(10) + f"Commande: `{path_cmd}`"
                        else:
                             check_result["status"] = "Error"
                             err_detail = path_stderr if path_stderr else "Impossible d'exécuter la commande client MariaDB/MySQL (vérifier si le service est démarré ou conteneur Docker actif). [Erreur d'Exécution de Commande - Non-conformité de sécurité non évaluée]"
                             check_result["output"] = "Error lors de l'obtention du chemin via:" + chr(10) + f"`{path_cmd}`" + chr(10) + "Output:" + chr(10) + err_detail
                             check_result["error"] = err_detail
                        results[category].append(check_result)
                        continue"""

    if old_target in content:
        content = content.replace(old_target, new_target)
        with open(afile, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Updated path_returncode handling in {os.path.basename(afile)}")

print("All history and path_command updates applied successfully.")
