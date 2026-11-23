"""Build a multi-version MkDocs Material site bundle for IONOS Apache hosting."""

from __future__ import annotations

import argparse
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess  # nosec B404
import sys
import tempfile
import zipfile

DEFAULT_BASE_URL = "https://cis-benchmarks.lightpath.fr"
_SEMVER_TAG_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")
_SAFE_REF_RE = re.compile(r"^[A-Za-z0-9._/\-]+$")
_PRIVATE_OUTPUT_RE = re.compile(
    r"(?i)(?:(?:^|/)(?:\.env[^/]*|id_rsa[^/]*)$|\.(?:kdbx|keyx|pid)$|(?:^|/)CIS_DATA/.*\.pdf$)"
)
ALWAYS_OVERLAY_FILES: tuple[str, ...] = (
    "mkdocs.yml", "scripts/mkdocs_hooks.py", "docs/stylesheets/extra.css", "docs/javascripts/katex.js"
)
FALLBACK_OVERLAY_FILES: tuple[str, ...] = (
    "docs/index.md", "docs/assets/logo.svg", "docs/assets/header-banner.svg"
)
_PROTECTED = (
    ".git", ".github", "docs", "documentation", "tests", "scripts", "rules",
    "templates", "docker", "conf", "CIS_DATA", "reports", "archive", ".agents",
)


def parse_semver_tag(tag: str) -> tuple[int, int, int] | None:
    """Parse a semantic version tag such as `v2.10.0` into `(major, minor, patch)`."""
    m = _SEMVER_TAG_RE.fullmatch(tag.strip())
    return (int(m[1]), int(m[2]), int(m[3])) if m else None


def _sort_tags_descending(tags: list[str]) -> list[str]:
    uniq = list(dict.fromkeys(t.strip() for t in tags if t.strip()))
    return sorted(uniq, key=lambda t: (1, p, t) if (p := parse_semver_tag(t)) else (0, (0, 0, 0), t), reverse=True)


def discover_release_tags(repo_root: Path) -> list[str]:
    """Discover semantic-version Git release tags sorted newest-first."""
    proc = subprocess.run(  # nosec B603, B607
        ["git", "-C", str(repo_root), "tag", "--list"], capture_output=True, text=True, check=True
    )
    return _sort_tags_descending([ln.strip() for ln in proc.stdout.splitlines() if parse_semver_tag(ln.strip())])


def build_versions_manifest(release_tags: list[str], include_main: bool = True) -> list[dict[str, object]]:
    """Build Material (`provider: mike`) `versions.json` entries ordered newest-first."""
    tags = _sort_tags_descending(release_tags)
    entries: list[dict[str, object]] = [
        {"version": t, "title": t, "aliases": ["latest"] if i == 0 else []} for i, t in enumerate(tags)
    ]
    if include_main:
        entries.append({"version": "main", "title": "main (dev)", "aliases": ["dev"] if tags else ["latest", "dev"]})
    return entries


def render_redirect_html(target_url: str, title: str = "CIS Benchmarks Tools Documentation") -> str:
    """Render a minimal HTML redirect fallback page for static hosting."""
    u, t = html.escape(target_url, quote=True), html.escape(title, quote=True)
    return (
        f'<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="utf-8">\n  <title>{t}</title>\n'
        f'  <meta http-equiv="refresh" content="0; url={u}">\n  <link rel="canonical" href="{u}">\n'
        f'  <script>window.location.replace({json.dumps(target_url)});</script>\n</head>\n<body>\n'
        f'  <p>Redirecting to <a href="{u}">{u}</a>...</p>\n</body>\n</html>\n'
    )


