#!/usr/bin/env python3
"""
Crash-Resilient Post-Execution Audit Report Publisher (Python PSL ONLY).
Guarantees atomic file writing and deterministic report generation across all target formats
even in the presence of partial audit test failures or unhandled exceptions.
"""

import os
import sys
import tempfile
import time
from typing import Callable, Dict, List, Optional, Tuple, Any

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from temporal_metadata import TemporalAuditMetadata


def atomic_write_text(file_path: str, content: str, encoding: str = "utf-8") -> str:
    """Writes text to a destination path atomically using a temporary file and atomic rename."""
    abs_path = os.path.abspath(file_path)
    parent_dir = os.path.dirname(abs_path)
    os.makedirs(parent_dir, exist_ok=True)

    # Use NamedTemporaryFile in the same filesystem directory to ensure atomic os.replace
    prefix = f".tmp_pub_{os.getpid()}_"
    tmp_fd, tmp_path = tempfile.mkstemp(prefix=prefix, dir=parent_dir, text=True)
    try:
        with open(tmp_fd, "w", encoding=encoding) as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, abs_path)
    except Exception:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        raise
    return abs_path


class AuditReportPublisher:
    """Coordinates unconditional report export and atomic delivery to reports/ directory."""

    def __init__(
        self,
        target_name: str,
        output_dir: str = "reports",
        custom_output: Optional[str] = None,
        formats: Optional[List[str]] = None,
        temporal_metadata: Optional[TemporalAuditMetadata] = None
    ):
        self.target_name = target_name
        self.output_dir = os.path.abspath(os.path.join(REPO_ROOT, output_dir))
        self.custom_output = custom_output
        self.formats = formats or ["html", "json", "xml", "txt"]
        self.temporal_metadata = temporal_metadata or TemporalAuditMetadata.create_now()
        self.published_reports: Dict[str, str] = {}
        os.makedirs(self.output_dir, exist_ok=True)

    def resolve_destination(self, fmt: str) -> str:
        """Determines destination file path for a given format."""
        if self.custom_output and (len(self.formats) == 1 or fmt == self.formats[0]):
            return os.path.abspath(self.custom_output)

        slug = self.target_name.lower().replace(" ", "_").replace(".", "")
        filename = f"rapport_cis_{slug}.{fmt}"
        return os.path.join(self.output_dir, filename)

    def publish_content(self, fmt: str, content: str) -> str:
        """Atomically writes content for the given format."""
        dest = self.resolve_destination(fmt)
        atomic_write_text(dest, content)
        self.published_reports[fmt] = dest
        return dest

    def execute_with_guaranteed_publishing(
        self,
        audit_func: Callable[[], Tuple[Any, float, Dict[str, Any]]],
        export_func: Callable[..., Any],
        lang: str = "en",
        execution_context: Optional[Any] = None
    ) -> Tuple[bool, Optional[Exception], Dict[str, str]]:
        """
        Executes the audit function and guarantees that export_func is called in a finally block.
        Returns: (success_bool, exception_if_any, published_reports_dict)
        """
        success = False
        captured_exc = None
        results = {}
        overall_score = 0.0
        categories_scores = {}

        try:
            results, overall_score, categories_scores, *extra = audit_func()
            success = True
        except Exception as exc:
            captured_exc = exc
            # Fallback results structure to allow emergency reporting
            results = {"Execution Failure": [{"number": "ERR.1", "name": f"Audit exception: {exc}", "status": "Error", "output": str(exc), "test_procedure": "Audit Runner", "remediation": "Investigate runtime logs"}]}
            overall_score = 0.0
            categories_scores = {"Execution Failure": {"score": 0.0, "passed_automated": 0, "failed_automated": 0, "manual_checks": 0, "error_checks": 1, "na_checks": 0}}
        finally:
            self.temporal_metadata.finish()
            for fmt in self.formats:
                dest = self.resolve_destination(fmt)
                try:
                    export_func(
                        results=results,
                        overall_score=overall_score,
                        categories_scores=categories_scores,
                        target_name=self.target_name,
                        filename=dest,
                        fmt=fmt,
                        lang=lang,
                        execution_context=execution_context,
                        temporal_metadata=self.temporal_metadata
                    )
                    self.published_reports[fmt] = dest
                except TypeError:
                    try:
                        export_func(
                            results=results,
                            overall_score=overall_score,
                            categories_scores=categories_scores,
                            target_name=self.target_name,
                            filename=dest,
                            fmt=fmt,
                            lang=lang,
                            execution_context=execution_context
                        )
                        self.published_reports[fmt] = dest
                    except Exception as exp_err:
                        print(f"⚠️ Warning: Export failed for format {fmt}: {exp_err}", file=sys.stderr)

        return success, captured_exc, self.published_reports
