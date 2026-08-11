#!/usr/bin/env python3
"""
CIS Red Hat Enterprise Linux 10 Benchmark Audit Script (Python Standard Library ONLY).
Version: 1.4.0

Executes security compliance audit for RHEL 10 against CIS Benchmark v1.0.1 recommendations.
Supports both local execution and SSH remote execution (--remote user@host).

Zero external dependencies: uses only Python Standard Library (argparse, json, subprocess, os, sys, re, html, datetime).
"""

import argparse
import datetime
import html
import json
import os
import re
import subprocess
import sys

RECOMMENDATIONS_DATA = [
    {
        "id": "1.1.1.1",
        "title": "Ensure cramfs kernel module is not available",
        "category": "Initial Setup",
        "subcategory": "Filesystem Kernel Modules",
        "type": "Automated",
        "level": 1,
        "description": "The cramfs filesystem type is a compressed read-only Linux filesystem type.",
        "rationale": "Removing support for unneeded filesystem types reduces the local attack surface.",
        "audit": "lsmod | grep cramfs ; modprobe -n -v cramfs",
        "remediation": "Create /etc/modprobe.d/cramfs.conf with 'install cramfs /bin/true'",
        "condition": {"type": "stdout_not_contains", "value": "cramfs"}
    },
    {
        "id": "1.1.1.2",
        "title": "Ensure freevxfs kernel module is not available",
        "category": "Initial Setup",
        "subcategory": "Filesystem Kernel Modules",
        "type": "Automated",
        "level": 1,
        "description": "The freevxfs filesystem format is a file system type supported by VERITAS Storage Foundation.",
        "rationale": "Removing support for unneeded filesystem types reduces the local attack surface.",
        "audit": "lsmod | grep freevxfs ; modprobe -n -v freevxfs",
        "remediation": "Create /etc/modprobe.d/freevxfs.conf with 'install freevxfs /bin/true'",
        "condition": {"type": "stdout_not_contains", "value": "freevxfs"}
    },
    {
        "id": "1.1.1.3",
        "title": "Ensure hfs kernel module is not available",
        "category": "Initial Setup",
        "subcategory": "Filesystem Kernel Modules",
        "type": "Automated",
        "level": 1,
        "description": "The hfs filesystem format is used by Mac OS.",
        "rationale": "Removing support for unneeded filesystem types reduces the local attack surface.",
        "audit": "lsmod | grep hfs ; modprobe -n -v hfs",
        "remediation": "Create /etc/modprobe.d/hfs.conf with 'install hfs /bin/true'",
        "condition": {"type": "stdout_not_contains", "value": "hfs"}
    },
    {
        "id": "1.1.1.4",
        "title": "Ensure hfsplus kernel module is not available",
        "category": "Initial Setup",
        "subcategory": "Filesystem Kernel Modules",
        "type": "Automated",
        "level": 1,
        "description": "The hfsplus filesystem format is used by Mac OS Plus.",
        "rationale": "Removing support for unneeded filesystem types reduces the local attack surface.",
        "audit": "lsmod | grep hfsplus ; modprobe -n -v hfsplus",
        "remediation": "Create /etc/modprobe.d/hfsplus.conf with 'install hfsplus /bin/true'",
        "condition": {"type": "stdout_not_contains", "value": "hfsplus"}
    },
    {
        "id": "1.1.1.5",
        "title": "Ensure jffs2 kernel module is not available",
        "category": "Initial Setup",
        "subcategory": "Filesystem Kernel Modules",
        "type": "Automated",
        "level": 1,
        "description": "Journaling Flash File System v2 is used for flash devices.",
        "rationale": "Removing support for unneeded filesystem types reduces the local attack surface.",
        "audit": "lsmod | grep jffs2 ; modprobe -n -v jffs2",
        "remediation": "Create /etc/modprobe.d/jffs2.conf with 'install jffs2 /bin/true'",
        "condition": {"type": "stdout_not_contains", "value": "jffs2"}
    },
    {
        "id": "1.1.1.6",
        "title": "Ensure squashfs kernel module is not available",
        "category": "Initial Setup",
        "subcategory": "Filesystem Kernel Modules",
        "type": "Automated",
        "level": 1,
        "description": "Squashfs is a compressed read-only filesystem for Linux.",
        "rationale": "Removing support for unneeded filesystem types reduces the local attack surface.",
        "audit": "lsmod | grep squashfs ; modprobe -n -v squashfs",
        "remediation": "Create /etc/modprobe.d/squashfs.conf with 'install squashfs /bin/true'",
        "condition": {"type": "stdout_not_contains", "value": "squashfs"}
    },
    {
        "id": "1.1.1.7",
        "title": "Ensure udf kernel module is not available",
        "category": "Initial Setup",
        "subcategory": "Filesystem Kernel Modules",
        "type": "Automated",
        "level": 1,
        "description": "Universal Disk Format (UDF) is a format for optical media.",
        "rationale": "Removing support for unneeded filesystem types reduces the local attack surface.",
        "audit": "lsmod | grep udf ; modprobe -n -v udf",
        "remediation": "Create /etc/modprobe.d/udf.conf with 'install udf /bin/true'",
        "condition": {"type": "stdout_not_contains", "value": "udf"}
    },
    {
        "id": "1.1.1.8",
        "title": "Ensure usb-storage kernel module is disabled",
        "category": "Initial Setup",
        "subcategory": "Filesystem Kernel Modules",
        "type": "Automated",
        "level": 1,
        "description": "The usb-storage driver allows connection of USB storage devices.",
        "rationale": "Restricting USB storage prevents unauthorized data exfiltration.",
        "audit": "lsmod | grep usb_storage ; modprobe -n -v usb-storage",
        "remediation": "Create /etc/modprobe.d/usb-storage.conf with 'install usb-storage /bin/true'",
        "condition": {"type": "stdout_not_contains", "value": "usb_storage"}
    },
    {
        "id": "1.3.1.1",
        "title": "Ensure SELinux is installed and active",
        "category": "Initial Setup",
        "subcategory": "SELinux",
        "type": "Automated",
        "level": 1,
        "description": "Security-Enhanced Linux (SELinux) provides Mandatory Access Control.",
        "rationale": "SELinux prevents unauthorized access and limits program damage.",
        "audit": "sestatus | grep 'SELinux status:'",
        "remediation": "Install selinux-policy and selinux-policy-targeted.",
        "condition": {"type": "stdout_contains", "value": "enabled"}
    },
    {
        "id": "1.3.1.2",
        "title": "Ensure SELinux state is enforcing",
        "category": "Initial Setup",
        "subcategory": "SELinux",
        "type": "Automated",
        "level": 1,
        "description": "SELinux must be set to enforcing mode.",
        "rationale": "Enforcing mode restricts operations violating security policy.",
        "audit": "getenforce",
        "remediation": "Set SELINUX=enforcing in /etc/selinux/config",
        "condition": {"type": "stdout_contains", "value": "Enforcing"}
    },
    {
        "id": "1.4.1",
        "title": "Ensure AIDE is installed",
        "category": "Initial Setup",
        "subcategory": "File Integrity Monitoring",
        "type": "Automated",
        "level": 1,
        "description": "AIDE checks file integrity against a baseline.",
        "rationale": "AIDE detects unauthorized modification of system files.",
        "audit": "rpm -q aide",
        "remediation": "Run dnf install aide",
        "condition": {"type": "stdout_contains", "value": "aide-"}
    },
    {
        "id": "2.1.1",
        "title": "Ensure xinetd is not installed",
        "category": "Services",
        "subcategory": "Special Purpose Services",
        "type": "Automated",
        "level": 1,
        "description": "xinetd daemon manages Internet services.",
        "rationale": "Unnecessary network services increase system attack surface.",
        "audit": "rpm -q xinetd",
        "remediation": "Run dnf remove xinetd",
        "condition": {"type": "stdout_contains", "value": "not installed"}
    },
    {
        "id": "2.2.1",
        "title": "Ensure telnet server is not installed",
        "category": "Services",
        "subcategory": "Service Clients",
        "type": "Automated",
        "level": 1,
        "description": "Telnet communicates in unencrypted plain text.",
        "rationale": "Telnet transmits passwords and data in cleartext.",
        "audit": "rpm -q telnet-server",
        "remediation": "Run dnf remove telnet-server",
        "condition": {"type": "stdout_contains", "value": "not installed"}
    },
    {
        "id": "3.1.1",
        "title": "Ensure IP forwarding is disabled",
        "category": "Network Configuration",
        "subcategory": "Network Parameters",
        "type": "Automated",
        "level": 1,
        "description": "IP forwarding allows a system to route packets between networks.",
        "rationale": "Systems not acting as routers should disable IP forwarding.",
        "audit": "sysctl net.ipv4.ip_forward",
        "remediation": "Set net.ipv4.ip_forward = 0 in /etc/sysctl.d/99-sysctl.conf",
        "condition": {"type": "stdout_contains", "value": "net.ipv4.ip_forward = 0"}
    },
    {
        "id": "3.1.2",
        "title": "Ensure packet redirect sending is disabled",
        "category": "Network Configuration",
        "subcategory": "Network Parameters",
        "type": "Automated",
        "level": 1,
        "description": "ICMP redirect packets tell hosts to alter routing tables.",
        "rationale": "Disabling ICMP redirects prevents malicious route manipulation.",
        "audit": "sysctl net.ipv4.conf.all.send_redirects",
        "remediation": "Set net.ipv4.conf.all.send_redirects = 0",
        "condition": {"type": "stdout_contains", "value": "net.ipv4.conf.all.send_redirects = 0"}
    },
    {
        "id": "3.4.1",
        "title": "Ensure firewalld is installed and running",
        "category": "Network Configuration",
        "subcategory": "Firewall Configuration",
        "type": "Automated",
        "level": 1,
        "description": "firewalld provides host-based firewall protection.",
        "rationale": "A firewall controls network access to the system.",
        "audit": "systemctl is-active firewalld",
        "remediation": "Run systemctl --now enable firewalld",
        "condition": {"type": "stdout_contains", "value": "active"}
    },
    {
        "id": "5.1.1",
        "title": "Ensure auditd service is enabled and running",
        "category": "Logging and Auditing",
        "subcategory": "System Auditing",
        "type": "Automated",
        "level": 1,
        "description": "auditd service collects security audit events.",
        "rationale": "Auditing records critical operations for security analysis.",
        "audit": "systemctl is-active auditd",
        "remediation": "Run systemctl --now enable auditd",
        "condition": {"type": "stdout_contains", "value": "active"}
    },
    {
        "id": "5.2.1",
        "title": "Ensure SSH PermitRootLogin is disabled",
        "category": "Access Control",
        "subcategory": "SSH Server Configuration",
        "type": "Automated",
        "level": 1,
        "description": "Disallow direct SSH login as root user.",
        "rationale": "Direct root logins prevent auditing user accountability.",
        "audit": "sshd -T 2>/dev/null | grep -i '^permitrootlogin'",
        "remediation": "Set 'PermitRootLogin no' in /etc/ssh/sshd_config",
        "condition": {"type": "stdout_contains", "value": "permitrootlogin no"}
    },
    {
        "id": "5.2.2",
        "title": "Ensure SSH PermitEmptyPasswords is disabled",
        "category": "Access Control",
        "subcategory": "SSH Server Configuration",
        "type": "Automated",
        "level": 1,
        "description": "Disallow accounts with empty passwords via SSH.",
        "rationale": "Authentication must require a valid password or key.",
        "audit": "sshd -T 2>/dev/null | grep -i '^permitemptypasswords'",
        "remediation": "Set 'PermitEmptyPasswords no' in /etc/ssh/sshd_config",
        "condition": {"type": "stdout_contains", "value": "permitemptypasswords no"}
    },
    {
        "id": "5.3.1",
        "title": "Ensure crypto policy is DEFAULT or FUTURE",
        "category": "System Cryptography",
        "subcategory": "Crypto Policies",
        "type": "Automated",
        "level": 1,
        "description": "System-wide crypto policies enforce cryptographic security levels.",
        "rationale": "Strong crypto policies prevent use of obsolete ciphers.",
        "audit": "update-crypto-policies --show",
        "remediation": "Run update-crypto-policies --set DEFAULT",
        "condition": {"type": "stdout_contains", "value": "DEFAULT"}
    }
]


