#!/usr/bin/env python3
"""
CIS Red Hat Enterprise Linux 9 Benchmark & STIG Audit Script (Python Standard Library ONLY).
Version: 1.4.0

Executes security compliance audit for RHEL 9 against CIS Benchmark v2.0.0 and STIG v1.0.0 recommendations.
Supports both local execution and SSH remote execution (--remote user@host).

Zero external dependencies: uses only Python Standard Library (argparse, json, subprocess, os, sys, re, html, datetime).
"""

import argparse
from datetime import datetime
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



def build_inline_svg_donut_chart(passed, failed, errors, na, score):
    """Generate 100% self-contained Inline SVG Donut Chart (PSL ONLY, Zero JS)."""
    total = passed + failed + errors + na
    p_pass = (passed / total * 100) if total > 0 else 0
    p_fail = (failed / total * 100) if total > 0 else 0
    p_err = (errors / total * 100) if total > 0 else 0
    p_na = (na / total * 100) if total > 0 else 0

    offset_pass = 25
    offset_fail = 25 - p_pass
    offset_err = offset_fail - p_fail
    offset_na = offset_err - p_err

    return f"""
    <div style="display: flex; align-items: center; justify-content: center; gap: 40px; margin: 20px 0; flex-wrap: wrap;">
      <div style="position: relative; width: 170px; height: 170px;">
        <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg);">
          <path stroke-dasharray="100 100" stroke="#e5e7eb" stroke-width="3.8" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          <path stroke-dasharray="{p_na:.1f} 100" stroke-dashoffset="{offset_na:.1f}" stroke="#9ca3af" stroke-width="3.8" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          <path stroke-dasharray="{p_err:.1f} 100" stroke-dashoffset="{offset_err:.1f}" stroke="#6b7280" stroke-width="3.8" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          <path stroke-dasharray="{p_fail:.1f} 100" stroke-dashoffset="{offset_fail:.1f}" stroke="#ef4444" stroke-width="3.8" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          <path stroke-dasharray="{p_pass:.1f} 100" stroke-dashoffset="{offset_pass:.1f}" stroke="#10b981" stroke-width="3.8" stroke-linecap="round" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
        </svg>
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
          <span style="font-size: 24px; font-weight: 800; color: #111827;">{score:.1f}%</span>
          <span style="font-size: 11px; color: #6b7280; font-weight: 600;">Score Global</span>
        </div>
      </div>
      <div style="display: flex; flex-direction: column; gap: 8px; font-size: 13px;">
        <div style="display: flex; align-items: center; gap: 8px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #10b981; display: inline-block;"></span> <strong>Réussi (PASS) :</strong> {passed}</div>
        <div style="display: flex; align-items: center; gap: 8px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #ef4444; display: inline-block;"></span> <strong>Échoué (FAIL) :</strong> {failed}</div>
        <div style="display: flex; align-items: center; gap: 8px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #6b7280; display: inline-block;"></span> <strong>Erreur (Error) :</strong> {errors}</div>
        <div style="display: flex; align-items: center; gap: 8px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #9ca3af; display: inline-block;"></span> <strong>Non Applicable (N/A) :</strong> {na}</div>
      </div>
    </div>
    """


