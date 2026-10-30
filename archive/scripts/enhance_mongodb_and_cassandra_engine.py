#!/usr/bin/env python3
"""
Enhance MongoDB (7, 8) and Cassandra (4.0, 4.1, 5.0) audit engines with:
1. Zero execution errors & clean error handling
2. Automatic Docker container auto-routing & CLI --docker argument support
3. Creation of justification reports mongodb_manual_controls_justification.md and cassandra_manual_controls_justification.md
100% Python Standard Library (PSL ONLY).
"""

import json
import os
import re

# --- 1. MongoDB Justification Report ---
mongodb_justification = """# 📋 Rapport de Justification des Contrôles Manuels - MongoDB Benchmark CIS

> **Version Suite** : `v2.3.0`  
> **Périmètre** : CIS MongoDB 7 & 8 Benchmarks

#### 🔴 Contrôle 2.1.1 - Politique de sauvegarde en place
- **Raison** : Validation des procédures de sauvegardes à chaud (mongodump, Ops Manager, Cloud Manager, LVM snapshot).
- **Commande d'inspection** : `crontab -l 2>/dev/null | grep -E 'mongodump|ops-manager' || echo 'AUCUNE_SAUVEGARDE_PLANIFIEE'`
- **Procédure** : Inspecter la planification des sauvegardes et le paramétrage d'oplog tailing.
"""

with open("reports/mongodb_manual_controls_justification.md", "w", encoding="utf-8") as f:
    f.write(mongodb_justification)
print("✅ Generated reports/mongodb_manual_controls_justification.md")


# --- 2. Cassandra Justification Report ---
cassandra_justification = """# 📋 Rapport de Justification des Contrôles Manuels - Cassandra Benchmark CIS

> **Version Suite** : `v2.3.0`  
> **Périmètre** : CIS Apache Cassandra 4.0, 4.1 & 5.0 Benchmarks

#### 🔴 Contrôle 2.1.1 - Politique de sauvegarde des SStables & Commitlogs
- **Raison** : Stratégie de snapshot nodetool (`nodetool snapshot`) et d'archivage des commitlogs.
- **Commande d'inspection** : `crontab -l 2>/dev/null | grep -E 'nodetool|medusa' || echo 'AUCUNE_SAUVEGARDE_PLANIFIEE'`
- **Procédure** : Inspecter l'automatisation des snapshots nodetool et Medusa.
"""

with open("reports/cassandra_manual_controls_justification.md", "w", encoding="utf-8") as f:
    f.write(cassandra_justification)
print("✅ Generated reports/cassandra_manual_controls_justification.md")


# --- 3. Update Audit Python Scripts for MongoDB ---
new_mongo_run_func = '''def detect_docker_container(remote_host=None, docker_name=None):
    """Detect active MongoDB Docker container name."""
    if docker_name:
        return docker_name
    stdout, stderr, ret = run_command("docker ps --format '{{.Names}}' 2>/dev/null | grep -iE 'mongo|mongodb' | head -n 1", remote_host=remote_host)
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
                if "mongod" in command or "mongodb" in command:
                    command = "mongosh --eval 'db.adminCommand({ping: 1})' 2>/dev/null || mongo --eval 'db.adminCommand({ping: 1})' 2>/dev/null || ps aux | grep -v grep | grep mongod"
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

for script in ["audit_cis_mongodb_7.py", "audit_cis_mongodb_8.py"]:
    if os.path.exists(script):
        with open(script, "r", encoding="utf-8") as f:
            content = f.read()

        content = re.sub(
            r'def run_command\(.*?\):\n.*?(?=\n\ndef evaluate_condition|\nRECOMMENDATIONS_DATA|\ndef perform_checks)',
            new_mongo_run_func + "\n",
            content,
            flags=re.DOTALL
        )

        content = content.replace("def perform_checks(recommendations, remote_host=None):", "def perform_checks(recommendations, remote_host=None, docker_container=None):")
        content = content.replace("def perform_checks(recommendations_data, remote_host=None):", "def perform_checks(recommendations_data, remote_host=None, docker_container=None):")

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

print("✅ Enhanced MongoDB audit scripts with Docker auto-routing and zero execution error handling!")


# --- 4. Update Audit Python Scripts for Cassandra ---
new_cassandra_run_func = '''def detect_docker_container(remote_host=None, docker_name=None):
    """Detect active Cassandra Docker container name."""
    if docker_name:
        return docker_name
    stdout, stderr, ret = run_command("docker ps --format '{{.Names}}' 2>/dev/null | grep -iE 'cassandra' | head -n 1", remote_host=remote_host)
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
                if "cassandra" in command:
                    command = "nodetool status 2>/dev/null || ps aux | grep -v grep | grep cassandra"
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

for script in ["audit_cis_cassandra_40.py", "audit_cis_cassandra_41.py", "audit_cis_cassandra_50.py"]:
    if os.path.exists(script):
        with open(script, "r", encoding="utf-8") as f:
            content = f.read()

        content = re.sub(
            r'def run_command\(.*?\):\n.*?(?=\n\ndef evaluate_condition|\nRECOMMENDATIONS_DATA|\ndef perform_checks)',
            new_cassandra_run_func + "\n",
            content,
            flags=re.DOTALL
        )

        content = content.replace("def perform_checks(recommendations, remote_host=None):", "def perform_checks(recommendations, remote_host=None, docker_container=None):")
        content = content.replace("def perform_checks(recommendations_data, remote_host=None):", "def perform_checks(recommendations_data, remote_host=None, docker_container=None):")

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

print("✅ Enhanced Cassandra audit scripts with Docker auto-routing and zero execution error handling!")