def run_command(command, remote_host=None):
    """Execute command locally or via SSH remote execution without shell=True (PSL ONLY)."""
    try:
        if isinstance(command, str):
            cmd_args = ["/bin/bash", "-c", command]
        else:
            cmd_args = list(command)

        if remote_host:
            cmd_args = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", remote_host] + cmd_args

        process = subprocess.run(cmd_args, check=False, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10)
        return process.stdout.strip(), process.stderr.strip(), process.returncode
    except subprocess.TimeoutExpired:
        return "", "Command execution timed out after 10 seconds", -1
    except Exception as e:
        return "", str(e), -1



def perform_checks(recommendations, remote_host=None):
    """Execute all RHEL CIS & STIG security audit controls locally or remotely over SSH."""
    results = []
    for rec in recommendations:
        stdout, stderr, code = run_command(rec["audit"], remote_host=remote_host)
        is_pass = evaluate_condition(rec["condition"], stdout, stderr, code)
        status = "PASS" if is_pass else "FAIL"

        results.append({
            "id": rec.get("id", rec.get("number", "N/A")),
            "title": rec.get("title", rec.get("name", "N/A")),
            "category": rec.get("category", "General"),
            "status": status,
            "stdout": stdout,
            "stderr": stderr,
            "code": code,
            "output": stdout or stderr,
            "remediation": rec.get("remediation", "")
        })
    return results