def build_inline_svg_category_chart(categories_scores):
    """Generate 100% self-contained Inline SVG/HTML5 Horizontal Stacked Bar Charts per category (PSL ONLY, Zero JS)."""
    if not categories_scores or not isinstance(categories_scores, dict):
        return ""
    items_html = []
    for label, cat in categories_scores.items():
        p = cat.get("passed_automated", cat.get("passed", 0))
        f = cat.get("failed_automated", cat.get("failed", 0))
        e = cat.get("error_checks", cat.get("errors", 0))
        n = cat.get("na_checks", cat.get("na", 0))
        cat_total = p + f + e + n
        cat_score = cat.get("score", (p / cat_total * 100) if cat_total > 0 else 0)

        p_pass = (p / cat_total * 100) if cat_total > 0 else 0
        p_fail = (f / cat_total * 100) if cat_total > 0 else 0
        p_err = (e / cat_total * 100) if cat_total > 0 else 0
        p_na = (n / cat_total * 100) if cat_total > 0 else 0

        badge_color = "#10b981" if cat_score >= 80 else ("#f59e0b" if cat_score >= 50 else "#ef4444")

        bar_segments = []
        if p > 0: bar_segments.append(f'<div style="width: {p_pass:.1f}%; background: #10b981;" title="Réussi: {p}"></div>')
        if f > 0: bar_segments.append(f'<div style="width: {p_fail:.1f}%; background: #ef4444;" title="Échoué: {f}"></div>')
        if e > 0: bar_segments.append(f'<div style="width: {p_err:.1f}%; background: #6b7280;" title="Error: {e}"></div>')
        if n > 0: bar_segments.append(f'<div style="width: {p_na:.1f}%; background: #9ca3af;" title="N/A: {n}"></div>')
        if not bar_segments:
            bar_segments.append('<div style="width: 100%; background: #e5e7eb;" title="Aucun contrôle"></div>')

        items_html.append(f"""
        <div style="margin-bottom: 16px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-weight: 600; font-size: 14px; color: #374151;">{label}</span>
            <span style="font-weight: 700; font-size: 13px; color: {badge_color};">{cat_score:.1f}% ({p}/{cat_total})</span>
          </div>
          <div style="display: flex; height: 16px; width: 100%; border-radius: 8px; overflow: hidden; background: #f3f4f6; border: 1px solid #e5e7eb;">
            {''.join(bar_segments)}
          </div>
        </div>
        """)

    legend_html = """
    <div style="display: flex; gap: 20px; justify-content: center; margin-bottom: 20px; font-size: 13px;">
      <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #10b981; display: inline-block;"></span> Réussi</div>
      <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #ef4444; display: inline-block;"></span> Échoué</div>
      <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #6b7280; display: inline-block;"></span> Erreur</div>
      <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #9ca3af; display: inline-block;"></span> N/A</div>
    </div>
    """

    return f"""
    <div style="background: #ffffff; padding: 24px; border-radius: 12px; border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-top: 24px;">
      <h3 style="font-size: 18px; font-weight: 700; color: #111827; margin-bottom: 16px; text-align: center;">Répartition des contrôles automatisés par catégorie</h3>
      {legend_html}
      {''.join(items_html)}
    </div>
    """


def load_recommendations(target_key):
    """Load audit control specifications from rules/<target_key>.json with inline fallback (PSL ONLY)."""
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rules", f"{target_key}.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Warning: Could not load rule spec '{json_path}': {e}", file=sys.stderr)
    return RECOMMENDATIONS_DATA




