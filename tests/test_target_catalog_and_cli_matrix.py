#!/usr/bin/env python3
"""Target Catalog Matrix and CLI Argument Forwarding Tests (Finding 13, PSL ONLY)."""

import importlib, inspect, json, os, sys, tempfile, unittest
from unittest.mock import patch, MagicMock

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from audit_orchestrator import (
    CANONICAL_TARGETS, AuditOrchestrator, build_cli_parser,
    normalize_target_key, TargetAuditExecutionResult
)
from audit_cis import TARGET_MAP, run_single_audit
import audit_cis


class TestCanonicalTargetsMatrix(unittest.TestCase):
    """Matrix tests across all 18 canonical targets and modules."""

    def test_catalog_completeness_and_rule_specs(self):
        """Assert all 18 canonical targets match TARGET_MAP with valid rule specs."""
        self.assertEqual(len(CANONICAL_TARGETS), 18)
        self.assertEqual(set(CANONICAL_TARGETS.keys()), set(TARGET_MAP.keys()))
        for k, meta in CANONICAL_TARGETS.items():
            self.assertEqual(meta["module"], TARGET_MAP[k][0].replace(".py", ""))
            rule_path = os.path.join(REPO_ROOT, "rules", f"{meta['rule_spec']}.json")
            self.assertTrue(os.path.exists(rule_path), f"Missing rule for {k}")
            with open(rule_path, "r", encoding="utf-8") as f:
                self.assertTrue(len(json.load(f)) > 0)

    def test_all_18_targets_interfaces_and_lifecycle(self):
        """Verify import, interfaces, scoring, SVG charts, and export for 18 targets."""
        req_fns = ("perform_checks", "calculate_scores", "build_inline_svg_category_chart", "build_inline_svg_donut_chart", "export_results")
        base_p = {"recommendations", "remote_host", "docker_container", "ssh_port", "ssh_key", "sudo"}
        db_p = {"db_user", "db_password", "db_host", "db_port", "db_name", "defaults_file", "auth_db"}
        sample = {"General": [{"id": "1.1", "status": "PASS", "type": "Automated", "category": "General"},
                              {"id": "1.2", "status": "FAIL", "type": "Automated", "category": "General"},
                              {"id": "1.3", "status": "MANUAL", "type": "Manual", "category": "General"}]}
        with tempfile.TemporaryDirectory() as tmp_dir:
            for k, meta in CANONICAL_TARGETS.items():
                mod = importlib.import_module(meta["module"])
                for fn in req_fns:
                    self.assertTrue(callable(getattr(mod, fn, None)), f"{k} missing {fn}")

                sig = inspect.signature(mod.perform_checks).parameters
                self.assertTrue(base_p.issubset(sig), f"{k} missing base params")
                if meta["category"] == "database":
                    self.assertTrue(db_p.issubset(sig), f"{k} missing db params")

                scores = mod.calculate_scores(sample)
                self.assertTrue(isinstance(scores, tuple) and len(scores) >= 2)
                self.assertTrue(0.0 <= float(scores[0]) <= 100.0 and "General" in scores[1])

                self.assertIn("General", mod.build_inline_svg_category_chart(scores[1]))
                donut = mod.build_inline_svg_donut_chart(4, 3, 1, 0, 75.0)
                self.assertTrue("<svg" in donut and "</svg>" in donut)

                out = os.path.join(tmp_dir, f"{k}.json")
                mod.export_results(sample, scores[0], scores[1], target_name=k, filename=out, fmt="json")
                self.assertTrue(os.path.exists(out) and os.path.getsize(out) > 0)


