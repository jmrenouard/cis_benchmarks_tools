#!/usr/bin/env python3
"""
Standardize and normalize all command-line parameters across all 18 audit scripts
and audit_cis.py bundler (100% PSL ONLY).
"""

import glob
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NORMALIZED_PARSER_SNIPPET = """    parser = argparse.ArgumentParser(
        description="{script_description}",
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
    args = parser.parse_args()"""

def update_audit_scripts():
    audit_files = sorted(glob.glob(os.path.join(REPO_ROOT, "audit_cis_*.py")))
    print(f"Standardizing CLI argument parsers across {len(audit_files)} audit scripts...")

    for fpath in audit_files:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract current description or script title
        desc_match = re.search(r'parser\s*=\s*argparse\.ArgumentParser\(\s*description=(?:f?"|\'\'\'|""")(.*?)(?:"""|\'\'\'|"|\'),', content, re.DOTALL)
        script_desc = desc_match.group(1).strip() if desc_match else "CIS Benchmark Automated Audit Tool (PSL ONLY)"

        parser_code = NORMALIZED_PARSER_SNIPPET.format(script_description=script_desc)

        # Replace parser definition block
        pattern = r'    parser\s*=\s*argparse\.ArgumentParser\(.*?\n    args\s*=\s*parser\.parse_args\(\)'
        new_content = re.sub(pattern, parser_code, content, flags=re.DOTALL)

        if new_content != content:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  ✓ Standardized parser in {os.path.basename(fpath)}")
        else:
            print(f"  - No parser changes needed in {os.path.basename(fpath)}")

update_audit_scripts()
