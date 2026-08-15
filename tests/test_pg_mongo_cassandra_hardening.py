#!/usr/bin/env python3
"""
Unit tests for PostgreSQL, MongoDB, and Cassandra Docker testing configurations and hardening scripts (PSL ONLY).
"""

import os
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")


class TestPgMongoCassandraHardening(unittest.TestCase):

    def test_postgresql_startup_script_hardening(self):
        """Ensure start_postgresql.sh configures log_error_verbosity, %t in log_line_prefix, and psql history disable."""
        spath = os.path.join(SCRIPTS_DIR, "start_postgresql.sh")
        self.assertTrue(os.path.exists(spath))
        with open(spath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("log_error_verbosity = 'verbose'", content)
        self.assertIn("%t", content)
        self.assertIn(".psql_history", content)

    def test_mongodb_startup_script_hardening(self):
        """Ensure start_mongodb.sh configures authorization, TLS, and audit logging."""
        spath = os.path.join(SCRIPTS_DIR, "start_mongodb.sh")
        self.assertTrue(os.path.exists(spath))
        with open(spath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("authorization: enabled", content)
        self.assertIn("mode: requireTLS", content)
        self.assertIn("FIPSMode: true", content)
        self.assertIn("auditLog:", content)

    def test_cassandra_startup_script_hardening(self):
        """Ensure start_cassandra.sh configures PasswordAuthenticator and system.log."""
        spath = os.path.join(SCRIPTS_DIR, "start_cassandra.sh")
        self.assertTrue(os.path.exists(spath))
        with open(spath, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("PasswordAuthenticator", content)
        self.assertIn("system.log", content)


if __name__ == "__main__":
    unittest.main()
