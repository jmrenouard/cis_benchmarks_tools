#!/usr/bin/env python3
"""
Automated Unit Test Suite for CIS Condition Evaluator Engine.
100% Code Coverage for evaluate_condition logic across all operators.
Uses Python Standard Library ONLY (unittest).
"""

import os
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from audit_cis_postgresql_18 import evaluate_condition


class TestEvaluateConditionEngine(unittest.TestCase):
    """100% Code Coverage unit tests for evaluate_condition engine."""

    def test_empty_or_none_condition(self):
        self.assertFalse(evaluate_condition(None, "output", "", 0))
        self.assertFalse(evaluate_condition({}, "output", "", 0))

    def test_returncode_zero(self):
        cond = {"type": "returncode_zero"}
        self.assertTrue(evaluate_condition(cond, "", "", 0))
        self.assertFalse(evaluate_condition(cond, "", "error", 1))

    def test_returncode_equals(self):
        cond = {"type": "returncode_equals", "value": 0}
        self.assertTrue(evaluate_condition(cond, "", "", 0))
        self.assertFalse(evaluate_condition(cond, "", "error", 127))

    def test_stdout_equals(self):
        cond = {"type": "stdout_equals", "value": "postgres"}
        self.assertTrue(evaluate_condition(cond, "postgres", "", 0))
        self.assertFalse(evaluate_condition(cond, "mysql", "", 0))

    def test_stdout_not_equals(self):
        cond = {"type": "stdout_not_equals", "value": "/"}
        self.assertTrue(evaluate_condition(cond, "/var/lib/postgresql", "", 0))
        self.assertFalse(evaluate_condition(cond, "/", "", 0))

    def test_stdout_contains(self):
        cond = {"type": "stdout_contains", "value": "STRICT_ALL_TABLES"}
        self.assertTrue(evaluate_condition(cond, "ONLY_FULL_GROUP_BY,STRICT_ALL_TABLES", "", 0))
        self.assertFalse(evaluate_condition(cond, "NO_ENGINE_SUBSTITUTION", "", 0))

    def test_stdout_not_contains(self):
        cond = {"type": "stdout_not_contains", "value": "OFF"}
        self.assertTrue(evaluate_condition(cond, "ON", "", 0))
        self.assertFalse(evaluate_condition(cond, "OFF", "", 0))

    def test_stdout_is_empty(self):
        cond = {"type": "stdout_is_empty"}
        self.assertTrue(evaluate_condition(cond, "", "", 0))
        self.assertFalse(evaluate_condition(cond, "data", "", 0))

    def test_stdout_not_empty(self):
        cond = {"type": "stdout_not_empty"}
        self.assertTrue(evaluate_condition(cond, "active", "", 0))
        self.assertFalse(evaluate_condition(cond, "", "", 0))

    def test_stdout_contains_any(self):
        cond = {"type": "stdout_contains_any", "values": ["/bin/false", "/sbin/nologin"]}
        self.assertTrue(evaluate_condition(cond, "/sbin/nologin", "", 0))
        self.assertFalse(evaluate_condition(cond, "/bin/bash", "", 0))

        # None values fallback
        cond_none = {"type": "stdout_contains_any", "values": None}
        self.assertFalse(evaluate_condition(cond_none, "output", "", 0))

    def test_stdout_not_contains_any(self):
        cond = {"type": "stdout_not_contains_any", "values": ["root", "admin"]}
        self.assertTrue(evaluate_condition(cond, "postgres", "", 0))
        self.assertFalse(evaluate_condition(cond, "root", "", 0))

        # None values fallback
        cond_none = {"type": "stdout_not_contains_any", "values": None}
        self.assertTrue(evaluate_condition(cond_none, "output", "", 0))

    def test_stdout_regex_match(self):
        cond = {"type": "stdout_regex_match", "pattern": r"^mysql:mysql\s+7[05][05]$"}
        self.assertTrue(evaluate_condition(cond, "mysql:mysql 700", "", 0))
        self.assertFalse(evaluate_condition(cond, "root:root 777", "", 0))

        # None pattern fallback
        cond_none = {"type": "stdout_regex_match", "pattern": None}
        self.assertFalse(evaluate_condition(cond_none, "output", "", 0))

    def test_stdout_is_numeric_greater_than(self):
        cond = {"type": "stdout_is_numeric_greater_than", "value": 100}
        self.assertTrue(evaluate_condition(cond, "200MB", "", 0))
        self.assertFalse(evaluate_condition(cond, "50MB", "", 0))
        self.assertFalse(evaluate_condition(cond, "non_numeric", "", 0))

    def test_unknown_condition_type(self):
        cond = {"type": "unknown_invalid_type"}
        self.assertFalse(evaluate_condition(cond, "output", "", 0))


if __name__ == "__main__":
    unittest.main()