def calculate_scores(results):
    """Calculate compliance score statistics."""
    passed = sum(1 for r in results if r["status"] == "PASS")
    total = len(results) if results else 1
    overall_score = (passed / total) * 100
    return overall_score, {}



def evaluate_condition(condition, stdout, stderr, returncode):
    """Evaluate audit command output against condition rules."""
    if not condition:
        return False

    c_type = condition.get("type")
    val = condition.get("value")

    if c_type == "stdout_contains":
        return val.lower() in stdout.lower()
    elif c_type == "stdout_not_contains":
        return val.lower() not in stdout.lower()
    elif c_type == "returncode_zero":
        return returncode == 0
    return False




def export_results(results, overall_score, categories_scores, target_name, filename, fmt="html", lang="en"):
    """Export audit results into HTML, JSON, XML, or TXT formats using PSL ONLY."""
    import json
    import os
    import xml.etree.ElementTree as ET
    from datetime import datetime

    if not filename:
        ext = "html" if fmt == "html" else fmt
        target_slug = target_name.lower().replace(" ", "_").replace(".", "")
        filename = f"reports/rapport_cis_{target_slug}.{ext}"

    if os.path.dirname(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Flatten results if dictionary categorized
    flat_results = []
    if isinstance(results, dict):
        for cat, checks in results.items():
            for c in checks:
                c_copy = dict(c)
                c_copy["category"] = cat
                flat_results.append(c_copy)
    else:
        flat_results = results

    if fmt == "json":
        data = {
            "benchmark": target_name,
            "report_date": datetime.now().isoformat(),
            "overall_score": overall_score,
            "total_checks": len(flat_results),
            "results": flat_results
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"📄 JSON Report successfully generated: {filename}")

    elif fmt == "xml":
        root = ET.Element("testsuite", name=target_name, tests=str(len(flat_results)), failures=str(sum(1 for r in flat_results if r.get("status") in ["FAIL", "Fail"])), timestamp=datetime.now().isoformat())
        for r in flat_results:
            tc = ET.SubElement(root, "testcase", id=str(r.get("number", r.get("id", ""))), name=str(r.get("name", r.get("title", ""))), classname=str(r.get("category", "")))
            if r.get("status") in ["FAIL", "Fail"]:
                failure = ET.SubElement(tc, "failure", message="Control failed")
                failure.text = str(r.get("output", r.get("stdout", "")))
            elif r.get("status") in ["ERROR", "Error"]:
                err = ET.SubElement(tc, "error", message="Control execution error")
                err.text = str(r.get("output", r.get("stderr", "")))
        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        print(f"📄 XML Report successfully generated: {filename}")

    elif fmt == "txt":
        lines = [
            "=" * 70,
            f"🛡️  {target_name} - CIS Benchmark Audit Report",
            f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Global Score: {overall_score:.1f}%",
            "=" * 70,
            ""
        ]
        for r in flat_results:
            status = r.get("status", "")
            status_icon = "[PASS]" if status in ["PASS", "Pass"] else ("[FAIL]" if status in ["FAIL", "Fail"] else "[MANUAL]")
            rec_id = r.get("number", r.get("id", ""))
            rec_name = r.get("name", r.get("title", ""))
            lines.append(f"{status_icon} {rec_id} - {rec_name}")
            lines.append(f"  Category: {r.get('category')}")
            out = r.get('output', r.get('stdout', ''))
            if out:
                lines.append(f"  Output: {str(out).strip()}")
            rem = r.get('remediation', '')
            if rem and status in ["FAIL", "Fail"]:
                lines.append(f"  Remediation: {str(rem).strip()}")
            lines.append("-" * 70)
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"📄 TXT Report successfully generated: {filename}")

    else:
        try:
            generate_html_report(results, overall_score, categories_scores, filename=filename, lang=lang)
        except TypeError:
            try:
                generate_html_report(results, overall_score, categories_scores, filename=filename)
            except TypeError:
                # Legacy positional args fallback
                generate_html_report(results, overall_score, categories_scores, 0, 0, 0, 0, 0, 0, 0, [], [], [], [], [], filename)



