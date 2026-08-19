#!/usr/bin/env python3
"""
Unit test suite for report template rendering and elimination of hardcoded data (Python PSL ONLY).
"""

import os
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(REPO_ROOT, "templates", "report_template.html")


class TestReportTemplateRendering(unittest.TestCase):
    """Test suite for report template rendering."""

    def test_no_hardcoded_thematic_percentages_in_template(self):
        """Verify report_template.html contains no hardcoded 85%, 90%, 75% mock bars."""
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            template_content = f.read()

        self.assertNotIn('width: 85%', template_content)
        self.assertNotIn('width: 90%', template_content)
        self.assertNotIn('width: 75%', template_content)
        self.assertIn('{thematic_security_metrics_html}', template_content)
        self.assertIn('{scan_duration}', template_content)
        self.assertIn('{report_timezone}', template_content)

    def test_template_formatting_with_safedict(self):
        """Verify template format_map works reliably with SafeDict."""
        class SafeDict(dict):
            def __missing__(self, key):
                return f"{{{key}}}"

        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            template_content = f.read()

        rendered = template_content.format_map(SafeDict(
            product_title="MariaDB 10.6",
            benchmark_title="MariaDB 10.6",
            benchmark_version="1.0.0",
            suite_version="2.7.0",
            execution_context="Local Docker",
            execution_context_card_html="<div>Context Card</div>",
            lang="en",
            report_date="19/08/2026 10:45:00 CEST",
            scan_duration="1.45s",
            report_timezone="CEST (+02:00)",
            overall_score=94.5,
            overall_score_class="score-high",
            passed_automated_count=45,
            failed_automated_count=5,
            manual_checks=10,
            error_count=0,
            thematic_security_metrics_html="<div>Thematic Metrics</div>",
            sidebar_links="<a href='#'>Link</a>",
            categories_reports="<div>Categories</div>",
            donut_svg="<svg>Donut</svg>",
            bar_svg="<svg>Bar</svg>"
        ))

        self.assertIn("Rapport d'Audit CIS - MariaDB 10.6", rendered)
        self.assertIn("19/08/2026 10:45:00 CEST", rendered)
        self.assertIn("1.45s", rendered)
        self.assertIn("CEST (+02:00)", rendered)
        self.assertIn("94.5%", rendered)


if __name__ == "__main__":
    unittest.main()
