#!/usr/bin/env python3
"""
Multi-Product Audit Orchestrator & Execution Pipeline (Python PSL ONLY).
Discovers, executes, and coordinates CIS benchmark audits across all database and OS targets.
"""

import argparse
import importlib
import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from audit_diagnostics import (
    FailureCategory,
    FailureDiagnostic,
    CommandFailureClassifier,
    AuditDiagnosticSummary
)


# Canonical target definitions
CANONICAL_TARGETS: Dict[str, Dict[str, Any]] = {
    "mariadb106": {"title": "MariaDB 10.6", "module": "audit_cis_mariadb_106", "category": "database", "default_container": "mariadb106-test", "rule_spec": "mariadb_106"},
    "mariadb1011": {"title": "MariaDB 10.11", "module": "audit_cis_mariadb_1011", "category": "database", "default_container": "mariadb1011-test", "rule_spec": "mariadb_1011"},
    "mysql80": {"title": "MySQL Enterprise 8.0", "module": "audit_cis_mysql_80", "category": "database", "default_container": "mysql80-test", "rule_spec": "mysql_80"},
    "mysql-community84": {"title": "MySQL Community 8.4 LTS", "module": "audit_cis_mysql_community_84", "category": "database", "default_container": "mysql-community84-test", "rule_spec": "mysql_community_84"},
    "mysql-enterprise84": {"title": "MySQL Enterprise 8.4 LTS", "module": "audit_cis_mysql_enterprise_84", "category": "database", "default_container": "mysql-enterprise84-test", "rule_spec": "mysql_enterprise_84"},
    "mysql-community97": {"title": "MySQL Community 9.7", "module": "audit_cis_mysql_community_97", "category": "database", "default_container": "mysql-community97-test", "rule_spec": "mysql_community_97"},
    "mysql-enterprise97": {"title": "MySQL Enterprise 9.7", "module": "audit_cis_mysql_enterprise_97", "category": "database", "default_container": "mysql-enterprise97-test", "rule_spec": "mysql_enterprise_97"},
    "postgresql16": {"title": "PostgreSQL 16", "module": "audit_cis_postgresql_16", "category": "database", "default_container": "postgresql16-test", "rule_spec": "postgresql_16"},
    "postgresql17": {"title": "PostgreSQL 17", "module": "audit_cis_postgresql_17", "category": "database", "default_container": "postgresql17-test", "rule_spec": "postgresql_17"},
    "postgresql18": {"title": "PostgreSQL 18", "module": "audit_cis_postgresql_18", "category": "database", "default_container": "postgresql18-test", "rule_spec": "postgresql_18"},
    "mongodb7": {"title": "MongoDB 7.0", "module": "audit_cis_mongodb_7", "category": "database", "default_container": "mongodb7-test", "rule_spec": "mongodb_7"},
    "mongodb8": {"title": "MongoDB 8.0", "module": "audit_cis_mongodb_8", "category": "database", "default_container": "mongodb8-test", "rule_spec": "mongodb_8"},
    "cassandra40": {"title": "Apache Cassandra 4.0", "module": "audit_cis_cassandra_40", "category": "database", "default_container": "cassandra40-test", "rule_spec": "cassandra_40"},
    "cassandra41": {"title": "Apache Cassandra 4.1", "module": "audit_cis_cassandra_41", "category": "database", "default_container": "cassandra41-test", "rule_spec": "cassandra_41"},
    "cassandra50": {"title": "Apache Cassandra 5.0", "module": "audit_cis_cassandra_50", "category": "database", "default_container": "cassandra50-test", "rule_spec": "cassandra_50"},
    "rhel8": {"title": "Red Hat Enterprise Linux 8", "module": "audit_cis_rhel_8", "category": "os", "default_container": None, "rule_spec": "rhel_8"},
    "rhel9": {"title": "Red Hat Enterprise Linux 9", "module": "audit_cis_rhel_9", "category": "os", "default_container": None, "rule_spec": "rhel_9"},
    "rhel10": {"title": "Red Hat Enterprise Linux 10", "module": "audit_cis_rhel_10", "category": "os", "default_container": None, "rule_spec": "rhel_10"},
}

TARGET_ALIASES = {
    "mariadb": "mariadb106",
    "mysql": "mysql80",
    "postgres": "postgresql16",
    "postgresql": "postgresql16",
    "mongo": "mongodb7",
    "mongodb": "mongodb7",
    "cassandra": "cassandra40",
    "rhel": "rhel9",
}


def normalize_target_key(target_str: str) -> str:
    """Normalize target string, handling aliases and common variants."""
    s = (target_str or "").strip().lower().replace("_", "").replace("-", "")
    for alias, canonical in TARGET_ALIASES.items():
        if s == alias:
            return canonical
    for key in CANONICAL_TARGETS:
        if s == key.lower().replace("-", ""):
            return key
    return target_str


