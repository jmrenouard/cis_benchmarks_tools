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


    def test_entrypoint_main_callable_in_audit_cis(self) -> None:
        """Verify audit_cis module defines a callable main() entrypoint."""
        import audit_cis
        self.assertTrue(hasattr(audit_cis, "main"), "audit_cis must expose a main function")
        self.assertTrue(callable(getattr(audit_cis, "main")), "audit_cis.main must be callable")

    def test_audit_cis_version_matches_version_file(self) -> None:
        """Verify audit_cis.__version__ matches the string in VERSION file."""
        import audit_cis
        version = VERSION_PATH.read_text(encoding="utf-8").strip()
        self.assertEqual(audit_cis.__version__, version, "audit_cis.__version__ must match VERSION")

    def test_wheel_archive_contains_required_modules_and_entrypoints(self) -> None:
        """If distribution wheels are present in dist/, verify their archive layout."""
        import zipfile
        dist_dir = ROOT / "dist"
        if not dist_dir.is_dir():
            return
        wheels = list(dist_dir.glob("*.whl"))
        if not wheels:
            return

        for whl in wheels:
            with zipfile.ZipFile(whl, "r") as z:
                names = z.namelist()
                self.assertIn("audit_cis.py", names, f"{whl.name} missing audit_cis.py")
                entry_points = [n for n in names if n.endswith("entry_points.txt")]
                self.assertTrue(len(entry_points) > 0, f"{whl.name} missing entry_points.txt")
                ep_content = z.read(entry_points[0]).decode("utf-8")
                self.assertIn("audit-cis = audit_cis:main", ep_content)
                self.assertIn("audit_cis = audit_cis:main", ep_content)


if __name__ == "__main__":
    unittest.main()
