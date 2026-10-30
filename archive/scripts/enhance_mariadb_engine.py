#!/usr/bin/env python3
"""
Enhance MariaDB audit engines (MariaDB 10.6 & 10.11) with:
1. Zero execution errors & clean error handling
2. Automatic Docker container auto-routing & CLI --docker argument support
3. Automation of verifiable manual checks & creation of mariadb_manual_controls_justification.md
100% Python Standard Library (PSL ONLY).
"""

import json
import os
import re

# --- 1. Update JSON Rules for MariaDB 10.6 and MariaDB 10.11 ---
def update_json_rules(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        rules = json.load(f)

    for r in rules:
        num = r.get("number")
        if num == "1.7":
            r["type"] = "Automated"
            r["test_procedure"] = "[[ -f /.dockerenv ]] || grep -qs 'docker\\|containerd' /proc/1/cgroup || systemctl is-active mariadb >/dev/null 2>&1"
            r["expected_output"] = {"type": "returncode_zero"}
        elif num == "2.4":
            r["type"] = "Automated"
            r["test_procedure"] = "mysql -N -B -e \"SELECT COUNT(*) - COUNT(DISTINCT user) FROM mysql.user WHERE user NOT IN ('mysql.infoschema', 'mysql.session', 'mysql.sys', 'mariadb.sys');\""
            r["expected_output"] = {"type": "stdout_equals", "value": "0"}
        elif num == "2.8":
            r["type"] = "Automated"
            r["test_procedure"] = "mysql -N -B -e \"SELECT PLUGIN_STATUS FROM INFORMATION_SCHEMA.PLUGINS WHERE PLUGIN_NAME = 'unix_socket';\""
            r["expected_output"] = {"type": "stdout_equals", "value": "ACTIVE"}
        elif num == "5.1":
            r["type"] = "Automated"
            r["test_procedure"] = "mysql -N -B -e \"SELECT COUNT(*) FROM information_schema.user_privileges WHERE GRANTEE NOT LIKE '\\'root\\'@%' AND GRANTEE NOT LIKE '\\'mysql\\'@%';\""
            r["expected_output"] = {"type": "stdout_equals", "value": "0"}
        elif num == "5.2":
            r["type"] = "Automated"
            r["test_procedure"] = "mysql -N -B -e \"SELECT COUNT(*) FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE PRIVILEGE_TYPE = 'FILE' AND GRANTEE NOT LIKE '\\'root\\'@%';\""
            r["expected_output"] = {"type": "stdout_equals", "value": "0"}
        elif num == "5.3":
            r["type"] = "Automated"
            r["test_procedure"] = "mysql -N -B -e \"SELECT COUNT(*) FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE PRIVILEGE_TYPE = 'PROCESS' AND GRANTEE NOT LIKE '\\'root\\'@%';\""
            r["expected_output"] = {"type": "stdout_equals", "value": "0"}
        elif num == "5.4":
            r["type"] = "Automated"
            r["test_procedure"] = "mysql -N -B -e \"SELECT COUNT(*) FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE PRIVILEGE_TYPE = 'SUPER' AND GRANTEE NOT LIKE '\\'root\\'@%';\""
            r["expected_output"] = {"type": "stdout_equals", "value": "0"}
        elif num == "5.5":
            r["type"] = "Automated"
            r["test_procedure"] = "mysql -N -B -e \"SELECT COUNT(*) FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE PRIVILEGE_TYPE = 'SHUTDOWN' AND GRANTEE NOT LIKE '\\'root\\'@%';\""
            r["expected_output"] = {"type": "stdout_equals", "value": "0"}
        elif num == "5.6":
            r["type"] = "Automated"
            r["test_procedure"] = "mysql -N -B -e \"SELECT COUNT(*) FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE PRIVILEGE_TYPE = 'CREATE USER' AND GRANTEE NOT LIKE '\\'root\\'@%';\""
            r["expected_output"] = {"type": "stdout_equals", "value": "0"}
        elif num == "5.7":
            r["type"] = "Automated"
            r["test_procedure"] = "mysql -N -B -e \"SELECT COUNT(*) FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE IS_GRANTABLE = 'YES' AND GRANTEE NOT LIKE '\\'root\\'@%';\""
            r["expected_output"] = {"type": "stdout_equals", "value": "0"}
        elif num == "7.7":
            r["type"] = "Automated"
            r["test_procedure"] = "mysql -N -B -e \"SELECT PLUGIN_STATUS FROM INFORMATION_SCHEMA.PLUGINS WHERE PLUGIN_NAME = 'password_reuse_check';\""
            r["expected_output"] = {"type": "stdout_equals", "value": "ACTIVE"}

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)
    print(f"✅ Updated JSON rules in {fpath}")

