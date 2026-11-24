"""MkDocs Material hooks for CIS Benchmarks Tools Suite documentation."""

from __future__ import annotations

import os
from pathlib import Path
import posixpath
import re
from typing import TYPE_CHECKING, Any, Iterable
from urllib.parse import urlsplit

if TYPE_CHECKING:
    from mkdocs.structure.files import Files

DEFAULT_REPO_URL = "https://github.com/jmrenouard/cis_benchmarks_tools"
VIRTUAL_DOCS: dict[str, tuple[str, str]] = {
    "overview-en.md": ("README.md", ""),
    "overview-fr.md": ("README_fr.md", ""),
    "ROADMAP.md": ("ROADMAP.md", ""),
}
for _n in (
    "architecture", "benchmark-targets", "execution-contexts",
    "project-governance", "reporting-and-metrics", "testing-and-quality-assurance",
):
    VIRTUAL_DOCS[f"specs/{_n}.md"] = (f"documentation/specifications/{_n}.md", "documentation/specifications")
_R2V = {s: u for u, (s, _) in VIRTUAL_DOCS.items()}
QUADRANT_HISTORICAL_FALLBACKS = {
    "01-tutorials": "overview-en.md", "02-how-to-guides": "specs/execution-contexts.md",
    "03-reference": "specs/benchmark-targets.md", "04-explanation": "specs/architecture.md",
    "fr": "overview-fr.md",
}
ALERT_MAP = {"NOTE": "note", "TIP": "tip", "IMPORTANT": "info", "WARNING": "warning", "CAUTION": "danger"}
_FENCE_RE = re.compile(r"(?ms)^[ \t]*(`{3,}|~{3,})[^\r\n]*\r?\n.*?(?:^[ \t]*\1[ \t]*(?:\r?\n|\Z)|\Z)")
_ALERT_RE = re.compile(
    r"(?m)^([ \t]*)>[ \t]*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\][ \t]*([^\r\n]*)\r?\n((?:[ \t]*>.*(?:\r?\n|$))*)"
)
_CODE_RE = re.compile(r"(?s)(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)")
_REL_RE = re.compile(r"^RELEASE_NOTES_v?(\d+)\.(\d+)\.(\d+)\.md$")
_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
_EXCLUDED_TARGET_RE = re.compile(
    r"(?i)(?:(?:^|/)(?:\.env[^/]*|id_rsa[^/]*)$|\.(?:kdbx|keyx|pid)$|(?:^|/)CIS_DATA/.*\.pdf$)"
)
_HTML_RE = re.compile(r"""(<(?:img|a|source)\b[^>]*?\b(?:src|href)\s*=\s*)(["'])([^"']+)\2""", re.I)
_MD_RE = re.compile(
    r"(!?)\[((?:[^\[\]\\]|\\.|\[(?:[^\[\]\\]|\\.)*\])*)\]"
    r"\(\s*(?:<([^>\n]+)>|([^\s()\n]+(?:\([^()\n]*\)[^\s()\n]*)*))([^)\n]*)\)"
)


def gfm_slugify(value: str, separator: str = "-") -> str:
    """Slugify headings with GitHub Flavored Markdown rules."""
    return "".join(separator if c == " " else c for c in value.strip().lower() if c.isalnum() or c in " -_")


def _ref(raw=None) -> str:
    r = (raw if raw is not None else os.environ.get("CIS_DOCS_REF", "main")).strip()
    return "main" if not r or r in {"WORKTREE", "HEAD", "origin/main"} else r


def _outside_fences(md: str, fn) -> str:
    out, pos = [], 0
    for m in _FENCE_RE.finditer(md):
        if m.start() > pos:
            out.append(fn(md[pos : m.start()]))
        out.append(m[0])
        pos = m.end()
    return "".join(out) + (fn(md[pos:]) if pos < len(md) else "")


def convert_github_alerts(markdown: str) -> str:
    """Convert GitHub blockquote alerts into Material admonitions."""

    def _sub(m) -> str:
        ws, k, ttl = m[1], ALERT_MAP[m[2].upper()], m[3].strip()
        hdr = f'{ws}!!! {k} "{ttl}"\n' if ttl else f"{ws}!!! {k}\n"
        return hdr + "".join(
            f"{ws}    {b}" if (b := re.sub(r"^[ \t]*>[ \t]?", "", ln)).strip() else ln[len(ln.rstrip("\r\n")) :] or "\n"
            for ln in m[4].splitlines(keepends=True)
        )

    return _outside_fences(markdown, lambda s: _ALERT_RE.sub(_sub, s))


