# CIS Benchmarks Tools

Automated security audit tool for CIS (Center for Internet Security) benchmarks compliance checking on Linux systems.

## Overview

This tool automates the process of auditing system configurations against CIS security benchmarks. It performs a series of configurable checks and generates comprehensive reports in multiple formats (JSON, HTML, and text).

## Features

- **Automated Security Audits**: Run multiple security checks automatically
- **Configurable Checks**: Define custom checks via YAML configuration files
- **Multiple Check Types**: 
  - Command-based checks (verify command output)
  - File-based checks (verify file permissions and existence)
- **Multiple Report Formats**: 
  - JSON (machine-readable)
  - HTML (human-readable with visual styling)
  - Text (simple text format)
- **Severity Levels**: Categorize checks by severity (high, medium, low)
- **Remediation Guidance**: Each check includes remediation instructions
- **Default Checks**: Built-in CIS benchmark checks for common scenarios

## Installation

### Requirements

- Python 3.6 or higher
- Linux-based operating system

### Setup

1. Clone the repository:
```bash
git clone https://github.com/jmrenouard/cis_benchmarks_tools.git
cd cis_benchmarks_tools
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make the script executable:
```bash
chmod +x cis_audit.py
```

## Usage

### Basic Usage

Run with default checks:
```bash
python3 cis_audit.py --use-defaults
```

### Using Configuration File

Run with a custom configuration file:
```bash
python3 cis_audit.py -c config/default_checks.yaml
```

### Specify Output Format

Generate an HTML report:
```bash
python3 cis_audit.py --use-defaults -f html -o my_audit_report
```

Generate a text report:
```bash
python3 cis_audit.py -c config/minimal_checks.yaml -f text -o audit_results
```

### Command-Line Options

```
Options:
  -h, --help            Show help message and exit
  -c CONFIG, --config CONFIG
                        Path to YAML configuration file with custom checks
  -o OUTPUT, --output OUTPUT
                        Output file for report (default: cis_audit_report)
  -f {json,text,html}, --format {json,text,html}
                        Report format (default: json)
  --use-defaults        Use default CIS checks even without config file
```

## Configuration

### Configuration File Format

Create a YAML file with your checks. Example:

```yaml
checks:
  - id: "1.1.1"
    type: command
    title: "Ensure password expiration is configured"
    description: "Password maximum age should be set"
    command: "grep ^PASS_MAX_DAYS /etc/login.defs"
    expected_output: "PASS_MAX_DAYS"
    severity: medium
    remediation: "Set PASS_MAX_DAYS to 90 in /etc/login.defs"

  - id: "1.2.1"
    type: file
    title: "Ensure permissions on /etc/passwd are configured"
    description: "/etc/passwd should have 644 permissions"
    filepath: "/etc/passwd"
    expected_perms: "644"
    severity: high
    remediation: "Run: chmod 644 /etc/passwd"
```

### Check Types

#### Command Checks
Execute shell commands and verify output:
- `command`: Shell command to execute
- `expected_output`: Optional expected string in output
- `should_exist`: Whether command should succeed (default: true)

#### File Checks
Verify file permissions and existence:
- `filepath`: Path to the file
- `expected_perms`: Expected permissions (e.g., "644")
- `should_exist`: Whether file should exist (default: true)

### Severity Levels
- `high`: Critical security issues
- `medium`: Important security configurations
- `low`: Best practice recommendations

## Examples

### Example 1: Quick Security Audit

```bash
python3 cis_audit.py --use-defaults -f html -o security_audit
```

This runs default checks and generates an HTML report.

### Example 2: Custom Configuration

Create a custom config file `my_checks.yaml`:
```yaml
checks:
  - id: "custom.1"
    type: command
    title: "Check if firewall is running"
    description: "Verify firewall status"
    command: "systemctl is-active ufw"
    expected_output: "active"
    severity: high
    remediation: "Enable ufw: systemctl enable ufw && systemctl start ufw"
```

Run the audit:
```bash
python3 cis_audit.py -c my_checks.yaml -f json
```

### Example 3: Automated Reporting

Run audit and save all report formats:
```bash
python3 cis_audit.py -c config/default_checks.yaml -f json -o report
python3 cis_audit.py -c config/default_checks.yaml -f html -o report
python3 cis_audit.py -c config/default_checks.yaml -f text -o report
```

## Default Checks

The tool includes built-in checks for:
- Password policies and expiration
- File permissions (/etc/passwd, /etc/shadow, /etc/group)
- Firewall status
- SSH configuration
- System updates

## Output Examples

### JSON Output
```json
{
  "timestamp": "2026-01-18T22:45:00.000000",
  "hostname": "server01",
  "total_checks": 5,
  "passed": 3,
  "failed": 2,
  "errors": 0,
  "checks": [...]
}
```

### HTML Report
Generates a styled HTML page with:
- Summary statistics
- Detailed check results with color coding
- Pass/Fail status indicators
- Remediation instructions for failed checks

## Security Considerations

- **Run as Root**: Many checks require root privileges to access system files
- **Audit Only**: This tool only audits; it does not make changes to the system
- **Regular Audits**: Schedule regular audits to maintain security posture
- **Review Reports**: Always review failed checks and apply remediations as appropriate

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- New CIS benchmark checks
- Additional check types
- Report format improvements
- Bug fixes

## License

See the LICENSE file for details.

## Resources

- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
- [Linux Security Documentation](https://www.kernel.org/doc/html/latest/security/)

## Support

For issues, questions, or contributions, please open an issue on GitHub.