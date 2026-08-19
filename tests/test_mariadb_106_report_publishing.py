#!/usr/bin/env python3
"""
Integration test suite for MariaDB 10.6 audit report publishing and temporal metadata (Python PSL ONLY).
"""

import json
import os
import tempfile
import unittest
import xml.etree.ElementTree as ET

from audit_cis_mariadb_106 import export_results, generate_html_report, build_thematic_security_metrics
from temporal_metadata import TemporalAuditMetadata


class TestMariaDB106ReportPublishing(unittest.TestCase):
    """Test suite for MariaDB 10.6 audit report publishing."""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.sample_results = {
            "1. OS Configuration": [
                {"number": "1.1", "name": "Check datadir", "status": "Pass", "output": "/var/lib/mysql", "test_procedure": "df -P", "remediation": "Move datadir"}
            ],
            "2. Access & Privileges": [
                {"number": "2.1", "name": "No root remote", "status": "Fail", "output": "Root accessible", "test_procedure": "SELECT user", "remediation": "Revoke root remote"}
            ]
        }
        self.categories_scores = {
            "1. OS Configuration": {"score": 100.0, "passed_automated": 1, "failed_automated": 0, "manual_checks": 0, "error_checks": 0, "na_checks": 0},
            "2. Access & Privileges": {"score": 50.0, "passed_automated": 0, "failed_automated": 1, "manual_checks": 0, "error_checks": 0, "na_checks": 0}
        }
        self.overall_score = 75.0
        self.t_meta = TemporalAuditMetadata.create_now()
        self.t_meta.finish()

    def test_export_html_with_temporal_metadata(self):
        """Test HTML report export contains localized start time, duration, and timezone."""
        html_file = os.path.join(self.tmp_dir, "report.html")
        export_results(
            self.sample_results,
            self.overall_score,
            self.categories_scores,
            target_name="mariadb_106",
            filename=html_file,
            fmt="html",
            temporal_metadata=self.t_meta
        )

        self.assertTrue(os.path.exists(html_file))
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn(self.t_meta.localized_start, content)
        self.assertIn(self.t_meta.formatted_duration, content)
        self.assertIn(self.t_meta.timezone_name, content)
        self.assertIn("Rapport d'Audit CIS - MariaDB 10.6", content)

    def test_export_json_with_temporal_metadata(self):
        """Test JSON report export contains full temporal_metadata dict."""
        json_file = os.path.join(self.tmp_dir, "report.json")
        export_results(
            self.sample_results,
            self.overall_score,
            self.categories_scores,
            target_name="mariadb_106",
            filename=json_file,
            fmt="json",
            temporal_metadata=self.t_meta
        )

        self.assertTrue(os.path.exists(json_file))
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("temporal_metadata", data)
        self.assertEqual(data["temporal_metadata"]["iso_start"], self.t_meta.iso_start)
        self.assertEqual(data["temporal_metadata"]["timezone_name"], self.t_meta.timezone_name)

    def test_export_xml_with_temporal_metadata(self):
        """Test XML testsuite element contains timestamp and time attributes."""
        xml_file = os.path.join(self.tmp_dir, "report.xml")
        export_results(
            self.sample_results,
            self.overall_score,
            self.categories_scores,
            target_name="mariadb_106",
            filename=xml_file,
            fmt="xml",
            temporal_metadata=self.t_meta
        )

        self.assertTrue(os.path.exists(xml_file))
        tree = ET.parse(xml_file)
        root = tree.getroot()
        self.assertEqual(root.tag, "testsuite")
        self.assertEqual(root.attrib.get("timestamp"), self.t_meta.iso_start)
        self.assertIn("time", root.attrib)

    def test_export_txt_with_temporal_metadata(self):
        """Test TXT report header contains Report Date, Duration, and Timezone."""
        txt_file = os.path.join(self.tmp_dir, "report.txt")
        export_results(
            self.sample_results,
            self.overall_score,
            self.categories_scores,
            target_name="mariadb_106",
            filename=txt_file,
            fmt="txt",
            temporal_metadata=self.t_meta
        )

        self.assertTrue(os.path.exists(txt_file))
        with open(txt_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn(f"Report Date   : {self.t_meta.localized_start}", content)
        self.assertIn(f"Duration      : {self.t_meta.formatted_duration}", content)
        self.assertIn(f"Timezone      : {self.t_meta.timezone_name}", content)

    def test_build_thematic_security_metrics(self):
        """Test dynamic thematic security metric generation."""
        html_cards = build_thematic_security_metrics(self.categories_scores)
        self.assertIn("OS Configuration", html_cards)
        self.assertIn("100.0%", html_cards)
        self.assertIn("50.0%", html_cards)


if __name__ == "__main__":
    unittest.main()
