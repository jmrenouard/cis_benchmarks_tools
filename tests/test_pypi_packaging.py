"""Unit tests verifying PyPI packaging configuration and pyproject.toml."""

from __future__ import annotations

import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PYPROJECT_PATH = ROOT / "pyproject.toml"
MANIFEST_PATH = ROOT / "MANIFEST.in"
VERSION_PATH = ROOT / "VERSION"


class TestPyPIPackaging(unittest.TestCase):
    """Validate PyPI packaging configuration for CIS Benchmarks Tools Suite."""

    def test_pyproject_toml_exists_and_declares_core_metadata(self) -> None:
        """Verify pyproject.toml exists and declares standard metadata and zero external runtime dependencies."""
        self.assertTrue(PYPROJECT_PATH.is_file(), "pyproject.toml must exist at repo root")
        content = PYPROJECT_PATH.read_text(encoding="utf-8")

        self.assertIn('name = "cis-benchmarks-tools"', content)
        self.assertIn('dependencies = []', content)
        self.assertIn('requires-python = ">=3.8"', content)
        self.assertIn('build-backend = "setuptools.build_meta"', content)
        self.assertIn('audit-cis = "audit_cis:main"', content)
        self.assertIn('audit_cis = "audit_cis:main"', content)

    def test_manifest_in_includes_rules_templates_and_licenses(self) -> None:
        """Verify MANIFEST.in ensures distribution of JSON rules, templates, and licenses."""
        self.assertTrue(MANIFEST_PATH.is_file(), "MANIFEST.in must exist at repo root")
        content = MANIFEST_PATH.read_text(encoding="utf-8")

        self.assertIn("rules *.json", content)
        self.assertIn("templates *.html", content)
        self.assertIn("LICENSE", content)
        self.assertIn("VERSION", content)

    def test_version_format_and_dynamic_sync(self) -> None:
        """Verify VERSION file contains a valid semantic version string."""
        self.assertTrue(VERSION_PATH.is_file(), "VERSION file must exist")
        version = VERSION_PATH.read_text(encoding="utf-8").strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+$", f"Invalid semantic version: {version}")

    def test_all_packaged_modules_exist_in_repository(self) -> None:
        """Verify that every py-module declared in pyproject.toml exists as a python file."""
        content = PYPROJECT_PATH.read_text(encoding="utf-8")
        modules_block_match = re.search(r'py-modules = \[(.*?)\]', content, re.DOTALL)
        self.assertIsNotNone(modules_block_match, "py-modules list must be defined in pyproject.toml")

        modules = re.findall(r'"([a-zA-Z0-9_]+)"', modules_block_match.group(1))
        self.assertGreater(len(modules), 15, "Expected at least 15 core modules in pyproject.toml")

        for mod in modules:
            py_file = ROOT / f"{mod}.py"
            self.assertTrue(
                py_file.is_file(),
                f"Declared module {mod}.py does not exist in repository root: {py_file}",
            )


if __name__ == "__main__":
    unittest.main()
