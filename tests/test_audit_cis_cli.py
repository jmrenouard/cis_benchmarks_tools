#!/usr/bin/env python3
"""
Unit Test Suite for Unified Audit CLI Engine and Target Mapping Integrity.
100% Python Standard Library (PSL ONLY).
"""

import os
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from audit_cis import TARGET_MAP, list_targets, run_single_audit


class TestAuditCisCliEngine(unittest.TestCase):
    """Unit tests for audit_cis CLI target map and execution engine."""

    def test_target_map_integrity(self):
        self.assertIsInstance(TARGET_MAP, dict)
        self.assertEqual(len(TARGET_MAP), 18)
        for key, value in TARGET_MAP.items():
            self.assertEqual(len(value), 3, f"Expected 3 elements for target {key}")
            script_file, label, count = value
            self.assertTrue(script_file.endswith(".py"))
            self.assertIsInstance(label, str)
            self.assertGreater(count, 0)
            script_path = os.path.join(REPO_ROOT, script_file)
            self.assertTrue(os.path.exists(script_path), f"Audit script file missing: {script_path}")

    def test_run_single_audit_invalid_target(self):
        result = run_single_audit("invalid_target_123")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