def load_html_template():
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "report_template.html")
    if os.path.exists(template_path):
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return """<!DOCTYPE html>
<html lang="{lang}" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CIS Benchmark Audit Report - {benchmark_title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body { font-family: 'Inter', sans-serif; transition: background-color 0.3s, color 0.3s; }
        .status-pass { background-color: #DEF7EC; color: #03543F; }
        .status-fail { background-color: #FDE8E8; color: #9B1C1C; }
        .status-manual { background-color: #FEF3C7; color: #92400E; }
        .status-error { background-color: #F3F4F6; color: #1F2937; }
        .status-na { background-color: #E5E7EB; color: #4B5563; }
        pre { white-space: pre-wrap; word-wrap: break-word; font-size: 0.75rem; }
        body.dark-mode { background-color: #0f172a; color: #f8fafc; }
        body.dark-mode aside, body.dark-mode header, body.dark-mode footer, body.dark-mode .bg-white { background-color: #1e293b !important; color: #f8fafc !important; border-color: #334155 !important; }
        body.dark-mode .text-gray-900, body.dark-mode .text-gray-800 { color: #f8fafc !important; }
        body.dark-mode .text-gray-700, body.dark-mode .text-gray-600 { color: #cbd5e1 !important; }
        body.dark-mode .text-gray-500, body.dark-mode .text-gray-400 { color: #94a3b8 !important; }
        body.dark-mode .bg-gray-50, body.dark-mode .bg-gray-100 { background-color: #0f172a !important; }
    </style>
</head>
<body class="bg-gray-50 flex">
    <aside class="w-64 h-screen bg-white border-r border-gray-200 sticky top-0 overflow-y-auto hidden lg:block">
        <div class="p-6">
            <h2 class="text-xl font-bold text-blue-600 flex items-center gap-2"><i class="fas fa-shield-halved"></i>{benchmark_title}</h2>
            <p class="text-xs text-gray-500 mt-1">Audit Security Report v2.1.0</p>
        </div>
        <nav class="px-4 pb-6">
            <a href="#summary" class="flex items-center p-3 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors mb-1 font-medium">
                <i class="fas fa-chart-pie w-5 mr-3 text-blue-500"></i> Synthèse & Métriques
            </a>
            <div class="mt-4 mb-2 text-xs font-semibold text-gray-400 uppercase px-3">Catégories</div>
            {sidebar_links}
        </nav>
    </aside>
    <main class="flex-1 min-w-0">
        <header class="bg-white border-b border-gray-200 p-6 flex justify-between items-center">
            <div>
                <h1 class="text-2xl font-bold text-gray-900">Benchmark CIS {benchmark_title}</h1>
                <p class="text-sm text-gray-500">Date du rapport: {report_date}</p>
            </div>
            <div class="flex items-center space-x-3">
                <button id="themeToggle" onclick="toggleDarkMode()" class="px-3 py-1.5 bg-gray-100 border border-gray-300 text-gray-700 rounded-lg text-xs font-semibold hover:bg-gray-200 transition-colors flex items-center gap-1.5">
                    <i class="fas fa-moon"></i> Mode Sombre
                </button>
                <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">{target_version}</span>
            </div>
        </header>
        <div class="p-8 max-w-7xl mx-auto">
            <section id="summary" class="mb-12">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col items-center">
                        <span class="text-sm font-medium text-gray-500 uppercase tracking-wider mb-2">Score Global</span>
                        <div class="relative flex items-center justify-center">
                            <span class="text-3xl font-black text-gray-900">{overall_score:.1f}%</span>
                        </div>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 border-l-4 border-l-green-500">
                        <span class="text-xs font-bold text-green-600 uppercase tracking-widest">Succès</span>
                        <div class="text-3xl font-bold text-gray-900 mt-1">{passed_automated_count}</div>
                        <p class="text-xs text-gray-500 mt-1">Vérifications conformes</p>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 border-l-4 border-l-red-500">
                        <span class="text-xs font-bold text-red-600 uppercase tracking-widest">Échecs</span>
                        <div class="text-3xl font-bold text-gray-900 mt-1">{failed_automated_count}</div>
                        <p class="text-xs text-gray-500 mt-1">Non-conformités détectées</p>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 border-l-4 border-l-amber-500">
                        <span class="text-xs font-bold text-amber-600 uppercase tracking-widest">Manuels</span>
                        <div class="text-3xl font-bold text-gray-900 mt-1">{manual_checks}</div>
                        <p class="text-xs text-gray-500 mt-1">À vérifier manuellement</p>
                    </div>
                </div>
                {donut_svg}
                {bar_svg}
            </section>
            <section id="details">
                <div class="flex items-center justify-between mb-6">
                    <h2 class="text-xl font-bold text-gray-900">Détails des Contrôles d'Audit</h2>
                    <div class="flex gap-2">
                        <button onclick="filterStatus('all')" class="px-3 py-1.5 bg-blue-600 text-white rounded-lg text-xs font-semibold hover:bg-blue-700 transition-colors">Tous</button>
                        <button onclick="filterStatus('PASS')" class="px-3 py-1.5 bg-green-100 text-green-800 rounded-lg text-xs font-semibold hover:bg-green-200 transition-colors">Succès</button>
                        <button onclick="filterStatus('FAIL')" class="px-3 py-1.5 bg-red-100 text-red-800 rounded-lg text-xs font-semibold hover:bg-red-200 transition-colors">Échecs</button>
                        <button onclick="filterStatus('MANUAL')" class="px-3 py-1.5 bg-amber-100 text-amber-800 rounded-lg text-xs font-semibold hover:bg-amber-200 transition-colors">Manuels</button>
                        <button onclick="filterStatus('ERROR')" class="px-3 py-1.5 bg-gray-100 text-gray-800 rounded-lg text-xs font-semibold hover:bg-gray-200 transition-colors">Erreurs</button>
                    </div>
                </div>
                {categories_reports}
            </section>
        </div>
    </main>
    <script>
        function toggleDarkMode() { document.body.classList.toggle('dark-mode'); }
        function filterStatus(status) {
            document.querySelectorAll('tr[data-status]').forEach(row => {
                if (status === 'all' || row.getAttribute('data-status') === status) { row.style.display = ''; }
                else { row.style.display = 'none'; }
            });
        }
    </script>
</body>
</html>"""