def render_htaccess(latest_version: str, main_version: str = "main") -> str:
    """Render Apache `.htaccess` for IONOS with HTTPS, headers, and version redirects."""
    latest, main_v = latest_version.strip("/"), main_version.strip("/")
    return f"""# CIS Benchmarks Tools Versioned Docs (IONOS)
Options -Indexes -MultiViews
DirectoryIndex index.html
ErrorDocument 404 /{latest}/404.html

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/css text/xml
  AddOutputFilterByType DEFLATE application/javascript application/json image/svg+xml
</IfModule>

<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"
  Header always set X-Frame-Options "SAMEORIGIN"
  <FilesMatch "versions\\.json$">
    Header set Cache-Control "public, max-age=300, must-revalidate"
  </FilesMatch>
</IfModule>

<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteCond %{{HTTPS}} !=on
  RewriteCond %{{HTTP:X-Forwarded-Proto}} !https [NC]
  RewriteRule ^ https://%{{HTTP_HOST}}%{{REQUEST_URI}} [R=301,L]
  RewriteRule ^$ /{latest}/ [R=302,L]
  RewriteRule ^latest(?:/(.*))?$ /{latest}/$1 [R=302,L]
  RewriteRule ^dev(?:/(.*))?$ /{main_v}/$1 [R=302,L]
</IfModule>
"""


def _validate_git_ref(git_ref: str) -> str:
    cleaned = git_ref.strip()
    if not cleaned or cleaned.startswith("-") or not _SAFE_REF_RE.fullmatch(cleaned):
        raise ValueError(f"Invalid git ref: {git_ref!r}")
    return cleaned


def _safe_extract_zip(archive_path: Path, dest_dir: Path) -> None:
    """Extract a ZIP archive into `dest_dir` while blocking path traversal."""
    root = dest_dir.resolve()
    with zipfile.ZipFile(archive_path, "r") as zf:
        for info in zf.infolist():
            member = (root / info.filename).resolve()
            if not member.is_relative_to(root):
                raise ValueError(f"Unsafe archive member path detected: {info.filename!r}")
            if info.is_dir():
                member.mkdir(parents=True, exist_ok=True)
                continue
            member.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info, "r") as src_f, open(member, "wb") as dst_f:
                shutil.copyfileobj(src_f, dst_f)


def _overlay_repo_files(repo_root: Path, snapshot_dir: Path) -> None:
    for rel, overwrite in [(r, True) for r in ALWAYS_OVERLAY_FILES] + [(r, False) for r in FALLBACK_OVERLAY_FILES]:
        src, dst = repo_root / rel, snapshot_dir / rel
        if src.is_file() and (overwrite or not dst.is_file()):
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def assert_no_private_files(output_dir: Path) -> None:
    """Verify zero private key, vault, PID, PDF, or `.env*` files exist in `output_dir`."""
    bad = [
        rel for p in output_dir.rglob("*")
        if p.is_file() and _PRIVATE_OUTPUT_RE.search(rel := p.relative_to(output_dir).as_posix())
    ]
    if bad:
        raise RuntimeError(f"Privacy violation in built documentation output ({output_dir}): {bad}")


def _run_mkdocs_build(project_dir: Path, site_out: Path, git_ref: str, slug: str, base_url: str, strict: bool) -> None:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["CIS_DOCS_REF"] = "main" if git_ref in {"WORKTREE", "origin/main", "main", "HEAD"} else git_ref
    env["CIS_DOCS_SITE_URL"] = f"{base_url.rstrip('/')}/{slug}/"
    cmd = [sys.executable, "-m", "mkdocs", "build", "-f", str(project_dir / "mkdocs.yml"), "-d", str(site_out)]
    if strict:
        cmd.append("--strict")
    subprocess.run(cmd, cwd=str(project_dir), env=env, check=True)  # nosec B603


