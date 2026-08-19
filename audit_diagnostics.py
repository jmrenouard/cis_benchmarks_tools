#!/usr/bin/env python3
"""
Audit Diagnostics & Root Cause Analysis (RCA) Engine (Python PSL ONLY).
Categorizes test failures, command errors, and execution issues into structured
root-cause classifications to distinguish between genuine security non-compliance
and environmental / tooling defects.
"""

import os
import re
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any


class FailureCategory:
    """Standardized failure categories for CIS benchmark audits."""
    SECURITY_NON_COMPLIANCE = "SECURITY_NON_COMPLIANCE"
    MISSING_BINARY = "MISSING_BINARY"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    AUTH_FAILURE = "AUTH_FAILURE"
    CONNECTION_ERROR = "CONNECTION_ERROR"
    TIMEOUT = "TIMEOUT"
    SYNTAX_ERROR = "SYNTAX_ERROR"
    CONFIGURATION_NOT_FOUND = "CONFIGURATION_NOT_FOUND"
    MANUAL_ASSESSMENT_REQUIRED = "MANUAL_ASSESSMENT_REQUIRED"
    CLEAN_PASS = "CLEAN_PASS"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class FailureDiagnostic:
    """Structured diagnostic representation of a command or control result."""

    def __init__(
        self,
        category: str,
        severity: str,
        root_cause: str,
        remediation_suggestion: str,
        is_environment_error: bool,
        evidence: str = "",
        raw_error: str = "",
        command: str = "",
        returncode: int = 0
    ):
        self.category = category
        self.severity = severity
        self.root_cause = root_cause
        self.remediation_suggestion = remediation_suggestion
        self.is_environment_error = is_environment_error
        self.evidence = evidence
        self.raw_error = raw_error
        self.command = command
        self.returncode = returncode

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category,
            "severity": self.severity,
            "root_cause": self.root_cause,
            "remediation_suggestion": self.remediation_suggestion,
            "is_environment_error": self.is_environment_error,
            "evidence": self.evidence,
            "raw_error": self.raw_error,
            "command": self.command,
            "returncode": self.returncode
        }

    def __repr__(self) -> str:
        return f"<FailureDiagnostic category={self.category} env_err={self.is_environment_error} cause='{self.root_cause[:40]}...'>"