def is_valid_executable_command(cmd_str):
    """Check if command string is a valid shell executable command rather than descriptive human text."""
    if not cmd_str or not isinstance(cmd_str, str):
        return False
    s = cmd_str.strip()
    if not s:
        return False
    if s.startswith("!") or s.startswith("[") or s.startswith("(") or s.startswith("/") or s.startswith("."):
        return True
    first_word = s.split()[0].lower()
    known_commands = {
        "cat", "ls", "grep", "egrep", "fgrep", "find", "ps", "awk", "cut", "sed", "head", "tail",
        "echo", "getent", "crontab", "df", "stat", "test", "dpkg", "rpm", "systemctl", "service",
        "mysql", "mariadb", "psql", "cqlsh", "mongo", "mongosh", "python3", "python", "bash", "sh",
        "docker", "curl", "wget", "sshd", "which", "id", "whoami", "uname", "chmod", "chown"
    }
    if first_word in known_commands:
        return True
    if any(token in s for token in ["|", "&&", ";", ">", "||", "$"]):
        return True
    return False


def run_command(command, remote_host=None):
    """Execute command safely with timeout=10, stdin=DEVNULL, and clean SSH noise (PSL ONLY)."""
    try:
        if isinstance(command, str):
            if "systemctl" in command and (os.path.exists("/.dockerenv") or not os.path.exists("/run/systemd/system")):
                if "postgresql" in command:
                    command = "pg_isready -h localhost -p 5432 || ps aux | grep -v grep | grep postgres"
                elif "mariadb" in command or "mysql" in command:
                    command = "mariadb -e 'SELECT 1;' 2>/dev/null || mysql -e 'SELECT 1;' 2>/dev/null || ps aux | grep -v grep | grep mysqld"
            cmd_args = ["/bin/bash", "-c", command]
        else:
            cmd_args = list(command)

        if remote_host:
            cmd_args = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", "-i", "/root/.ssh/id_rsa", remote_host] + cmd_args

        process = subprocess.run(cmd_args, check=False, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10, env=env)
        stdout_text = process.stdout.strip()
        stderr_text = process.stderr.strip()

        if stderr_text:
            filtered_lines = [
                line for line in stderr_text.splitlines()
                if not line.startswith("Warning: Permanently added")
                and "pseudo-terminal" not in line
            ]
            stderr_text = chr(10).join(filtered_lines).strip()

        return stdout_text, stderr_text, process.returncode
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
            "test_procedure": rec.get("audit", rec.get("test_procedure", "")),
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
    if stdout is None:
        stdout = ""
    if stderr is None:
        stderr = ""

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
            test_proc = r.get("test_procedure", r.get("audit", ""))
            if test_proc:
                cmd_elem = ET.SubElement(tc, "system-out")
                cmd_elem.text = f"Test Command: {str(test_proc).strip()}"
            rem = r.get("remediation", "")
            if rem:
                rem_elem = ET.SubElement(tc, "remediation")
                rem_elem.text = str(rem).strip()
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
            "=" * 90,
            f"               CIS BENCHMARK AUDIT REPORT - {target_name.upper()}",
            "=" * 90,
            f"Report Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Global Score  : {overall_score:.1f}%",
            f"Total Controls: {len(flat_results)}",
            "-" * 90,
            " CATEGORY BREAKDOWN & COMPLIANCE SUMMARY TABLE",
            "-" * 90,
            f"  {'ID':<6} {'Category Name':<45} {'Pass':<6} {'Fail':<6} {'Manual':<8} {'Score':<8}",
            f"  {'-'*6} {'-'*45} {'-'*6} {'-'*6} {'-'*8} {'-'*8}",
        ]
        if isinstance(categories_scores, dict):
            for cat_id, data in categories_scores.items():
                name = str(data.get('name', cat_id))[:44]
                p = data.get('passed_automated', 0)
                f = data.get('failed_automated', 0)
                m = data.get('manual_checks', 0)
                sc = data.get('score', 0.0)
                lines.append(f"  {str(cat_id):<6} {name:<45} {p:<6} {f:<6} {m:<8} {sc:>6.1f}%")
        lines.extend([
            "=" * 90,
            " DETAILED CONTROL RESULTS",
            "=" * 90,
            ""
        ])
        for r in flat_results:
            status = r.get("status", "")
            status_icon = "[PASS]" if status in ["PASS", "Pass"] else ("[FAIL]" if status in ["FAIL", "Fail"] else "[MANUAL]")
            rec_id = r.get("number", r.get("id", ""))
            rec_name = r.get("name", r.get("title", ""))
            lines.append(f"{status_icon} {rec_id} - {rec_name}")
            lines.append(f"  Category: {r.get('category')}")
            test_proc = r.get("test_procedure", r.get("audit", ""))
            if test_proc:
                lines.append(f"  Commande de test: {str(test_proc).strip()}")
            out = r.get('output', r.get('stdout', ''))
            if out:
                lines.append(f"  Output: {str(out).strip()}")
            rem = r.get('remediation', '')
            if rem:
                lines.append(f"  Procédure de remédiation: {str(rem).strip()}")
            lines.append("-" * 90)
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






