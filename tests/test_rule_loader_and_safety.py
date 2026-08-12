#!/usr/bin/env python3
"""
Unit Test Suite for External Rule Specifications Loader and Command Execution Safety.
100% Python Standard Library (PSL ONLY).
"""

import os
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from audit_cis_mariadb_106 import load_recommendations


def validate_command_safety(cmd):
    """Sanitize shell inputs and block execution of unsafe or destructive commands (PSL ONLY)."""
    if not cmd or not isinstance(cmd, str):
        return False, "Empty or non-string command"
    forbidden_tokens = ["rm -rf /", ":(){ :|:& };:", "> /dev/sda", "mkfs.", "dd if=/dev/zero"]
    for token in forbidden_tokens:
        if token in cmd:
            return False, f"Forbidden unsafe command token detected: '{token}'"
    return True, "Safe"


class TestRuleLoaderAndSafety(unittest.TestCase):
    """Unit tests for JSON recommendation loader and command safety validator."""

    def test_load_recommendations_valid(self):
        rules = load_recommendations("mariadb_106")
        self.assertIsInstance(rules, list)
        self.assertGreater(len(rules), 0)
        first_rule = rules[0]
        self.assertIn("number", first_rule)
        self.assertIn("name", first_rule)
        self.assertIn("category", first_rule)

    def test_load_recommendations_fallback(self):
        rules = load_recommendations("non_existent_product_xyz")
        self.assertIsInstance(rules, list)

    def test_validate_command_safety_safe(self):
        valid_cmds = [
            "mariadb -e 'SHOW VARIABLES LIKE \"have_ssl\";'",
            "psql -U postgres -c 'SHOW ssl;'",
            "cat /etc/rhel-release",
            "stat -c '%a %U %G' /etc/shadow"
        ]
        for cmd in valid_cmds:
            safe, note = validate_command_safety(cmd)
            self.assertTrue(safe, f"Expected command to be safe: {cmd}")
            self.assertEqual(note, "Safe")

    def test_validate_command_safety_unsafe(self):
        unsafe_cmds = [
            "rm -rf /",
            "dd if=/dev/zero of=/dev/sda",
            "mkfs.ext4 /dev/sdb1"
        ]
        for cmd in unsafe_cmds:
            safe, note = validate_command_safety(cmd)
            self.assertFalse(safe, f"Expected command to be blocked: {cmd}")
            self.assertIn("Forbidden unsafe command token", note)

    def test_validate_command_safety_invalid_type(self):
        safe, note = validate_command_safety(None)
        self.assertFalse(safe)
        self.assertEqual(note, "Empty or non-string command")


if __name__ == "__main__":
    unittest.main()
