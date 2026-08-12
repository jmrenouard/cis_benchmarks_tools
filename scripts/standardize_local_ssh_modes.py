#!/usr/bin/env python3
"""
Standardize Local Mode & SSH Remote Mode CLI arguments and execution logic across all 18 audit scripts.
Adds SSH options (--mode, --remote/--ssh, --ssh-port, --ssh-key, --sudo)
and Database Connection parameters (--db-host, --db-port, --db-user, --db-password).
100% Python Standard Library (PSL ONLY).
"""

import glob
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def standardize_script(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    filename = os.path.basename(file_path)

    standard_args_block = '''    parser.add_argument("-m", "--mode", choices=["local", "ssh"], default="local", help="Audit execution mode (local or ssh)")
    parser.add_argument("-r", "--remote", "--ssh", dest="remote_host", default=None, help="Remote SSH server target (e.g. user@hostname)")
    parser.add_argument("--ssh-port", type=int, default=22, help="SSH port for remote execution (default: 22)")
    parser.add_argument("--ssh-key", default=None, help="Path to SSH private key file")
    parser.add_argument("--sudo", action="store_true", help="Execute remote/local commands with sudo privileges")
    parser.add_argument("--db-host", "--host", dest="db_host", default="localhost", help="Database host address (default: localhost)")
    parser.add_argument("--db-port", "--port", dest="db_port", type=int, default=None, help="Database port number")
    parser.add_argument("--db-user", "--user", dest="db_user", default=None, help="Database username")
    parser.add_argument("--db-password", "--password", dest="db_password", default=None, help="Database password")
    parser.add_argument("--local", action="store_true", help="Force local audit execution mode")
    parser.add_argument("-f", "--format", choices=["html", "json", "xml", "txt"], default="html", help="Report output format")
    parser.add_argument("-l", "--lang", choices=["en", "fr"], default="en", help="Report language choice (en/fr)")
    parser.add_argument("-o", "--output", default=None, help="Custom output report file path")'''

    pattern = r'    parser\.add_argument\("-m", "--mode".*?args = parser\.parse_args\(\)'
    if re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, standard_args_block + "\n    args = parser.parse_args()", content, flags=re.DOTALL)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ Standardized Local & SSH CLI arguments in {filename}")


def main():
    audit_files = sorted(glob.glob(os.path.join(REPO_ROOT, "audit_cis_*.py")))
    print(f"Standardizing Local & SSH execution parameters across {len(audit_files)} audit scripts...")
    for f in audit_files:
        standardize_script(f)


if __name__ == "__main__":
    main()
