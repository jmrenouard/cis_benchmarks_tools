"""
Tests for Dynamic Rule Category Scoring in calculate_scores() (Ponytail Audit Finding 10).
Verifies that audit engines discover rule categories dynamically from results data
rather than relying on hardcoded RECOMMENDATIONS_DATA.
"""

import unittest
import json
import audit_cis_mariadb_106 as mariadb_106
import audit_cis_mariadb_1011 as mariadb_1011
import audit_cis_mysql_80 as mysql_80
import audit_cis_mysql_community_84 as mysql_comm_84
import audit_cis_mysql_community_97 as mysql_comm_97
import audit_cis_mysql_enterprise_84 as mysql_ent_84
import audit_cis_mysql_enterprise_97 as mysql_ent_97
import audit_cis_postgresql_16 as postgresql_16
import audit_cis_postgresql_17 as postgresql_17
import audit_cis_postgresql_18 as postgresql_18
import audit_cis_mongodb_7 as mongodb_7
import audit_cis_mongodb_8 as mongodb_8
import audit_cis_cassandra_40 as cassandra_40
import audit_cis_cassandra_41 as cassandra_41
import audit_cis_cassandra_50 as cassandra_50


class TestDynamicCategoryScoringMariaDB(unittest.TestCase):
    """Test dynamic category discovery and scoring across MariaDB engines."""

    def setUp(self):
        self.mariadb_modules = [
            ("mariadb_106", mariadb_106),
            ("mariadb_1011", mariadb_1011),
        ]

    def test_dynamic_custom_category_discovery(self):
        """Verify custom dynamic categories not in RECOMMENDATIONS_DATA are scored properly without skipping."""
        custom_results = {
            "99. Custom Dynamic Rules": [
                {"number": "99.1", "name": "Custom Pass", "type": "Automated", "status": "Pass"},
                {"number": "99.2", "name": "Custom Fail", "type": "Automated", "status": "Fail"},
                {"number": "99.3", "name": "Custom NA", "type": "Automated", "status": "Not Applicable"},
                {"number": "99.4", "name": "Custom Manual", "type": "Manual", "status": "Manual"},
            ]
        }

        for name, mod in self.mariadb_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores(custom_results)
                self.assertIn("99. Custom Dynamic Rules", cat_scores, f"{name} failed to discover dynamic category")
                cat_data = cat_scores["99. Custom Dynamic Rules"]
                self.assertEqual(cat_data["passed_automated"], 1)
                self.assertEqual(cat_data["failed_automated"], 1)
                self.assertEqual(cat_data["na_checks"], 1)
                self.assertEqual(cat_data["manual_checks"], 1)
                # In MariaDB/MySQL formula: (Pass + NA) / (Pass + Fail + NA) * 100 = 2 / 3 * 100 = 66.666...
                self.assertAlmostEqual(cat_data["score"], 66.6666, places=2)
                self.assertAlmostEqual(overall_score, 66.6666, places=2)

                # Ensure category_labels JSON contains the dynamic category
                cat_labels_json = rest[7]  # category_labels
                labels = json.loads(cat_labels_json)
                self.assertEqual(labels, ["99. Custom Dynamic Rules"])

    def test_filtered_categories_only_contain_audited_categories(self):
        """Verify that when only a single category is audited, cat_scores only contains audited categories."""
        subset_results = {
            "1. Configuration": [
                {"number": "1.1", "name": "Check 1", "type": "Automated", "status": "Pass"},
                {"number": "1.2", "name": "Check 2", "type": "Automated", "status": "Pass"},
            ]
        }
        for name, mod in self.mariadb_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores(subset_results)
                self.assertIn("1. Configuration", cat_scores)
                self.assertEqual(list(cat_scores.keys()), ["1. Configuration"])
                self.assertEqual(overall_score, 100.0)

    def test_flat_list_results_support(self):
        """Verify calculate_scores accepts flat list of check result dictionaries."""
        flat_results = [
            {"category": "Alpha", "number": "A.1", "type": "Automated", "status": "Pass"},
            {"category": "Beta", "number": "B.1", "type": "Automated", "status": "Fail"},
        ]
        for name, mod in self.mariadb_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores(flat_results)
                self.assertIn("Alpha", cat_scores)
                self.assertIn("Beta", cat_scores)
                self.assertEqual(cat_scores["Alpha"]["passed_automated"], 1)
                self.assertEqual(cat_scores["Beta"]["failed_automated"], 1)
                self.assertEqual(overall_score, 50.0)

    def test_empty_results_resilience(self):
        """Verify empty results dictionary or list yields safe zero score without exceptions."""
        for name, mod in self.mariadb_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores({})
                self.assertEqual(overall_score, 0.0)
                self.assertEqual(cat_scores, {})


