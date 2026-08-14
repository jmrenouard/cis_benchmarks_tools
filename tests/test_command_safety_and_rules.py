#!/usr/bin/env python3
"""
Unit tests for command execution safety guard and rules validation (100% PSL ONLY).
"""

import glob
import json
import os
import unittest


def is_valid_executable_command(cmd_str):
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
        "docker", "curl", "wget", "sshd", "which", "id", "whoami", "uname", "chmod", "chown",
        "su", "sudo", "pgbackrest", "export", "set", "env"
    }
    if first_word in known_commands:
        return True
    if any(token in s for token in ["|", "&&", ";", ">", "||", "$"]):
        return True
    return False


class TestCommandSafetyAndRules(unittest.TestCase):
    def test_valid_commands(self):
        self.assertTrue(is_valid_executable_command("ls -la /var/lib/mysql"))
        self.assertTrue(is_valid_executable_command("grep -i 'local' /etc/hosts"))
        self.assertTrue(is_valid_executable_command("mysql -N -B -e 'SELECT 1;'"))
        self.assertTrue(is_valid_executable_command("! find /root -name '.mysql_history'"))
        self.assertTrue(is_valid_executable_command("echo 'MANUAL_CHECK'"))
        self.assertTrue(is_valid_executable_command("ps aux | grep postgres"))
        self.assertTrue(is_valid_editable := is_valid_executable_command("sudo pgbackrest info"))

    def test_natural_language_rejection(self):
        self.assertFalse(is_valid_executable_command("Vérifier l'existence du plan DR."))
        self.assertFalse(is_valid_executable_command("Consulter la documentation technique."))
        self.assertFalse(is_valid_executable_command("Review security policy and approve."))
        self.assertFalse(is_valid_executable_command(""))
        self.assertFalse(is_valid_executable_command(None))

    def test_all_rules_json_integrity(self):
        rule_files = sorted(glob.glob("rules/*.json"))
        self.assertGreater(len(rule_files), 0, "Rule specification files must exist in rules/")
        for rfile in rule_files:
            with open(rfile, "r", encoding="utf-8") as f:
                rules = json.load(f)
            self.assertIsInstance(rules, list)
            for r in rules:
                tp = r.get("test_procedure", "")
                if tp:
                    self.assertTrue(is_valid_executable_command(tp), f"Invalid test_procedure in {rfile} check {r.get('number')}: {tp}")


if __name__ == "__main__":
    unittest.main()
