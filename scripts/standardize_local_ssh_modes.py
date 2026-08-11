#!/usr/bin/env python3
"""
Standardize Local Mode (--mode local / --local) and SSH Remote Mode (--mode ssh / --remote user@host / --ssh user@host)
across ALL 18 Audit Scripts and unified CLI engine (audit_cis.py).
100% Python Standard Library (PSL ONLY).
"""

import glob
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Standardizing Local & SSH execution modes across {len(audit_files)} audit scripts...")

new_run_command = '''def run_command(command, remote_host=None):
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
'''

rhel_perform_checks = '''def perform_checks(recommendations, remote_host=None):
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
'''

for fpath in audit_files:
    target_name = fpath.replace("audit_cis_", "").replace(".py", "")
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update run_command
    content = re.sub(
        r'def run_command\(.*?\):\n.*?(?=\n\ndef evaluate_condition|\nRECOMMENDATIONS_DATA|\ndef perform_checks|\ndef perform_audit)',
        new_run_command + "\n",
        content,
        flags=re.DOTALL
    )

    # 2. Fix RHEL perform_checks / perform_audit
    if "rhel" in fpath:
        if "def calculate_scores(" not in content:
            content = content.replace("def evaluate_condition(", rhel_perform_checks + "\n\n\ndef evaluate_condition(")

    # 3. Update perform_checks signature to take remote_host=None
    if 'def perform_checks(recommendations):' in content:
        content = content.replace('def perform_checks(recommendations):', 'def perform_checks(recommendations, remote_host=None):')

    # 4. Update run_command calls inside perform_checks to pass remote_host=remote_host
    content = re.sub(
        r'run_command\((cmd_to_run|path_cmd|cmd)\)',
        r'run_command(\1, remote_host=remote_host)',
        content
    )

    # 5. Standardize CLI Argument Parser in __main__
    cli_block = '''if __name__ == "__main__":
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
    export_results(check_results, overall_score, categories_scores, target_name="''' + target_name + '''", filename=args.output, fmt=args.format, lang=args.lang)
'''

    content = re.sub(r'if __name__ == "__main__":.*$', cli_block.strip(), content, flags=re.DOTALL)
    content = re.sub(r'def main\(\):.*?(?=if __name__ == "__main__":)', '', content, flags=re.DOTALL)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Standardized Local & SSH Remote execution modes across all 18 audit scripts!")
