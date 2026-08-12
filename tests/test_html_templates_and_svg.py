#!/usr/bin/env python3
"""
Unit Test Suite for HTML Template Loaders and Pure PSL Inline SVG Charts Engine.
100% Python Standard Library (PSL ONLY).
"""

import os
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from audit_cis_mariadb_106 import (
    load_html_template,
    load_category_template,
    build_inline_svg_donut_chart,
    build_inline_svg_category_chart
)


class TestHtmlTemplatesAndSVG(unittest.TestCase):
    """Unit tests for HTML templates loader and PSL SVG chart generation."""

    def test_load_html_template(self):
        tmpl = load_html_template()
        self.assertIsInstance(tmpl, str)
        self.assertIn("<html", tmpl)
        self.assertIn("toggleDarkMode", tmpl)

    def test_load_category_template(self):
        tmpl = load_category_template()
        self.assertIsInstance(tmpl, str)
        self.assertIn("category_name", tmpl)

    def test_build_inline_svg_donut_chart(self):
        svg = build_inline_svg_donut_chart(10, 5, 1, 1, 66.7)
        self.assertIsInstance(svg, str)
        self.assertIn("<svg", svg)
        self.assertIn("path", svg)
        self.assertIn("66.7%", svg)

    def test_build_inline_svg_donut_chart_zero_checks(self):
        svg = build_inline_svg_donut_chart(0, 0, 0, 0, 0.0)
        self.assertIsInstance(svg, str)
        self.assertIn("<svg", svg)

    def test_build_inline_svg_category_chart(self):
        sample_categories_scores = {
            "1. Operating System": {
                "passed_automated": 5,
                "failed_automated": 2,
                "error_checks": 0,
                "na_checks": 1,
                "score": 71.4
            }
        }
        svg = build_inline_svg_category_chart(sample_categories_scores)
        self.assertIsInstance(svg, str)
        self.assertIn("1. Operating System", svg)


if __name__ == "__main__":
    unittest.main()
