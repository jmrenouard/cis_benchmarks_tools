#!/usr/bin/env python3
"""
Unit Test Suite for Multi-Format Audit Exporters (HTML, JSON, STIG XML, TXT ASCII Tables).
100% Python Standard Library (PSL ONLY).
"""

import json
import os
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from audit_cis_mariadb_106 import export_results


class TestFormatExporters(unittest.TestCase):
    """Unit tests for export_results logic across all report formats."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.sample_results = {
            "1. Installation and Planning": [
                {
                    "number": "1.1",
                    "name": "Ensure latest MariaDB version is installed",
                    "category": "1. Installation and Planning",
                    "status": "Pass",
                    "output": "10.6.12",
                    "remediation": "Update package via yum"
                },
                {
                    "number": "1.2",
                    "name": "Ensure dedicated user for MariaDB service",
                    "category": "1. Installation and Planning",
                    "status": "Fail",
                    "output": "root",
                    "remediation": "Create mysql user"
                }
            ]
        }
        self.categories_scores = {
            "1. Installation and Planning": {
                "name": "1. Installation and Planning",
                "passed_automated": 1,
                "failed_automated": 1,
                "manual_checks": 0,
                "score": 50.0
            }
        }

    def tearDown(self):
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for f in files:
                os.remove(os.path.join(root, f))
            for d in dirs:
                os.rmdir(os.path.join(root, d))
        os.rmdir(self.test_dir)

    def test_export_json_format(self):
        json_file = os.path.join(self.test_dir, "report.json")
        export_results(self.sample_results, 50.0, self.categories_scores, "MariaDB 10.6", json_file, fmt="json")
        self.assertTrue(os.path.exists(json_file))
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["benchmark"], "MariaDB 10.6")
        self.assertEqual(data["overall_score"], 50.0)
        self.assertEqual(data["total_checks"], 2)

    def test_export_xml_format(self):
        xml_file = os.path.join(self.test_dir, "report.xml")
        export_results(self.sample_results, 50.0, self.categories_scores, "MariaDB 10.6", xml_file, fmt="xml")
        self.assertTrue(os.path.exists(xml_file))
        tree = ET.parse(xml_file)
        root = tree.getroot()
        self.assertEqual(root.tag, "testsuite")
        self.assertEqual(root.attrib["name"], "MariaDB 10.6")
        self.assertEqual(len(root.findall("testcase")), 2)

    def test_export_txt_ascii_summary_table_format(self):
        txt_file = os.path.join(self.test_dir, "report.txt")
        export_results(self.sample_results, 50.0, self.categories_scores, "MariaDB 10.6", txt_file, fmt="txt")
        self.assertTrue(os.path.exists(txt_file))
        with open(txt_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("CIS BENCHMARK AUDIT REPORT - MARIADB 10.6", content)
        self.assertIn("CATEGORY BREAKDOWN & COMPLIANCE SUMMARY TABLE", content)
        self.assertIn("50.0%", content)

    def test_export_html_format(self):
        html_file = os.path.join(self.test_dir, "report.html")
        export_results(self.sample_results, 50.0, self.categories_scores, "MariaDB 10.6", html_file, fmt="html")
        self.assertTrue(os.path.exists(html_file))
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("<html", content)
        self.assertIn("toggleDarkMode", content)


if __name__ == "__main__":
    unittest.main()