class TestDynamicCategoryScoringMySQL(unittest.TestCase):
    """Test dynamic category discovery and scoring across MySQL engines."""

    def setUp(self):
        self.mysql_modules = [
            ("mysql_80", mysql_80),
            ("mysql_comm_84", mysql_comm_84),
            ("mysql_comm_97", mysql_comm_97),
            ("mysql_ent_84", mysql_ent_84),
            ("mysql_ent_97", mysql_ent_97),
        ]

    def test_dynamic_custom_category_discovery(self):
        """Verify custom dynamic categories not in RECOMMENDATIONS_DATA are scored properly without skipping."""
        custom_results = {
            "99. Custom Dynamic Rules": [
                {"number": "99.1", "name": "Custom Pass", "type": "Automated", "status": "Pass"},
                {"number": "99.2", "name": "Custom Fail", "type": "Automated", "status": "Fail"},
                {"number": "99.3", "name": "Custom NA", "type": "Automated", "status": "Not Applicable"},
                {"number": "99.4", "name": "Custom Manual", "type": "Manual", "status": "Manual"},
            ]
        }
        for name, mod in self.mysql_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores(custom_results)
                self.assertIn("99. Custom Dynamic Rules", cat_scores, f"{name} failed to discover dynamic category")
                cat_data = cat_scores["99. Custom Dynamic Rules"]
                self.assertEqual(cat_data["passed_automated"], 1)
                self.assertEqual(cat_data["failed_automated"], 1)
                self.assertEqual(cat_data["na_checks"], 1)
                self.assertEqual(cat_data["manual_checks"], 1)
                self.assertAlmostEqual(cat_data["score"], 66.6666, places=2)
                self.assertAlmostEqual(overall_score, 66.6666, places=2)

    def test_filtered_categories_only_contain_audited_categories(self):
        """Verify that when only a single category is audited, cat_scores only contains audited categories."""
        subset_results = {
            "1. Configuration": [
                {"number": "1.1", "name": "Check 1", "type": "Automated", "status": "Pass"},
                {"number": "1.2", "name": "Check 2", "type": "Automated", "status": "Pass"},
            ]
        }
        for name, mod in self.mysql_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores(subset_results)
                self.assertIn("1. Configuration", cat_scores)
                self.assertEqual(list(cat_scores.keys()), ["1. Configuration"])
                self.assertEqual(overall_score, 100.0)

    def test_flat_list_results_support(self):
        """Verify calculate_scores accepts flat list of check result dictionaries."""
        flat_results = [
            {"category": "Alpha", "number": "A.1", "type": "Automated", "status": "Pass"},
            {"category": "Beta", "number": "B.1", "type": "Automated", "status": "Fail"},
        ]
        for name, mod in self.mysql_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores(flat_results)
                self.assertIn("Alpha", cat_scores)
                self.assertIn("Beta", cat_scores)
                self.assertEqual(cat_scores["Alpha"]["passed_automated"], 1)
                self.assertEqual(cat_scores["Beta"]["failed_automated"], 1)
                self.assertEqual(overall_score, 50.0)

    def test_empty_results_resilience(self):
        """Verify empty results dictionary or list yields safe zero score without exceptions."""
        for name, mod in self.mysql_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores({})
                self.assertEqual(overall_score, 0.0)
                self.assertEqual(cat_scores, {})



