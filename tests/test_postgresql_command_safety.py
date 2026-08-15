#!/usr/bin/env python3
"""
Unit tests for PostgreSQL command safety and zero execution errors (PSL ONLY).
"""

import json
import os
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_DIR = os.path.join(REPO_ROOT, "rules")


class TestPostgreSQLCommandSafety(unittest.TestCase):

    def test_no_raw_sql_in_postgresql_rules(self):
        """Ensure test_procedure in PostgreSQL rules does not contain raw SQL without psql wrapper."""
        for rf in ["postgresql_16.json", "postgresql_17.json", "postgresql_18.json"]:
            rpath = os.path.join(RULES_DIR, rf)
            self.assertTrue(os.path.exists(rpath))
            with open(rpath, "r", encoding="utf-8") as f:
                rules = json.load(f)

            for r in rules:
                tp = r.get("test_procedure", "").strip()
                if tp.startswith("SELECT ") or tp.startswith("SHOW "):
                    self.assertIn("psql", tp, f"Rule {r.get('number')} in {rf} contains raw SQL without psql: {tp}")
                self.assertNotIn("|| SHOW ", tp, f"Rule {r.get('number')} in {rf} contains invalid trailing || SHOW: {tp}")
                self.assertNotIn("|| SELECT ", tp, f"Rule {r.get('number')} in {rf} contains invalid trailing || SELECT: {tp}")


if __name__ == "__main__":
    unittest.main()
