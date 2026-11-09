#!/usr/bin/env python3
"""
Unit tests for normalized database credentials and connection options injection (PSL ONLY).
"""

import os
import unittest
from unittest.mock import MagicMock, patch

import audit_cis_mariadb_106 as mariadb_106
import audit_cis_mariadb_1011 as mariadb_1011
import audit_cis_mysql_80 as mysql_80, audit_cis_mysql_community_84 as mysql_c84
import audit_cis_mysql_community_97 as mysql_c97, audit_cis_mysql_enterprise_84 as mysql_e84, audit_cis_mysql_enterprise_97 as mysql_e97
import audit_cis_postgresql_16 as postgresql_16, audit_cis_postgresql_17 as pg17, audit_cis_postgresql_18 as pg18
import audit_cis_mongodb_7 as mg7, audit_cis_mongodb_8 as mg8, audit_cis_cassandra_40 as cas40, audit_cis_cassandra_41 as cas41, audit_cis_cassandra_50 as cas50


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

        called_args = mock_sub.call_args[0][0]
        called_cmd = " ".join(called_args) if isinstance(called_args, list) else str(called_args)
        self.assertIn("-e", called_args)
        self.assertIn("MYSQL_PWD", called_args)
        self.assertNotIn("MariaPassword789!", called_cmd)
        self.assertIn("mariadb-test-cont", called_cmd)
        called_env = mock_sub.call_args[1].get("env", {})
        self.assertEqual(called_env.get("MYSQL_PWD"), "MariaPassword789!")

    @patch("subprocess.run")
    def test_all_mariadb_mysql_engines_docker_password_not_in_argv(self, mock_sub):
        """Finding 1: verify docker exec fallback across all MariaDB and MySQL engines never exposes db_password in argv."""
        mock_process = MagicMock()
        mock_process.stdout = "1\n"
        mock_process.stderr = ""
        mock_process.returncode = 0
        mock_sub.return_value = mock_process

        secret = "S3cr3t_P@ssw0rd!_WithSpaces"
        engines = [
            (mariadb_106, True), (mariadb_1011, True), (mysql_80, False),
            (mysql_c84, False), (mysql_c97, False), (mysql_e84, False), (mysql_e97, False),
            (postgresql_16, False), (pg17, False), (pg18, False),
            (mg7, False), (mg8, False), (cas40, False), (cas41, False), (cas50, False),
        ]
        for engine, sudo in engines:
            with self.subTest(engine=engine.__name__):
                mock_sub.reset_mock()
                engine.run_command("status", docker_container="test-cont", db_password=secret, sudo=sudo)
                called_args = mock_sub.call_args[0][0]
                called_cmd = " ".join(called_args) if isinstance(called_args, list) else str(called_args)
                self.assertNotIn(secret, called_cmd, f"{engine.__name__} leaked password in process args: {called_cmd}")
                self.assertNotIn(f"MYSQL_PWD={secret}", called_cmd)
                self.assertNotIn(f"PGPASSWORD={secret}", called_cmd)
                called_env = mock_sub.call_args[1].get("env", {})
                self.assertEqual(called_env.get("MYSQL_PWD"), secret, f"{engine.__name__} failed to pass MYSQL_PWD in env")


if __name__ == "__main__":
    unittest.main()