def generate_html_report(results, overall_score, categories_scores, filename=None, lang="en", execution_context=None):
    """Generate modern unified responsive HTML audit report for RHEL."""
    target_name = "RHEL"
    if filename:
        if "rhel_8" in filename: target_name = "RHEL 8"
        elif "rhel_9" in filename: target_name = "RHEL 9"
        elif "rhel_10" in filename: target_name = "RHEL 10"

    if not filename:
        filename = "reports/rapport_cis_rhel.html"

    if os.path.dirname(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    report_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    flat_results = []
    if isinstance(results, dict):
        for cat, checks in results.items():
            for c in checks: flat_results.append(c)
    else:
        flat_results = list(results)

    passed_count = sum(1 for c in flat_results if c.get("status") in ["PASS", "Pass"])
    failed_count = sum(1 for c in flat_results if c.get("status") in ["FAIL", "Fail"])
    manual_count = sum(1 for c in flat_results if c.get("status") in ["MANUAL", "Manual"])
    error_count = sum(1 for c in flat_results if c.get("status") in ["ERROR", "Error"])
    na_count = sum(1 for c in flat_results if c.get("status") in ["N/A", "NA"])

    donut_svg = build_inline_svg_donut_chart(passed_count, failed_count, error_count, na_count, overall_score)

    # Categories Breakdown & Sidebar Links
    cat_names = []
    cat_pass = []
    cat_fail = []
    cat_err = []
    cat_na = []

    sidebar_links_html = ""
    categories_reports_html = ""

    # Group by category if flat list
    cat_groups = {}
    for item in flat_results:
        c_name = item.get("category", "General")
        cat_groups.setdefault(c_name, []).append(item)

    for cat_idx, (cat_name, items) in enumerate(cat_groups.items(), 1):
        cat_anchor = f"category-{cat_idx}"
        sidebar_links_html += f"""
        <a href="#{cat_anchor}" class="flex items-center px-3 py-2 text-xs text-gray-600 hover:bg-gray-100 rounded-lg transition-colors truncate">
            <span class="truncate">{html.escape(cat_name)}</span>
        </a>"""

        p_c = sum(1 for c in items if c.get("status") in ["PASS", "Pass"])
        f_c = sum(1 for c in items if c.get("status") in ["FAIL", "Fail"])
        e_c = sum(1 for c in items if c.get("status") in ["ERROR", "Error"])
        n_c = sum(1 for c in items if c.get("status") in ["N/A", "NA"])

        cat_names.append(cat_name)
        cat_pass.append(p_c)
        cat_fail.append(f_c)
        cat_err.append(e_c)
        cat_na.append(n_c)

        rows_html = ""
        for item in items:
            st = item.get("status", "FAIL").upper()
            st_class = "status-pass" if st == "PASS" else ("status-fail" if st == "FAIL" else ("status-manual" if st == "MANUAL" else "status-error"))
            st_badge = f'<span class="px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wider {st_class}">{st}</span>'

            ctrl_id = html.escape(str(item.get("id", item.get("number", ""))))
            ctrl_title = html.escape(str(item.get("title", item.get("name", ""))))
            test_proc = html.escape(str(item.get("test_procedure", item.get("audit", ""))))
            out_txt = html.escape(str(item.get("output", item.get("stdout", ""))))
            rem_txt = html.escape(str(item.get("remediation", "")))

            rows_html += f"""
            <tr data-status="{st}" class="hover:bg-gray-50 transition-colors border-b border-gray-100">
                <td class="py-4 px-4 text-sm font-bold text-gray-500 align-top">{ctrl_id}</td>
                <td class="py-4 px-4 align-top">
                    <div class="text-sm font-bold text-gray-900 mb-1">{ctrl_title}</div>
                    {f'<div class="text-xs text-gray-500 font-mono bg-gray-100 p-1.5 rounded mt-1 truncate max-w-md"><code>{test_proc}</code></div>' if test_proc else ''}
                </td>
                <td class="py-4 px-4 align-top text-center">{st_badge}</td>
                <td class="py-4 px-4 text-sm align-top">
                    <div class="mb-3">
                        <div class="text-[10px] font-bold text-gray-400 uppercase mb-1">Résultat de l'audit / Output:</div>
                        <div class="bg-gray-900 text-gray-100 p-3 rounded-lg border border-gray-700">
                            <pre class="overflow-x-auto">{out_txt}</pre>
                        </div>
                    </div>
                    {f'<div class="p-3 bg-blue-50 border-l-4 border-blue-400 rounded-r-lg"><div class="text-[10px] font-bold text-blue-600 uppercase mb-1"><i class="fas fa-wrench mr-1"></i> Procédure de remédiation:</div><div class="text-xs text-blue-800 leading-relaxed font-medium">{rem_txt}</div></div>' if rem_txt else ''}
                </td>
            </tr>"""

        categories_reports_html += f"""
        <div id="{cat_anchor}" class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8 overflow-hidden">
            <div class="bg-gray-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
                <h3 class="font-bold text-gray-800 text-lg flex items-center gap-2"><i class="fas fa-folder text-blue-500"></i> {html.escape(cat_name)}</h3>
                <span class="text-xs font-semibold text-gray-500">{len(items)} contrôles</span>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-gray-50/50 text-xs font-bold text-gray-500 uppercase border-b border-gray-200">
                            <th class="py-3 px-4 w-16">#</th>
                            <th class="py-3 px-4">Contrôle / Nom & Commande</th>
                            <th class="py-3 px-4 text-center w-28">Statut</th>
                            <th class="py-3 px-4">Détails (Résultat & Remédiation)</th>
                        </tr>
                    </thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>
        </div>"""

    bar_svg = build_inline_svg_category_chart(cat_names, cat_pass, cat_fail, cat_err, cat_na)

    html_template = load_html_template()
    html_content = html_template.format(
        benchmark_title=target_name,
        lang=lang,
        report_date=report_date,
        suite_version="2.1.0",
        target_version="1.4.0",
        overall_score=overall_score,
        passed_automated_count=passed_count,
        failed_automated_count=failed_count,
        manual_checks=manual_count,
        sidebar_links=sidebar_links_html,
        donut_svg=donut_svg,
        bar_svg=bar_svg,
        categories_reports=categories_reports_html
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"📄 Unified HTML Report successfully generated: {filename}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CIS Audit Benchmark (Local & SSH Remote Modes)",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-c", "--docker", "--container", dest="docker_container", default=None, help="Target Docker container name or ID")
    parser.add_argument("-m", "--mode", choices=["local", "ssh"], default="local", help="Audit execution mode (local or ssh)")
    parser.add_argument("-r", "--remote", "--ssh", dest="remote_host", default=None, help="Remote SSH server target (e.g. user@hostname)")
    parser.add_argument("--ssh-port", type=int, default=22, help="SSH port for remote execution (default: 22)")
    parser.add_argument("-i", "--ssh-key", dest="ssh_key", default=None, help="Path to SSH private key file")
    parser.add_argument("--sudo", action="store_true", help="Execute remote/local commands with sudo privileges")
    parser.add_argument("-H", "--host", "--db-host", dest="db_host", default="localhost", help="Database host address (default: localhost)")
    parser.add_argument("-P", "--port", "--db-port", dest="db_port", type=int, default=None, help="Database port number")
    parser.add_argument("-u", "--user", "--db-user", dest="db_user", default=None, help="Database username")
    parser.add_argument("-p", "--password", "--db-password", dest="db_password", default=None, help="Database password")
    parser.add_argument("-D", "-d", "--database", "--db-name", dest="db_name", default=None, help="Database name")
    parser.add_argument("--defaults-file", "--config-file", dest="defaults_file", default=None, help="Path to database option/configuration file (.my.cnf, .pgpass, cqlshrc)")
    parser.add_argument("--auth-db", dest="auth_db", default=None, help="Authentication database (MongoDB)")
    parser.add_argument("--local", action="store_true", help="Force local audit execution mode")
    parser.add_argument("-f", "--format", choices=["html", "json", "xml", "txt"], default="html", help="Report output format (html/json/xml/txt)")
    parser.add_argument("-l", "--lang", choices=["en", "fr"], default="en", help="Report language choice (en/fr)")
    parser.add_argument("-o", "--output", dest="output", default=None, help="Custom output report file path")
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

    rules_data = load_recommendations("rhel_9")
    check_results = perform_checks(rules_data, remote_host=remote_target)
    (overall_score, categories_scores, *rest) = calculate_scores(check_results)
    export_results(check_results, overall_score, categories_scores, target_name="rhel_9", filename=args.output, fmt=args.format, lang=args.lang)