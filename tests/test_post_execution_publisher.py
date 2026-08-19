#!/usr/bin/env python3
"""
Unit test suite for post_execution_publisher.py (Python PSL ONLY).
"""

import os
import tempfile
import unittest

from post_execution_publisher import AuditReportPublisher, atomic_write_text
from temporal_metadata import TemporalAuditMetadata


class TestPostExecutionPublisher(unittest.TestCase):
    """Test suite for crash-resilient post-execution report publisher."""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def test_atomic_write_text(self):
        """Test atomic file writing creates file with expected content."""
        target_path = os.path.join(self.tmp_dir, "test_file.txt")
        written = atomic_write_text(target_path, "Hello Atomic World!")
        self.assertEqual(written, target_path)
        self.assertTrue(os.path.exists(target_path))
        with open(target_path, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "Hello Atomic World!")

    def test_publisher_destination_resolution(self):
        """Test resolving destination report paths."""
        publisher = AuditReportPublisher(target_name="mariadb_106", output_dir=self.tmp_dir)
        html_dest = publisher.resolve_destination("html")
        self.assertTrue(html_dest.endswith("rapport_cis_mariadb_106.html"))
        self.assertEqual(os.path.dirname(html_dest), self.tmp_dir)

    def test_guaranteed_publishing_on_success(self):
        """Test report publication during a normal successful audit run."""
        publisher = AuditReportPublisher(target_name="mariadb_106", output_dir=self.tmp_dir, formats=["html", "json"])

        def dummy_audit():
            return {"Cat 1": [{"number": "1.1", "name": "Check", "status": "Pass"}]}, 100.0, {"Cat 1": {"score": 100.0}}

        exported_calls = []
        def dummy_export(results, overall_score, categories_scores, target_name, filename, fmt, **kwargs):
            exported_calls.append(filename)
            atomic_write_text(filename, f"Dummy {fmt} content")

        success, exc, published = publisher.execute_with_guaranteed_publishing(dummy_audit, dummy_export)

        self.assertTrue(success)
        self.assertIsNone(exc)
        self.assertEqual(len(published), 2)
        for p in published.values():
            self.assertTrue(os.path.exists(p))

    def test_guaranteed_publishing_on_exception(self):
        """Test that reports are STILL generated when audit_func raises an unhandled exception."""
        publisher = AuditReportPublisher(target_name="mariadb_106", output_dir=self.tmp_dir, formats=["html", "json"])

        def failing_audit():
            raise RuntimeError("Database connection suddenly dropped")

        exported_calls = []
        def dummy_export(results, overall_score, categories_scores, target_name, filename, fmt, **kwargs):
            exported_calls.append(filename)
            atomic_write_text(filename, f"Emergency report for {fmt}: {results}")

        success, exc, published = publisher.execute_with_guaranteed_publishing(failing_audit, dummy_export)

        self.assertFalse(success)
        self.assertIsInstance(exc, RuntimeError)
        self.assertEqual(len(published), 2)
        for p in published.values():
            self.assertTrue(os.path.exists(p))
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("Emergency report", content)


if __name__ == "__main__":
    unittest.main()
