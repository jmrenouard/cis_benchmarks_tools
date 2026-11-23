"""Unit and E2E tests for versioned MkDocs Material publishing and IONOS hosting (100% PSL)."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
HOOKS, BUILD = ROOT / "scripts/mkdocs_hooks.py", ROOT / "scripts/build_versioned_docs.py"
PORTAL, REPO = "https://cis-benchmarks.lightpath.fr", "https://github.com/jmrenouard/cis_benchmarks_tools"


class _Cfg(dict):
    def __getattr__(self, k: str):
        if k in self:
            return self[k]
        raise AttributeError(k)

    __setattr__ = dict.__setitem__


def _load(name: str, path: Path):
    sys.path.insert(0, str(path.parent))
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        return mod
    finally:
        sys.path.remove(str(path.parent))


class TestMkDocsPublishing(unittest.TestCase):
    """Validate mkdocs.yml, hooks, multi-version site builder, and E2E build."""

    def setUp(self) -> None:
        self._td = tempfile.TemporaryDirectory()
        self.tmp = Path(self._td.name)
        self.addCleanup(self._td.cleanup)

    def test_mkdocs_yml_assets_and_requirements(self) -> None:
        mk = (ROOT / "mkdocs.yml").read_text("utf-8")
        toks = (
            PORTAL, "jmrenouard/cis_benchmarks_tools", "docs_dir: docs", "scripts/mkdocs_hooks.py", "name: material",
            "navigation.tabs", "navigation.indexes", "provider: mike", "default: latest", "stylesheets/extra.css",
            "javascripts/katex.js", "katex.min.js", "auto-render.min.js", "admonition", "pymdownx.arithmatex",
            "generic: true", "pymdownx.superfences", "name: mermaid", "class: mermaid", "fence_code_format",
            "*.kdbx", "*.keyx", "*.pid", ".env",
        )
        self.assertTrue(all(t in mk for t in toks))
        nav = re.split(r"\n(?=[A-Za-z0-9_]+:)", mk.split("\nnav:", 1)[1], maxsplit=1)[0].splitlines()
        self.assertEqual([m.group(1).strip() for l in nav if (m := re.match(r"^  -\s+['\"]?([^'\":\n]+?)['\"]?:", l))],
                         ["Home", "Tutorials", "How-To Guides", "Reference", "Explanation", "Releases & Governance"])
        self.assertTrue(all((ROOT / p).is_file() for p in (
            "docs/index.md", "docs/stylesheets/extra.css", "docs/assets/logo.svg", "docs/assets/header-banner.svg")))
        kjs, rq, gi = [(ROOT / p).read_text("utf-8") for p in
                       ("docs/javascripts/katex.js", "requirements-docs.txt", ".gitignore")]
        self.assertTrue("document$.subscribe" in kjs and "renderMathInElement" in kjs and "site_dist/" in gi)
        self.assertTrue(".worktrees/" in gi and all(
            p in rq for p in ("mkdocs>=", "mkdocs-material>=", "pymdown-extensions>=")))

    def test_hooks_alerts_slugify_and_importability_without_mkdocs(self) -> None:
        blk = {m: None for m in ("mkdocs", "mkdocs.structure", "mkdocs.structure.files", "pathspec", "pathspec.gitignore")}
        with patch.dict(sys.modules, blk):
            h = _load("mkdocs_hooks_nodeps", HOOKS)
            try:
                s = ("> [!NOTE]\n> A\n\n> [!TIP]\n> B\n\n> [!IMPORTANT]\n> C\n\n> [!WARNING]\n> D\n\n"
                     "> [!CAUTION]\n> E\n\n```md\n> [!NOTE]\n> K\n```\n")
                out, fen = h.convert_github_alerts(s).split("```md", 1)
                self.assertTrue(all(a in out for a in ("!!! note", "!!! tip", "!!! info", "!!! warning", "!!! danger")))
                self.assertTrue("> [!NOTE]" in fen and not any(
                    f"[!{t}]" in out for t in ("NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION")))
                self.assertEqual((h.gfm_slugify("Docs & Hub"), h.gfm_slugify("cli_flags"),
                                  h.gfm_slugify("Évaluation (18)")), ("docs--hub", "cli_flags", "évaluation-18"))
                (self.tmp / "docs").mkdir()
                (self.tmp / "docs/index.md").write_text("# H\n", encoding="utf-8")
                cfg = _Cfg({"docs_dir": str(self.tmp / "docs"), "site_url": "", "edit_uri": "", "mdx_configs": {}, "nav": []})
                h.on_config(cfg)
                self.assertEqual(cfg["edit_uri"], "edit/main/docs/")
            finally:
                sys.modules.pop("mkdocs_hooks_nodeps", None)

    def test_hooks_rewrite_relative_links_and_exclusions(self) -> None:
        h = _load("mkdocs_hooks", HOOKS)
        ov = ('<img src="docs/assets/logo.svg" />\n[E](README.md) [F](README_fr.md) [R](ROADMAP.md) [P](docs/index.md) '
              '[S](documentation/specifications/architecture.md) [C](audit_cis.py) [K](s.kdbx) [X](v.keyx) [P](d.pid) '
              '[E](.env) [R](id_rsa) [B](CIS_DATA/b.pdf)\n```md\n[Keep](README_fr.md)\n```\n')
        out, fen = h.rewrite_relative_links(ov, "overview-en.md", ref="v2.10.0").split("```md", 1)
        self.assertTrue(all(x in out for x in (
            '<img src="../assets/logo.svg"', "](overview-en.md)", "](overview-fr.md)", "](ROADMAP.md)",
            "](index.md)", "](specs/architecture.md)", f"]({REPO}/blob/v2.10.0/audit_cis.py)")))
        self.assertTrue("[Keep](README_fr.md)" in fen and not any(
            b in out for b in ("s.kdbx", "v.keyx", "d.pid", "(.env)", "id_rsa", "b.pdf")))
        self.assertIn('<img src="assets/logo.svg"', h.rewrite_relative_links(
            '<img src="docs/assets/logo.svg" />', "overview-en.md", use_directory_urls=False))
        d2 = h.rewrite_relative_links(
            "[R](../../../README.md) [S](../../../documentation/specifications/reporting-and-metrics.md) "
            "[A](../../../audit_cis.py) [Ref](../../03-reference/index.md)",
            "02-how-to-guides/deployment/run-remote-ssh-and-docker-audits.md", ref="main")
        self.assertTrue(all(x in d2 for x in (
            "](../../overview-en.md)", "](../../specs/reporting-and-metrics.md)",
            f"]({REPO}/blob/main/audit_cis.py)", "](../../03-reference/index.md)")))

    def test_hooks_historical_tag_fallbacks_and_nav_pruning(self) -> None:
        h, dd = _load("mkdocs_hooks", HOOKS), self.tmp / "docs"
        for rel in ("README.md", ".agents/AGENTS.md", "reports/mariadb_manual_controls_justification.md",
                    "archive/scripts/standardize_generate_html_report.py", "docs/index.md", "docs/ACTION_LOGBOOK.md",
                    "docs/RELEASE_NOTES_v2.9.0.md", "docs/RELEASE_NOTES_v2.9.1.md", "docs/RELEASE_NOTES_v2.10.0.md"):
            (self.tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.tmp / rel).write_text("# x\n", encoding="utf-8")
        lrw = h.rewrite_relative_links(
            "[A](.agents/AGENTS.md) [M](reports/mariadb_manual_controls_justification.md) "
            "[S](../scripts/standardize_generate_html_report.py)", "ACTION_LOGBOOK.md", ref="v2.9.1", docs_dir=dd)
        self.assertTrue(
            f"{REPO}/blob/v2.9.1/.agents/AGENTS.md" in lrw and "](.agents/AGENTS.md)" not in lrw
            and f"{REPO}/blob/v2.9.1/reports/mariadb_manual_controls_justification.md" in lrw)
        self.assertEqual(h.rewrite_relative_links(
            "[T](01-tutorials/index.md) [H](02-how-to-guides/index.md)", "index.md", ref="v2.9.0",
            docs_dir=dd, available_root_docs=("overview-en.md", "specs/project-governance.md"),
        ), "[T](overview-en.md) [H](overview-en.md)")
        self.assertEqual(h.rewrite_relative_links("[H](02-how-to-guides/index.md)", "index.md", ref="v2.10.0",
                                                  docs_dir=dd), "[H](specs/execution-contexts.md)")
        nav = [{"Home": "index.md"}, {"HT": ["02-how-to-guides/x.md"]}, {"Exp": [{"EN": "overview-en.md"},
               {"FR": "overview-fr.md"}]}, {"Releases & Governance": [{"R": "RELEASE_NOTES_v9.9.9.md"},
                                                                     {"Log": "ACTION_LOGBOOK.md"}]}]
        flat = json.dumps(h.prune_nav_for_existing_files(nav, dd, self.tmp))
        pos = [flat.index(f"RELEASE_NOTES_{v}.md") for v in ("v2.10.0", "v2.9.1", "v2.9.0")]
        self.assertTrue("Home" in flat and "HT" not in flat and "overview-en.md" in flat and "overview-fr.md" not in flat)
        self.assertEqual((pos, "v9.9.9" not in flat), (sorted(pos), True))

    def test_hooks_on_config_and_virtual_edit_url(self) -> None:
        h, dd = _load("mkdocs_hooks", HOOKS), self.tmp / "docs"
        dd.mkdir()
        (dd / "index.md").write_text("# H\n", encoding="utf-8")
        pg = SimpleNamespace(file=SimpleNamespace(src_uri="overview-en.md", src_path="overview-en.md"), edit_url="x")
        for ref, uri, eurl in (("WORKTREE", "edit/main/docs/", f"{REPO}/edit/main/README.md"), ("v2.10.0", "", None)):
            with patch.dict(os.environ, {"CIS_DOCS_REF": ref, "CIS_DOCS_SITE_URL": f"{PORTAL}/main"}):
                cfg = _Cfg({"docs_dir": str(dd), "site_url": "", "edit_uri": "x", "repo_url": REPO,
                            "mdx_configs": {"toc": {}}, "nav": [{"Home": "index.md"}]})
                h.on_config(cfg)
                h.on_page_markdown("# O\n", pg, cfg, None)
                self.assertEqual((cfg["edit_uri"], cfg["site_url"], pg.edit_url), (uri, f"{PORTAL}/main/", eurl))
                self.assertIs(cfg["mdx_configs"]["toc"]["slugify"], h.gfm_slugify)

    def test_builder_semver_manifest_htaccess_redirect_zip_and_privacy(self) -> None:
        b = _load("build_versioned_docs", BUILD)
        self.assertEqual((b.parse_semver_tag("v2.10.0"), b.parse_semver_tag("main")), ((2, 10, 0), None))
        man = b.build_versions_manifest(["v2.9.0", "v2.10.0", "v2.9.1"], include_main=True)
        self.assertEqual(([e["version"] for e in man], man[0]["aliases"], man[-1]["aliases"]),
                         (["v2.10.0", "v2.9.1", "v2.9.0", "main"], ["latest"], ["dev"]))
        self.assertEqual(b.build_versions_manifest([], include_main=True)[0]["aliases"], ["latest", "dev"])
        ht = b.render_htaccess("v2.10.0", main_version="main")
        self.assertTrue(all(t in ht for t in (
            "Options -Indexes -MultiViews", "DirectoryIndex index.html", "RewriteEngine On", "R=301", "R=302",
            "^latest(?:/(.*))?$", "/v2.10.0/$1", "^dev(?:/(.*))?$", "/main/$1",
            "ErrorDocument 404 /v2.10.0/404.html", "max-age=300")))
        rd = b.render_redirect_html("/v2.10.0/", "CIS Docs")
        self.assertTrue("<!doctype html>" in rd.lower() and "/v2.10.0/" in rd and 'http-equiv="refresh"' in rd.lower())
        evil, repo, priv = self.tmp / "e.zip", self.tmp / "repo", self.tmp / "priv"
        with zipfile.ZipFile(evil, "w") as zf:
            zf.writestr("../x.txt", "bad")
        with self.assertRaises(ValueError):
            b._safe_extract_zip(evil, self.tmp / "out")
        for s in ("docs", "scripts", "rules", "CIS_DATA", ".git"):
            (repo / s).mkdir(parents=True)
        for bad in (repo, self.tmp, repo / "docs", repo / "CIS_DATA", repo / ".git"):
            with self.assertRaisesRegex(ValueError, "protected"):
                b.build_versioned_site(repo_root=repo, output_dir=bad, skip_tags=True)
        priv.mkdir()
        (priv / ".env").write_text("S=1\n", encoding="utf-8")
        with self.assertRaises(RuntimeError):
            b.assert_no_private_files(priv)

    def test_builder_e2e_multi_version_worktree_and_tags(self) -> None:
        if importlib.util.find_spec("mkdocs") is None or not (ROOT / ".git").exists() or not shutil.which("git"):
            self.skipTest("mkdocs and git required")
        tags = set(subprocess.run(["git", "-C", str(ROOT), "tag", "--list"],
                                  capture_output=True, text=True).stdout.splitlines())
        if not {"v2.10.0", "v2.9.1", "v2.9.0"}.issubset(tags):
            self.skipTest("Tags unavailable")
        out = self.tmp / "site_dist"
        proc = subprocess.run(
            [sys.executable, str(BUILD), "--output", str(out), "--base-url", PORTAL,
             "--main-ref", "WORKTREE", "--tags", "v2.10.0", "v2.9.1", "v2.9.0"],
            cwd=str(ROOT), capture_output=True, text=True, check=False)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(all((out / r).is_file() for r in (
            "versions.json", "index.html", ".htaccess", "latest/index.html", "dev/index.html", "main/index.html",
            "main/stylesheets/extra.css", "main/javascripts/katex.js",
            "v2.10.0/index.html", "v2.9.1/index.html", "v2.9.0/index.html")))
        man = json.loads((out / "versions.json").read_text("utf-8"))
        self.assertEqual([e["version"] for e in man], ["v2.10.0", "v2.9.1", "v2.9.0", "main"])
        self.assertTrue("latest" in man[0]["aliases"] and "dev" in man[-1]["aliases"])


if __name__ == "__main__":
    unittest.main()