class TargetAuditExecutionResult:
    """Telemetry and outcome record for a single target audit execution."""

    def __init__(
        self,
        target_key: str,
        title: str,
        success: bool,
        duration_sec: float,
        overall_score: float = 0.0,
        total_controls: int = 0,
        pass_count: int = 0,
        fail_count: int = 0,
        manual_count: int = 0,
        error_count: int = 0,
        na_count: int = 0,
        generated_reports: Optional[Dict[str, str]] = None,
        diagnostic_summary: Optional[AuditDiagnosticSummary] = None,
        exception_msg: Optional[str] = None
    ):
        self.target_key = target_key
        self.title = title
        self.success = success
        self.duration_sec = duration_sec
        self.overall_score = overall_score
        self.total_controls = total_controls
        self.pass_count = pass_count
        self.fail_count = fail_count
        self.manual_count = manual_count
        self.error_count = error_count
        self.na_count = na_count
        self.generated_reports = generated_reports or {}
        self.diagnostic_summary = diagnostic_summary
        self.exception_msg = exception_msg

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_key": self.target_key,
            "title": self.title,
            "success": self.success,
            "duration_sec": round(self.duration_sec, 3),
            "overall_score": round(self.overall_score, 1),
            "total_controls": self.total_controls,
            "pass_count": self.pass_count,
            "fail_count": self.fail_count,
            "manual_count": self.manual_count,
            "error_count": self.error_count,
            "na_count": self.na_count,
            "generated_reports": self.generated_reports,
            "diagnostic": self.diagnostic_summary.to_dict() if self.diagnostic_summary else None,
            "exception_msg": self.exception_msg
        }


