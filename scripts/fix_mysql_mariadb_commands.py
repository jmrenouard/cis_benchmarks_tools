#!/usr/bin/env python3
"""
Ensure mysql/mariadb commands are resilient across all MySQL and MariaDB audit scripts.
Supports both mariadb and mysql CLI binaries with sudo and fallback handling (PSL ONLY).
"""

import glob
import re

db_audit_files = sorted(glob.glob("audit_cis_mariadb_*.py") + glob.glob("audit_cis_mysql_*.py"))
print(f"Updating MySQL/MariaDB command resilience across {len(db_audit_files)} scripts...")

for fpath in db_audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Make MYSQL_CMD use mariadb 2>/dev/null || mysql fallback
    if "audit_cis_mariadb" in fpath:
        content = content.replace('MYSQL_CMD = "mysql -N -B"', 'MYSQL_CMD = "mariadb -N -B 2>/dev/null || mysql -N -B"')
    elif "audit_cis_mysql" in fpath:
        content = content.replace('MYSQL_CMD = "mysql -N -B"', 'MYSQL_CMD = "mysql -N -B 2>/dev/null || mariadb -N -B"')

    # Replace old_path_block with enhanced fallback block in perform_checks
    old_path_block = r'''                if "path_command" in rec:
                    path_cmd = rec["path_command"]
                    path_stdout, path_stderr, path_returncode = run_command(path_cmd, remote_host=remote_host)

                    if path_returncode != 0 or not path_stdout:
                        if "Unknown system variable" in path_stderr or "ERROR 1193" in path_stderr:
                             check_result["status"] = "Not Applicable"
                             check_result["output"] = f"Variable/Plugin non disponible (N/A).\nStderr:\n{path_stderr}"
                        else:
                             check_result["status"] = "Error"
                             check_result["output"] = f"Error lors de l'obtention du chemin via:\n`{path_cmd}`\nStdout:\n{path_stdout}\nStderr:\n{path_stderr}"
                             check_result["error"] = path_stderr
                        results[category].append(check_result)
                        continue'''

    new_path_block = '''                if "path_command" in rec:
                    path_cmd = rec["path_command"]
                    path_cmd_to_run = path_cmd
                    if ("mysql -N -B" in path_cmd or "mariadb -N -B" in path_cmd) and "SELECT @@datadir;" in path_cmd:
                        path_cmd_to_run = f"{path_cmd} 2>/dev/null || mariadb -N -B -e \\\"SELECT @@datadir;\\\" 2>/dev/null || sudo mysql -N -B -e \\\"SELECT @@datadir;\\\" 2>/dev/null || sudo mariadb -N -B -e \\\"SELECT @@datadir;\\\" 2>/dev/null"
                    
                    path_stdout, path_stderr, path_returncode = run_command(path_cmd_to_run, remote_host=remote_host)

                    if (path_returncode != 0 or not path_stdout) and "datadir" in path_cmd:
                        fb_stdout, fb_stderr, fb_ret = run_command("ls -d /var/lib/mariadb /var/lib/mysql 2>/dev/null | head -n 1", remote_host=remote_host)
                        if fb_ret == 0 and fb_stdout:
                            path_stdout = fb_stdout.strip()
                            path_returncode = 0

                    if path_returncode != 0 or not path_stdout:
                        if "Unknown system variable" in path_stderr or "ERROR 1193" in path_stderr:
                             check_result["status"] = "Not Applicable"
                             check_result["output"] = f"Variable/Plugin non disponible (N/A).\nStderr:\n{path_stderr}"
                        else:
                             check_result["status"] = "Error"
                             err_detail = path_stderr if path_stderr else "Impossible d'exécuter la commande client MariaDB/MySQL (vérifier si le service est démarré)."
                             check_result["output"] = f"Error lors de l'obtention du chemin via:\n`{path_cmd}`\nOutput:\n{err_detail}"
                             check_result["error"] = err_detail
                        results[category].append(check_result)
                        continue'''

    if old_path_block in content:
        content = content.replace(old_path_block, new_path_block)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Enhanced MySQL/MariaDB command resilience across all database audit scripts!")
