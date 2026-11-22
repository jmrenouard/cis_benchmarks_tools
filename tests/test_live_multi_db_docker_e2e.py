#!/usr/bin/env python3
"""Tests for live multi-db-docker-env before/after verifier (PSL ONLY, APP-001)."""
import json, os, pathlib, sys, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import audit_cis, live_e2e_verifier as v
from sarif_exporter import build_sarif_document


class TestLiveMultiDbE2EVerifier(unittest.TestCase):
    def test_profiles_guardrails_delta_and_pipeline(self):
        self.assertTrue(all(t in audit_cis.TARGET_MAP for t in v.MULTI_DB_PROFILES))
        self.assertFalse(v.is_ephemeral_lab_container("prod-db-01", {}) or v.is_ephemeral_lab_container("mariadb-10.11", {}))
        self.assertTrue(v.is_ephemeral_lab_container("mariadb-10.11", {"cis.ephemeral_lab": "true"}) and v.is_ephemeral_lab_container("cis-e2e-mariadb", {}))
        b = {"overall_score": None, "results": [{"number": "4.4", "status": "FAIL"}, {"number": "1.2", "status": "PASS"}, {"number": "2.1", "status": "ERROR"}]}
        a = {"overall_score": 100.0, "results": [{"number": "4.4", "status": "PASS"}, {"number": "1.2", "status": "PASS"}, {"number": "2.1", "status": "PASS"}]}
        d = v.compute_compliance_delta(b, a)
        self.assertEqual((d["score_delta"], d["fixed_controls"], d["regressed_controls"], d["error_count_before"], d["error_count_after"]), (100.0, ["2.1", "4.4"], [], 1, 0))
        st = {"applied": False, "bad_sarif": False}
        def fake_run(cmd, env=None, check=False, **kw):
            if cmd[:2] == ["docker", "exec"]:
                st["applied"] = True
                return type("R", (), {"returncode": 0, "stdout": ""})()
            self.assertTrue("Sec99" not in " ".join(cmd) and env.get("CIS_DB_PASSWORD") == "Sec99")
            fmt, out = cmd[cmd.index("--format") + 1], cmd[cmd.index("--output") + 1]
            rows = [{"number": "4.4", "name": "local_infile", "status": "PASS" if st["applied"] else "FAIL", "type": "Automated"}]
            sc = 100.0 if st["applied"] else 0.0
            doc = {"version": "0.0"} if (fmt == "sarif" and st["bad_sarif"]) else (build_sarif_document(rows, overall_score=sc, target_name="mariadb1011") if fmt == "sarif" else {"target": "mariadb1011", "overall_score": sc, "results": rows})
            pathlib.Path(out).write_text(json.dumps(doc), encoding="utf-8")
            return type("R", (), {"returncode": 0, "stdout": ""})()

        with tempfile.TemporaryDirectory() as td:
            self.assertRaises(ValueError, v.verify_target, "mariadb1011", "-u=root-test", td, None, None, "Sec99", True, {}, fake_run)
            self.assertRaises(PermissionError, v.verify_target, "mariadb1011", "prod-mariadb", td, None, None, "Sec99", True, {}, fake_run)
            res = v.verify_target("mariadb1011", "cis-e2e-mariadb", td, None, None, "Sec99", True, {}, fake_run)
            self.assertTrue(res["applied"] and os.path.exists(res["artifacts"]["before_sarif"]) and os.path.exists(res["artifacts"]["after_sarif"]))
            self.assertEqual((res["delta"]["score_before"], res["delta"]["score_after"], res["delta"]["fixed_controls"]), (0.0, 100.0, ["4.4"]))
            st["bad_sarif"] = True
            self.assertRaises(ValueError, v.verify_target, "mariadb1011", "cis-e2e-mariadb", td, None, None, "Sec99", False, {}, fake_run)


@unittest.skipUnless(os.environ.get("CIS_LIVE_DOCKER_E2E") == "1", "Set CIS_LIVE_DOCKER_E2E=1 for live Docker E2E")
class TestOptInLiveDockerE2E(unittest.TestCase):
    def test_live_container_dry_run_verification(self):
        with tempfile.TemporaryDirectory() as td:
            res = v.verify_target(os.environ.get("CIS_LIVE_TARGET", "mariadb1011"), os.environ.get("CIS_LIVE_CONTAINER"), td, db_password=os.environ.get("CIS_DB_PASSWORD"), allow_ephemeral_apply=False)
            self.assertEqual(res["delta"]["error_count_before"], 0)


if __name__ == "__main__":
    unittest.main()
