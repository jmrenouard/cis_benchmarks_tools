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

    def test_mongo_cassandra_rhel_and_audit_cli(self):
        import audit_cis
        for tgt, cid, d_tok, s_tok in (
            ("mongodb7", "2.1", "authorization: enabled", "mongod.conf"),
            ("mongodb8", "4.3", "requireTLS", "mongod.conf"),
            ("cassandra40", "2.1", "PasswordAuthenticator", "cassandra.yaml"),
            ("cassandra50", "2.2", "CassandraAuthorizer", "cassandra.yaml"),
            ("rhel9", "1.1.1.1", "install cramfs /bin/false", "cramfs.conf"),
            ("rhel9", "5.2.1", "PermitRootLogin no", "99-cis.conf"),
            ("rhel10", "5.3.1", "-LEGACY\n+DEFAULT", "update-crypto-policies"),
        ):
            plan = rem.build_remediation_plan([{"number": cid, "status": "FAIL"}], tgt)
            diff_out, sh_out = rem.render_remediation(plan, "diff"), rem.render_remediation(plan, "shell")
            self.assertIn(d_tok, diff_out)
            self.assertIn(s_tok, sh_out)
            self.assertNotIn("crypto-p***", diff_out + sh_out)
            self.assertIn("check_mode: true", rem.render_remediation(plan, "ansible"))
        with tempfile.TemporaryDirectory() as td:
            rep, out = os.path.join(td, "m.json"), os.path.join(td, "fix.diff")
            pathlib.Path(rep).write_text(json.dumps({"target": "mongodb7", "results": [{"number": "2.1", "status": "FAIL"}]}), encoding="utf-8")
            with patch.object(sys, "argv", ["audit_cis.py", "--remediate-dry-run", "--from-report", rep, "--remediation-format", "diff", "--remediation-output", out]):
                with self.assertRaises(SystemExit) as cm:
                    audit_cis.main()
            self.assertEqual(cm.exception.code, 0)
            self.assertIn("authorization: enabled", pathlib.Path(out).read_text(encoding="utf-8"))
            with patch.object(sys, "argv", ["audit_cis.py", "--remediate-dry-run"]):
                with self.assertRaises(SystemExit) as cm:
                    audit_cis.main()
            self.assertEqual(cm.exception.code, 2)
            out2 = os.path.join(td, "m_pipe.sql")
            def _fake_audit(t, output_file=None, fmt=None, **kw):
                self.assertEqual((t, fmt), ("mariadb106", "json"))
                pathlib.Path(output_file).write_text(json.dumps({"target": t, "results": [{"number": "4.4", "status": "FAIL"}]}), encoding="utf-8")
                return True
            with patch.object(audit_cis, "run_single_audit", side_effect=_fake_audit), patch.object(sys, "argv", ["audit_cis.py", "--remediate-dry-run", "-t", "mariadb106", "--remediation-format", "sql", "--remediation-output", out2]):
                with self.assertRaises(SystemExit) as cm:
                    audit_cis.main()
            self.assertEqual(cm.exception.code, 0)
            self.assertIn("SET GLOBAL local_infile = OFF;", pathlib.Path(out2).read_text(encoding="utf-8"))
            with patch.object(audit_cis, "run_single_audit", return_value=False), patch.object(sys, "argv", ["audit_cis.py", "--remediate-dry-run", "-t", "mariadb106"]):
                with self.assertRaises(SystemExit) as cm:
                    audit_cis.main()
            self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