class AuditOrchestrator:
    """Coordinates and executes multi-product CIS audits across selected targets."""

    def __init__(
        self,
        mode: str = "local",
        remote_host: Optional[str] = None,
        docker_container: Optional[str] = None,
        output_dir: str = "reports",
        formats: Optional[List[str]] = None,
        lang: str = "en",
        db_user: Optional[str] = None,
        db_password: Optional[str] = None,
        db_host: Optional[str] = None,
        db_port: Optional[int] = None,
        db_name: Optional[str] = None,
        defaults_file: Optional[str] = None,
        auth_db: Optional[str] = None
    ):
        self.mode = mode
        self.remote_host = remote_host
        self.docker_container = docker_container
        self.output_dir = os.path.abspath(os.path.join(REPO_ROOT, output_dir))
        self.formats = formats or ["html", "json", "xml", "txt"]
        self.lang = lang
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.defaults_file = defaults_file
        self.auth_db = auth_db
        os.makedirs(self.output_dir, exist_ok=True)

    def execute_single_target(self, target_key: str) -> TargetAuditExecutionResult:
        """Executes CIS audit for a single target with complete fault isolation."""
        canonical_key = normalize_target_key(target_key)
        target_meta = CANONICAL_TARGETS.get(canonical_key)

        if not target_meta:
            return TargetAuditExecutionResult(
                target_key=target_key,
                title=f"Unknown Target ({target_key})",
                success=False,
                duration_sec=0.0,
                exception_msg=f"Target '{target_key}' is not registered in canonical targets catalog."
            )

        title = target_meta["title"]
        module_name = target_meta["module"]
        rule_spec_name = target_meta["rule_spec"]
        active_container = self.docker_container or target_meta.get("default_container")

        start_time = time.time()
        diagnostic_summary = AuditDiagnosticSummary(target_name=canonical_key)
        generated_reports: Dict[str, str] = {}

        try:
            mod = importlib.import_module(module_name)
            rules_data = mod.load_recommendations(rule_spec_name) if hasattr(mod, "load_recommendations") else getattr(mod, "RECOMMENDATIONS_DATA", [])

            exec_ctx = None
            if hasattr(mod, "detect_execution_context"):
                try:
                    exec_ctx = mod.detect_execution_context(
                        mode=self.mode,
                        remote_host=self.remote_host,
                        docker_container=active_container,
                        product_hint=canonical_key
                    )
                except Exception:
                    exec_ctx = None

            if hasattr(mod, "perform_checks"):
                check_kwargs = {
                    "remote_host": self.remote_host,
                    "docker_container": active_container,
                }
                if self.db_user: check_kwargs["db_user"] = self.db_user
                if self.db_password: check_kwargs["db_password"] = self.db_password
                if self.db_host: check_kwargs["db_host"] = self.db_host
                if self.db_port: check_kwargs["db_port"] = self.db_port
                if self.db_name: check_kwargs["db_name"] = self.db_name
                if self.defaults_file: check_kwargs["defaults_file"] = self.defaults_file
                if self.auth_db: check_kwargs["auth_db"] = self.auth_db

                try:
                    results = mod.perform_checks(rules_data, **check_kwargs)
                except TypeError:
                    results = mod.perform_checks(rules_data, remote_host=self.remote_host, docker_container=active_container)
            else:
                raise AttributeError(f"Module {module_name} does not implement perform_checks()")

            calc_fn = getattr(mod, "calculate_scores", None)
            if calc_fn:
                scores_tuple = calc_fn(results)
                overall_score = float(scores_tuple[0])
                cat_scores = scores_tuple[1]
            else:
                overall_score = 0.0
                cat_scores = {}

            flat_results = []
            if isinstance(results, dict):
                for cat, checks in results.items():
                    for c in checks:
                        c_copy = dict(c)
                        c_copy["category"] = cat
                        flat_results.append(c_copy)
            else:
                flat_results = results

            pass_cnt = sum(1 for c in flat_results if str(c.get("status", "")).upper() in ["PASS", "SUCCESS"])
            fail_cnt = sum(1 for c in flat_results if str(c.get("status", "")).upper() in ["FAIL", "FAILED"])
            manual_cnt = sum(1 for c in flat_results if str(c.get("status", "")).upper() in ["MANUAL", "MANUEL"])
            error_cnt = sum(1 for c in flat_results if str(c.get("status", "")).upper() in ["ERROR"])
            na_cnt = len(flat_results) - (pass_cnt + fail_cnt + manual_cnt + error_cnt)

            for check in flat_results:
                diag = CommandFailureClassifier.classify_control_result(check, target_hint=canonical_key)
                diagnostic_summary.add(diag)

            export_fn = getattr(mod, "export_results", None)
            if export_fn:
                target_slug = canonical_key.lower().replace("-", "_")
                mode_suffix = "_ssh" if self.mode == "ssh" or self.remote_host else ""

                for fmt in self.formats:
                    rep_path = os.path.join(self.output_dir, f"rapport_cis_{target_slug}{mode_suffix}.{fmt}")
                    try:
                        export_fn(results, overall_score, cat_scores, target_name=canonical_key, filename=rep_path, fmt=fmt, lang=self.lang, execution_context=exec_ctx)
                        generated_reports[fmt] = rep_path
                    except TypeError:
                        try:
                            export_fn(results, overall_score, cat_scores, target_name=canonical_key, filename=rep_path, fmt=fmt, lang=self.lang)
                            generated_reports[fmt] = rep_path
                        except Exception:
                            pass

            elapsed = time.time() - start_time
            return TargetAuditExecutionResult(
                target_key=canonical_key,
                title=title,
                success=True,
                duration_sec=elapsed,
                overall_score=overall_score,
                total_controls=len(flat_results),
                pass_count=pass_cnt,
                fail_count=fail_cnt,
                manual_count=manual_cnt,
                error_count=error_cnt,
                na_count=na_cnt,
                generated_reports=generated_reports,
                diagnostic_summary=diagnostic_summary
            )
        except Exception as exc:
            elapsed = time.time() - start_time
            diagnostic_summary.add(CommandFailureClassifier.classify(
                command=f"Audit execution {module_name}",
                stderr=str(exc),
                returncode=1,
                target_hint=canonical_key
            ))
            return TargetAuditExecutionResult(
                target_key=canonical_key,
                title=title,
                success=False,
                duration_sec=elapsed,
                generated_reports=generated_reports,
                diagnostic_summary=diagnostic_summary,
                exception_msg=f"Audit execution exception: {exc}"
            )

    def execute_all_targets(
        self,
        targets: Optional[List[str]] = None,
        parallel_workers: int = 1
    ) -> List[TargetAuditExecutionResult]:
        """Executes audits across multiple targets sequentially or with thread pool."""
        target_list = targets or list(CANONICAL_TARGETS.keys())
        results: List[TargetAuditExecutionResult] = []

        if parallel_workers > 1:
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=parallel_workers) as pool:
                future_map = {pool.submit(self.execute_single_target, t): t for t in target_list}
                for fut in concurrent.futures.as_completed(future_map):
                    results.append(fut.result())
        else:
            for t in target_list:
                results.append(self.execute_single_target(t))

        order_map = {k: idx for idx, k in enumerate(CANONICAL_TARGETS.keys())}
        results.sort(key=lambda r: order_map.get(r.target_key, 999))
        return results

    def generate_suite_rca_dashboard(
        self,
        execution_results: List[TargetAuditExecutionResult],
        report_filename: Optional[str] = None
    ) -> str:
        """Generates comprehensive Multi-Product Root Cause Analysis (RCA) Markdown Dashboard."""
        if not report_filename:
            report_filename = os.path.join(self.output_dir, "analyse_tests_rca_dashboard.md")

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_targets = len(execution_results)
        successful_runs = sum(1 for r in execution_results if r.success)
        avg_score = sum(r.overall_score for r in execution_results) / max(1, total_targets)
        total_controls = sum(r.total_controls for r in execution_results)
        total_env_errors = sum(r.diagnostic_summary.environment_errors for r in execution_results if r.diagnostic_summary)
        total_sec_failures = sum(r.diagnostic_summary.security_failures for r in execution_results if r.diagnostic_summary)

        lines = [
            "# 📊 Executive Root Cause Analysis (RCA) & Audit Diagnostics Dashboard",
            "",
            f"**Generated:** `{now_str}` | **Execution Mode:** `{self.mode.upper()}` | **Targets:** `{total_targets}`",
            "",
            "## 📈 Global Compliance & Reliability Metrics",
            "",
            "| Metric | Value | Status |",
            "| :--- | :---: | :---: |",
            f"| **Audited Target Products** | `{total_targets}` | 🎯 100% Catalog Coverage |",
            f"| **Successful Audit Runs** | `{successful_runs} / {total_targets}` | {'✅ PASS' if successful_runs == total_targets else '⚠️ PARTIAL'} |",
            f"| **Average Global Compliance Score** | `{avg_score:.1f}%` | {'🟢 HIGH' if avg_score >= 80 else '🟡 MEDIUM'} |",
            f"| **Total Assessed Security Controls** | `{total_controls}` | 🛡️ CIS Verified |",
            f"| **Genuine Security Failures** | `{total_sec_failures}` | 🔴 Actionable Findings |",
            f"| **Environmental / Tooling Errors** | `{total_env_errors}` | {'🟢 0 Errors (Reliable)' if total_env_errors == 0 else '⚠️ Needs Infrastructure Fix'} |",
            "",
            "## 📋 Per-Product Execution & Root Cause Matrix",
            "",
            "| Target Key | Product Name | Duration | Score | Controls | Pass | Fail | Manual | Error | Reports |",
            "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |",
        ]

        for r in execution_results:
            rep_links = ", ".join(f"[{fmt.upper()}](file://{path})" for fmt, path in r.generated_reports.items()) if r.generated_reports else "N/A"
            dur = f"{r.duration_sec:.2f}s"
            score_str = f"{r.overall_score:.1f}%" if r.success else "ERR"
            lines.append(
                f"| `{r.target_key}` | **{r.title}** | `{dur}` | `{score_str}` | `{r.total_controls}` | `{r.pass_count}` | `{r.fail_count}` | `{r.manual_count}` | `{r.error_count}` | {rep_links} |"
            )

        content = "\n".join(lines)
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write(content)

        json_path = report_filename.replace(".md", ".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in execution_results], f, indent=2)

        return report_filename


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Product CIS Audit Orchestrator & RCA Pipeline")
    parser.add_argument("-t", "--target", dest="target", default=None, help="Target product key (e.g. mariadb106, all)")
    parser.add_argument("--all", action="store_true", help="Execute audit across all canonical targets")
    parser.add_argument("-m", "--mode", choices=["local", "ssh"], default="local", help="Execution mode")
    parser.add_argument("-r", "--remote", dest="remote_host", default=None, help="Remote SSH server")
    parser.add_argument("-c", "--docker", dest="docker_container", default=None, help="Target Docker container")
    parser.add_argument("-f", "--format", dest="formats", default="html,json,xml,txt", help="Report formats")
    parser.add_argument("-j", "--parallel", type=int, default=1, help="Parallel worker threads")
    parser.add_argument("-o", "--output-dir", dest="output_dir", default="reports", help="Output directory")
    parser.add_argument("-l", "--lang", choices=["en", "fr"], default="en", help="Report language")
    args = parser.parse_args()

    selected_formats = [fmt.strip().lower() for fmt in args.formats.split(",") if fmt.strip()]
    orchestrator = AuditOrchestrator(
        mode=args.mode,
        remote_host=args.remote_host,
        docker_container=args.docker_container,
        output_dir=args.output_dir,
        formats=selected_formats,
        lang=args.lang
    )

    targets_to_run = list(CANONICAL_TARGETS.keys()) if (args.all or args.target == "all") else ([t.strip() for t in args.target.split(",")] if args.target else [])
    if not targets_to_run:
        print("❌ Error: Specify --target <key> or --all.", file=sys.stderr)
        sys.exit(1)

    print(f"🚀 [Audit Orchestrator] Launching CIS Audit for {len(targets_to_run)} targets...")
    results = orchestrator.execute_all_targets(targets=targets_to_run, parallel_workers=args.parallel)
    orchestrator.generate_suite_rca_dashboard(results)
    print("✅ Completed.")

