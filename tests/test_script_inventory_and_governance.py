#!/usr/bin/env python3
"""Script inventory governance tests (100% PSL ONLY). Verifies Finding 12 / IMP-005."""
import os
import py_compile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
ESSENTIAL_SCRIPTS = {
    "bundle_audit_cis.py", "pre_commit_checks.py", "pre-commit.sh",
    "download_cis_benchmarks.py", "verify_benchmarks_and_reports.py",
    "clean_ssh_warnings_from_reports.py", "run_e2e_tests.py", "analyze_e2e_reports.py",
    "start_mariadb.sh", "start_mysql.sh", "start_postgresql.sh",
    "start_mongodb.sh", "start_cassandra.sh"
}


class TestScriptInventoryAndGovernance(unittest.TestCase):
    def test_scripts_directory_contains_only_whitelisted_essential_tools(self):
        current_files = {f for f in os.listdir(SCRIPTS_DIR) if os.path.isfile(os.path.join(SCRIPTS_DIR, f))}
        self.assertEqual(current_files - ESSENTIAL_SCRIPTS, set())
        self.assertEqual(current_files, ESSENTIAL_SCRIPTS)

    def test_essential_scripts_exist_and_compile(self):
        for name in ESSENTIAL_SCRIPTS:
            path = os.path.join(SCRIPTS_DIR, name)
            self.assertTrue(os.path.exists(path))
            self.assertGreater(os.path.getsize(path), 0)
            if name.endswith(".py"):
                py_compile.compile(path, doraise=True)

    def test_archived_scripts_relocated(self):
        archive_dir = os.path.join(REPO_ROOT, "archive", "scripts")
        self.assertTrue(os.path.isdir(archive_dir))
        files = [f for f in os.listdir(archive_dir) if os.path.isfile(os.path.join(archive_dir, f))]
        self.assertEqual(len(files), 65)


if __name__ == "__main__":
    unittest.main()
