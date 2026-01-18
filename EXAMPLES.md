# CIS Benchmarks Tool - Examples

This document provides practical examples of using the CIS Benchmarks automation tool.

## Quick Start

### 1. Run a Quick Audit with Default Checks

```bash
./audit.sh quick
```

This will:
- Run 5 default security checks
- Generate an HTML report with timestamp
- Display results in the terminal

### 2. Run Comprehensive Audit

```bash
./audit.sh full
```

This runs all 11 checks from `config/default_checks.yaml` including:
- Password policies
- File permissions
- Network configuration
- SSH settings
- System maintenance

## Using the Python Script Directly

### Basic Usage

```bash
# Run with default checks, JSON output
python3 cis_audit.py --use-defaults

# Run with custom config, HTML output
python3 cis_audit.py -c config/default_checks.yaml -f html -o my_audit
```

### Advanced Usage

```bash
# Generate multiple report formats
python3 cis_audit.py -c config/default_checks.yaml -f json -o security_audit
python3 cis_audit.py -c config/default_checks.yaml -f html -o security_audit
python3 cis_audit.py -c config/default_checks.yaml -f text -o security_audit

# This creates:
# - security_audit.json
# - security_audit.html
# - security_audit.text
```

## Creating Custom Checks

### Example 1: Check for Specific User

Create `my_checks.yaml`:

```yaml
checks:
  - id: "custom.1"
    type: command
    title: "Ensure specific user exists"
    description: "Check if audit user exists"
    command: "id audit-user"
    should_exist: true
    severity: medium
    remediation: "Create user: useradd audit-user"
```

Run it:
```bash
python3 cis_audit.py -c my_checks.yaml -f html -o custom_audit
```

### Example 2: Multiple File Permission Checks

Create `file_security.yaml`:

```yaml
checks:
  - id: "file.1"
    type: file
    title: "Check /etc/passwd permissions"
    description: "User database should be readable by all"
    filepath: "/etc/passwd"
    expected_perms: "644"
    severity: high
    remediation: "chmod 644 /etc/passwd"

  - id: "file.2"
    type: file
    title: "Check /etc/shadow permissions"
    description: "Password hashes should be protected"
    filepath: "/etc/shadow"
    expected_perms: "000"
    severity: high
    remediation: "chmod 000 /etc/shadow"

  - id: "file.3"
    type: file
    title: "Check /etc/gshadow permissions"
    description: "Group password hashes should be protected"
    filepath: "/etc/gshadow"
    expected_perms: "000"
    severity: high
    remediation: "chmod 000 /etc/gshadow"
```

Run it:
```bash
python3 cis_audit.py -c file_security.yaml -f text
```

### Example 3: Network Security Checks

Create `network_security.yaml`:

```yaml
checks:
  - id: "net.1"
    type: command
    title: "Ensure IPv6 is disabled"
    description: "IPv6 should be disabled if not needed"
    command: "sysctl net.ipv6.conf.all.disable_ipv6"
    expected_output: "net.ipv6.conf.all.disable_ipv6 = 1"
    severity: low
    remediation: "Add 'net.ipv6.conf.all.disable_ipv6=1' to /etc/sysctl.conf"

  - id: "net.2"
    type: command
    title: "Check firewall status"
    description: "Firewall should be active"
    command: "systemctl is-active ufw"
    expected_output: "active"
    severity: high
    remediation: "systemctl enable ufw && systemctl start ufw"

  - id: "net.3"
    type: command
    title: "Ensure IP forwarding is disabled"
    description: "IP forwarding should be off on non-router systems"
    command: "sysctl net.ipv4.ip_forward"
    expected_output: "net.ipv4.ip_forward = 0"
    severity: medium
    remediation: "echo 'net.ipv4.ip_forward=0' >> /etc/sysctl.conf && sysctl -p"
```

Run it:
```bash
python3 cis_audit.py -c network_security.yaml -f html -o network_audit
```

## Automation and Scheduling

### Schedule Daily Audits with Cron

Add to crontab:

```bash
# Run CIS audit daily at 2 AM
0 2 * * * /path/to/cis_benchmarks_tools/audit.sh full
```

### Create Weekly Reports

```bash
#!/bin/bash
# weekly_audit.sh

DATE=$(date +%Y%m%d)
REPORT_DIR="/var/log/security_audits"

mkdir -p "$REPORT_DIR"

cd /path/to/cis_benchmarks_tools

# Run full audit
./audit.sh full

# Move report to archive
mv cis_full_audit_*.html "$REPORT_DIR/cis_audit_${DATE}.html"

# Email report (requires mailutils)
echo "CIS Audit report for $DATE" | mail -s "Security Audit Report" -A "$REPORT_DIR/cis_audit_${DATE}.html" admin@example.com
```

### Integration with CI/CD

```yaml
# .github/workflows/security-audit.yml
name: CIS Security Audit

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
  workflow_dispatch:

jobs:
  security-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run CIS audit
        run: python3 cis_audit.py --use-defaults -f json -o audit_results
      
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: security-audit-report
          path: audit_results.json
```

## Understanding Results

### Reading JSON Reports

```bash
# View summary
cat audit_results.json | jq '.total_checks, .passed, .failed, .errors'

# List all failed checks
cat audit_results.json | jq '.checks[] | select(.status == "fail") | {check_id, title, message, remediation}'

# List high severity failures
cat audit_results.json | jq '.checks[] | select(.severity == "high" and .status == "fail")'
```

### Analyzing HTML Reports

HTML reports provide:
- Color-coded status indicators (green=pass, red=fail, yellow=error)
- Severity badges (high, medium, low)
- Expandable remediation instructions
- Summary statistics at the top

### Processing Text Reports

Text reports are ideal for:
- Email notifications
- Log aggregation
- Simple text-based analysis
- Command-line viewing

## Best Practices

1. **Start with minimal checks** to understand the tool
2. **Customize checks** for your specific environment
3. **Schedule regular audits** for continuous monitoring
4. **Review failures** and apply remediations systematically
5. **Archive reports** for compliance and trend analysis
6. **Integrate with monitoring** systems for alerts

## Troubleshooting

### Permission Denied Errors

Run with sudo for system-level checks:
```bash
sudo python3 cis_audit.py --use-defaults
```

### Custom Checks Not Loading

Verify YAML syntax:
```bash
python3 -c "import yaml; yaml.safe_load(open('my_checks.yaml'))"
```

### Reports Not Generated

Check write permissions in current directory:
```bash
ls -la
chmod +w .
```
