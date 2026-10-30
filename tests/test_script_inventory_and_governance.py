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
        """Assert scripts/ entries match whitelist exactly (excluding ephemeral __pycache__)."""
        all_entries = {e for e in os.listdir(SCRIPTS_DIR) if e != "__pycache__"}
        self.assertEqual(all_entries - ESSENTIAL_SCRIPTS, set())
        self.assertEqual(all_entries, ESSENTIAL_SCRIPTS)

    def test_scripts_directory_has_no_unexpected_subdirectories(self):
        """Ensure no unauthorized subdirectories exist in scripts/ (only __pycache__ permitted)."""
        subdirs = {
            d for d in os.listdir(SCRIPTS_DIR)
            if os.path.isdir(os.path.join(SCRIPTS_DIR, d)) and d != "__pycache__"
        }
        self.assertEqual(subdirs, set(), f"Unexpected subdirectories in scripts/: {subdirs}")

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

    def test_security_workflow_excludes_archive_from_bandit(self):
        """Ensure .github/workflows/security.yml excludes ./archive in Bandit SAST scan."""
        workflow_path = os.path.join(REPO_ROOT, ".github", "workflows", "security.yml")
        self.assertTrue(os.path.isfile(workflow_path), "security.yml workflow file must exist")
        with open(workflow_path, "r", encoding="utf-8") as f:
            content = f.read()

        bandit_lines = [
            line.strip()
            for line in content.splitlines()
            if "bandit" in line and "-x" in line
        ]
        self.assertTrue(len(bandit_lines) > 0, "Bandit command line with -x flag not found in security.yml")
        for line in bandit_lines:
            self.assertIn(
                "./archive",
                line,
                f"Bandit command line in security.yml must exclude './archive': {line}",
            )

    def test_pre_commit_checks_anchors_archive_path(self):
        """Ensure scripts/pre_commit_checks.py avoids loose 'archive' substring matches."""
        pre_commit_path = os.path.join(SCRIPTS_DIR, "pre_commit_checks.py")
        self.assertTrue(os.path.isfile(pre_commit_path))
        with open(pre_commit_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertTrue(
            'norm_path.startswith("archive/")' in content or 'norm_py.startswith("archive/")' in content,
            "pre_commit_checks.py must anchor archive check with startswith('archive/')",
        )

    def test_pre_commit_syntax_exclusion_logic(self):
        """Verify pre-commit checks skip archive/ and caches without over-matching active files."""
        import sys
        if SCRIPTS_DIR not in sys.path:
            sys.path.insert(0, SCRIPTS_DIR)
        from pre_commit_checks import should_skip_syntax_validation

        # Positive cases: must be skipped
        self.assertTrue(should_skip_syntax_validation("archive/scripts/generate_missing_reports.py"))
        self.assertTrue(should_skip_syntax_validation("archive\\scripts\\generate_missing_reports.py"))
        self.assertTrue(should_skip_syntax_validation("./archive/scripts/tool.py"))
        self.assertTrue(should_skip_syntax_validation(".agents/teamwork/plan.py"))
        self.assertTrue(should_skip_syntax_validation(".ruff_cache/content.py"))

        # Negative cases: must NOT be skipped (active code and tests)
        self.assertFalse(should_skip_syntax_validation("tests/test_archive_inventory.py"))
        self.assertFalse(should_skip_syntax_validation("tests\\test_archive_inventory.py"))
        self.assertFalse(should_skip_syntax_validation("audit_cis_cassandra_311_archive.py"))
        self.assertFalse(should_skip_syntax_validation("scripts/archive_reports.py"))
        self.assertFalse(should_skip_syntax_validation("tests/test_agents.py"))


if __name__ == "__main__":
    unittest.main()

