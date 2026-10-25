#!/usr/bin/env python3
"""CIS Benchmarks Manifest & Integrity Verifier (100% PSL ONLY)."""

import argparse
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request

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


def download_file(url: str, dest: str, expected_sha256: str = None, timeout: int = 30, opener=None):
    if d := os.path.dirname(dest):
        os.makedirs(d, exist_ok=True)
    part, h, count = f"{dest}.part", hashlib.sha256(), 0
    req = urllib.request.Request(url, headers={"User-Agent": "cis-benchmarks-tools/2.9.1"})
    try:
        with (opener or urllib.request.urlopen)(req, timeout=timeout) as resp, open(part, "wb") as out:
            while chunk := resp.read(65536):
                h.update(chunk); out.write(chunk); count += len(chunk)
        digest = h.hexdigest()
        if expected_sha256 and digest.lower() != expected_sha256.lower():
            raise ValueError(f"Checksum mismatch: exp {expected_sha256}, got {digest}")
        os.replace(part, dest)
        return True, digest, count
    except Exception:
        if os.path.isfile(part):
            try: os.remove(part)
            except OSError: pass
        raise


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


def sync_benchmarks(data_dir=None, manifest_path=None, targets=None, file_types=("md", "pdf"),
                    force=False, verify_only=False, base_url=None, opener=None, dry_run=False):
    if verify_only:
        return verify_benchmarks(data_dir, manifest_path, targets, file_types)
    manifest = load_manifest(manifest_path)
    base = (base_url or manifest.get("base_url", "")).rstrip("/")
    tdir = data_dir or DEFAULT_DATA_DIR
    os.makedirs(tdir, exist_ok=True)
    bmarks = manifest.get("benchmarks", {})
    if targets:
        bmarks = {k: v for k, v in bmarks.items() if k in targets}

    res = {"total": 0, "verified": 0, "downloaded": 0, "skipped": 0, "failed": 0, "details": []}
    for tgt, entry in bmarks.items():
        for ft in file_types:
            fname, sha = resolve_file_spec(entry, ft)
            if not sha:
                continue
            res["total"] += 1
            fpath = os.path.join(tdir, fname)
            st, key, msg = "FAILED", "failed", None
            if not force and os.path.isfile(fpath) and verify_file(fpath, sha)[0]:
                st, key = "UP_TO_DATE", "skipped"
            elif dry_run:
                st, key = "DRY_RUN", "skipped"
            else:
                try:
                    download_file(f"{base}/{urllib.parse.quote(fname)}", fpath, sha, opener=opener)
                    st, key = "DOWNLOADED", "downloaded"
                except Exception as e:
                    msg = str(e)
            res[key] += 1
            d = {"target": tgt, "file": fname, "status": st}
            if msg: d["msg"] = msg
            res["details"].append(d)
    return res


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="CIS Integrity Verifier")
    p.add_argument("-t", "--target", action="append")
    p.add_argument("--types", default="all")
    p.add_argument("--verify-only", action="store_true")
    p.add_argument("--force", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--data-dir")
    p.add_argument("--manifest")
    p.add_argument("--base-url")
    p.add_argument("-q", "--quiet", action="store_true")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    fts = ("md", "pdf") if args.types == "all" else (args.types,)
    tgts = set(args.target) if args.target else None
    if not args.quiet:
        act = "Verifying" if args.verify_only else "Synchronizing"
        print(f"📦 [CIS Data] {act} specifications ({', '.join(fts)})...")

    s = sync_benchmarks(args.data_dir, args.manifest, tgts, fts, force=args.force,
                        verify_only=args.verify_only, base_url=args.base_url, dry_run=args.dry_run)
    if not args.quiet:
        for it in s["details"]:
            sym = "✓" if it["status"] in ("VERIFIED", "UP_TO_DATE", "DOWNLOADED") else "✗"
            print(f"  {sym} [{it['target']}] {it['file']} -> {it['status']}")
        print("\n📊 " + " | ".join(f"{k.capitalize()}: {v}" for k, v in s.items() if k != "details"))

    return 1 if (s.get("failed", 0) or s.get("corrupted", 0) or (args.verify_only and s.get("missing", 0))) else 0


if __name__ == "__main__":
    sys.exit(main())
