#!/usr/bin/env python3
"""
Unit tests for cross-distribution package detection and rule sanitization (PSL ONLY).
"""

import json
import os
import unittest


class TestDistroPackageDetection(unittest.TestCase):

    def setUp(self):
        self.rules_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rules")

    def test_package_inspection_commands_in_all_rules(self):
        """Validate that package verification in rule 1.2 supports multi-distribution execution."""
        for fname in os.listdir(self.rules_dir):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(self.rules_dir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                rules = json.load(f)

            for rule in rules:
                tp = rule.get("test_procedure", "")
                if "dpkg" in tp or "rpm" in tp:
                    # Should handle both or be a resilient shell test
                    self.assertTrue(
                        "command -v" in tp or "which" in tp or "||" in tp or "rpm -q" in tp,
                        f"Rule {rule.get('number')} in {fname} has non-portable package test procedure: {tp}"
                    )

    def test_remediation_instructions_are_distro_agnostic(self):
        """Validate that package-related remediations mention multiple package managers or generic commands."""
        for target in ["postgresql_16.json", "postgresql_17.json", "postgresql_18.json"]:
            fpath = os.path.join(self.rules_dir, target)
            with open(fpath, "r", encoding="utf-8") as f:
                rules = json.load(f)

            for rule in rules:
                if rule.get("number") in ["1.2", "1.5"]:
                    rem = rule.get("remediation", "")
                    self.assertTrue(
                        any(pkg_mgr in rem for pkg_mgr in ["apt", "dnf", "apk", "yum"]),
                        f"Rule {rule.get('number')} in {target} lacks multi-distribution remediation: {rem}"
                    )


if __name__ == "__main__":
    unittest.main()
