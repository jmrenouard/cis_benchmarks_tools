#!/usr/bin/env python3
"""Tests for PSL deterministic dry-run remediation generator."""
import json, os, pathlib, sys, tempfile, unittest
from unittest.mock import patch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import remediation_generator as rem


class TestRemediationGenerator(unittest.TestCase):
    def test_plan_formats_guards_and_cli(self):
        sample = {"4": [
            {"number": "4.4", "name": "local_infile", "status": "FAIL", "type": "Automated"},
            {"number": "4.6", "name": "symlinks", "status": "FAIL", "type": "Automated"},
            {"number": "9.9", "name": "Unmapped", "status": "FAIL", "type": "Automated", "remediation": "password=Sec1\nDROP TABLE x;"},
            {"number": "1.1", "name": "Manual", "status": "MANUAL", "type": "Manual", "remediation": "token=Sec2"},
            {"number": "1.2", "name": "Pass", "status": "PASS", "type": "Automated"},
        ]}
        with patch("subprocess.run", side_effect=AssertionError("No exec")):
            p1, p2 = rem.build_remediation_plan(sample, "mysql80"), rem.build_remediation_plan(sample, "mysql80")
            self.assertEqual((p1, p1["dry_run"], p1["family"], p1["total_items"]), (p2, True, "mysql", 4))
            by = {i["control_id"]: i for i in p1["items"]}
            self.assertEqual((by["4.4"]["action_type"], by["9.9"]["action_type"], by["1.1"]["action_type"]), ("sql_and_config", "manual_only", "manual_only"))
            self.assertIn("@@have_symlink", by["4.6"]["verification_command"])
            outs = {f: rem.render_remediation(p1, f) for f in rem.SUPPORTED_FORMATS}
            for f, txt in outs.items():
                self.assertEqual(txt, rem.render_remediation(p2, f))
                self.assertTrue("Sec1" not in txt and "Sec2" not in txt)
            self.assertFalse(any(ln.startswith("DROP TABLE") for ln in outs["sql"].splitlines() + outs["shell"].splitlines()))
            for k, tok in (("sql", "SET PERSIST local_infile = OFF;"), ("shell", "set -euo pipefail"), ("ansible", "check_mode: true"), ("diff", "--- a/")):
                self.assertIn(tok, outs[k])
            self.assertEqual(json.loads(outs["json"])["total_items"], 4)
        self.assertRaises(ValueError, rem.build_remediation_plan, sample, "mysql80", False)
        self.assertRaises(ValueError, rem.render_remediation, p1, "yaml")
        with tempfile.TemporaryDirectory() as td:
            rep, out = os.path.join(td, "pg.json"), os.path.join(td, "fix.sql")
            pathlib.Path(rep).write_text(json.dumps({"target": "postgresql16", "results": [{"id": "3.1.20", "status": "FAIL"}, {"id": "3.1.2", "status": "FAIL"}]}), encoding="utf-8")
            self.assertEqual(rem.main(["--from-report", rep, "-f", "sql", "-o", out]), 0)
            sql = pathlib.Path(out).read_text(encoding="utf-8")
            self.assertLess(sql.index("3.1.2"), sql.index("3.1.20"))
            self.assertIn("ALTER SYSTEM SET log_connections = 'on';", sql)
        self.assertIn("SET GLOBAL local_infile = OFF;", rem.render_remediation(rem.build_remediation_plan([{"number": "4.4", "status": "FAIL"}], "mariadb106"), "sql"))
        for f, tok in (("pyproject.toml", '"remediation_generator"'), ("Dockerfile", "remediation_generator.py")):
            self.assertIn(tok, (pathlib.Path(ROOT) / f).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
