#!/usr/bin/env python3
"""
Docker In-Container E2E Execution & Verification Engine (Python PSL ONLY).
Orchestrates in-container audit execution, artifact injection, report extraction,
and comprehensive multi-format verification without host command escape.
"""

import argparse
import concurrent.futures
import datetime
import json
import os
import shlex
import subprocess
import sys
import time
from typing import Dict, List, Optional, Tuple, Any

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from docker_transport import ContainerInfo, DockerContainerDiscovery, DockerDaemonProbe
from temporal_metadata import TemporalAuditMetadata


class TargetE2ESpec:
    """Specification of an in-container E2E audit target."""

    def __init__(
        self,
        key: str,
        dockerfile: str,
        image_name: str,
        container_name: str,
        script_name: str,
        report_prefix: str,
        init_wait_sec: int = 15,
        env_vars: Optional[Dict[str, str]] = None
    ):
        self.key = key
        self.dockerfile = dockerfile
        self.image_name = image_name
        self.container_name = container_name
        self.script_name = script_name
        self.report_prefix = report_prefix
        self.init_wait_sec = init_wait_sec
        self.env_vars = env_vars or {}


class E2ERunResult:
    """Structured result of an in-container E2E execution."""

    def __init__(
        self,
        target_key: str,
        container_name: str,
        success: bool,
        duration_sec: float,
        format_validations: Optional[Dict[str, Tuple[bool, str]]] = None,
        extracted_reports: Optional[Dict[str, str]] = None,
        error_message: Optional[str] = None,
        temporal_metadata: Optional[Dict[str, Any]] = None
    ):
        self.target_key = target_key
        self.container_name = container_name
        self.success = success
        self.duration_sec = duration_sec
        self.format_validations = format_validations or {}
        self.extracted_reports = extracted_reports or {}
        self.error_message = error_message
        self.temporal_metadata = temporal_metadata

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_key": self.target_key,
            "container_name": self.container_name,
            "success": self.success,
            "duration_sec": round(self.duration_sec, 3),
            "format_validations": {k: {"valid": v[0], "note": v[1]} for k, v in self.format_validations.items()},
            "extracted_reports": self.extracted_reports,
            "error_message": self.error_message,
            "temporal_metadata": self.temporal_metadata
        }


