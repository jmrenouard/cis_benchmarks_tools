"""Unit tests verifying the project governance rules, Action Logbook, and RCA Register."""

from __future__ import annotations

import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class TestProjectGovernanceRules(unittest.TestCase):
    """Validate English project governance rules, Action Logbook, and RCA Register."""

    def test_governance_rules_inscribed_in_agents_and_rules_dir(self) -> None:
        """Verify AGENTS.md and .agents/rules/*.md enforce Logbook, RCA, and GitHub workflow in English."""
        agents_md = ROOT / "AGENTS.md"
        workspace_agents_md = ROOT / ".agents" / "AGENTS.md"
        gov_rule_md = ROOT / ".agents" / "rules" / "project-governance.md"
        git_rule_md = ROOT / ".agents" / "rules" / "git-workflow.md"
        gh_rule_md = ROOT / ".agents" / "rules" / "github-workflow.md"

        self.assertTrue(agents_md.is_file(), "AGENTS.md must exist at repository root")
        self.assertTrue(workspace_agents_md.is_file(), ".agents/AGENTS.md must exist")
        self.assertTrue(gov_rule_md.is_file(), ".agents/rules/project-governance.md must exist")
        self.assertTrue(git_rule_md.is_file(), ".agents/rules/git-workflow.md must exist")
        self.assertTrue(gh_rule_md.is_file(), ".agents/rules/github-workflow.md must exist")

        agents_content = agents_md.read_text(encoding="utf-8")
        gov_content = gov_rule_md.read_text(encoding="utf-8")
        git_content = git_rule_md.read_text(encoding="utf-8")
        gh_content = gh_rule_md.read_text(encoding="utf-8")

        self.assertIn("trigger: always_on", gov_content)
        self.assertIn("trigger: always_on", git_content)
        self.assertIn("trigger: always_on", gh_content)

        for content in (agents_content, gov_content):
            self.assertIn("docs/ACTION_LOGBOOK.md", content)
            self.assertIn("docs/RCA_REGISTER.md", content)
            self.assertIn("every request", content.lower())
            self.assertIn("every change", content.lower())
            self.assertIn("every result", content.lower())

        for content in (agents_content, git_content, gh_content):
            self.assertIn("gh issue comment", content)
            self.assertIn("gh issue close", content)

    def test_action_logbook_exists_in_english_and_tracks_ongoing_and_completed_actions(self) -> None:
        """Verify docs/ACTION_LOGBOOK.md exists in English and contains structured ongoing/completed sections."""
        logbook_path = ROOT / "docs" / "ACTION_LOGBOOK.md"
        self.assertTrue(logbook_path.is_file(), "docs/ACTION_LOGBOOK.md must exist")

        content = logbook_path.read_text(encoding="utf-8")
        self.assertIn("Ongoing Actions", content)
        self.assertIn("Completed Actions", content)
        self.assertIn("Request", content)
        self.assertIn("Changes", content)
        self.assertIn("Result", content)

    def test_rca_register_exists_in_english_and_covers_all_four_mandatory_categories(self) -> None:
        """Verify docs/RCA_REGISTER.md covers Errors (RCA), Dead-Ends, Approximations, and Unimplemented Ideas."""
        rca_path = ROOT / "docs" / "RCA_REGISTER.md"
        self.assertTrue(rca_path.is_file(), "docs/RCA_REGISTER.md must exist")

        content = rca_path.read_text(encoding="utf-8")
        self.assertIn("Errors & Bugs Encountered", content)
        self.assertIn("RCA", content)
        self.assertIn("Technical Dead-Ends", content)
        self.assertIn("Current Approximations", content)
        self.assertIn("Unimplemented Ideas", content)

        self.assertIn("RCA-001", content)
        self.assertIn("IMP-001", content)
        self.assertIn("APP-001", content)
        self.assertIn("IDEA-001", content)

    def test_execution_rules_and_best_practices_aligned_with_core_pillars(self) -> None:
        """Verify 03_execution_rules.md and 04_best_practices.md enforce PSL, offline SVG, and diff limits."""
        exec_rules = ROOT / "03_execution_rules.md"
        best_practices = ROOT / "04_best_practices.md"

        self.assertTrue(exec_rules.is_file(), "03_execution_rules.md must exist")
        self.assertTrue(best_practices.is_file(), "04_best_practices.md must exist")

        exec_content = exec_rules.read_text(encoding="utf-8")
        bp_content = best_practices.read_text(encoding="utf-8")

        self.assertIn("15,000 characters", exec_content)
        self.assertIn("100% Python Standard Library", exec_content)
        self.assertIn("4-Tier Execution Contexts", exec_content)

        self.assertIn("100% Offline Inline SVG Reporting", bp_content)
        self.assertIn("Chart.js is permanently prohibited", bp_content)
        self.assertIn("SecretSanitizer", bp_content)

    def test_core_specifications_governance_and_architecture(self) -> None:
        """Verify project-governance.md and architecture.md exist with expected sections."""
        specs_dir = ROOT / "documentation" / "specifications"
        self.assertTrue(specs_dir.is_dir(), "documentation/specifications must exist")

        expected_specs = {
            "project-governance.md": [
                "# Project Governance Specification",
                "## 1. Overview & Rationale",
                "## 2. Core Architectural Pillars",
                "## 3. Mandatory 9-Step GitHub Lifecycle",
                "## 4. Mandatory Living Registers",
                "## 5. Strict English-Only Policy",
            ],
            "architecture.md": [
                "# System Architecture Specification",
                "## 1. Architectural Philosophy",
                "## 2. 100% Python Standard Library",
                "## 3. Dual-Mode Architecture",
                "## 4. Component Interaction Diagram",
            ],
        }

        for filename, headers in expected_specs.items():
            file_path = specs_dir / filename
            self.assertTrue(file_path.is_file(), f"{filename} must exist under documentation/specifications/")
            content = file_path.read_text(encoding="utf-8")
            self.assertGreater(len(content.strip()), 100, f"{filename} must not be empty")
            for header in headers:
                self.assertIn(header, content, f"{filename} missing required header: {header}")


if __name__ == "__main__":
    unittest.main()



