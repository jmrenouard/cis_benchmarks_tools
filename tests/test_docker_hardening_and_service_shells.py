#!/usr/bin/env python3
"""
Unit tests for Dockerfile hardening, service account shell validation, and Makefile orchestration (PSL ONLY).
"""

import os
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestDockerHardeningAndServiceShells(unittest.TestCase):

    def setUp(self):
        self.docker_dir = os.path.join(REPO_ROOT, "docker")
        self.scripts_dir = os.path.join(REPO_ROOT, "scripts")
        self.makefile_path = os.path.join(REPO_ROOT, "Makefile")

    def test_mariadb_and_mysql_dockerfiles_contain_nologin_hardening(self):
        """Ensure all MariaDB and MySQL Dockerfiles contain usermod -s /sbin/nologin mysql."""
        target_dockerfiles = [
            "Dockerfile_mariadb106",
            "Dockerfile_mariadb1011",
            "Dockerfile_mysql80",
            "Dockerfile_mysql_community_84",
            "Dockerfile_mysql_enterprise_84",
            "Dockerfile_mysql_community_97",
            "Dockerfile_mysql_enterprise_97",
        ]

        for df_name in target_dockerfiles:
            df_path = os.path.join(self.docker_dir, df_name)
            self.assertTrue(os.path.exists(df_path), f"Missing Dockerfile: {df_name}")
            with open(df_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("usermod -s /sbin/nologin mysql", content, f"{df_name} missing usermod -s /sbin/nologin mysql hardening")

    def test_startup_scripts_contain_nologin_hardening(self):
        """Ensure start_mariadb.sh and start_mysql.sh contain usermod -s /sbin/nologin mysql."""
        for script_name in ["start_mariadb.sh", "start_mysql.sh"]:
            sp_path = os.path.join(self.scripts_dir, script_name)
            self.assertTrue(os.path.exists(sp_path), f"Missing startup script: {script_name}")
            with open(sp_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("usermod -s /sbin/nologin mysql", content, f"{script_name} missing usermod -s /sbin/nologin mysql hardening")

    def test_makefile_audit_and_rules_copy_synchronization(self):
        """Ensure Makefile copies templates and rules into container and passes -o flag to audit targets."""
        with open(self.makefile_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("audit-mariadb106:", content)
        self.assertIn("-o /datas/$(MARIADB106_REPORT)", content)
        self.assertIn("audit-mariadb1011:", content)
        self.assertIn("-o /datas/$(MARIADB1011_REPORT)", content)


if __name__ == "__main__":
    unittest.main()
