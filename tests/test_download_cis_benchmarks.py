#!/usr/bin/env python3
"""Unit tests for CIS Benchmarks manifest and verifier (PSL ONLY)."""

import hashlib
import json
import os
import shutil
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.download_cis_benchmarks import (
    calculate_sha256,
    load_manifest,
    main,
    parse_args,
    verify_benchmarks,
    verify_file,
)


class TestCISBenchmarksManifestAndVerifier(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.m_path = os.path.join(self.tmp, "test_manifest.json")
        self.content = b"# Sample CIS Benchmark\n"
        self.c_hash = hashlib.sha256(self.content).hexdigest()
        data = {
            "version": "1.0",
            "base_url": "https://example.com/cis_data",
            "benchmarks": {
                "mariadb106": {"stem": "CIS_MariaDB_10.6_Benchmark_v1.1.0", "ver": "1.1.0", "md": self.c_hash, "pdf": "0" * 64}
            },
        }
        with open(self.m_path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_official_manifest_structure(self):
        m = load_manifest()
        self.assertGreaterEqual(len(m.get("benchmarks", {})), 22)
        for _, s in m["benchmarks"].items():
            self.assertEqual(len(s.get("md") or s.get("md_sha256")), 64)
            self.assertEqual(len(s.get("pdf") or s.get("pdf_sha256")), 64)

    def test_load_manifest_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_manifest(os.path.join(self.tmp, "missing.json"))

    def test_calculate_sha256_and_verify_file(self):
        p = os.path.join(self.tmp, "test.md")
        with open(p, "wb") as f:
            f.write(self.content)

        self.assertEqual(calculate_sha256(p), self.c_hash)
        self.assertTrue(verify_file(p, self.c_hash)[0])
        self.assertFalse(verify_file(p, "bad_hash")[0])
        self.assertFalse(verify_file(os.path.join(self.tmp, "404.md"), self.c_hash)[0])

    def test_verify_benchmarks_statuses(self):
        self.assertEqual(verify_benchmarks(self.tmp, self.m_path, file_types=("md",))["missing"], 1)
        p = os.path.join(self.tmp, "CIS_MariaDB_10.6_Benchmark_v1.1.0.md")
        with open(p, "wb") as f:
            f.write(self.content)
        self.assertEqual(verify_benchmarks(self.tmp, self.m_path, file_types=("md",))["verified"], 1)

    def test_cli_parsing_and_main_verify(self):
        args = parse_args(["-t", "mariadb106", "--types", "md"])
        self.assertEqual(args.target, ["mariadb106"])
        self.assertEqual(main(["-t", "mariadb106", "--types", "md", "--quiet"]), 0)


if __name__ == "__main__":
    unittest.main()
