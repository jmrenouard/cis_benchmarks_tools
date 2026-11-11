"""Unit tests verifying Docker packaging, security standards, and publishing workflow."""

from __future__ import annotations

import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCKERFILE = (ROOT / "Dockerfile").read_text(encoding="utf-8")
DOCKERIGNORE = (ROOT / ".dockerignore").read_text(encoding="utf-8")
WORKFLOW = (ROOT / ".github" / "workflows" / "docker-publish.yml").read_text(encoding="utf-8")


class TestDockerPackagingAndWorkflow(unittest.TestCase):
    """Validate Docker packaging and publishing workflow for CIS Benchmarks Tools."""

    def test_dockerfile_exists_and_uses_pinned_slim_base(self) -> None:
        self.assertTrue((ROOT / "Dockerfile").is_file())
        self.assertIn("FROM python:3.12-slim", DOCKERFILE)
        self.assertNotIn("FROM python:latest", DOCKERFILE)

    def test_dockerfile_enforces_non_root_user(self) -> None:
        for s in ("groupadd -g 10001 cisgroup", "useradd -u 10001 -g cisgroup", "USER cisuser"):
            self.assertIn(s, DOCKERFILE)
        matches = re.findall(r"USER\s+([a-zA-Z0-9_-]+)", DOCKERFILE)
        self.assertEqual(matches[-1], "cisuser")

    def test_dockerfile_adheres_to_psl_zero_dependencies(self) -> None:
        self.assertNotIn("pip install", DOCKERFILE)
        self.assertNotIn("apt-get install", DOCKERFILE)

    def test_dockerfile_working_directory_and_exec_entrypoint(self) -> None:
        for s in ("WORKDIR /app", "ENTRYPOINT", "audit_cis.py", 'CMD ["--help"]', "VOLUME"):
            self.assertIn(s, DOCKERFILE)

    def test_dockerfile_copies_data_rules_and_templates(self) -> None:
        for s in ("rules/ ./rules/", "templates/ ./templates/", "VERSION"):
            self.assertIn(s, DOCKERFILE)

    def test_dockerfile_healthcheck_defined(self) -> None:
        self.assertIn("HEALTHCHECK", DOCKERFILE)
        self.assertIn("python3 audit_cis.py --version", DOCKERFILE)

    def test_dockerignore_excludes_development_and_temporary_artifacts(self) -> None:
        self.assertTrue((ROOT / ".dockerignore").is_file())
        for pat in (".git", ".agents", "tests", "docker", "build", "dist", ".venv", "__pycache__"):
            self.assertIn(pat, DOCKERIGNORE)

    def test_docker_publish_workflow_triggers_isolation(self) -> None:
        self.assertTrue((ROOT / ".github" / "workflows" / "docker-publish.yml").is_file())
        on_b = WORKFLOW.split("jobs:")[0]
        self.assertIn("types: [published]", on_b)
        self.assertIn("workflow_dispatch:", on_b)
        self.assertNotIn("tags:", on_b)
        self.assertNotIn("push:", on_b)

    def test_docker_publish_workflow_targets_dockerhub_and_secrets(self) -> None:
        for s in (
            "jmrenouard/cis-benchmarks-tools",
            "DOCKERHUB_USERNAME",
            "DOCKER_USER_LOGIN",
            "DOCKERHUB_TOKEN",
            "DOCKER_USER_PASSWORD",
            "docker_preflight",
            "org.opencontainers.image.licenses",
            "com.cis-benchmarks-tools.release-notes",
        ):
            self.assertIn(s, WORKFLOW)

    def test_docker_publish_workflow_multiplatform_build(self) -> None:
        for s in ("platforms: linux/amd64,linux/arm64", "setup-qemu", "setup-buildx", "build-push-action@v6"):
            self.assertIn(s, WORKFLOW)


if __name__ == "__main__":
    unittest.main()