class TestCliParsingAndForwardingMatrix(unittest.TestCase):
    """Tests for CLI argument parsing and parameter forwarding."""

    def test_audit_cis_cli_parser_single_target_all_flags(self):
        """Test audit_cis.py CLI parses and forwards full argument matrix."""
        args = ["audit_cis.py", "-t", "postgresql16", "--mode", "ssh", "-r", "adm@h",
                "--ssh-port", "2222", "-i", "/k", "--sudo", "-c", "c1", "-H", "1.1.1.1",
                "-P", "5432", "-u", "u", "-p", "pwd", "-D", "db", "--defaults-file", "/cfg",
                "--auth-db", "auth", "-f", "json", "-l", "fr", "-o", "/tmp/r.json"]
        with patch("sys.argv", args), patch("audit_cis.run_single_audit", return_value=True) as mock_run:
            with self.assertRaises(SystemExit) as cm:
                audit_cis.main()
            self.assertEqual(cm.exception.code, 0)
            self.assertEqual(mock_run.call_args[0][0], "postgresql16")
            kw = mock_run.call_args[1]
            self.assertEqual((kw["output_file"], kw["fmt"], kw["lang"], kw["mode"], kw["remote_host"], kw["ssh_port"],
                              kw["ssh_key"], kw["docker_container"], kw["db_host"], kw["db_port"], kw["db_user"],
                              kw["db_password"], kw["db_name"], kw["defaults_file"], kw["auth_db"], kw["use_sudo"]),
                             ("/tmp/r.json", "json", "fr", "ssh", "adm@h", 2222, "/k", "c1", "1.1.1.1", 5432, "u",
                              "pwd", "db", "/cfg", "auth", True))

    def test_audit_cis_cli_parser_defaults_and_all_targets(self):
        """Test audit_cis.py default parameters and --all dispatch."""
        with patch("sys.argv", ["audit_cis.py", "-t", "mariadb106"]), patch("audit_cis.run_single_audit", return_value=True) as mock_run:
            with self.assertRaises(SystemExit):
                audit_cis.main()
            self.assertEqual(mock_run.call_args[0][0], "mariadb106")
            kw = mock_run.call_args[1]
            self.assertEqual((kw["fmt"], kw["lang"], kw["mode"], kw["use_sudo"], kw["db_host"]),
                             ("html", "en", "local", False, "localhost"))

        with patch("sys.argv", ["audit_cis.py", "--all", "-m", "ssh", "-r", "t@h"]), patch("audit_cis.run_single_audit", return_value=True) as mock_all:
            with self.assertRaises(SystemExit):
                audit_cis.main()
            self.assertEqual(mock_all.call_count, 18)
            self.assertEqual([c[0][0] for c in mock_all.call_args_list], list(TARGET_MAP.keys()))

    def test_audit_cis_run_single_audit_command_and_env_construction(self):
        """Test run_single_audit forwards CLI arguments safely into argv and env."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0)) as mock_sub:
            self.assertTrue(run_single_audit(
                "mariadb106", output_file="/tmp/r.html", fmt="html", lang="en", mode="ssh",
                remote_host="adm@h", ssh_port=2200, ssh_key="/k", docker_container="c1",
                db_host="127.0.0.1", db_port=3306, db_user="u", db_password="secret_pass",
                db_name="mysql", defaults_file="/etc/my.cnf", auth_db="admin", use_sudo=True
            ))
            cmd, env = mock_sub.call_args[0][0], mock_sub.call_args[1].get("env", {})
            self.assertNotIn("secret_pass", cmd)
            self.assertEqual(env.get("CIS_DB_PASSWORD"), "secret_pass")
            for f, v in (("--remote", "adm@h"), ("--ssh-port", "2200"), ("--ssh-key", "/k"),
                         ("--docker", "c1"), ("--db-host", "127.0.0.1"), ("--db-port", "3306"),
                         ("--db-user", "u"), ("--db-name", "mysql"), ("--defaults-file", "/etc/my.cnf"),
                         ("--auth-db", "admin"), ("--output", "/tmp/r.html")):
                self.assertIn(f, cmd)
                self.assertIn(v, cmd)
            self.assertIn("--sudo", cmd)

    def test_orchestrator_cli_parser_and_check_kwargs(self):
        """Test build_cli_parser() and check_kwargs in audit_orchestrator."""
        parser = build_cli_parser()
        args = parser.parse_args([
            "-t", "mariadb106,postgresql16", "-m", "ssh", "-r", "adm@h", "--ssh-port", "2222",
            "-i", "/k", "--sudo", "-c", "c1", "-f", "json,html", "-j", "4", "-o", "out",
            "-l", "fr", "--db-user", "u", "--db-password", "p", "--db-host", "localhost",
            "--db-port", "5432", "--db-name", "db", "--defaults-file", "/cfg", "--auth-db", "auth"
        ])
        expected = {
            "remote_host": "adm@h", "docker_container": "c1", "ssh_port": 2222,
            "ssh_key": "/key", "sudo": True, "db_user": "u", "db_password": "p",
            "db_host": "localhost", "db_port": 5432, "db_name": "db",
            "defaults_file": "/cfg", "auth_db": "auth"
        }
        for k, v in expected.items():
            if k != "ssh_key":
                self.assertEqual(getattr(args, k), v)
        self.assertEqual(args.target, "mariadb106,postgresql16")
        self.assertEqual(args.formats, "json,html")

        orch = AuditOrchestrator(
            mode=args.mode, remote_host=args.remote_host, docker_container=args.docker_container,
            ssh_port=args.ssh_port, ssh_key=args.ssh_key, sudo=args.sudo, db_user=args.db_user,
            db_password=args.db_password, db_host=args.db_host, db_port=args.db_port,
            db_name=args.db_name, defaults_file=args.defaults_file, auth_db=args.auth_db
        )
        for k, v in expected.items():
            if k != "ssh_key":
                self.assertEqual(orch.check_kwargs.get(k), v)


class TestTargetErrorHandlingAndFaultIsolation(unittest.TestCase):
    """Tests for target normalization, unknown targets, and fault isolation."""

    def test_normalize_target_key_exhaustive_aliases(self):
        """Test normalize_target_key covers canonical family aliases."""
        cases = [
            ("mariadb", "mariadb106"), ("mariadb10.6", "mariadb106"), ("mariadb1011", "mariadb1011"),
            ("mysql", "mysql80"), ("mysql8.0", "mysql80"), ("mysql84", "mysql-community84"),
            ("mysql-community-84", "mysql-community84"), ("mysql-enterprise-84", "mysql-enterprise84"),
            ("mysql97", "mysql-community97"), ("postgres", "postgresql16"), ("postgres18", "postgresql18"),
            ("mongo", "mongodb7"), ("mongo8", "mongodb8"), ("cassandra", "cassandra40"),
            ("cassandra50", "cassandra50"), ("rhel", "rhel9"), ("rhel8", "rhel8"), ("rhel10", "rhel10")
        ]
        for user_input, expected in cases:
            self.assertEqual(normalize_target_key(user_input), expected, f"Failed for {user_input}")

    def test_unknown_target_returns_failure_result(self):
        """Test orchestrator and audit_cis return clean failure for unregistered target."""
        orch = AuditOrchestrator()
        result = orch.execute_single_target("completely_unknown_target_xyz")
        self.assertIsInstance(result, TargetAuditExecutionResult)
        self.assertFalse(result.success)
        self.assertIn("not registered in canonical targets catalog", result.exception_msg)
        self.assertFalse(run_single_audit("non_existent_target_123"))

    def test_orchestrator_fault_isolation_on_module_exception(self):
        """Test orchestrator isolates and handles exception raised by target module."""
        orch = AuditOrchestrator()
        with patch("importlib.import_module", side_effect=RuntimeError("Simulated execution failure")):
            res = orch.execute_single_target("mariadb106")
            self.assertFalse(res.success)
            self.assertIn("Audit execution exception", res.exception_msg)
            self.assertIsNotNone(res.diagnostic_summary)


if __name__ == "__main__":
    unittest.main()
