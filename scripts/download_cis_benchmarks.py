#!/usr/bin/env python3
"""CIS Benchmarks Manifest & Integrity Verifier (100% PSL ONLY)."""

import argparse
import hashlib
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MANIFEST = os.path.join(REPO_ROOT, "conf", "cis_manifest.json")
DEFAULT_DATA_DIR = os.path.join(REPO_ROOT, "CIS_DATA")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def calculate_sha256(filepath: str, chunk_size: int = 65536):
    if not os.path.isfile(filepath):
        return None
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def verify_file(filepath: str, expected_sha256: str):
    if not os.path.isfile(filepath):
        return False, "File missing"
    actual = calculate_sha256(filepath)
    if actual.lower() != expected_sha256.lower():
        return False, f"SHA-256 mismatch: exp {expected_sha256}, got {actual}"
    return True, "Integrity verified"


def load_manifest(manifest_path: str = None):
    path = manifest_path or DEFAULT_MANIFEST
    if not os.path.isfile(path):
        raise FileNotFoundError(f"CIS manifest not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_file_spec(entry: dict, ftype: str):
    sha = entry.get(f"{ftype}_sha256") or entry.get(ftype)
    return f"{entry['stem']}.{ftype}", sha


def verify_benchmarks(data_dir=None, manifest_path=None, targets=None, file_types=("md", "pdf")):
    manifest = load_manifest(manifest_path)
    bmarks = manifest.get("benchmarks", {})
    if targets:
        bmarks = {k: v for k, v in bmarks.items() if k in targets}
    tdir = data_dir or DEFAULT_DATA_DIR
    res = {"total": 0, "verified": 0, "missing": 0, "corrupted": 0, "details": []}

    for tgt, entry in bmarks.items():
        for ft in file_types:
            fname, sha = resolve_file_spec(entry, ft)
            if not sha:
                continue
            res["total"] += 1
            fpath = os.path.join(tdir, fname)
            if not os.path.isfile(fpath):
                res["missing"] += 1
                res["details"].append({"target": tgt, "file": fname, "status": "MISSING"})
            else:
                ok, _ = verify_file(fpath, sha)
                st = "VERIFIED" if ok else "CORRUPTED"
                res["verified" if ok else "corrupted"] += 1
                res["details"].append({"target": tgt, "file": fname, "status": st})
    return res


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="CIS Integrity Verifier")
    p.add_argument("-t", "--target", action="append")
    p.add_argument("--types", default="all")
    p.add_argument("--verify-only", action="store_true", default=True)
    p.add_argument("--data-dir")
    p.add_argument("--manifest")
    p.add_argument("-q", "--quiet", action="store_true")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    fts = ("md", "pdf") if args.types == "all" else (args.types,)
    tgts = set(args.target) if args.target else None
    if not args.quiet:
        print(f"📦 [CIS Data] Verifying specifications ({', '.join(fts)})...")

    s = verify_benchmarks(args.data_dir, args.manifest, tgts, fts)
    if not args.quiet:
        for it in s["details"]:
            sym = "✓" if it["status"] == "VERIFIED" else "✗"
            print(f"  {sym} [{it['target']}] {it['file']} -> {it['status']}")
        print(f"\n📊 Total: {s['total']} | Verified: {s['verified']} | Missing: {s['missing']} | Corrupted: {s['corrupted']}")

    return 1 if (s["corrupted"] > 0 or s["missing"] > 0) else 0


if __name__ == "__main__":
    sys.exit(main())
