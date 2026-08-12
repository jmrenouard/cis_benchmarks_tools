#!/usr/bin/env python3
"""
Ensure mysql/mariadb commands are resilient across all MySQL and MariaDB audit scripts.
Supports both mariadb and mysql CLI binaries with non-interactive sudo (-n) and fallback handling (PSL ONLY).
"""

import glob
import re

db_audit_files = sorted(glob.glob("audit_cis_mariadb_*.py") + glob.glob("audit_cis_mysql_*.py"))
print(f"Updating MySQL/MariaDB command resilience across {len(db_audit_files)} scripts...")

new_path_block = '''                if "path_command" in rec:
                    path_cmd = rec["path_command"]
                    path_cmd_to_run = path_cmd
                    if ("mysql -N -B" in path_cmd or "mariadb -N -B" in path_cmd) and "SELECT @@datadir;" in path_cmd:
                        path_cmd_to_run = f"{path_cmd} 2>/dev/null || mariadb -N -B -e \\\"SELECT @@datadir;\\\" 2>/dev/null || sudo -n mysql -N -B -e \\\"SELECT @@datadir;\\\" 2>/dev/null || sudo -n mariadb -N -B -e \\\"SELECT @@datadir;\\\" 2>/dev/null"
                    
                    path_stdout, path_stderr, path_returncode = run_command(path_cmd_to_run, remote_host=remote_host)

                    if (path_returncode != 0 or not path_stdout) and "datadir" in path_cmd:
                        fb_stdout, fb_stderr, fb_ret = run_command("ls -d /var/lib/mariadb /var/lib/mysql 2>/dev/null | head -n 1", remote_host=remote_host)
                        if fb_ret == 0 and fb_stdout:
                            path_stdout = fb_stdout.strip()
                            path_returncode = 0

                    if path_returncode != 0 or not path_stdout:
                        if "Unknown system variable" in path_stderr or "ERROR 1193" in path_stderr:
                             check_result["status"] = "Not Applicable"
                             check_result["output"] = "Variable/Plugin non disponible (N/A)." + chr(10) + "Stderr:" + chr(10) + path_stderr
                        else:
                             check_result["status"] = "Error"
                             err_detail = path_stderr if path_stderr else "Impossible d'exécuter la commande client MariaDB/MySQL (vérifier si le service est démarré)."
                             check_result["output"] = "Error lors de l'obtention du chemin via:" + chr(10) + f"`{path_cmd}`" + chr(10) + "Output:" + chr(10) + err_detail
                             check_result["error"] = err_detail
                        results[category].append(check_result)
                        continue'''

for fpath in db_audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'                if "path_command" in rec:\n.*?(?=\n                    dynamic_path = |\n                elif "test_procedure" in rec:)'
    content = re.sub(pattern, new_path_block, content, flags=re.DOTALL)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Updated MySQL/MariaDB command resilience with non-interactive sudo (-n)!")
