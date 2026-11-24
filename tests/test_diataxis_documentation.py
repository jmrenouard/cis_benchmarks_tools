"""Diataxis 4-quadrant, ASD-STE100 Issue 9, and Docs-as-Code test suite (100% PSL)."""

from __future__ import annotations

import configparser
import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PORTAL = "https://cis-benchmarks.lightpath.fr"
QUADS = ("01-tutorials", "02-how-to-guides", "03-reference", "04-explanation")
VIRTUAL = {"overview-en.md": "README.md", "overview-fr.md": "README_fr.md", "ROADMAP.md": "ROADMAP.md"}

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")
HTML_RE = re.compile(r"""<(?:img|a|source)\b[^>]*?\b(?:src|href)=["']([^"']+)["']""", re.I)
HEAD_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
TBL_RE = re.compile(r"^\s*(?:\|.*\||(?:[-*+]|\d+\.)\s+\S+)")
EXT_RE = re.compile(r"^(?:https?|mailto|ftp|tel|data):", re.I)
MATH_SP_RE = re.compile(r"(?<!\\)\$[ \t]+[^\s\d$\n][^\n$]*?(?<!\\)\$|(?<!\\)\$[^\s\d$\n][^\n$]*?[ \t]+(?<!\\)\$")
ING_OK = frozenset("during missing remaining opening routing servicing something string thing ring".split())
MODALS = frozenset({"should", "would", "may", "might", "shall", "ought"})
NON_PART = frozenset("between even green need often open red screen seed seven speed when".split())
_IRR = (
    "been|done|made|gone|put|set|cut|kept|held|taken|given|found|left|lost|sent|shown|told|"
    "built|broken|brought|come|fallen|felt|got|known|read|run|seen|written|sold"
)
_PART = rf"(?:[a-z]{{2,}}(?:ed|en)|{_IRR})"
STE_RULES = (
    ("GR-6", re.compile(r"(?<![A-Za-z])(?:e\.g\.|i\.e\.|etc\.)(?![A-Za-z])", re.I), frozenset()),
    ("Rule 4.2", re.compile(r"\b\w+n['\u2019]t\b|\b\w+['\u2019](?:re|ll|ve|m|d)\b|\b(?:it|that)['\u2019]s\b", re.I),
     frozenset()),
    ("Rule 3.4", re.compile(rf"\b(?:has|have|had)\s+(?:not\s+|never\s+)?(?:[a-z]{{2,}}ed|{_IRR})\b", re.I), NON_PART),
    ("Rule 3.4", re.compile(rf"\b(?:can|will|must|could|would|should|may|might|shall)\s+(?:not\s+)?be\s+{_PART}\b",
                            re.I), NON_PART),
    ("Rule 3.6", re.compile(rf"\b(?:is|are|was|were|be|been|being)\s+(?:\w+\s+)?{_PART}(?=\s+by\b)", re.I), NON_PART),
    ("Rule 3.5", re.compile(r"\b(?:is|are|was|were|be|been|am)\s+[a-z]+ing\b", re.I), ING_OK),
)
UNIT_RE = re.compile(r"(?<!\w)[+-]?\d+(?:[.,:]\d+)*\s*(?:seconds?|minutes?|hours?|percent|KiB|MiB|GiB|KB|MB|ms|%)(?!\w)")
SENT_RE = re.compile(r"(?<!No\.)(?<!e\.g\.)(?<!i\.e\.)(?<!etc\.)(?<=[.!?:])\s+")
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[.'&/\u2019-][A-Za-z0-9]+)*")


def _non_code(text: str) -> list[tuple[int, str]]:
    out, fc, fl = [], "", 0
    for ln, raw in enumerate(text.splitlines(), 1):
        if fc:
            if re.match(rf"^\s*{re.escape(fc)}{{{fl},}}\s*$", raw):
                fc = ""
        elif m := FENCE_RE.match(raw):
            fc, fl = m.group(1)[0], len(m.group(1))
        else:
            out.append((ln, re.sub(r"``[^`\n]+``|`[^`\n]+`", " ", raw)))
    return out


def _links(md: Path) -> list[tuple[int, str, Path]]:
    res: list[tuple[int, str, Path]] = []
    for ln, line in _non_code(md.read_text("utf-8")):
        for m in [*LINK_RE.finditer(line), *HTML_RE.finditer(line)]:
            t = m.group(1).strip()
            t = t[1 : t.find(">")].strip() if t.startswith("<") and ">" in t else (t.split()[0] if t else "")
            if t and not t.startswith(("#", "//")) and not EXT_RE.match(t):
                if c := unquote(t.split("#", 1)[0].split("?", 1)[0].strip()):
                    res.append((ln, c, (DOCS / c.lstrip("/") if c.startswith("/") else md.parent / c).resolve()))
    return res


def _ste_sent(sent: str, loc: str) -> list[str]:
    cl = UNIT_RE.sub(" N ", re.sub(r"\([^()]*\)", " P ", sent))
    wc = len(WORD_RE.findall(re.sub(r"\*\*|__|#+|\*|(?<!\w)_|_(?!\w)", " ", cl)))
    errs = [f"{loc} [Rule 5.1]: {wc}w"] if wc > 20 else []
    if ";" in sent:
        errs.append(f"{loc} [Rule 8.1]: {sent[:35]!r}")
    pl = re.sub(r"\*\*|__|(?<!\w)_|_(?!\w)|\*", "", sent)
    for tag, rx, skip in STE_RULES:
        if (m := rx.search(pl)) and m.group(0).split()[-1].lower() not in skip:
            errs.append(f"{loc} [{tag}]: {m.group(0)!r}")
    errs.extend(f"{loc} [Rule 3.2]: {t!r}" for t in re.findall(r"[A-Za-z-]+", pl) if t.lower() in MODALS)
    return errs


def collect_ste_structural_violations(md: Path) -> list[str]:
    """Check Markdown file against ASD-STE100 Issue 9 structural rules."""
    t = re.sub(r"\A---\n.*?\n---(?:\n|\Z)|```.*?```|~~~.*?~~~", " ", md.read_text("utf-8").replace("\r\n", "\n"), flags=re.S)
    t = re.sub(r"(?<!\\)\$\$[\s\S]*?(?<!\\)\$\$|(?<!\\)\$(?!\s)[^\n$]+?(?<!\s)\$|`[^`\n]+`", " ", t)
    t = re.sub(r"!?\[([^\]]*)\]\((?:[^()]|\([^)]*\))*\)|https?://\S+", r"\1", t)
    t = re.sub(r"^[ \t]*(?:>.*|#.*|\|.*|---+|\*\*\*+|___+|===+)$|\"[^\"\n]*\"|\u201c[^\u201d\n]*\u201d", " ", t, flags=re.M)
    t, b_re, errs = re.sub(r"\n(?:  |\t)(?=\S)", " ", t), re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+"), []
    for idx, par in enumerate(re.split(r"\n\s*\n", t), 1):
        lines = par.strip().splitlines()
        prose = [ln for ln in lines if not b_re.match(ln) and WORD_RE.search(ln)]
        for ln in lines:
            if b_re.match(ln):
                for s in SENT_RE.split(b_re.sub("", ln, count=1)):
                    if WORD_RE.search(s):
                        errs.extend(_ste_sent(s.strip(), f"{md.name}:list"))
        if prose:
            sents = [s.strip() for s in SENT_RE.split("\n".join(prose)) if WORD_RE.search(s)]
            if len(sents) > 6:
                errs.append(f"{md.name}:par{idx} [Rule 6.6]: {len(sents)}")
            for s in sents:
                errs.extend(_ste_sent(s, f"{md.name}:par{idx}"))
    return errs


def _quads(md: Path) -> set[str]:
    return {r.relative_to(DOCS).parts[0] for _, _, r in _links(md)
            if r.is_relative_to(DOCS) and r.relative_to(DOCS).parts[0] in QUADS}


def _non_idx(quad: str) -> list[Path]:
    return [p for p in sorted((DOCS / quad).rglob("*.md")) if p.name.lower() != "index.md"]


_STF_BANNED_RE = re.compile(
    r"\b(?:devrait|devraient|pourrait|pourraient|serait|seraient|faudrait|éventuellement|"
    r"potentiellement|susceptible\s+de|il\s+faut|vous\s+devez|il\s+convient\s+de|"
    r"il\s+est\s+nécessaire\s+de|afin\s+de|à\s+l'aide\s+de|procéder\s+à|via)\b|"
    r"\b(?:e\.g\.|i\.e\.|etc\.|cf\.)", re.I)
_BOX_DRAW_RE = re.compile(r"[\u2500-\u257f]")
_MERMAID_TYPES = (
    "flowchart", "graph", "sequencediagram", "classdiagram", "statediagram",
    "erdiagram", "gantt", "pie", "gitgraph", "mindmap", "timeline",
)


def _fenced_blocks(text: str) -> list[tuple[int, int, str, str]]:
    """Extract (lineno, indent, lang, body) for every fenced code block."""
    blocks: list[tuple[int, int, str, str]] = []
    cur: tuple[int, int, str, list[str]] | None = None
    for idx, line in enumerate(text.splitlines(), 1):
        m = re.match(r"^( *)```(.*)$", line)
        if m and cur is None:
            cur = (idx, len(m.group(1)), m.group(2).strip().lower(), [])
        elif m and cur is not None and not m.group(2).strip():
            blocks.append((cur[0], cur[1], cur[2], "\n".join(cur[3])))
            cur = None
        elif cur is not None:
            cur[3].append(line)
    return blocks


def collect_stf_structural_violations(md: Path) -> list[str]:
    """Validate ASD-STF100 structural rules on French procedural guides."""
    out: list[str] = []
    for ln, raw in _non_code(md.read_text("utf-8")):
        line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", raw.strip())
        line = re.sub(r"`[^`]+`", "code", line)
        if not line or line.startswith(("#", "|", "---")):
            continue
        is_note = bool(re.match(r"^(?:\*\*)?NOTE\s*:", line, re.I))
        body = re.sub(r"^(?:[-*+]|\d+\.)\s+|\*\*(?:ATTENTION|AVERTISSEMENT|NOTE)\s*:\*\*\s*", "", line)
        for sent in (s.strip() for s in re.split(r"(?<=[.!?])\s+", body) if s.strip()):
            if ";" in sent:
                out.append(f"{md.name}:{ln}: semicolon violates ASD-STF100 Rule 8.1")
            if _STF_BANNED_RE.search(sent):
                out.append(f"{md.name}:{ln}: disallowed STF modal/phrase in {sent!r}")
            words = [w for w in re.findall(r"[^\s,;:.!?]+", sent) if w]
            limit = 25 if is_note else 20
            if len(words) > limit:
                out.append(f"{md.name}:{ln}: sentence length {len(words)} > {limit}")
    return out


class TestDiataxisDocumentation(unittest.TestCase):
    """Validate Diataxis structure, links, genre rules, STE compliance, math, and configs."""

    def test_diataxis_quadrant_structure_and_indexes_exist(self) -> None:
        self.assertTrue((DOCS / "index.md").is_file())
        for q in QUADS:
            self.assertTrue((DOCS / q / "index.md").is_file() and bool(_non_idx(q)), q)

    def test_zero_broken_relative_links_across_all_docs(self) -> None:
        self.assertEqual([
            f"{md.name}:{ln}:{tgt}" for md in sorted(DOCS.rglob("*.md")) for ln, tgt, res in _links(md)
            if not (res.is_file() or (res.is_dir() and (res / "index.md").is_file()))
        ], [])

    def test_quadrant_genre_guardrails_prevent_genre_mixing(self) -> None:
        issues: list[str] = []
        for q in QUADS[1:]:
            for md in _non_idx(q):
                nc = _non_code(md.read_text("utf-8"))
                hdrs = [(ln, m.group(1)) for ln, l in nc if (m := HEAD_RE.match(l))]
                body = "\n".join(l for _, l in nc)
                if q == "02-how-to-guides":
                    if not (re.search(r"\b(?:validat\w+|verif\w+|check)\b", body, re.I)
                            and re.search(r"\b(?:rollback|revert|backout|back-out|undo)\b", body, re.I)):
                        issues.append(f"{md.name}:no-val-rb")
                    issues.extend(f"{md.name}:{ln}:{h}" for ln, h in hdrs
                                  if re.search(r"\b(?:why|architecture|theory|explanation|context|background)\b", h, re.I))
                elif q == "03-reference":
                    if not any(TBL_RE.match(l) for _, l in nc):
                        issues.append(f"{md.name}:no-tbl")
                    issues.extend(f"{md.name}:{ln}:tut" for ln, l in nc if re.search(
                        r"\bin\s+this\s+tutorial\b|\blet['\u2019]?s\b|\blet\s+us\b|\bstep\s+1\b", l, re.I))
                else:
                    issues.extend(f"{md.name}:{ln}:{h}" for ln, h in hdrs
                                  if re.search(r"\b(?:step\s+\d+|rollback|remediation|prerequisites|procedure)\b", h, re.I))
        self.assertEqual(issues, [])

    def test_quadrant_cross_linking_mesh(self) -> None:
        tuts, hts = _non_idx("01-tutorials"), _non_idx("02-how-to-guides")
        adrs = sorted((DOCS / "04-explanation" / "design-decisions").glob("adr-*.md"))
        mx = DOCS / "03-reference" / "troubleshooting-codes" / "error-and-alert-matrix.md"
        self.assertTrue(tuts and hts and adrs and mx.is_file())
        self.assertTrue(all({"02-how-to-guides", "03-reference", "04-explanation"} <= _quads(d) for d in tuts))
        self.assertTrue(all({"03-reference", "04-explanation"} <= _quads(d) for d in hts))
        self.assertIn("02-how-to-guides", _quads(mx))
        self.assertTrue(all({"03-reference", "02-how-to-guides"} <= _quads(a) for a in adrs))

    def test_howto_guides_asd_ste100_structural_compliance(self) -> None:
        files = _non_idx("02-how-to-guides")
        self.assertEqual([v for md in files for v in collect_ste_structural_violations(md)], [] if files else ["empty"])

    def test_docs_as_code_configs_and_math_syntax_valid(self) -> None:
        mk = (ROOT / "mkdocs.yml").read_text("utf-8")
        self.assertTrue(all(x in mk for x in ("navigation.tabs", "navigation.indexes", "scripts/mkdocs_hooks.py")))
        nav = re.split(r"\n(?=[A-Za-z0-9_]+:)", mk.split("\nnav:", 1)[1], maxsplit=1)[0].splitlines() if "\nnav:" in mk else []
        self.assertEqual(
            [m.group(1).strip() for l in nav if (m := re.match(r"^  -\s+['\"]?([^'\":\n]+?)['\"]?:", l))],
            ["Home", "Tutorials", "How-To Guides", "Reference", "Explanation", "Releases & Governance"],
        )
        for np in [m.group(1) for l in nav
                   if (m := re.search(r"(?:^-\s+|:\s+)['\"]?([^'\"\s]+\.md)['\"]?\s*$", l.split("#", 1)[0].strip()))]:
            tgt = (ROOT / VIRTUAL[np] if np in VIRTUAL else
                   ROOT / "documentation" / "specifications" / np[6:] if np.startswith("specs/") else DOCS / np)
            self.assertTrue(tgt.is_file(), np)

        v = configparser.ConfigParser()
        v.optionxform = str
        v.read_string("[r]\n" + (ROOT / ".vale.ini").read_text("utf-8"))
        self.assertEqual((v["r"]["StylesPath"], v["r"]["MinAlertLevel"]), (".vale/styles", "suggestion"))
        self.assertTrue(all(s in v for s in ("*.md", *(f"docs/{q}/**/*.md" for q in QUADS))))
        hv = v["docs/02-how-to-guides/**/*.md"]
        self.assertEqual(hv["MinAlertLevel"], "error")
        self.assertTrue(all(hv.get(k) == "YES" for k in (
            "Google.FirstPerson", "Google.Passive", "Google.Contractions", "Google.We", "Vale.Spelling")))

        ml = json.loads((ROOT / ".markdownlint.json").read_text("utf-8"))
        self.assertEqual(
            (ml.get("default"), ml.get("MD013"), ml.get("MD024", {}).get("siblings_only"), ml.get("MD033"), ml.get("MD041")),
            (True, {"line_length": 120, "code_blocks": False, "tables": False}, True, False, False),
        )
        self.assertEqual([
            f"{md.name}:{ln}" for md in sorted(DOCS.rglob("*.md")) for ln, l in _non_code(md.read_text("utf-8"))
            if ("$$" in l and l != "$$") or "\\operatorname" in l or (l != "$$" and MATH_SP_RE.search(l))
        ], [])

    def test_portal_and_readmes_expose_all_diataxis_quadrants(self) -> None:
        portal = (DOCS / "index.md").read_text("utf-8")
        self.assertTrue(all(t in portal for t in (
            *[f"{q}/index.md" for q in QUADS], "ACTION_LOGBOOK.md", "RCA_REGISTER.md", PORTAL)))
        en_txt = (ROOT / "README.md").read_text("utf-8")
        en_ok = "docs/index.md" in en_txt and PORTAL in en_txt
        self.assertTrue(en_ok and all(f"docs/{q}/index.md" in en_txt for q in QUADS))
        fr_txt = (ROOT / "README_fr.md").read_text("utf-8")
        fr_quads = ("01-tutoriels", "02-guides-pratiques", "03-reference", "04-explications")
        self.assertTrue("docs/fr/index.md" in fr_txt and f"{PORTAL}/fr/" in fr_txt
                        and all(f"docs/fr/{q}/index.md" in fr_txt for q in fr_quads))

    def test_ste_structural_checker_catches_violations_and_passes_valid_prose(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ok, bad = Path(tmp) / "ok.md", Path(tmp) / "bad.md"
            ok.write_text("# Step\n\n1. Stop the daemon.\n2. Run the audit.\n\nExit code is zero.\n", encoding="utf-8")
            self.assertEqual(collect_ste_structural_violations(ok), [])
            bad.write_text(
                "# Bad\n\n1. You should restart the daemon; don't ignore errors.\n"
                "2. The report was written by the worker after twenty seconds of continuous polling "
                "across every remote target database server on the host.\n", encoding="utf-8",
            )
            joined = "\n".join(collect_ste_structural_violations(bad))
            self.assertTrue(all(r in joined for r in ("[Rule 3.2]", "[Rule 8.1]", "[Rule 4.2]", "[Rule 3.6]", "[Rule 5.1]")))

    def test_french_diataxis_stf100_and_i18n_isolation(self) -> None:
        fr_root = DOCS / "fr"
        fr_quads = ("01-tutoriels", "02-guides-pratiques", "03-reference", "04-explications")
        self.assertTrue((fr_root / "index.md").is_file())
        for q in fr_quads:
            self.assertTrue((fr_root / q / "index.md").is_file(), q)
        fr_guides = sorted((fr_root / "02-guides-pratiques").rglob("*.md"))
        self.assertGreaterEqual(len([p for p in fr_guides if p.name != "index.md"]), 4)
        for md in fr_guides:
            self.assertEqual(collect_stf_structural_violations(md), [], md.as_posix())
            if md.name != "index.md":
                txt = md.read_text("utf-8")
                self.assertIn("Vérification", txt, md.name)
                self.assertIn("Retour arrière", txt, md.name)
                self.assertRegex(txt, r"\*\*(?:ATTENTION|AVERTISSEMENT)\s*:", md.name)
        fr_tuts = [p for p in (fr_root / "01-tutoriels").glob("*.md") if p.name != "index.md"]
        self.assertEqual(len(fr_tuts), 2)
        for tut in fr_tuts:
            txt = tut.read_text("utf-8")
            self.assertTrue(all(q in txt for q in ("02-guides-pratiques", "03-reference", "04-explications")))
        en_cfg = (ROOT / "mkdocs.yml").read_text("utf-8")
        fr_cfg = (ROOT / "mkdocs.fr.yml").read_text("utf-8")
        self.assertIn("language: en", en_cfg)
        self.assertIn("language: fr", fr_cfg)
        self.assertNotIn("overview-fr.md", en_cfg.split("\nnav:", 1)[1])
        self.assertNotIn("overview-en.md", fr_cfg.split("\nnav:", 1)[1])

    def test_zero_ascii_diagrams_and_valid_mermaid_across_authored_docs(self) -> None:
        authored = list(ROOT.glob("*.md")) + list(DOCS.rglob("*.md")) + list((ROOT / "documentation").rglob("*.md"))
        mermaid_count = 0
        for md in sorted(authored):
            txt = md.read_text("utf-8")
            self.assertIsNone(_BOX_DRAW_RE.search(txt), f"Unicode box-drawing in {md.as_posix()}")
            for ln, indent, lang, body in _fenced_blocks(txt):
                if lang == "mermaid":
                    mermaid_count += 1
                    self.assertEqual(indent, 0, f"Indented mermaid fence at {md.as_posix()}:{ln}")
                    self.assertNotIn("<br", body.lower(), f"HTML <br> in mermaid at {md.as_posix()}:{ln}")
                    first = next((l.strip().lower() for l in body.splitlines() if l.strip()), "")
                    self.assertTrue(any(first.startswith(k) for k in _MERMAID_TYPES), f"Bad header at {md.name}:{ln}")
                elif lang in ("", "text", "ascii"):
                    self.assertNotRegex(body, r"(\+[-=]{2,}\+|-->|<--)", f"ASCII diagram in {md.as_posix()}:{ln}")
        self.assertGreaterEqual(mermaid_count, 6)
        for folder in ("01-tutorials", "02-how-to-guides", "fr/01-tutoriels", "fr/02-guides-pratiques"):
            for md in sorted((DOCS / folder).rglob("*.md")):
                for ln, _, lang, body in _fenced_blocks(md.read_text("utf-8")):
                    if lang in ("bash", "sh", "shell"):
                        self.assertNotIn("2>/dev/null", body, f"{md.as_posix()}:{ln}")

    def test_executable_tutorial_howto_cli_scripts_and_presets(self) -> None:
        hlp = subprocess.run([sys.executable, str(ROOT / "audit_cis.py"), "--help"], capture_output=True, text=True)
        self.assertEqual(hlp.returncode, 0, hlp.stderr)
        lst = subprocess.run([sys.executable, str(ROOT / "audit_cis.py"), "--list-targets"],
                             capture_output=True, text=True)
        self.assertEqual(lst.returncode, 0, lst.stderr)
        self.assertIn("18 Benchmarks / 887 Controls", lst.stdout)
        presets = json.loads((ROOT / "conf" / "mcp_api_executor_presets.json").read_text("utf-8"))
        self.assertTrue(presets.get("read_only"))
        targets = set(presets.get("allowed_targets", []))
        self.assertEqual(len(targets), 18)
        for t in targets:
            self.assertIn(t, lst.stdout)
        valid_flags = set(re.findall(r"--[a-z][a-z0-9-]+", hlp.stdout))
        for folder in ("01-tutorials", "02-how-to-guides", "fr/01-tutoriels", "fr/02-guides-pratiques"):
            for md in sorted((DOCS / folder).rglob("*.md")):
                for ln, _, lang, body in _fenced_blocks(md.read_text("utf-8")):
                    if lang not in ("bash", "sh", "shell"):
                        continue
                    joined = re.sub(r"\\\s*\n\s*", " ", body)
                    for cmd_line in joined.splitlines():
                        if "audit_cis.py" not in cmd_line:
                            continue
                        toks = shlex.split(cmd_line.strip())
                        if "audit_cis.py" not in toks:
                            continue
                        self.assertFalse(("-o" in toks or "--output" in toks)
                                         and ("-j" in toks or "--output-json" in toks),
                                         f"Combined -o/-j unsupported at {md.name}:{ln}")
                        for fl in (x for x in toks if x.startswith("--")):
                            self.assertIn(fl.split("=", 1)[0], valid_flags, f"{md.name}:{ln}")
                        for i, x in enumerate(toks[:-1]):
                            if x in ("-t", "--target"):
                                self.assertIn(toks[i + 1], targets, f"{md.name}:{ln}")
        with tempfile.TemporaryDirectory() as tmp:
            rep, out_diff, out_sarif = Path(tmp) / "r.json", Path(tmp) / "p.diff", Path(tmp) / "r.sarif"
            ctrl = {"id": "4.3", "title": "Disallow local_infile", "status": "FAIL",
                    "severity": "HIGH", "remediation": "SET GLOBAL local_infile = OFF;"}
            rep.write_text(json.dumps({"target": "mariadb106", "controls": [ctrl]}), encoding="utf-8")
            for fmt in ("diff", "sql", "ansible", "json"):
                r = subprocess.run([
                    sys.executable, str(ROOT / "audit_cis.py"), "--remediate-dry-run", "--from-report", str(rep),
                    "--remediation-format", fmt, "--remediation-output", str(out_diff),
                ], capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertTrue(out_diff.read_text("utf-8").strip(), fmt)
            sys.path.insert(0, str(ROOT))
            try:
                import sarif_exporter
                doc = sarif_exporter.build_sarif_document([ctrl], target_name="mariadb106")
                ok, msg = sarif_exporter.validate_sarif_document(doc)
                self.assertTrue(ok, msg)
                sarif_exporter.export_sarif_report([ctrl], 0.0, {}, "mariadb106", str(out_sarif))
                self.assertTrue(out_sarif.is_file())
            finally:
                sys.path.pop(0)
        for sh in sorted((ROOT / "scripts").glob("*.sh")):
            self.assertTrue(sh.read_text("utf-8").startswith("#!/"))
            if shutil.which("bash"):
                res = subprocess.run(
                    ["bash", "-n", f"scripts/{sh.name}"], cwd=str(ROOT), capture_output=True, text=True)
                if res.returncode != 0 and not any(k in (res.stderr or "") for k in ("WSL", "0x8007")):
                    self.fail(f"bash -n failed on {sh.name}: {res.stderr}")


if __name__ == "__main__":
    unittest.main()