def _lang(config: Any) -> str:
    th = config.get("theme") if isinstance(config, dict) else getattr(config, "theme", None)
    v = (th.get("language") if hasattr(th, "get") else getattr(th, "language", None)) if th is not None else None
    return "fr" if str(v or "en").lower().startswith("fr") else "en"


def rewrite_relative_links(
    markdown: str, page_src_path: str, ref: str = "main", repo_url: str = DEFAULT_REPO_URL,
    docs_dir: Path | None = None, use_directory_urls: bool = True, available_root_docs: Iterable[str] | None = None,
    included_docs: Iterable[str] | None = None, lang: str = "en",
) -> str:
    """Rewrite repository-relative Markdown and HTML links outside fences."""
    src = page_src_path.replace("\\", "/").lstrip("/")
    d = src.count("/")
    flat = not use_directory_urls or src == "index.md" or src.endswith("/index.md")
    mp, hp = "../" * d, "../" * (d + (0 if flat else 1))
    rr, repo = _ref(ref), repo_url.rstrip("/")
    rt = frozenset(VIRTUAL_DOCS if available_root_docs is None else available_root_docs)
    inc = frozenset(included_docs) if included_docs is not None else None
    docs = Path(docs_dir) if docs_dir else None
    root = docs.parent if docs else None
    fr_home = lang == "fr" and src == "index.md" and docs and (docs / "fr/index.md").is_file()
    sd = VIRTUAL_DOCS[src][1] if src in VIRTUAL_DOCS else ("docs/fr" if fr_home else posixpath.dirname(f"docs/{src}"))

    def _gh(rel, sl, an):
        kind = "tree" if sl or (root and (root / rel).is_dir()) else "blob"
        return f"{repo}/{kind}/{rr}/{rel}{'/' if sl and not rel.endswith('/') else ''}{an}"

    def _vt(u, px, an=""):
        return f"{px}{u}{an}" if u in rt else f"{repo}/blob/{rr}/{VIRTUAL_DOCS[u][0]}{an}"

    def _res(raw, px):
        if not raw or raw.startswith(("#", "/", "\\")) or _SCHEME_RE.match(raw):
            return raw, False
        path, sep, frag = raw.partition("#")
        if not path:
            return raw, False
        an, sl = sep + frag, path.endswith("/")
        rel = posixpath.normpath(posixpath.join(sd, path)) if sd else posixpath.normpath(path)
        if _EXCLUDED_TARGET_RE.search(rel) or _EXCLUDED_TARGET_RE.search(path):
            return None, True
        if rel in _R2V:
            return _vt(_R2V[rel], px, an), False
        if rel == "docs/index.md" or (lang == "fr" and rel in {"docs/fr/index.md", "docs/index_fr.md"}):
            if rel == "docs/index.md" and lang == "fr" and inc is not None and "index.md" in inc:
                return _gh(rel, sl, an), False
            return f"{px}index.md{an}", False
        if not rel.startswith("docs/"):
            return (repo if rel in (".", "..") or rel.startswith("../") else _gh(rel, sl, an)), False
        sub = rel[5:]
        if lang == "fr" and sub == "fr/index.md":
            return _vt("index.md", px, an), False
        if sub in VIRTUAL_DOCS and (not docs or not (docs / sub).is_file()):
            return _vt(sub, px, an), False
        ov_px = _vt("overview-fr.md", px) if lang == "fr" else _vt("overview-en.md", px)
        if docs:
            top = sub.split("/", 1)[0]
            if top in QUADRANT_HISTORICAL_FALLBACKS and not (docs / top).is_dir():
                fb = "overview-fr.md" if lang == "fr" and top == "03-reference" else QUADRANT_HISTORICAL_FALLBACKS[top]
                ok = (((docs / fb).is_file() and (inc is None or fb in inc)) or fb in rt)
                return (f"{px}{fb}" if ok else ov_px), False
            if root and not (docs / sub).exists() and (root / sub).exists():  # v2.10.0 root links
                return _gh(sub, sl, an), False
            tag_root = "fr" if lang == "fr" else "01-tutorials"
            if src == "index.md" and not (docs / tag_root).is_dir() and not (docs / sub).exists() and sub not in rt:
                if sub.startswith("RELEASE_NOTES_") and lang != "fr":
                    for c in ("ROADMAP.md", "ACTION_LOGBOOK.md"):
                        if c in rt or (docs / c).is_file():
                            return f"{px}{c}", False
                return ov_px, False
            if (docs / sub).is_dir() and (docs / sub / "index.md").is_file():
                cand = f"{posixpath.join(sub.rstrip('/'), 'index.md')}"
                return (_gh(rel, sl, an) if inc is not None and cand not in inc else f"{px}{cand}{an}"), False
        if inc is not None and sub not in inc:
            return _gh(rel, sl, an), False
        return f"{px}{sub}{'/' if sl and sub and not sub.endswith('/') else ''}{an}", False

    def _rw(text):
        def _sub(m):
            if (m.start() - len(text[: m.start()].rstrip("\\"))) & 1:
                return m[0]
            img, lbl, u1, u2, sfx = m.groups()
            lbl = _rw(lbl) if "[" in lbl else lbl
            res, blk = _res(u1.strip() if u1 is not None else u2, mp)
            return ("" if img else lbl) if blk else f"{img}[{lbl}]({f'<{res}>' if u1 is not None else res}{sfx})"

        return _MD_RE.sub(_sub, text)

    def _chunk(chunk):
        sp = []
        mk = _CODE_RE.sub(lambda m: sp.append(m[0]) or f"\uE000{len(sp) - 1}\uE001", chunk)
        rw = _HTML_RE.sub(
            lambda m: f"{m[1]}{m[2]}{'#' if (r := _res(m[3], hp))[1] else r[0]}{m[2]}", _rw(mk)
        )
        return re.sub(r"\uE000(\d+)\uE001", lambda m: sp[int(m[1])], rw)

    return _outside_fences(markdown, _chunk)


