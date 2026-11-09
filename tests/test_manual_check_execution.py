#!/usr/bin/env python3
"""
Unit tests for Manual control single execution across MariaDB and MySQL engines (PSL ONLY).
Finding 2: Ensures perform_checks executes Manual controls with shell commands exactly once.
"""

import unittest
from unittest.mock import patch

import audit_cis_mariadb_106 as m106
import audit_cis_mariadb_1011 as m1011
import audit_cis_mysql_80 as my80, audit_cis_mysql_community_84 as myc84, audit_cis_mysql_community_97 as myc97
import audit_cis_mysql_enterprise_84 as mye84, audit_cis_mysql_enterprise_97 as mye97


class TestManualCheckExecution(unittest.TestCase):
    """Verify single execution of Manual controls across all MariaDB and MySQL engines."""

    def setUp(self):
        self.engines = [("mariadb_106", m106), ("mariadb_1011", m1011), ("mysql_80", my80),
                        ("mysql_community_84", myc84), ("mysql_community_97", myc97),
                        ("mysql_enterprise_84", mye84), ("mysql_enterprise_97", mye97)]

    def _run_rule(self, mod, tp):
        rule = [{"category": "1. Setup", "number": "1.1", "name": "Manual", "type": "Manual", "test_procedure": tp}]
        return mod.perform_checks(rule)["1. Setup"][0]

    def test_manual_control_single_execution(self):
        """Assert Manual controls with shell commands call run_command exactly once."""
        for name, mod in self.engines:
            with self.subTest(engine=name):
                with patch.object(mod, "run_command", return_value=("10.6-OK", "", 0)) as m:
                    res = self._run_rule(mod, "mysql -e 'SELECT 1;'")
                    self.assertEqual(m.call_count, 1, f"{name} called run_command {m.call_count} times")
                    self.assertEqual(res["status"], "Manual")
                    self.assertIn("10.6-OK", res["output"])

    def test_manual_control_empty_output(self):
        """Assert Manual controls with empty output still run once and format output."""
        for name, mod in self.engines:
            with self.subTest(engine=name):
                with patch.object(mod, "run_command", return_value=("", "", 0)) as m:
                    res = self._run_rule(mod, "mysql -e 'SELECT 1;'")
                    self.assertEqual(m.call_count, 1)
                    self.assertIn("(Aucune sortie retournée)", res["output"])

    def test_manual_control_procedural_text_zero_calls(self):
        """Assert procedural text test_procedures do not trigger run_command."""
        for name, mod in self.engines:
            with self.subTest(engine=name):
                with patch.object(mod, "run_command") as m:
                    res = self._run_rule(mod, "Consulter la documentation manuellement")
                    self.assertEqual(m.call_count, 0)
                    self.assertEqual(res["status"], "Manual")


if __name__ == "__main__":
    unittest.main()