def build_single_version(
    repo_root: Path, git_ref: str, version_slug: str, output_dir: Path, base_url: str, strict: bool = True
) -> Path:
    """Build a single documentation version (`WORKTREE` or Git archive snapshot)."""
    ref = _validate_git_ref(git_ref)
    ver_out = output_dir / version_slug
    ver_out.parent.mkdir(parents=True, exist_ok=True)
    if ref == "WORKTREE":
        _run_mkdocs_build(repo_root, ver_out, ref, version_slug, base_url, strict)
    else:
        with tempfile.TemporaryDirectory(prefix=f"cis-docs-{version_slug}-") as tmp:
            arc, snap = Path(tmp) / "snapshot.zip", Path(tmp) / "src"
            snap.mkdir(parents=True, exist_ok=True)
            subprocess.run(  # nosec B603, B607
                ["git", "-C", str(repo_root), "archive", "--format=zip", "-o", str(arc), ref], check=True
            )
            _safe_extract_zip(arc, snap)
            _overlay_repo_files(repo_root, snap)
            _run_mkdocs_build(snap, ver_out, ref, version_slug, base_url, strict)
    assert_no_private_files(ver_out)
    return ver_out


def build_versioned_site(
    repo_root: Path, output_dir: Path, base_url: str = DEFAULT_BASE_URL,
    main_ref: str = "WORKTREE", tags: list[str] | None = None, skip_tags: bool = False, strict: bool = True,
) -> dict[str, object]:
    """Build the multi-version site bundle with redirects, `.htaccess`, and `versions.json`."""
    r_repo, r_out = repo_root.resolve(), output_dir.resolve()
    protected = {r_repo / name for name in _PROTECTED}
    if r_out == r_repo or r_repo.is_relative_to(r_out) or any(r_out == p or r_out.is_relative_to(p) for p in protected):
        raise ValueError(f"Output directory must not overwrite repository or protected paths: {r_out}")

    if r_out.exists():
        shutil.rmtree(r_out)
    r_out.mkdir(parents=True, exist_ok=True)

    rel_tags = [] if skip_tags else (_sort_tags_descending(tags) if tags is not None else discover_release_tags(r_repo))
    manifest = build_versions_manifest(rel_tags, include_main=True)
    (r_out / "versions.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    build_single_version(r_repo, main_ref, "main", r_out, base_url, strict)
    for tag in rel_tags:
        build_single_version(r_repo, tag, tag, r_out, base_url, strict)

    latest = rel_tags[0] if rel_tags else "main"
    (r_out / ".htaccess").write_text(render_htaccess(latest, "main"), encoding="utf-8")
    (r_out / "index.html").write_text(render_redirect_html(f"./{latest}/"), encoding="utf-8")
    for alias, tgt, ttl in (
        ("latest", f"../{latest}/", f"CIS Benchmarks Tools Documentation ({latest})"),
        ("dev", "../main/", "CIS Benchmarks Tools Documentation (main / dev)"),
    ):
        (r_out / alias).mkdir(parents=True, exist_ok=True)
        (r_out / alias / "index.html").write_text(render_redirect_html(tgt, ttl), encoding="utf-8")

    assert_no_private_files(r_out)
    return {"output_dir": str(r_out), "latest_version": latest, "versions": [e["version"] for e in manifest]}


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for versioned MkDocs Material site generation."""
    parser = argparse.ArgumentParser(description="Build versioned CIS Benchmarks MkDocs Material docs.")
    parser.add_argument("--output", default="site_dist", help="Output directory (default: site_dist).")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help=f"Base URL (default: {DEFAULT_BASE_URL}).")
    parser.add_argument("--main-ref", default="WORKTREE", help="Git ref for /main/ (default: WORKTREE).")
    parser.add_argument("--tags", nargs="*", default=None, help="Explicit release tags (space/comma-separated).")
    parser.add_argument("--skip-tags", action="store_true", help="Skip release tags and build only /main/.")
    parser.add_argument("--no-strict", action="store_true", help="Disable MkDocs --strict checks.")
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[1]), help="Repository root.")
    args = parser.parse_args(argv)

    explicit = [x.strip() for raw in args.tags for x in raw.split(",") if x.strip()] if args.tags is not None else None
    summary = build_versioned_site(
        Path(args.repo_root), Path(args.output), args.base_url, args.main_ref, explicit, args.skip_tags, not args.no_strict
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
