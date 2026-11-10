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
            "docker-publish.yml",
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
        """Verify release.yml triggers on published release, generates SHA256SUMS.txt and attaches standalone audit bundle."""
        rel_path = WORKFLOWS_DIR / "release.yml"
        content = rel_path.read_text(encoding="utf-8")
        self.assertIn("release:", content)
        self.assertIn("types: [published]", content)
        self.assertIn("workflow_dispatch:", content)
        self.assertIn("pre_commit_checks.py", content)
        self.assertIn("sha256sum * > SHA256SUMS.txt", content)
        self.assertIn("softprops/action-gh-release@", content)
        self.assertNotIn("tags:", content.split("jobs:")[0])
        self.assertNotIn("push:", content.split("jobs:")[0])

    def test_commit_testing_workflows_trigger_on_all_pushes_and_pull_requests(self) -> None:
        """Verify ci.yml and unit-tests.yml run on all pushed commits and pull requests."""
        for wf_name in ("ci.yml", "unit-tests.yml"):
            wf_path = WORKFLOWS_DIR / wf_name
            content = wf_path.read_text(encoding="utf-8")
            self.assertIn("push:", content)
            self.assertIn("pull_request:", content)
            self.assertIn("actions/checkout@", content)
            self.assertIn("actions/setup-python@", content)

    def test_ci_and_unit_tests_python_matrix_excludes_eol_versions(self) -> None:
        """Verify CI workflows exclude EOL Python versions (<= 3.9) and test active versions (3.10-3.13)."""
        for wf_name in ("ci.yml", "unit-tests.yml"):
            wf_path = WORKFLOWS_DIR / wf_name
            content = wf_path.read_text(encoding="utf-8")
            self.assertNotIn('"3.9"', content, f"{wf_name} must not test EOL Python 3.9 on modern runners")
            self.assertNotIn('"3.8"', content, f"{wf_name} must not test EOL Python 3.8 on modern runners")
            for active_ver in ("3.10", "3.11", "3.12", "3.13"):
                self.assertIn(
                    f'"{active_ver}"',
                    content,
                    f"{wf_name} must include active Python version {active_ver}",
                )

    def test_pypi_publish_workflow_configured_correctly(self) -> None:
        """Verify pypi-publish.yml builds distribution and publishes with token secret."""
        pypi_path = WORKFLOWS_DIR / "pypi-publish.yml"
        self.assertTrue(pypi_path.is_file(), "pypi-publish.yml must exist")
        content = pypi_path.read_text(encoding="utf-8")
        self.assertIn("pypa/gh-action-pypi-publish@", content)
        self.assertIn("secrets.PYPI_API_TOKEN", content)
        self.assertIn("secrets.PIPY_API_TOKEN", content)
        self.assertIn("secrets.PYPI_TOKEN", content)
        self.assertIn("pypi_preflight", content)
        self.assertIn("python -m build", content)
        self.assertIn("twine check --strict", content)
        self.assertIn("types: [published]", content)
        self.assertIn("workflow_dispatch:", content)
        self.assertIn("cancel-in-progress: false", content)
        self.assertNotIn("tags:", content, "pypi-publish.yml must not trigger on tag pushes (push: tags: removed)")
        self.assertNotIn("push:", content, "pypi-publish.yml must not trigger on push events")

    def test_docker_publish_workflow_configured_correctly(self) -> None:
        """Verify docker-publish.yml triggers on published release, gates :latest on prereleases, and publishes to Docker Hub."""
        c = (WORKFLOWS_DIR / "docker-publish.yml").read_text(encoding="utf-8")
        self.assertIn("docker/build-push-action@", c)
        self.assertIn("secrets.DOCKERHUB_USERNAME", c)
        self.assertIn("IS_PRERELEASE", c)
        self.assertNotIn("tags:", c.split("jobs:")[0])


if __name__ == "__main__":
    unittest.main()
