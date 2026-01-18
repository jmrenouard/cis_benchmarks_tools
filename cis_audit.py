#!/usr/bin/env python3
"""
CIS Benchmarks Audit Tool

This script automates CIS (Center for Internet Security) benchmarks audit
for Linux systems. It performs security configuration checks and generates
detailed reports.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required but not installed.", file=sys.stderr)
    print("Please install it using: pip install --user PyYAML", file=sys.stderr)
    sys.exit(1)


class BenchmarkCheck:
    """Base class for individual benchmark checks."""
    
    def __init__(self, check_id, title, description, severity="medium"):
        self.check_id = check_id
        self.title = title
        self.description = description
        self.severity = severity
        self.status = "not_run"
        self.result = None
        self.message = ""
        self.remediation = ""
    
    def run(self):
        """Execute the check. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement run()")
    
    def to_dict(self):
        """Convert check results to dictionary."""
        return {
            "check_id": self.check_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "status": self.status,
            "result": self.result,
            "message": self.message,
            "remediation": self.remediation
        }


class CommandCheck(BenchmarkCheck):
    """Check that executes a shell command."""
    
    def __init__(self, check_id, title, description, command, 
                 expected_output=None, should_exist=True, severity="medium", remediation=""):
        super().__init__(check_id, title, description, severity)
        self.command = command
        self.expected_output = expected_output
        self.should_exist = should_exist
        self.remediation = remediation
    
    def run(self):
        """Execute the command and evaluate results."""
        try:
            result = subprocess.run(
                self.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout.strip() + result.stderr.strip()
            
            if self.expected_output:
                if self.expected_output in output:
                    self.status = "pass"
                    self.result = True
                    self.message = f"Expected output found: {self.expected_output}"
                else:
                    self.status = "fail"
                    self.result = False
                    self.message = f"Expected output not found. Got: {output[:200]}"
            else:
                if result.returncode == 0 and self.should_exist:
                    self.status = "pass"
                    self.result = True
                    self.message = "Command executed successfully"
                elif result.returncode != 0 and not self.should_exist:
                    self.status = "pass"
                    self.result = True
                    self.message = "Command failed as expected"
                else:
                    self.status = "fail"
                    self.result = False
                    self.message = f"Command exit code: {result.returncode}"
            
        except subprocess.TimeoutExpired:
            self.status = "error"
            self.result = False
            self.message = "Command execution timeout"
        except Exception as e:
            self.status = "error"
            self.result = False
            self.message = f"Error executing command: {str(e)}"
        
        return self.result


class FileCheck(BenchmarkCheck):
    """Check that verifies file permissions or existence."""
    
    def __init__(self, check_id, title, description, filepath, 
                 expected_perms=None, should_exist=True, severity="medium", remediation=""):
        super().__init__(check_id, title, description, severity)
        self.filepath = filepath
        self.expected_perms = expected_perms
        self.should_exist = should_exist
        self.remediation = remediation
    
    def run(self):
        """Check file existence and permissions."""
        try:
            exists = os.path.exists(self.filepath)
            
            if self.should_exist and not exists:
                self.status = "fail"
                self.result = False
                self.message = f"File {self.filepath} does not exist"
                return False
            
            if not self.should_exist and exists:
                self.status = "fail"
                self.result = False
                self.message = f"File {self.filepath} should not exist"
                return False
            
            if not exists:
                self.status = "pass"
                self.result = True
                self.message = "File does not exist as expected"
                return True
            
            if self.expected_perms:
                stat_info = os.stat(self.filepath)
                actual_perms = oct(stat_info.st_mode)[-3:]
                
                if actual_perms == self.expected_perms:
                    self.status = "pass"
                    self.result = True
                    self.message = f"File permissions are correct: {actual_perms}"
                else:
                    self.status = "fail"
                    self.result = False
                    self.message = f"Expected {self.expected_perms}, got {actual_perms}"
            else:
                self.status = "pass"
                self.result = True
                self.message = "File exists as expected"
            
        except Exception as e:
            self.status = "error"
            self.result = False
            self.message = f"Error checking file: {str(e)}"
        
        return self.result


class CISAuditor:
    """Main auditor class that coordinates benchmark checks."""
    
    def __init__(self, config_file=None):
        self.checks = []
        self.config = {}
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "hostname": self._get_hostname(),
            "total_checks": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "checks": []
        }
        
        if config_file:
            self.load_config(config_file)
    
    def _get_hostname(self):
        """Get system hostname."""
        try:
            return subprocess.check_output(['hostname'], text=True).strip()
        except Exception:
            return "unknown"
    
    def load_config(self, config_file):
        """Load checks from YAML configuration file."""
        try:
            with open(config_file, 'r') as f:
                self.config = yaml.safe_load(f)
            
            if 'checks' in self.config:
                for check_config in self.config['checks']:
                    check_type = check_config.get('type', 'command')
                    
                    if check_type == 'command':
                        check = CommandCheck(
                            check_id=check_config.get('id', 'unknown'),
                            title=check_config.get('title', ''),
                            description=check_config.get('description', ''),
                            command=check_config.get('command', ''),
                            expected_output=check_config.get('expected_output'),
                            should_exist=check_config.get('should_exist', True),
                            severity=check_config.get('severity', 'medium'),
                            remediation=check_config.get('remediation', '')
                        )
                        self.checks.append(check)
                    
                    elif check_type == 'file':
                        check = FileCheck(
                            check_id=check_config.get('id', 'unknown'),
                            title=check_config.get('title', ''),
                            description=check_config.get('description', ''),
                            filepath=check_config.get('filepath', ''),
                            expected_perms=check_config.get('expected_perms'),
                            should_exist=check_config.get('should_exist', True),
                            severity=check_config.get('severity', 'medium'),
                            remediation=check_config.get('remediation', '')
                        )
                        self.checks.append(check)
            
            print(f"Loaded {len(self.checks)} checks from {config_file}")
            
        except Exception as e:
            print(f"Error loading configuration: {e}", file=sys.stderr)
            sys.exit(1)
    
    def add_check(self, check):
        """Add a benchmark check."""
        self.checks.append(check)
    
    def run_all_checks(self):
        """Execute all registered checks."""
        print(f"\nRunning {len(self.checks)} CIS benchmark checks...\n")
        
        for i, check in enumerate(self.checks, 1):
            print(f"[{i}/{len(self.checks)}] {check.check_id}: {check.title}...", end=" ")
            check.run()
            
            if check.status == "pass":
                print("✓ PASS")
                self.results["passed"] += 1
            elif check.status == "fail":
                print("✗ FAIL")
                self.results["failed"] += 1
            else:
                print("⚠ ERROR")
                self.results["errors"] += 1
            
            self.results["checks"].append(check.to_dict())
        
        self.results["total_checks"] = len(self.checks)
        
        print(f"\n{'='*60}")
        print(f"Summary: {self.results['passed']} passed, "
              f"{self.results['failed']} failed, "
              f"{self.results['errors']} errors")
        print(f"{'='*60}\n")
    
    def generate_report(self, output_file, format="json"):
        """Generate audit report in specified format."""
        if format == "json":
            with open(output_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"JSON report saved to: {output_file}")
        
        elif format == "text":
            with open(output_file, 'w') as f:
                f.write("CIS Benchmarks Audit Report\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Timestamp: {self.results['timestamp']}\n")
                f.write(f"Hostname: {self.results['hostname']}\n\n")
                f.write(f"Total Checks: {self.results['total_checks']}\n")
                f.write(f"Passed: {self.results['passed']}\n")
                f.write(f"Failed: {self.results['failed']}\n")
                f.write(f"Errors: {self.results['errors']}\n\n")
                f.write("=" * 60 + "\n\n")
                
                for check in self.results['checks']:
                    f.write(f"Check ID: {check['check_id']}\n")
                    f.write(f"Title: {check['title']}\n")
                    f.write(f"Severity: {check['severity']}\n")
                    f.write(f"Status: {check['status'].upper()}\n")
                    f.write(f"Message: {check['message']}\n")
                    if check['remediation']:
                        f.write(f"Remediation: {check['remediation']}\n")
                    f.write("-" * 60 + "\n\n")
            
            print(f"Text report saved to: {output_file}")
        
        elif format == "html":
            self._generate_html_report(output_file)
            print(f"HTML report saved to: {output_file}")
    
    def _generate_html_report(self, output_file):
        """Generate HTML report."""
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>CIS Benchmarks Audit Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
        .summary {{ background-color: #f8f9fa; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .summary-item {{ display: inline-block; margin-right: 30px; }}
        .check {{ margin: 20px 0; padding: 15px; border-left: 4px solid #ddd; background-color: #fafafa; }}
        .check.pass {{ border-left-color: #28a745; }}
        .check.fail {{ border-left-color: #dc3545; }}
        .check.error {{ border-left-color: #ffc107; }}
        .check-header {{ font-weight: bold; font-size: 1.1em; margin-bottom: 10px; }}
        .status {{ padding: 3px 8px; border-radius: 3px; color: white; font-weight: bold; }}
        .status.pass {{ background-color: #28a745; }}
        .status.fail {{ background-color: #dc3545; }}
        .status.error {{ background-color: #ffc107; color: #333; }}
        .severity {{ display: inline-block; padding: 3px 8px; border-radius: 3px; font-size: 0.9em; }}
        .severity.high {{ background-color: #dc3545; color: white; }}
        .severity.medium {{ background-color: #fd7e14; color: white; }}
        .severity.low {{ background-color: #ffc107; color: #333; }}
        .remediation {{ background-color: #e7f3ff; padding: 10px; margin-top: 10px; border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>CIS Benchmarks Audit Report</h1>
        
        <div class="summary">
            <div class="summary-item"><strong>Timestamp:</strong> {timestamp}</div>
            <div class="summary-item"><strong>Hostname:</strong> {hostname}</div>
            <div class="summary-item"><strong>Total Checks:</strong> {total_checks}</div>
            <div class="summary-item"><strong>Passed:</strong> <span style="color: #28a745;">{passed}</span></div>
            <div class="summary-item"><strong>Failed:</strong> <span style="color: #dc3545;">{failed}</span></div>
            <div class="summary-item"><strong>Errors:</strong> <span style="color: #ffc107;">{errors}</span></div>
        </div>
        
        <h2>Detailed Results</h2>
        {checks_html}
    </div>
</body>
</html>
"""
        
        checks_html = ""
        for check in self.results['checks']:
            remediation_html = ""
            if check.get('remediation'):
                remediation_html = f'<div class="remediation"><strong>Remediation:</strong> {check["remediation"]}</div>'
            
            checks_html += f"""
        <div class="check {check['status']}">
            <div class="check-header">
                {check['check_id']}: {check['title']}
                <span class="status {check['status']}">{check['status'].upper()}</span>
                <span class="severity {check['severity']}">{check['severity'].upper()}</span>
            </div>
            <div><strong>Description:</strong> {check['description']}</div>
            <div><strong>Message:</strong> {check['message']}</div>
            {remediation_html}
        </div>
"""
        
        html_content = html_template.format(
            timestamp=self.results['timestamp'],
            hostname=self.results['hostname'],
            total_checks=self.results['total_checks'],
            passed=self.results['passed'],
            failed=self.results['failed'],
            errors=self.results['errors'],
            checks_html=checks_html
        )
        
        with open(output_file, 'w') as f:
            f.write(html_content)


def create_default_checks():
    """Create default CIS benchmark checks for Linux systems."""
    checks = []
    
    # Check 1: Ensure password expiration is configured
    checks.append(CommandCheck(
        check_id="1.1.1",
        title="Ensure password expiration is 90 days or less",
        description="Password aging should be configured to prevent old passwords",
        command="grep ^PASS_MAX_DAYS /etc/login.defs",
        expected_output="PASS_MAX_DAYS",
        severity="medium",
        remediation="Set PASS_MAX_DAYS to 90 in /etc/login.defs"
    ))
    
    # Check 2: Ensure /etc/passwd permissions
    checks.append(FileCheck(
        check_id="1.2.1",
        title="Ensure permissions on /etc/passwd are configured",
        description="/etc/passwd should have 644 permissions",
        filepath="/etc/passwd",
        expected_perms="644",
        severity="high",
        remediation="Run: chmod 644 /etc/passwd"
    ))
    
    # Check 3: Ensure /etc/shadow permissions
    checks.append(FileCheck(
        check_id="1.2.2",
        title="Ensure permissions on /etc/shadow are configured",
        description="/etc/shadow should have 400 permissions",
        filepath="/etc/shadow",
        expected_perms="400",
        severity="high",
        remediation="Run: chmod 400 /etc/shadow"
    ))
    
    # Check 4: Ensure firewall is enabled
    checks.append(CommandCheck(
        check_id="2.1.1",
        title="Ensure firewall is enabled",
        description="A firewall should be running to protect the system",
        command="systemctl is-active ufw || systemctl is-active firewalld || systemctl is-active iptables",
        should_exist=True,
        severity="high",
        remediation="Enable firewall using ufw, firewalld, or iptables"
    ))
    
    # Check 5: Ensure SSH Protocol is set to 2
    checks.append(CommandCheck(
        check_id="3.1.1",
        title="Ensure SSH Protocol is set to 2",
        description="SSH should use protocol 2 only",
        command="grep '^Protocol 2' /etc/ssh/sshd_config || grep '^#Protocol' /etc/ssh/sshd_config",
        severity="high",
        remediation="Set 'Protocol 2' in /etc/ssh/sshd_config"
    ))
    
    return checks


def main():
    """Main entry point for CIS audit tool."""
    parser = argparse.ArgumentParser(
        description="CIS Benchmarks Audit Tool - Automate security configuration checks"
    )
    parser.add_argument(
        '-c', '--config',
        help='Path to YAML configuration file with custom checks',
        type=str
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file for report (default: cis_audit_report)',
        default='cis_audit_report',
        type=str
    )
    parser.add_argument(
        '-f', '--format',
        help='Report format: json, text, or html (default: json)',
        choices=['json', 'text', 'html'],
        default='json',
        type=str
    )
    parser.add_argument(
        '--use-defaults',
        help='Use default CIS checks even without config file',
        action='store_true'
    )
    
    args = parser.parse_args()
    
    # Create auditor instance
    auditor = CISAuditor(config_file=args.config if args.config else None)
    
    # Load default checks if requested or no config provided
    if args.use_defaults or (not args.config and len(auditor.checks) == 0):
        print("Loading default CIS benchmark checks...")
        for check in create_default_checks():
            auditor.add_check(check)
    
    if len(auditor.checks) == 0:
        print("No checks configured. Use --config or --use-defaults", file=sys.stderr)
        sys.exit(1)
    
    # Run all checks
    auditor.run_all_checks()
    
    # Generate report
    output_file = f"{args.output}.{args.format}"
    auditor.generate_report(output_file, format=args.format)
    
    # Exit with appropriate code
    if auditor.results['failed'] > 0 or auditor.results['errors'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
