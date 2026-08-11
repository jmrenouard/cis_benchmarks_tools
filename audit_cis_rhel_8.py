#!/usr/bin/env python3
"""
CIS Red Hat Enterprise Linux 8 Benchmark & STIG Audit Script (Python Standard Library ONLY).
Version: 1.4.0

Executes security compliance audit for RHEL 8 against CIS Benchmark v4.0.0 and STIG v2.0.0 recommendations.
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
        "description": "The cramfs filesystem type is a compressed read-only Linux filesystem type intended for small footprint systems.",
        "rationale": "Removing support for unneeded filesystem types reduces the local attack surface of the system.",
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
        "description": "The jffs2 (Journaling Flash File System v2) is used for flash devices.",
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
        "description": "SELinux must be set to enforcing mode to block unauthorized actions.",
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
        "title": "Ensure password hashing algorithm is SHA-512",
        "category": "Access Control",
        "subcategory": "PAM Configuration",
        "type": "Automated",
        "level": 1,
        "description": "Use SHA-512 for password hashing in PAM.",
        "rationale": "SHA-512 provides strong cryptographic protection for password hashes.",
        "audit": "authselect current 2>/dev/null | grep sha512",
        "remediation": "Configure authselect with sha512 option.",
        "condition": {"type": "stdout_contains", "value": "sha512"}
    }
]


def run_command(command, remote_host=None):
    """Execute command locally or via SSH remote execution without shell=True."""
    try:
        if remote_host:
            cmd_args = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", remote_host, command]
        else:
            cmd_args = ["/bin/bash", "-c", command]

        process = subprocess.run(cmd_args, check=False, capture_output=True, text=True, timeout=30)
        return process.stdout.strip(), process.stderr.strip(), process.returncode
    except FileNotFoundError:
        return "", f"Command '{command.split()[0]}' not found.", 127
    except Exception as e:
        return "", f"Execution error: {e}", 1


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


def generate_html_report(results, overall_score, categories_scores, filename="reports/rapport_cis_rhel_8.html"):
    """Generate responsive HTML audit report for RHEL 8."""
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
    <title>Rapport d'Audit CIS Red Hat Enterprise Linux 8 v1.4.0</title>
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
            <h1>🛡️ Rapport d'Audit CIS Red Hat Enterprise Linux 8 (STIG)</h1>
            <p>Version Suite: <strong>v1.4.0</strong> | Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <div class="score">Score Global: {overall_score:.1f}%</div>
        </div>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Titre du Contrôle</th>
                    <th>Catégorie</th>
                    <th>Statut</th>
                    <th>Extrait Sortie</th>
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
    print(f"📄 Rapport HTML RHEL 8 généré avec succès : {filename}")


def main():
    parser = argparse.ArgumentParser(description="CIS Red Hat Enterprise Linux 8 Audit Benchmark Suite (v1.4.0)")
    parser.add_argument("-r", "--remote", help="SSH remote target (e.g. user@hostname)")
    parser.add_argument("-o", "--output", default="reports/rapport_cis_rhel_8.html", help="Path to output HTML report")
    args = parser.parse_args()

    print(f"🚀 Running CIS Audit for Red Hat Enterprise Linux 8 (20 controls)...")
    results = []
    passed = 0

    for rec in RECOMMENDATIONS_DATA:
        stdout, stderr, code = run_command(rec["audit"], remote_host=args.remote)
        is_pass = evaluate_condition(rec["condition"], stdout, stderr, code)
        status = "PASS" if is_pass else "FAIL"
        if is_pass:
            passed += 1

        results.append({
            "id": rec["id"],
            "title": rec["title"],
            "category": rec["category"],
            "status": status,
            "stdout": stdout,
            "stderr": stderr,
            "code": code
        })

    overall_score = (passed / len(RECOMMENDATIONS_DATA)) * 100
    print(f"✅ RHEL 8 Audit Completed: {passed}/{len(RECOMMENDATIONS_DATA)} Passed ({overall_score:.1f}%)")

    generate_html_report(results, overall_score, {}, filename=args.output)


if __name__ == "__main__":
    main()
