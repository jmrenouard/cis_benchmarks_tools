#!/usr/bin/env python3
"""
Ensure generate_html_report() passes error_count and uses clean Command Error status across all 18 audit scripts (100% PSL ONLY).
"""

import glob
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Updating HTML template rendering across {len(audit_files)} audit scripts...")

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Ensure error_count is passed in template_kwargs / format call
    if "error_count=" not in content:
        content = re.sub(
            r'(\s*)"manual_checks":\s*overall\["manual"\],',
            r'\1"manual_checks": overall["manual"],\n\1"error_count": overall.get("error", 0),',
            content
        )
        content = re.sub(
            r'(\s*)manual_checks=overall\["manual"\],',
            r'\1manual_checks=overall["manual"],\n\1error_count=overall.get("error", 0),',
            content
        )

    # Enhance path_command error output formatting in perform_checks
    old_path_err = 'err_detail = path_stderr if path_stderr else "Impossible d\'exécuter la commande client MariaDB/MySQL (vérifier si le service est démarré)."'
    new_path_err = 'err_detail = path_stderr if path_stderr else "Impossible d\'exécuter la commande client MariaDB/MySQL (vérifier si le service est démarré ou conteneur Docker actif). [Erreur d\'Exécution de Commande - Non-conformité de sécurité non évaluée]"'
    if old_path_err in content:
        content = content.replace(old_path_err, new_path_err)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Successfully updated error_count and path_command error descriptions across all audit scripts!")
