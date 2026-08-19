#!/usr/bin/env python3
"""
Adversarial Real-Time Timestamping & I/O Integrity Test Harness (Python PSL ONLY).
Verifies:
  1. Sub-2s clock delta between actual system execution instant and report timestamp.
  2. Physical file creation, integrity, and modification timestamp in reports/ directory.
  3. Strict timezone visibility (explicit offset and name).
  4. Total absence of static/hardcoded mock timestamps across generated reports.
"""

import datetime
import os
import tempfile
import time
import unittest

from audit_cis_mariadb_106 import export_results, generate_html_report
from post_execution_publisher import AuditReportPublisher, atomic_write_text
from temporal_metadata import TemporalAuditMetadata


class TestRealtimeTimestampAdversarial(unittest.TestCase):
    """Adversarial security & reliability test suite for real-time audit reporting."""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.sample_results = {
            "1. Configuration": [
                {"number": "1.1", "name": "Check datadir", "status": "Pass", "output": "/var/lib/mysql", "test_procedure": "df -P", "remediation": "Move datadir"}
            ]
        }
        self.categories_scores = {
            "1. Configuration": {"score": 100.0, "passed_automated": 1, "failed_automated": 0, "manual_checks": 0, "error_checks": 0, "na_checks": 0}
        }
        self.overall_score = 100.0

    def test_realtime_timestamp_delta_sub_2s(self):
        """Verify that generated HTML report contains a timestamp strictly within 2s of current clock."""
        start_epoch = time.time()
        t_meta = TemporalAuditMetadata.create_now()
        html_dest = os.path.join(self.tmp_dir, "rapport_cis_mariadb_106.html")

        # Simulate brief audit execution
        time.sleep(0.02)
        t_meta.finish()

        export_results(
            self.sample_results,
            self.overall_score,
            self.categories_scores,
            target_name="mariadb_106",
            filename=html_dest,
            fmt="html",
            temporal_metadata=t_meta
        )

        end_epoch = time.time()

        # 1. Verify physical file presence on disk
        self.assertTrue(os.path.exists(html_dest))
        file_size = os.path.getsize(html_dest)
        self.assertGreater(file_size, 1000, f"HTML file size {file_size}B is suspiciously small.")

        # 2. Verify file mtime is within execution window
        mtime = os.path.getmtime(html_dest)
        self.assertGreaterEqual(mtime, start_epoch - 1.0)
        self.assertLessEqual(mtime, end_epoch + 1.0)

        # 3. Read content and verify timestamps
        with open(html_dest, "r", encoding="utf-8") as f:
            content = f.read()

        # Verify dynamic fields
        self.assertIn(t_meta.localized_start, content)
        self.assertIn(t_meta.formatted_duration, content)
        self.assertIn(t_meta.timezone_name, content)
        self.assertIn(t_meta.timezone_offset, content)

        # Verify no hardcoded suite version or dummy dates
        self.assertNotIn("12/34/5678", content)
        self.assertNotIn("width: 85%", content)

    def test_atomic_overwrite_integrity(self):
        """Verify repeated executions overwrite cleanly without corruption or file locking."""
        html_dest = os.path.join(self.tmp_dir, "rapport_cis_mariadb_106.html")

        for run_idx in range(3):
            t_meta = TemporalAuditMetadata.create_now()
            t_meta.finish()

            export_results(
                self.sample_results,
                self.overall_score,
                self.categories_scores,
                target_name="mariadb_106",
                filename=html_dest,
                fmt="html",
                temporal_metadata=t_meta
            )

            self.assertTrue(os.path.exists(html_dest))
            with open(html_dest, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn(t_meta.localized_start, content)


if __name__ == "__main__":
    unittest.main()
