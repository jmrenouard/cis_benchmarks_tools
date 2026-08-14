#!/usr/bin/env python3
"""
Unit tests for normalized database credentials and connection options injection (PSL ONLY).
"""

import os
import unittest
from unittest.mock import MagicMock, patch

import audit_cis_mariadb_106 as mariadb_106
import audit_cis_mysql_80 as mysql_80
import audit_cis_postgresql_16 as postgresql_16


class TestCredentialInjection(unittest.TestCase):

    @patch("subprocess.run")
    def test_mysql_credential_environment_injection(self, mock_sub):
        """Test that MySQL credentials are set in environment without leaking in shell arguments."""
        mock_process = MagicMock()
        mock_process.stdout = "1\n"
        mock_process.stderr = ""
        mock_process.returncode = 0
        mock_sub.return_value = mock_process

        mysql_80.run_command(
            "mysql -e 'SELECT 1;'",
            db_user="audit_user",
            db_password="SecretPassword123!",
            db_host="127.0.0.1",
            db_port=3306
        )

        kwargs = mock_sub.call_args[1]
        env = kwargs.get("env", {})
        self.assertEqual(env.get("MYSQL_USER"), "audit_user")
        self.assertEqual(env.get("MYSQL_PWD"), "SecretPassword123!")
        self.assertEqual(env.get("MYSQL_HOST"), "127.0.0.1")
        self.assertEqual(env.get("MYSQL_TCP_PORT"), "3306")

    @patch("subprocess.run")
    def test_postgresql_credential_environment_injection(self, mock_sub):
        """Test that PostgreSQL credentials are set in PG* environment variables."""
        mock_process = MagicMock()
        mock_process.stdout = "1\n"
        mock_process.stderr = ""
        mock_process.returncode = 0
        mock_sub.return_value = mock_process

        postgresql_16.run_command(
            "psql -c 'SELECT 1;'",
            db_user="pg_auditor",
            db_password="PgSecret456!",
            db_host="localhost",
            db_port=5432,
            db_name="postgres"
        )

        kwargs = mock_sub.call_args[1]
        env = kwargs.get("env", {})
        self.assertEqual(env.get("PGUSER"), "pg_auditor")
        self.assertEqual(env.get("PGPASSWORD"), "PgSecret456!")
        self.assertEqual(env.get("PGHOST"), "localhost")
        self.assertEqual(env.get("PGPORT"), "5432")
        self.assertEqual(env.get("PGDATABASE"), "postgres")

    @patch("subprocess.run")
    def test_docker_exec_credential_injection(self, mock_sub):
        """Test that Docker exec commands include environment variables via -e flags."""
        mock_process = MagicMock()
        mock_process.stdout = "1\n"
        mock_process.stderr = ""
        mock_process.returncode = 0
        mock_sub.return_value = mock_process

        mariadb_106.run_command(
            "mariadb -e 'SELECT 1;'",
            docker_container="mariadb-test-cont",
            db_user="maria_user",
            db_password="MariaPassword789!"
        )

        called_cmd = mock_sub.call_args[0][0][2]
        self.assertIn("-e MYSQL_USER=maria_user", called_cmd)
        self.assertIn("-e MYSQL_PWD=MariaPassword789!", called_cmd)
        self.assertIn("mariadb-test-cont", called_cmd)


if __name__ == "__main__":
    unittest.main()