class TestDynamicCategoryScoringPostgreSQL(unittest.TestCase):
    """Test dynamic category discovery and scoring across PostgreSQL engines."""

    def setUp(self):
        self.pg_modules = [
            ("postgresql_16", postgresql_16),
            ("postgresql_17", postgresql_17),
            ("postgresql_18", postgresql_18),
        ]

    def test_dynamic_custom_category_discovery(self):
        """Verify custom dynamic categories not in RECOMMENDATIONS_DATA are scored properly without skipping."""
        custom_results = {
            "99. Custom Dynamic Rules": [
                {"number": "99.1", "name": "Custom Pass", "type": "Automated", "status": "Pass"},
                {"number": "99.2", "name": "Custom Fail", "type": "Automated", "status": "Fail"},
                {"number": "99.3", "name": "Custom NA", "type": "Automated", "status": "Not Applicable"},
                {"number": "99.4", "name": "Custom Manual", "type": "Manual", "status": "Manual"},
            ]
        }
        for name, mod in self.pg_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores(custom_results)
                self.assertIn("99. Custom Dynamic Rules", cat_scores, f"{name} failed to discover dynamic category")
                cat_data = cat_scores["99. Custom Dynamic Rules"]
                self.assertEqual(cat_data["passed_automated"], 1)
                self.assertEqual(cat_data["failed_automated"], 1)
                self.assertEqual(cat_data["na_checks"], 1)
                self.assertEqual(cat_data["manual_checks"], 1)
                # In PostgreSQL formula: Pass / (Pass + Fail) * 100 = 1 / 2 * 100 = 50.0
                self.assertEqual(cat_data["score"], 50.0)
                self.assertEqual(overall_score, 50.0)

    def test_filtered_categories_only_contain_audited_categories(self):
        """Verify that when only a single category is audited, cat_scores only contains audited categories."""
        subset_results = {
            "1. Configuration": [
                {"number": "1.1", "name": "Check 1", "type": "Automated", "status": "Pass"},
                {"number": "1.2", "name": "Check 2", "type": "Automated", "status": "Pass"},
            ]
        }
        for name, mod in self.pg_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores(subset_results)
                self.assertIn("1. Configuration", cat_scores)
                self.assertEqual(list(cat_scores.keys()), ["1. Configuration"])
                self.assertEqual(overall_score, 100.0)

    def test_flat_list_results_support(self):
        """Verify calculate_scores accepts flat list of check result dictionaries."""
        flat_results = [
            {"category": "Alpha", "number": "A.1", "type": "Automated", "status": "Pass"},
            {"category": "Beta", "number": "B.1", "type": "Automated", "status": "Fail"},
        ]
        for name, mod in self.pg_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores(flat_results)
                self.assertIn("Alpha", cat_scores)
                self.assertIn("Beta", cat_scores)
                self.assertEqual(cat_scores["Alpha"]["passed_automated"], 1)
                self.assertEqual(cat_scores["Beta"]["failed_automated"], 1)
                self.assertEqual(overall_score, 50.0)

    def test_empty_results_resilience(self):
        """Verify empty results dictionary or list yields safe zero score without exceptions."""
        for name, mod in self.pg_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores({})
                self.assertEqual(overall_score, 0.0)
                self.assertEqual(cat_scores, {})



class TestDynamicCategoryScoringMongoDB(unittest.TestCase):
    """Test dynamic category discovery and scoring across MongoDB engines."""

    def setUp(self):
        self.mongo_modules = [
            ("mongodb_7", mongodb_7),
            ("mongodb_8", mongodb_8),
        ]

    def test_dynamic_custom_category_discovery(self):
        """Verify custom dynamic categories not in RECOMMENDATIONS_DATA are scored properly without skipping."""
        custom_results = {
            "99. Custom Dynamic Rules": [
                {"number": "99.1", "name": "Custom Pass", "type": "Automated", "status": "Pass"},
                {"number": "99.2", "name": "Custom Fail", "type": "Automated", "status": "Fail"},
                {"number": "99.3", "name": "Custom NA", "type": "Automated", "status": "Not Applicable"},
                {"number": "99.4", "name": "Custom Manual", "type": "Manual", "status": "Manual"},
            ]
        }
        for name, mod in self.mongo_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores(custom_results)
                self.assertIn("99. Custom Dynamic Rules", cat_scores, f"{name} failed to discover dynamic category")
                cat_data = cat_scores["99. Custom Dynamic Rules"]
                self.assertEqual(cat_data["passed_automated"], 1)
                self.assertEqual(cat_data["failed_automated"], 1)
                self.assertEqual(cat_data["na_checks"], 1)
                self.assertEqual(cat_data["manual_checks"], 1)
                # In MongoDB formula: Pass / (Pass + Fail) * 100 = 1 / 2 * 100 = 50.0
                self.assertEqual(cat_data["score"], 50.0)
                self.assertEqual(overall_score, 50.0)

    def test_filtered_categories_only_contain_audited_categories(self):
        """Verify that when only a single category is audited, cat_scores only contains audited categories."""
        subset_results = {
            "1. Configuration": [
                {"number": "1.1", "name": "Check 1", "type": "Automated", "status": "Pass"},
                {"number": "1.2", "name": "Check 2", "type": "Automated", "status": "Pass"},
            ]
        }
        for name, mod in self.mongo_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores(subset_results)
                self.assertIn("1. Configuration", cat_scores)
                self.assertEqual(list(cat_scores.keys()), ["1. Configuration"])
                self.assertEqual(overall_score, 100.0)

    def test_flat_list_results_support(self):
        """Verify calculate_scores accepts flat list of check result dictionaries."""
        flat_results = [
            {"category": "Alpha", "number": "A.1", "type": "Automated", "status": "Pass"},
            {"category": "Beta", "number": "B.1", "type": "Automated", "status": "Fail"},
        ]
        for name, mod in self.mongo_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores(flat_results)
                self.assertIn("Alpha", cat_scores)
                self.assertIn("Beta", cat_scores)
                self.assertEqual(cat_scores["Alpha"]["passed_automated"], 1)
                self.assertEqual(cat_scores["Beta"]["failed_automated"], 1)
                self.assertEqual(overall_score, 50.0)

    def test_empty_results_resilience(self):
        """Verify empty results dictionary or list yields safe zero score without exceptions."""
        for name, mod in self.mongo_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores({})
                self.assertEqual(overall_score, 0.0)
                self.assertEqual(cat_scores, {})