class CommandFailureClassifier:
    """Expert heuristics classifier for audit command I/O and CIS control outcomes."""

    MISSING_BINARY_PATTERNS = [
        r"command not found",
        r"No such file or directory",
        r"not installed",
        r"executable file not found",
        r"cannot execute binary file",
        r"which:\s*no\s+\S+\s+in",
    ]

    PERMISSION_PATTERNS = [
        r"Permission denied",
        r"Access denied",
        r"Operation not permitted",
        r"EACCES",
        r"must be run as root",
        r"requires root privileges",
        r"sudo:\s*a password is required",
    ]

    AUTH_PATTERNS = [
        r"password authentication failed",
        r"Access denied for user",
        r"Authentication failed",
        r"Auth failed",
        r"Login failed",
        r"Invalid password",
        r"AuthenticationFailed",
        r"wrong password",
    ]

    CONNECTION_PATTERNS = [
        r"Connection refused",
        r"could not connect to server",
        r"Can't connect to local MySQL server",
        r"Can't connect to MySQL server",
        r"is the server running locally and accepting",
        r"Network is unreachable",
        r"Connection timed out",
        r"No route to host",
        r"Failed to connect to",
        r"not reachable",
    ]

    TIMEOUT_PATTERNS = [
        r"Command execution timed out",
        r"timed out after \d+ seconds",
        r"TimeoutExpired",
        r"Operation timed out",
        r"statement timeout",
    ]

    SYNTAX_PATTERNS = [
        r"syntax error",
        r"You have an error in your SQL syntax",
        r"unknown option",
        r"unrecognized option",
        r"invalid option",
        r"Parse error",
        r"bad flag",
    ]

    @classmethod
    def classify(
        cls,
        command: str = "",
        stdout: str = "",
        stderr: str = "",
        returncode: int = 0,
        elapsed_sec: float = 0.0,
        target_hint: Optional[str] = None
    ) -> FailureDiagnostic:
        """Classify a raw command execution result into a FailureDiagnostic."""
        out_clean = (stdout or "").strip()
        err_clean = (stderr or "").strip()
        combined = f"{err_clean}\n{out_clean}".strip()

        if returncode == 0:
            return FailureDiagnostic(
                category=FailureCategory.CLEAN_PASS,
                severity="INFO",
                root_cause="Command executed successfully with return code 0",
                remediation_suggestion="None",
                is_environment_error=False,
                evidence=out_clean[:120] if out_clean else "Exit code 0",
                raw_error="",
                command=command,
                returncode=returncode
            )

        for pat in cls.TIMEOUT_PATTERNS:
            m = re.search(pat, combined, re.IGNORECASE)
            if m or elapsed_sec >= 10.0:
                evidence = m.group(0) if m else f"Execution elapsed {elapsed_sec:.2f}s"
                return FailureDiagnostic(
                    category=FailureCategory.TIMEOUT,
                    severity="HIGH",
                    root_cause=f"Command execution timed out after {elapsed_sec:.1f}s",
                    remediation_suggestion="Verify target responsiveness or check system load.",
                    is_environment_error=True,
                    evidence=evidence,
                    raw_error=combined,
                    command=command,
                    returncode=returncode
                )

        for pat in cls.MISSING_BINARY_PATTERNS:
            m = re.search(pat, combined, re.IGNORECASE)
            if m or returncode == 127:
                cmd_first = command.split()[0] if command else "executable"
                evidence = m.group(0) if m else f"Exit code {returncode}"
                return FailureDiagnostic(
                    category=FailureCategory.MISSING_BINARY,
                    severity="HIGH",
                    root_cause=f"Executable required by command is missing ({cmd_first})",
                    remediation_suggestion=f"Install client utility on target system for '{cmd_first}'.",
                    is_environment_error=True,
                    evidence=evidence,
                    raw_error=combined,
                    command=command,
                    returncode=returncode
                )

        for pat in cls.AUTH_PATTERNS:
            m = re.search(pat, combined, re.IGNORECASE)
            if m:
                return FailureDiagnostic(
                    category=FailureCategory.AUTH_FAILURE,
                    severity="HIGH",
                    root_cause="Database or service rejected provided credentials",
                    remediation_suggestion="Verify provided credentials (--user, --password, or ~/.my.cnf / .pgpass).",
                    is_environment_error=True,
                    evidence=m.group(0),
                    raw_error=combined,
                    command=command,
                    returncode=returncode
                )

        for pat in cls.CONNECTION_PATTERNS:
            m = re.search(pat, combined, re.IGNORECASE)
            if m:
                return FailureDiagnostic(
                    category=FailureCategory.CONNECTION_ERROR,
                    severity="HIGH",
                    root_cause="Target database or service is not reachable",
                    remediation_suggestion="Verify target service daemon is active and accepting connections.",
                    is_environment_error=True,
                    evidence=m.group(0),
                    raw_error=combined,
                    command=command,
                    returncode=returncode
                )

        for pat in cls.PERMISSION_PATTERNS:
            m = re.search(pat, combined, re.IGNORECASE)
            if m or returncode == 126:
                evidence = m.group(0) if m else f"Exit code {returncode}"
                return FailureDiagnostic(
                    category=FailureCategory.PERMISSION_DENIED,
                    severity="HIGH",
                    root_cause="Insufficient privileges to execute command or read target file",
                    remediation_suggestion="Run audit with appropriate sudo / administrative privileges.",
                    is_environment_error=True,
                    evidence=evidence,
                    raw_error=combined,
                    command=command,
                    returncode=returncode
                )

        for pat in cls.SYNTAX_PATTERNS:
            m = re.search(pat, combined, re.IGNORECASE)
            if m:
                return FailureDiagnostic(
                    category=FailureCategory.SYNTAX_ERROR,
                    severity="MEDIUM",
                    root_cause="CLI or SQL command contains invalid syntax",
                    remediation_suggestion="Check SQL/CLI dialect compatibility.",
                    is_environment_error=False,
                    evidence=m.group(0),
                    raw_error=combined,
                    command=command,
                    returncode=returncode
                )

        return FailureDiagnostic(
            category=FailureCategory.UNKNOWN_ERROR,
            severity="MEDIUM",
            root_cause=f"Command exited with non-zero status code {returncode}",
            remediation_suggestion="Inspect raw stderr/stdout logs.",
            is_environment_error=True,
            evidence=combined[:100] if combined else f"Exit code {returncode}",
            raw_error=combined,
            command=command,
            returncode=returncode
        )