def _discover_notes(docs: Path):
    found = []
    for p in docs.glob("RELEASE_NOTES_*.md") if docs.is_dir() else ():
        if p.is_file():
            m = _REL_RE.match(p.name)
            v = (int(m[1]), int(m[2]), int(m[3])) if m else (0, 0, 0)
            lbl = f"Release Notes v{v[0]}.{v[1]}.{v[2]}" if m else f"Release Notes {p.stem[14:]}"
            found.append((bool(m), v, lbl, p.name))
    return [{lbl: fn} for _, _, lbl, fn in sorted(found, key=lambda x: x[:3], reverse=True)]


def _prune_nav(items, docs: Path, root: Path, rel: bool = False):
    def _ok(p):
        return (docs / p).is_file() or (p in VIRTUAL_DOCS and (root / VIRTUAL_DOCS[p][0]).is_file())

    out, slot = [], -1
    for e in items:
        st, kp = isinstance(e, str), {}
        for k, v in ([(None, e)] if st else e.items() if isinstance(e, dict) else ()):
            if isinstance(v, str) and rel and Path(v).name.startswith("RELEASE_NOTES_"):
                slot = len(out) if slot < 0 else slot
            elif isinstance(v, str) and _ok(v):
                if st:
                    out.append(v)
                else:
                    kp[k] = v
            elif isinstance(v, list) and (s := _prune_nav(v, docs, root, k == "Releases & Governance")):
                kp[k] = s
            elif isinstance(v, dict) and (s := _prune_nav([v], docs, root)):
                kp[k] = s[0]
        if kp:
            out.append(kp)
    if rel and (notes := _discover_notes(docs)):
        if slot < 0:
            mk = {"ROADMAP.md", "CHANGELOG.md"}
            slot = next((i + 1 for i, x in enumerate(out) if isinstance(x, dict) and next(iter(x.values())) in mk), 0)
        out[slot:slot] = notes
    return out


def prune_nav_for_existing_files(nav: list[Any] | None, docs_dir: Path, repo_root: Path) -> list[Any]:
    """Prune missing pages and empty sections; auto-discover release notes."""
    return _prune_nav(list(nav), Path(docs_dir), Path(repo_root)) if nav else []


