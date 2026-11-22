#!/usr/bin/env python3
"""Contract tests for read-only MCP api_executor presets (100% PSL ONLY)."""
import json
import pathlib
import re
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import audit_cis
import audit_orchestrator as orch
import remediation_generator as rem

PRESET_PATH = ROOT / "conf" / "mcp_api_executor_presets.json"
CONTRACT_DOC = ROOT / "docs" / "MCP_API_EXECUTOR_CONTRACT.md"


class TestMcpApiExecutorContract(unittest.TestCase):
    def setUp(self):
        self.cfg = json.loads(PRESET_PATH.read_text(encoding="utf-8"))

    def test_contract_schema_targets_and_read_only_invariants(self):
        self.assertTrue(CONTRACT_DOC.is_file())
        self.assertEqual(self.cfg["schema_version"], "cis.mcp.contract.v1")
        self.assertIs(self.cfg["read_only"], True)
        self.assertEqual(self.cfg["credential_boundary"]["password_env_var"], "CIS_DB_PASSWORD")
        self.assertEqual(set(self.cfg["allowed_targets"]), set(audit_cis.TARGET_MAP.keys()))
        self.assertEqual(set(self.cfg["allowed_targets"]), set(orch.CANONICAL_TARGETS.keys()))
        self.assertEqual(len(self.cfg["allowed_targets"]), 18)

        forbidden = set(self.cfg["forbidden_flags"])
        self.assertTrue({"-p", "--password", "--db-password", "--apply", "--allow-ephemeral-apply", "--force"}.issubset(forbidden))
        self.assertEqual(set(self.cfg["optional_connection_flags"]) & forbidden, set())

        presets = self.cfg["presets"]
        self.assertEqual(set(presets.keys()), {"cis_list_targets", "cis_audit_json", "cis_audit_sarif", "cis_remediate_dry_run"})
        self.assertEqual(tuple(presets["cis_remediate_dry_run"]["allowed_remediation_formats"]), rem.SUPPORTED_FORMATS)
        for name, spec in presets.items():
            self.assertIs(spec["read_only"], True, f"{name} must be read_only")
            self.assertIs(spec["mutating"], False, f"{name} must not mutate")
            tokens = [t for t in spec["args"] + spec.get("optional_args", []) if t.startswith("-")]
            self.assertEqual(set(tokens) & forbidden, set(), f"Forbidden flag in {name}")

    def test_all_preset_cli_flags_exist_in_audit_cis_help(self):
        res = subprocess.run([sys.executable, str(ROOT / "audit_cis.py"), "--help"], capture_output=True, text=True, check=True)
        help_txt = res.stdout + res.stderr
        flags = set(self.cfg["optional_connection_flags"])
        for spec in self.cfg["presets"].values():
            for tok in spec["args"] + spec.get("optional_args", []):
                if tok.startswith("-"):
                    flags.add(tok)
        for flag in sorted(flags):
            self.assertRegex(help_txt, rf"(?<![\w-]){re.escape(flag)}(?![\w-])", f"Preset flag missing from audit_cis.py --help: {flag}")
        for doc_path in (ROOT / "README.md", ROOT / "README_fr.md"):
            self.assertIn("docs/MCP_API_EXECUTOR_CONTRACT.md", doc_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
