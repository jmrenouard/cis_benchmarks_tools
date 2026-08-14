#!/usr/bin/env python3
"""
Fix perform_checks() execution ordering across all 18 audit scripts so that
command execution failures (ERROR 2002, ERROR 1045, command not found, timeout, non-zero return codes)
systematically set status="Error" rather than dumping raw command errors in "Manual" controls (PSL ONLY).
"""

import glob
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Fixing command error precedence across {len(audit_files)} audit scripts...")

new_evaluation_block = '''                if cmd_to_run:
                    stdout, stderr, returncode = run_command(cmd_to_run, remote_host=remote_host, docker_container=docker_container) if 'docker_container' in locals() else run_command(cmd_to_run, remote_host=remote_host)
                    check_result["output"] = f"Stdout:\\n{stdout}\\nStderr:\\n{stderr}\\nReturn Code: {returncode}"
                    check_result["error"] = stderr
                    check_result["test_procedure"] = command_executed_display

                    # 1. Not Applicable (variable/plugin missing)
                    if "Unknown system variable" in stderr or "Unknown command" in stderr or "ERROR 1193" in stderr:
                        check_result["status"] = "Not Applicable"
                        check_result["output"] = f"Variable ou plugin non installé/activé.\\n{check_result['output']}"
                        results[category].append(check_result)
                        continue

                    # 2. Command Execution Errors (take precedence over Manual/Pass/Fail)
                    if returncode == 127 or ("command not found" in stderr.lower() and not cmd_to_run.strip().startswith('!')):
                        check_result["status"] = "Error"
                        check_result["output"] = f"Error: Command not found.\\n{check_result['output']}"
                        results[category].append(check_result)
                        continue
                    elif returncode == 124:
                        check_result["status"] = "Error"
                        check_result["output"] = f"Error: Timeout.\\n{check_result['output']}"
                        results[category].append(check_result)
                        continue
                    elif "ERROR 1045 (28000): Access denied" in stderr:
                        check_result["status"] = "Error"
                        check_result["output"] = f"Error: Accès refusé (vérifier les identifiants/privilèges).\\n{check_result['output']}"
                        results[category].append(check_result)
                        continue
                    elif "ERROR 2002 (HY000): Can't connect" in stderr:
                        check_result["status"] = "Error"
                        check_result["output"] = f"Error: Impossible de se connecter au serveur (service arrêté ou mauvais socket).\\n{check_result['output']}"
                        results[category].append(check_result)
                        continue

                    # 3. Manual Checks (when command executed without execution errors)
                    if rec["type"] == "Manual":
                        check_result["status"] = "Manual"
                        check_result["output"] = "This control requires manual verification.\\n\\nRésultat de l'extraction automatique pour aide:\\n" + check_result["output"]
                        results[category].append(check_result)
                        continue

                    # 4. Automated Evaluation
                    condition = rec.get("expected_output")
                    if condition:
                        is_pass = evaluate_condition(condition, stdout, stderr, returncode)
                        if is_pass and returncode != 0 and condition.get("type") not in ["returncode_zero", "returncode_equals"] and not cmd_to_run.strip().startswith('!'):
                            is_pass = False
                            check_result["output"] += f"\\n\\nÉchec car la commande a retourné une erreur (code {returncode})."
                        
                        if is_pass:
                            check_result["status"] = "Pass"
                        else:
                            check_result["status"] = "Fail"
                    else:
                        check_result["status"] = "Manual"
'''

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Match existing cmd_to_run evaluation block in perform_checks
    pattern = r'                if cmd_to_run:\n.*?(?=\n                    results\[category\]\.append\(check_result\)|\n            except Exception as e:)'
    content = re.sub(pattern, new_evaluation_block, content, flags=re.DOTALL)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Fixed command error precedence across all audit scripts!")
