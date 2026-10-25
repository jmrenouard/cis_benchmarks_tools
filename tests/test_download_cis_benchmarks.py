#!/usr/bin/env python3
"""Unit tests for CIS Benchmarks manifest and verifier (PSL ONLY)."""

import hashlib
import io
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
    download_file,
    sync_benchmarks,
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

    class DummyResp(io.BytesIO):
        def __enter__(self): return self
        def __exit__(self, *a): pass

    def test_download_file_success_atomic(self):
        dest = os.path.join(self.tmp, "dl.md")
        ok, dig, cnt = download_file("http://ex.com/t.md", dest, self.c_hash, opener=lambda r, **k: self.DummyResp(self.content))
        self.assertTrue(ok and dig == self.c_hash and cnt == len(self.content) and os.path.isfile(dest) and not os.path.isfile(f"{dest}.part"))

    def test_download_file_checksum_mismatch_cleans_part(self):
        dest = os.path.join(self.tmp, "c.md")
        with self.assertRaises(ValueError):
            download_file("http://ex.com/t.md", dest, self.c_hash, opener=lambda r, **k: self.DummyResp(b"bad"))
        self.assertTrue(not os.path.isfile(dest) and not os.path.isfile(f"{dest}.part"))

    def test_sync_benchmarks_workflow(self):
        op = lambda r, **k: self.DummyResp(self.content)
        self.assertEqual(sync_benchmarks(self.tmp, self.m_path, targets=["mariadb106"], file_types=("md",), dry_run=True)["skipped"], 1)
        self.assertEqual(sync_benchmarks(self.tmp, self.m_path, targets=["mariadb106"], file_types=("md",), opener=op)["downloaded"], 1)
        self.assertEqual(sync_benchmarks(self.tmp, self.m_path, targets=["mariadb106"], file_types=("md",), opener=op)["skipped"], 1)


if __name__ == "__main__":
    unittest.main()