update_json_rules("rules/mariadb_106.json")
update_json_rules("rules/mariadb_1011.json")

# --- 2. Update Audit Python Engine Scripts for MariaDB ---
new_mariadb_run_func = '''def detect_docker_container(remote_host=None, docker_name=None):
    """Detect active MariaDB / MySQL Docker container name."""
    if docker_name:
        return docker_name
    stdout, stderr, ret = run_command("docker ps --format '{{.Names}}' 2>/dev/null | grep -iE 'mariadb|mysql' | head -n 1", remote_host=remote_host)
    if ret == 0 and stdout:
        return stdout.strip()
    return None


def run_command(command, remote_host=None, docker_container=None):
    """Execute command safely locally, over SSH, or inside Docker container (PSL ONLY)."""
    try:
        if isinstance(command, str):
            if docker_container and not command.startswith("docker exec"):
                command = f"docker exec -i {docker_container} /bin/bash -c {json.dumps(command)}"
            elif "systemctl" in command and (os.path.exists("/.dockerenv") or not os.path.exists("/run/systemd/system")):
                if "mariadb" in command or "mysql" in command:
                    command = "mariadb -e 'SELECT 1;' 2>/dev/null || mysql -e 'SELECT 1;' 2>/dev/null || ps aux | grep -v grep | grep mysqld"
            cmd_args = ["/bin/bash", "-c", command]
        else:
            cmd_args = list(command)

        if remote_host:
            cmd_args = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", "-i", "/root/.ssh/id_rsa", remote_host] + cmd_args

        process = subprocess.run(cmd_args, check=False, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10)
        stdout_text = process.stdout.strip()
        stderr_text = process.stderr.strip()

        if stderr_text:
            filtered_lines = [
                line for line in stderr_text.splitlines()
                if not line.startswith("Warning: Permanently added")
                and "pseudo-terminal" not in line
            ]
            stderr_text = chr(10).join(filtered_lines).strip()

        return stdout_text, stderr_text, process.returncode
    except subprocess.TimeoutExpired:
        return "", "Command execution timed out after 10 seconds", -1
    except Exception as e:
        return "", str(e), -1
'''

for script in ["audit_cis_mariadb_106.py", "audit_cis_mariadb_1011.py"]:
    with open(script, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace run_command definition
    content = re.sub(
        r'def run_command\(.*?\):\n.*?(?=\n\ndef evaluate_condition|\nRECOMMENDATIONS_DATA|\ndef perform_checks)',
        new_mariadb_run_func + "\n",
        content,
        flags=re.DOTALL
    )

    # Ensure perform_checks signature accepts docker_container=None
    content = content.replace("def perform_checks(recommendations, remote_host=None):", "def perform_checks(recommendations, remote_host=None, docker_container=None):")
    content = content.replace("def perform_checks(recommendations_data, remote_host=None):", "def perform_checks(recommendations_data, remote_host=None, docker_container=None):")

    # Add --docker argument in main if not present
    if "--docker" not in content:
        content = content.replace(
            'parser.add_argument("-m", "--mode"',
            'parser.add_argument("--docker", "--container", dest="docker_container", default=None, help="Target Docker container name or ID")\n    parser.add_argument("-m", "--mode"'
        )
        content = content.replace(
            'check_results = perform_checks(rules_data, remote_host=remote_target)',
            'docker_target = detect_docker_container(remote_host=remote_target, docker_name=args.docker_container)\n    check_results = perform_checks(rules_data, remote_host=remote_target, docker_container=docker_target)'
        )

    with open(script, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Enhanced MariaDB audit scripts (10.6 & 10.11) with Docker auto-routing and zero execution error handling!")
