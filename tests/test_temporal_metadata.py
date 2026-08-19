#!/usr/bin/env python3
"""
Unit test suite for temporal_metadata.py (Python PSL ONLY).
"""

import datetime
import time
import unittest

from temporal_metadata import TemporalAuditMetadata, get_local_timezone_info


class TestTemporalMetadata(unittest.TestCase):
    """Test suite for timezone-aware temporal metadata module."""

    def test_get_local_timezone_info(self):
        """Test extraction of timezone name and offset."""
        tz_info = get_local_timezone_info()
        self.assertIn("timezone_name", tz_info)
        self.assertIn("timezone_offset", tz_info)
        self.assertTrue(tz_info["timezone_offset"].startswith("+") or tz_info["timezone_offset"].startswith("-"))
        self.assertEqual(len(tz_info["timezone_offset"]), 6)  # e.g. +02:00

    def test_temporal_metadata_creation_and_realtime(self):
        """Test that created metadata reflects the real-time system clock within 2s delta."""
        now_epoch = time.time()
        meta = TemporalAuditMetadata.create_now()

        start_epoch = meta.start_dt.timestamp()
        delta = abs(start_epoch - now_epoch)
        self.assertLess(delta, 2.0, f"Timestamp delta {delta}s exceeds 2s tolerance.")

        # Check ISO format
        self.assertIn("T", meta.iso_start)
        self.assertTrue("+" in meta.iso_start or "-" in meta.iso_start or "Z" in meta.iso_start)

        # Check localized format (DD/MM/YYYY HH:MM:SS)
        self.assertRegex(meta.localized_start, r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}")

    def test_temporal_metadata_duration_and_finish(self):
        """Test finish() and duration calculation."""
        meta = TemporalAuditMetadata.create_now()
        time.sleep(0.05)
        meta.finish()

        self.assertGreaterEqual(meta.duration_sec, 0.04)
        self.assertIn("ms", meta.formatted_duration)

        # Test with custom start and end
        t0 = datetime.datetime(2026, 8, 19, 10, 0, 0, tzinfo=datetime.timezone.utc)
        t1 = datetime.datetime(2026, 8, 19, 10, 0, 5, 500000, tzinfo=datetime.timezone.utc)
        custom_meta = TemporalAuditMetadata(start_time=t0, end_time=t1)
        self.assertAlmostEqual(custom_meta.duration_sec, 5.5, places=2)
        self.assertEqual(custom_meta.formatted_duration, "5.50s")

    def test_to_dict_serialization(self):
        """Test dictionary serialization of temporal metadata."""
        meta = TemporalAuditMetadata.create_now()
        meta.finish()
        d = meta.to_dict()

        expected_keys = [
            "iso_start", "iso_end", "localized_start", "localized_end",
            "standard_start", "standard_end", "duration_sec",
            "formatted_duration", "timezone_name", "timezone_offset"
        ]
        for k in expected_keys:
            self.assertIn(k, d)


if __name__ == "__main__":
    unittest.main()