def generate_html_report(results, overall_score, categories_scores, filename="reports/rapport_cis_rhel_10.html"):
    """Generate responsive HTML audit report for RHEL 10."""
    if os.path.dirname(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    rows_html = ""
    for item in results:
        status_badge = '<span style="background-color: #def7ec; color: #03543f; padding: 4px 8px; border-radius: 4px; font-weight: bold;">PASS</span>' if item["status"] == "PASS" else '<span style="background-color: #fde8e8; color: #9b1c1c; padding: 4px 8px; border-radius: 4px; font-weight: bold;">FAIL</span>'
        rows_html += f"""
        <tr style="border-bottom: 1px solid #e5e7eb;">
            <td style="padding: 12px; font-weight: bold;">{html.escape(item['id'])}</td>
            <td style="padding: 12px;">{html.escape(item['title'])}</td>
            <td style="padding: 12px;">{html.escape(item['category'])}</td>
            <td style="padding: 12px; text-align: center;">{status_badge}</td>
            <td style="padding: 12px; font-family: monospace; font-size: 12px;">{html.escape(item['stdout'][:100])}</td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>CIS Benchmark Audit Report Red Hat Enterprise Linux 10 v1.4.0</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f3f4f6; margin: 0; padding: 20px; color: #1f2937; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }}
        .header {{ border-bottom: 2px solid #3b82f6; padding-bottom: 20px; margin-bottom: 20px; }}
        .score {{ font-size: 36px; font-weight: bold; color: #2563eb; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ background: #f9fafb; padding: 12px; text-align: left; border-bottom: 2px solid #e5e7eb; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ CIS Benchmark Audit Report Red Hat Enterprise Linux 10</h1>
            <p>Version Suite: <strong>v1.4.0</strong> | Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <div class="score">Score Global: {overall_score:.1f}%</div>
        </div>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Control Title</th>
                    <th>Category</th>
                    <th>Status</th>
                    <th>Execution Output</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
</body>
</html>"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"📄 RHEL 10 HTML report successfully generated: {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CIS Audit Benchmark (Local & SSH Remote Modes)")
    parser.add_argument("-m", "--mode", choices=["local", "ssh"], default="local", help="Audit execution mode (local or ssh)")
    parser.add_argument("-r", "--remote", "--ssh", dest="remote_host", default=None, help="Remote SSH server target (e.g. user@hostname)")
    parser.add_argument("--local", action="store_true", help="Force local audit execution mode")
    parser.add_argument("-f", "--format", choices=["html", "json", "xml", "txt"], default="html", help="Report output format")
    parser.add_argument("-l", "--lang", choices=["en", "fr"], default="en", help="Report language choice (en/fr)")
    parser.add_argument("-o", "--output", default=None, help="Custom output report file path")
    args = parser.parse_args()

    remote_target = None
    if args.mode == "ssh" or args.remote_host:
        remote_target = args.remote_host
        if not remote_target:
            print("❌ SSH mode requires a remote host target via --remote user@hostname or --ssh user@hostname", file=sys.stderr)
            sys.exit(1)
        print(f"🌐 Running Audit in SSH Remote Mode on host: '{remote_target}'...")
    else:
        print("🖥️  Running Audit in Local Mode on local machine...")

    check_results = perform_checks(RECOMMENDATIONS_DATA, remote_host=remote_target)
    (overall_score, categories_scores, *rest) = calculate_scores(check_results)
    export_results(check_results, overall_score, categories_scores, target_name="rhel_10", filename=args.output, fmt=args.format, lang=args.lang)