class DockerE2EOrchestrator:
    """Coordinates automated in-container E2E audit runs and report extraction."""

    DEFAULT_FORMATS = ["html", "json", "xml", "txt"]

    def __init__(self, output_dir: str = "reports", container_cli: str = "docker"):
        self.output_dir = os.path.abspath(os.path.join(REPO_ROOT, output_dir))
        self.container_cli = container_cli
        os.makedirs(self.output_dir, exist_ok=True)

    def inject_artifacts(self, container_name: str) -> bool:
        """Inject templates/ and rules/ into /datas/ inside the target container."""
        try:
            subprocess.run([self.container_cli, "exec", container_name, "mkdir", "-p", "/datas/templates", "/datas/rules"], capture_output=True, check=False)
            t_src = os.path.join(REPO_ROOT, "templates")
            r_src = os.path.join(REPO_ROOT, "rules")
            if os.path.exists(t_src):
                subprocess.run([self.container_cli, "cp", t_src, f"{container_name}:/datas/"], capture_output=True, check=False)
            if os.path.exists(r_src):
                subprocess.run([self.container_cli, "cp", r_src, f"{container_name}:/datas/"], capture_output=True, check=False)
            return True
        except Exception:
            return False

    def execute_in_container_audit(
        self,
        spec: TargetE2ESpec,
        mode: str = "local",
        formats: Optional[List[str]] = None,
        timeout: int = 60
    ) -> Tuple[Dict[str, Tuple[bool, str]], Dict[str, str]]:
        """Run audit script inside target container for each requested format."""
        fmts = formats or self.DEFAULT_FORMATS
        validations: Dict[str, Tuple[bool, str]] = {}
        extracted: Dict[str, str] = {}

        self.inject_artifacts(spec.container_name)

        for fmt in fmts:
            rep_filename = f"{spec.report_prefix}.{fmt}" if mode == "local" else f"{spec.report_prefix}_ssh.{fmt}"
            in_container_out = f"/datas/{rep_filename}"
            host_dest = os.path.join(self.output_dir, rep_filename)

            exec_args = [
                self.container_cli, "exec", "-i", spec.container_name,
                "python3", f"/datas/{spec.script_name}",
                "-m", mode,
                "-f", fmt,
                "-o", in_container_out
            ]
            if mode == "ssh":
                exec_args.extend(["-r", "127.0.0.1"])

            try:
                p = subprocess.run(exec_args, capture_output=True, text=True, timeout=timeout, check=False)
                if p.returncode == 0:
                    cp_res = subprocess.run([self.container_cli, "cp", f"{spec.container_name}:{in_container_out}", host_dest], capture_output=True, check=False)
                    if cp_res.returncode == 0 and os.path.exists(host_dest):
                        size = os.path.getsize(host_dest)
                        validations[fmt] = (size > 50, f"Valid ({size} bytes)")
                        extracted[fmt] = host_dest
                    else:
                        validations[fmt] = (False, "Failed to copy report to host")
                else:
                    validations[fmt] = (False, f"Script failed with code {p.returncode}: {p.stderr.strip()[:100]}")
            except subprocess.TimeoutExpired:
                validations[fmt] = (False, f"Execution timed out after {timeout}s")
            except Exception as exc:
                validations[fmt] = (False, f"Execution error: {exc}")

        return validations, extracted

    def execute_target_flow(
        self,
        spec: TargetE2ESpec,
        formats: Optional[List[str]] = None
    ) -> E2ERunResult:
        """Runs the complete E2E workflow for a single target."""
        start_time = time.time()
        t_meta = TemporalAuditMetadata.create_now()
        container_info = DockerContainerDiscovery.inspect_container(spec.container_name, container_cli=self.container_cli)

        if not container_info or not container_info.is_running:
            dur = time.time() - start_time
            t_meta.finish()
            return E2ERunResult(
                target_key=spec.key,
                container_name=spec.container_name,
                success=False,
                duration_sec=dur,
                error_message=f"Target container '{spec.container_name}' is not running or not found.",
                temporal_metadata=t_meta.to_dict()
            )

        validations, extracted = self.execute_in_container_audit(spec, mode="local", formats=formats)
        all_passed = all(v[0] for v in validations.values()) and len(validations) > 0
        dur = time.time() - start_time
        t_meta.finish()

        return E2ERunResult(
            target_key=spec.key,
            container_name=spec.container_name,
            success=all_passed,
            duration_sec=dur,
            format_validations=validations,
            extracted_reports=extracted,
            temporal_metadata=t_meta.to_dict()
        )

    def generate_e2e_summary_dashboard(self, results: List[E2ERunResult], output_file: Optional[str] = None) -> str:
        """Generates markdown summary report for E2E runs."""
        if not output_file:
            output_file = os.path.join(self.output_dir, "analyse_tests_e2e_local.md")

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total = len(results)
        passed = sum(1 for r in results if r.success)

        lines = [
            "# 🐳 Docker In-Container E2E Execution & Compliance Dashboard",
            "",
            f"**Generated:** `{now_str}` | **Total Target Suites:** `{total}` | **Passed:** `{passed}/{total}`",
            "",
            "## 📊 Target Execution Status",
            "",
            "| Target Key | Container | Status | Duration | Formats Validated | Reports |",
            "| :--- | :--- | :---: | :---: | :--- | :--- |",
        ]

        for r in results:
            st = "✅ PASS" if r.success else "❌ FAIL"
            fmts_str = ", ".join(f"{k.upper()}: {'✓' if v[0] else '✗'}" for k, v in r.format_validations.items()) or (r.error_message or "N/A")
            reps_str = ", ".join(f"[{k.upper()}](file://{p})" for k, p in r.extracted_reports.items()) or "N/A"
            lines.append(f"| `{r.target_key}` | `{r.container_name}` | {st} | `{r.duration_sec:.2f}s` | {fmts_str} | {reps_str} |")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return output_file
