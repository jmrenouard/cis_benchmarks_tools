#!/usr/bin/env python3
"""
Unit Test Suite for Rule Exclusion Engine (--exclude-rules / --skip-rule).
100% Python Standard Library (PSL ONLY).
"""

import os
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def filter_excluded_checks(rules_data, exclude_rules=None):
    """Filter out excluded control IDs or categories from rule list (PSL ONLY)."""
    if not exclude_rules:
        return rules_data
    if isinstance(exclude_rules, str):
        exclude_set = {r.strip() for r in exclude_rules.split(",") if r.strip()}
    else:
        exclude_set = set(exclude_rules)

    filtered = []
    for check in rules_data:
        num = str(check.get("number", "")).strip()
        cat = str(check.get("category", "")).strip()
        if num in exclude_set or cat in exclude_set:
            continue
        filtered.append(check)
    return filtered


class TestRuleExclusionEngine(unittest.TestCase):
    """Unit tests for rule exclusion filtering logic."""

    def setUp(self):
        self.sample_rules = [
            {"number": "1.1", "name": "Rule 1.1", "category": "1. Operating System"},
            {"number": "1.2", "name": "Rule 1.2", "category": "1. Operating System"},
            {"number": "2.1", "name": "Rule 2.1", "category": "2. Parameter Settings"},
            {"number": "3.1", "name": "Rule 3.1", "category": "3. Network Security"}
        ]

    def test_no_exclusions(self):
        res = filter_excluded_checks(self.sample_rules, None)
        self.assertEqual(len(res), 4)

    def test_exclude_single_rule_string(self):
        res = filter_excluded_checks(self.sample_rules, "1.1")
        self.assertEqual(len(res), 3)
        nums = [r["number"] for r in res]
        self.assertNotIn("1.1", nums)
        self.assertIn("1.2", nums)

    def test_exclude_multiple_rules_comma_string(self):
        res = filter_excluded_checks(self.sample_rules, "1.1, 2.1")
        self.assertEqual(len(res), 2)
        nums = [r["number"] for r in res]
        self.assertNotIn("1.1", nums)
        self.assertNotIn("2.1", nums)

    def test_exclude_category_string(self):
        res = filter_excluded_checks(self.sample_rules, "1. Operating System")
        self.assertEqual(len(res), 2)
        nums = [r["number"] for r in res]
        self.assertNotIn("1.1", nums)
        self.assertNotIn("1.2", nums)
        self.assertIn("2.1", nums)

    def test_exclude_set_input(self):
        res = filter_excluded_checks(self.sample_rules, {"1.2", "3.1"})
        self.assertEqual(len(res), 2)
        nums = [r["number"] for r in res]
        self.assertNotIn("1.2", nums)
        self.assertNotIn("3.1", nums)


if __name__ == "__main__":
    unittest.main()
