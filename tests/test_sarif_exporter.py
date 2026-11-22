#!/usr/bin/env python3
"""Unit tests for PSL SARIF v2.1.0 exporter (IDEA-003, PSL ONLY)."""
import json, os, pathlib, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from audit_orchestrator import CANONICAL_TARGETS
import cis_core_engine as core, sarif_exporter as sarif


class TestSarifExporter(unittest.TestCase):
    def test_states_envelope_and_errors(self):
        sample = {"1. Auth": [
            {"number": "1.1", "name": "P", "status": "PASS", "output": "ok"},
            {"number": "1.2", "name": "F", "status": "FAIL", "output": "OFF", "remediation": "SET ssl=1"},
            {"number": "1.3", "name": "E", "status": "ERROR", "test_procedure": "mysql", "output": "Permission denied"},
            {"number": "1.4", "name": "M", "status": "MANUAL", "type": "Manual"},
            {"number": "1.5", "name": "N", "status": "Not Applicable"},
        ]}
        doc = sarif.build_sarif_document(sample, 50.0, {}, "mariadb106")
        run = doc["runs"][0]
        self.assertEqual((doc["$schema"], doc["version"], run["tool"]["driver"]["name"], len(run["tool"]["driver"]["rules"])), (sarif.SARIF_SCHEMA_URI, "2.1.0", "cis-benchmarks-tools", 5))
        self.assertTrue(run["invocations"][0]["executionSuccessful"] and run["invocations"][0]["startTimeUtc"].endswith("Z"))
        by = {r["properties"]["control_id"]: r for r in run["results"]}
        for cid, exp in (("1.1", ("pass", "none", "Pass")), ("1.2", ("fail", "error", "Fail")), ("1.3", ("open", "warning", "Error")), ("1.4", ("review", "note", "Manual")), ("1.5", ("notApplicable", "none", "Not Applicable"))):
            self.assertEqual((by[cid]["kind"], by[cid]["level"], by[cid]["properties"]["compliance_state"]), exp)
        self.assertEqual((by["1.3"]["properties"]["failure_category"], by["1.2"]["locations"][0]["physicalLocation"]["artifactLocation"]["uri"]), ("PERMISSION_DENIED", "rules/mariadb_106.json"))

    def test_secrets_fingerprints_targets_and_export(self):
        flat = [{"id": "5.2", "title": "SSH", "category": "A", "status": "FAIL", "audit": "mysql -pS1 --password=S2", "output": "MYSQL_PWD=S3 PGPASSWORD=S4 token=S5", "remediation": "password=S6"}]
        raw = json.dumps(sarif.build_sarif_document(flat, 0.0, target_name="Red Hat Enterprise Linux 9", execution_context="ssh password=S7"))
        self.assertFalse(any(s in raw for s in ("S1", "S2", "S3", "S4", "S5", "S6", "S7")))
        fp = lambda t: sarif.build_sarif_document(flat, target_name=t)["runs"][0]["results"][0]["partialFingerprints"]["primaryLocationLineHash"]
        self.assertEqual((fp("postgresql16"), len(fp("postgresql16"))), (fp("PostgreSQL 16"), 32))
        for k, m in CANONICAL_TARGETS.items():
            self.assertEqual((sarif.resolve_rule_spec(k), sarif.resolve_rule_spec(m["title"])), (m["rule_spec"], m["rule_spec"]))
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "a.sarif")
            core.export_results({"G": [{"id": "1.1", "status": "PASS"}]}, 100.0, {}, "mariadb106", filename=out, fmt="sarif")
            self.assertEqual(json.loads(pathlib.Path(out).read_text(encoding="utf-8"))["version"], "2.1.0")
        for f, tok in (("pyproject.toml", '"sarif_exporter"'), ("Dockerfile", "sarif_exporter.py")):
            self.assertIn(tok, (pathlib.Path(ROOT) / f).read_text(encoding="utf-8"))

    def test_sarif_validation_in_e2e_checkers(self):
        from unittest.mock import MagicMock, patch
        from docker_e2e_engine import DockerE2EOrchestrator, TargetE2ESpec
        from scripts.run_e2e_tests import analyze_report_integrity

        self.assertFalse(sarif.validate_sarif_document({})[0])
        self.assertFalse(sarif.validate_sarif_document({"version": "2.1.0", "runs": []})[0])
        self.assertFalse(sarif.validate_sarif_document({"version": "2.1.0", "runs": [{"tool": {"driver": {"name": "t", "rules": []}}, "results": [{"ruleId": "X"}]}]})[0])

        with tempfile.TemporaryDirectory() as td:
            good = os.path.join(td, "good.sarif")
            bad = os.path.join(td, "bad.sarif")
            sarif.export_sarif_report({"G": [{"id": "1.1", "status": "FAIL", "output": "OFF"}]}, 0.0, {}, "mariadb106", filename=good)
            pathlib.Path(bad).write_text(json.dumps({"version": "1.0.0", "runs": []}) + " " * 50, encoding="utf-8")
            self.assertTrue(analyze_report_integrity(good)[0])
            self.assertFalse(analyze_report_integrity(bad)[0])

            orch = DockerE2EOrchestrator(output_dir=td)
            self.assertEqual(orch.DEFAULT_FORMATS, ["html", "json", "xml", "txt"])
            spec = TargetE2ESpec("mariadb106", "d", "img", "c1", "audit_cis_mariadb_106.py", "rapport_cis_mariadb_106")
            expected_dest = os.path.join(td, "rapport_cis_mariadb_106.sarif")

            def fake_run(cmd, **kw):
                if len(cmd) >= 2 and cmd[1] == "cp" and cmd[-1] == expected_dest:
                    pathlib.Path(expected_dest).write_text(pathlib.Path(good).read_text(encoding="utf-8"), encoding="utf-8")
                return MagicMock(returncode=0, stdout="", stderr="")

            with patch("subprocess.run", side_effect=fake_run):
                vals, ext = orch.execute_in_container_audit(spec, mode="local", formats=["sarif"])
                self.assertTrue(vals["sarif"][0], vals["sarif"][1])
                self.assertEqual(ext["sarif"], expected_dest)


if __name__ == "__main__":
    unittest.main()