class TestDynamicCategoryScoringCassandra(unittest.TestCase):
    """Test dynamic category discovery and scoring across Cassandra engines."""

    def setUp(self):
        self.cas_modules = [
            ("cassandra_40", cassandra_40),
            ("cassandra_41", cassandra_41),
            ("cassandra_50", cassandra_50),
        ]

    def test_dynamic_custom_category_discovery(self):
        """Verify custom dynamic categories not in RECOMMENDATIONS_DATA are scored properly without skipping."""
        custom_results = {
            "99. Custom Dynamic Rules": [
                {"number": "99.1", "name": "Custom Pass", "type": "Automated", "status": "Pass"},
                {"number": "99.2", "name": "Custom Fail", "type": "Automated", "status": "Fail"},
                {"number": "99.3", "name": "Custom NA", "type": "Automated", "status": "Not Applicable"},
                {"number": "99.4", "name": "Custom Manual", "type": "Manual", "status": "Manual"},
            ]
        }
        for name, mod in self.cas_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores(custom_results)
                self.assertIn("99. Custom Dynamic Rules", cat_scores, f"{name} failed to discover dynamic category")
                cat_data = cat_scores["99. Custom Dynamic Rules"]
                self.assertEqual(cat_data["passed_automated"], 1)
                self.assertEqual(cat_data["failed_automated"], 1)
                self.assertEqual(cat_data["na_checks"], 1)
                self.assertEqual(cat_data["manual_checks"], 1)
                # In Cassandra formula: Pass / (Pass + Fail) * 100 = 1 / 2 * 100 = 50.0
                self.assertEqual(cat_data["score"], 50.0)
                self.assertEqual(overall_score, 50.0)

    def test_filtered_categories_only_contain_audited_categories(self):
        """Verify that when only a single category is audited, cat_scores only contains audited categories."""
        subset_results = {
            "1. Configuration": [
                {"number": "1.1", "name": "Check 1", "type": "Automated", "status": "Pass"},
                {"number": "1.2", "name": "Check 2", "type": "Automated", "status": "Pass"},
            ]
        }
        for name, mod in self.cas_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores(subset_results)
                self.assertIn("1. Configuration", cat_scores)
                self.assertEqual(list(cat_scores.keys()), ["1. Configuration"])
                self.assertEqual(overall_score, 100.0)

    def test_flat_list_results_support(self):
        """Verify calculate_scores accepts flat list of check result dictionaries."""
        flat_results = [
            {"category": "Alpha", "number": "A.1", "type": "Automated", "status": "Pass"},
            {"category": "Beta", "number": "B.1", "type": "Automated", "status": "Fail"},
        ]
        for name, mod in self.cas_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores(flat_results)
                self.assertIn("Alpha", cat_scores)
                self.assertIn("Beta", cat_scores)
                self.assertEqual(cat_scores["Alpha"]["passed_automated"], 1)
                self.assertEqual(cat_scores["Beta"]["failed_automated"], 1)
                self.assertEqual(overall_score, 50.0)

    def test_empty_results_resilience(self):
        """Verify empty results dictionary or list yields safe zero score without exceptions."""
        for name, mod in self.cas_modules:
            with self.subTest(engine=name):
                overall_score, cat_scores, *rest = mod.calculate_scores({})
                self.assertEqual(overall_score, 0.0)
                self.assertEqual(cat_scores, {})


if __name__ == "__main__":
    unittest.main()
