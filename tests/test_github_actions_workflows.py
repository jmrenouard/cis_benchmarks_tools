"""Unit tests verifying all GitHub Actions workflows and Dependabot configuration."""

from __future__ import annotations

import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOWS_DIR = ROOT / ".github" / "workflows"


class TestGitHubActionsWorkflows(unittest.TestCase):
    """Validate GitHub Actions CI/CD workflows for CIS Benchmarks Tools Suite."""

    def test_all_required_workflows_exist(self) -> None:
        """Verify that ci, unit-tests, lint, security, and release workflows exist."""
        expected_workflows = [
            "ci.yml",
            "unit-tests.yml",
            "lint.yml",
            "security.yml",
            "release.yml",
            "pypi-publish.yml",
        ]
        for wf_name in expected_workflows:
            wf_path = WORKFLOWS_DIR / wf_name
            self.assertTrue(
                wf_path.is_file(),
                f"Missing required GitHub Actions workflow: .github/workflows/{wf_name}",
            )

    def test_dependabot_config_exists(self) -> None:
        """Verify .github/dependabot.yml configures github-actions and docker ecosystems."""
        dependabot_path = ROOT / ".github" / "dependabot.yml"
        self.assertTrue(dependabot_path.is_file(), ".github/dependabot.yml must exist")

        content = dependabot_path.read_text(encoding="utf-8")
        self.assertIn("version: 2", content)
        self.assertIn("github-actions", content)
        self.assertIn("docker", content)

    def test_lint_workflow_checks_ruff_flake8_mypy_and_psl(self) -> None:
        """Verify lint.yml runs ruff, flake8, mypy, and pre_commit_checks.py."""
        lint_path = WORKFLOWS_DIR / "lint.yml"
        content = lint_path.read_text(encoding="utf-8")
        self.assertIn("push:", content)
        self.assertIn("pull_request:", content)
        self.assertIn("workflow_dispatch:", content)
        self.assertIn("actions/checkout@v4", content)
        self.assertIn("actions/setup-python@v5", content)
        self.assertIn("ruff check", content)
        self.assertIn("flake8", content)
        self.assertIn("mypy", content)
        self.assertIn("pre_commit_checks.py", content)

    def test_security_workflow_runs_bandit_and_pip_audit(self) -> None:
        """Verify security.yml runs bandit static analysis and pip-audit."""
        sec_path = WORKFLOWS_DIR / "security.yml"
        content = sec_path.read_text(encoding="utf-8")
        self.assertIn("push:", content)
        self.assertIn("pull_request:", content)
        self.assertIn("schedule:", content)
        self.assertIn("workflow_dispatch:", content)
        self.assertIn("bandit", content)
        self.assertIn("pip-audit", content)

    def test_release_workflow_bundles_and_attaches_artifacts(self) -> None:
        """Verify release.yml triggers on v* tags and attaches standalone audit bundle."""
        rel_path = WORKFLOWS_DIR / "release.yml"
        content = rel_path.read_text(encoding="utf-8")
        self.assertIn("tags:", content)
        self.assertIn("v*", content)
        self.assertIn("pre_commit_checks.py", content)
        self.assertIn("softprops/action-gh-release@", content)

    def test_commit_testing_workflows_trigger_on_all_pushes_and_pull_requests(self) -> None:
        """Verify ci.yml and unit-tests.yml run on all pushed commits and pull requests."""
        for wf_name in ("ci.yml", "unit-tests.yml"):
            wf_path = WORKFLOWS_DIR / wf_name
            content = wf_path.read_text(encoding="utf-8")
            self.assertIn("push:", content)
            self.assertIn("pull_request:", content)
            self.assertIn("actions/checkout@", content)
            self.assertIn("actions/setup-python@", content)

    def test_pypi_publish_workflow_configured_correctly(self) -> None:
        """Verify pypi-publish.yml builds distribution and publishes with token secret."""
        pypi_path = WORKFLOWS_DIR / "pypi-publish.yml"
        self.assertTrue(pypi_path.is_file(), "pypi-publish.yml must exist")
        content = pypi_path.read_text(encoding="utf-8")
        self.assertIn("pypa/gh-action-pypi-publish@", content)
        self.assertIn("secrets.PYPI_API_TOKEN", content)
        self.assertIn("secrets.PYPI_TOKEN", content)
        self.assertIn("python -m build", content)


if __name__ == "__main__":
    unittest.main()