def on_config(config: Any) -> Any:
    """Apply env `site_url`, `edit_uri`, GFM slugifier, and pruned nav."""
    if url := os.environ.get("CIS_DOCS_SITE_URL", "").strip():
        config.site_url = url.rstrip("/") + "/"
    config.edit_uri = "edit/main/docs/" if _ref() == "main" else ""
    if isinstance(ex := getattr(config, "extra", None), dict) and isinstance(alt := ex.get("alternate"), list):
        bp = urlsplit(str(getattr(config, "site_url", "") or "")).path.rstrip("/")
        bp = bp[:-3] if bp.endswith("/fr") else bp
        if bp:
            for item in alt:
                if isinstance(item, dict) and item.get("lang") in {"en", "fr"}:
                    item["link"] = f"{bp}/fr/" if item["lang"] == "fr" else f"{bp}/"
    if isinstance(mdx := getattr(config, "mdx_configs", None), dict):
        toc = mdx.setdefault("toc", {})
        if isinstance(toc, dict) and not toc.get("slugify"):
            toc["slugify"] = gfm_slugify
    if getattr(config, "nav", None):
        docs = Path(config.docs_dir)
        config.nav = prune_nav_for_existing_files(config.nav, docs, docs.parent)
    return config


def on_files(files: Files, config: Any) -> Files:
    """Exclude private files and mount virtual root overviews, roadmap, and specs."""
    from mkdocs.structure.files import File, Files as MkDocsFiles, InclusionLevel

    lang, docs = _lang(config), Path(config.docs_dir)
    root = docs.parent
    fr_idx = (docs / "fr/index.md") if (docs / "fr/index.md").is_file() else (root / "README_fr.md")
    kept = []
    for f in list(files):
        if _EXCLUDED_TARGET_RE.search(f.src_uri):
            f.inclusion = InclusionLevel.EXCLUDED
        elif lang == "fr" and f.src_uri in {"index.md", "fr/index.md"} and fr_idx.is_file():
            continue
        else:
            kept.append(f)
    if len(kept) != len(files):
        files = MkDocsFiles(kept)
    allowed = {"overview-fr.md"} if lang == "fr" else {u for u in VIRTUAL_DOCS if u != "overview-fr.md"}
    for uri, (rel, _) in VIRTUAL_DOCS.items():
        if uri in allowed and (src := root / rel).is_file() and files.get_file_from_path(uri) is None:
            files.append(File.generated(config, uri, abs_src_path=str(src)))
    if lang == "fr" and fr_idx.is_file() and files.get_file_from_path("index.md") is None:
        idx_f = File.generated(config, "index.md", abs_src_path=str(fr_idx))
        idx_f.inclusion = InclusionLevel.INCLUDED
        files.append(idx_f)
    return files


def on_page_markdown(markdown: str, page: Any, config: Any, files: Files) -> str:
    """Convert alerts, rewrite links, and adjust virtual edit URLs."""
    src = getattr(page.file, "src_uri", None) or str(page.file.src_path).replace("\\", "/")
    ref, repo, lang = _ref(), (getattr(config, "repo_url", None) or DEFAULT_REPO_URL).rstrip("/"), _lang(config)
    rd = config.get("docs_dir") if isinstance(config, dict) else getattr(config, "docs_dir", None)
    docs = Path(rd) if rd else None
    if src in VIRTUAL_DOCS:
        page.edit_url = f"{repo}/edit/main/{VIRTUAL_DOCS[src][0]}" if ref == "main" else None
    elif lang == "fr" and src == "index.md" and docs:
        ed = "docs/fr/index.md" if (docs / "fr/index.md").is_file() else "README_fr.md"
        page.edit_url = f"{repo}/edit/main/{ed}" if ref == "main" else None
    av = [u for u in VIRTUAL_DOCS if files.get_file_from_path(u)] if files else None
    inc = [f.src_uri for f in files if getattr(f.inclusion, "is_included", lambda: True)()] if files else None
    return rewrite_relative_links(
        convert_github_alerts(markdown), src, ref, repo,
        docs, bool(getattr(config, "use_directory_urls", True)), av, inc, lang,
    )
