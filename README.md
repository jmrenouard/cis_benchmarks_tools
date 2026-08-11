# 🛡️ CIS Benchmarks Tools Suite (v1.7.0)

> **Automated Security Compliance Audit Engine for Databases and Linux Systems (100% Python Standard Library - PSL ONLY).**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![PSL Compliance](https://img.shields.io/badge/Dependencies-Zero%20External%20(PSL%20ONLY)-brightgreen.svg)](https://docs.python.org/3/library/)

---

## 📋 Overview

**CIS Benchmarks Tools** is a lightweight, zero-dependency automated security audit suite designed to evaluate system and database configurations against official **CIS (Center for Internet Security) Benchmarks** and **DISA STIG** guidelines.

### Key Highlights
- 🔒 **100% Python Standard Library (PSL ONLY)**: Zero `pip` dependencies. Runs standalone on any standard Python 3 installation.
- 📁 **Decoupled Rule Specifications (`rules/*.json`)**: Audit control specifications are externalized into dedicated JSON rule files under `rules/` for easy editing, customization, and maintenance.
- 📊 **100% Offline Pure Inline SVG Charts Engine**: Self-contained SVG Donut Charts and Category Stacked Bar Charts generated natively in Python PSL without external JavaScript libraries or CDN dependencies.
- 💻 **Dual Execution Modes (Local & SSH Remote)**: Audit local machines/containers (`--mode local` / `--local`) or remote servers over SSH (`--mode ssh` / `--remote user@hostname` / `--ssh user@hostname`) natively without Paramiko or Ansible.
- 🗄️ **18 Audit Targets & 887 Controls**: Comprehensive coverage for MariaDB, MySQL, PostgreSQL, MongoDB, Apache Cassandra, and Red Hat Enterprise Linux (RHEL 8 / 9 / 10).
- ⚡ **Unified Execution CLI (`audit_cis.py`)**: Execute single audits, full benchmark suites, or auto-detect active targets via a single command-line interface.
- 🌐 **Multi-Language Support (i18n)**: English (`--lang en`) and French (`--lang fr`) CLI messages and HTML reports.
- 📄 **Multi-Format Exporters (`--format html|json|xml|txt`)**: Compliance output in HTML, JSON (SIEM/DevSecOps), XML (JUnit/STIG), and TXT text formats.

---

## 🗄️ Supported Audit Targets (18 Benchmarks / 887 Controls)

### Database Engines (15 Benchmarks)

| Target Key | Database Engine | Version / Profile | CIS Benchmark | Controls | Script | Rule Spec |
|---|---|---|---|:---:|---|---|
| `mariadb106` | MariaDB | 10.6 | v1.3.0 | 74 | [`audit_cis_mariadb_106.py`](audit_cis_mariadb_106.py) | [`rules/mariadb_106.json`](rules/mariadb_106.json) |
| `mariadb1011` | MariaDB | 10.11 | v1.0.0 | 75 | [`audit_cis_mariadb_1011.py`](audit_cis_mariadb_1011.py) | [`rules/mariadb_1011.json`](rules/mariadb_1011.json) |
| `mysql80` | MySQL Enterprise | 8.0 | v1.5.0 | 70 | [`audit_cis_mysql_80.py`](audit_cis_mysql_80.py) | [`rules/mysql_80.json`](rules/mysql_80.json) |
| `mysql-community84` | MySQL Community | 8.4 LTS | v1.1.0 | 79 | [`audit_cis_mysql_community_84.py`](audit_cis_mysql_community_84.py) | [`rules/mysql_community_84.json`](rules/mysql_community_84.json) |
| `mysql-enterprise84` | MySQL Enterprise | 8.4 LTS | v1.1.0 | 70 | [`audit_cis_mysql_enterprise_84.py`](audit_cis_mysql_enterprise_84.py) | [`rules/mysql_enterprise_84.json`](rules/mysql_enterprise_84.json) |
| `mysql-community97` | MySQL Community | 9.7 Innovation | v1.0.0 | 70 | [`audit_cis_mysql_community_97.py`](audit_cis_mysql_community_97.py) | [`rules/mysql_community_97.json`](rules/mysql_community_97.json) |
| `mysql-enterprise97` | MySQL Enterprise | 9.7 Innovation | v1.0.0 | 70 | [`audit_cis_mysql_enterprise_97.py`](audit_cis_mysql_enterprise_97.py) | [`rules/mysql_enterprise_97.json`](rules/mysql_enterprise_97.json) |
| `postgresql16` | PostgreSQL | 16 | v1.1.0 | 71 | [`audit_cis_postgresql_16.py`](audit_cis_postgresql_16.py) | [`rules/postgresql_16.json`](rules/postgresql_16.json) |
| `postgresql17` | PostgreSQL | 17 | v1.1.0 | 71 | [`audit_cis_postgresql_17.py`](audit_cis_postgresql_17.py) | [`rules/postgresql_17.json`](rules/postgresql_17.json) |
| `postgresql18` | PostgreSQL | 18 | v1.0.0 | 71 | [`audit_cis_postgresql_18.py`](audit_cis_postgresql_18.py) | [`rules/postgresql_18.json`](rules/postgresql_18.json) |
| `mongodb7` | MongoDB | 7.0 | v1.2.0 | 23 | [`audit_cis_mongodb_7.py`](audit_cis_mongodb_7.py) | [`rules/mongodb_7.json`](rules/mongodb_7.json) |
| `mongodb8` | MongoDB | 8.0 | v1.0.0 | 23 | [`audit_cis_mongodb_8.py`](audit_cis_mongodb_8.py) | [`rules/mongodb_8.json`](rules/mongodb_8.json) |
| `cassandra40` | Apache Cassandra | 4.0 | v1.3.0 | 20 | [`audit_cis_cassandra_40.py`](audit_cis_cassandra_40.py) | [`rules/cassandra_40.json`](rules/cassandra_40.json) |
| `cassandra41` | Apache Cassandra | 4.1 | v1.0.0 | 20 | [`audit_cis_cassandra_41.py`](audit_cis_cassandra_41.py) | [`rules/cassandra_41.json`](rules/cassandra_41.json) |
| `cassandra50` | Apache Cassandra | 5.0 | v1.1.0 | 20 | [`audit_cis_cassandra_50.py`](audit_cis_cassandra_50.py) | [`rules/cassandra_50.json`](rules/cassandra_50.json) |

### Linux Operating Systems & STIG (3 Benchmarks)

| Target Key | Operating System | Profile / STIG | CIS Benchmark | Controls | Script | Rule Spec |
|---|---|---|---|:---:|---|---|
| `rhel8` | Red Hat Enterprise Linux | RHEL 8 CIS & STIG | v4.0.0 / v2.0.0 | 20 | [`audit_cis_rhel_8.py`](audit_cis_rhel_8.py) | [`rules/rhel_8.json`](rules/rhel_8.json) |
| `rhel9` | Red Hat Enterprise Linux | RHEL 9 CIS & STIG | v2.0.0 / v1.0.0 | 20 | [`audit_cis_rhel_9.py`](audit_cis_rhel_9.py) | [`rules/rhel_9.json`](rules/rhel_9.json) |
| `rhel10` | Red Hat Enterprise Linux | RHEL 10 CIS | v1.0.1 | 20 | [`audit_cis_rhel_10.py`](audit_cis_rhel_10.py) | [`rules/rhel_10.json`](rules/rhel_10.json) |

---

## 🚀 Quick Start

### Requirements
- **Python 3.8+** (Standard Installation)
- **Docker** (Optional, for containerized test environments)

### 1. List All Available Audit Targets
```bash
python3 audit_cis.py --list-targets
```

### 2. Run Audit in Local Mode (`--mode local` / `--local`)
```bash
# Local PostgreSQL 16 Audit in HTML format
python3 audit_cis.py --target postgresql16 --mode local --format html

# Local RHEL 9 System Audit in JSON format
python3 audit_cis.py --target rhel9 --local --format json -o reports/audit_rhel9.json
```

### 3. Run Audit in Remote SSH Mode (`--mode ssh` / `--remote user@host`)
```bash
# Execute RHEL 8 CIS/STIG Audit on a remote server via SSH
python3 audit_cis.py --target rhel8 --mode ssh --remote root@192.168.1.50 -f txt

# Execute PostgreSQL 18 Audit remotely over SSH
python3 audit_cis_postgresql_18.py --ssh admin@db-server.domain.com --format json
```

### 4. Run All Audits / Auto-Detect
```bash
# Auto-detect running database services and execute corresponding audits
python3 audit_cis.py --auto-detect

# Execute all 18 benchmark audits sequentially
python3 audit_cis.py --all
```

---

## 📁 Repository Structure

```
cis_benchmarks_tools/
├── .github/
│   └── workflows/
│       └── ci.yml                     # GitHub Actions CI/CD Pipeline (Python 3.8-3.12)
├── README.md                          # Main Documentation (English)
├── README_fr.md                       # Synchronized Documentation (French)
├── audit_cis.py                       # Unified CLI Audit Engine (v1.7.0)
├── audit_cis_mariadb_106.py           # MariaDB 10.6 Audit Script
├── audit_cis_mariadb_1011.py          # MariaDB 10.11 Audit Script
├── audit_cis_mysql_80.py              # MySQL Enterprise 8.0 Audit Script
├── audit_cis_mysql_community_84.py    # MySQL Community 8.4 Audit Script
├── audit_cis_mysql_enterprise_84.py   # MySQL Enterprise 8.4 Audit Script
├── audit_cis_mysql_community_97.py    # MySQL Community 9.7 Audit Script
├── audit_cis_mysql_enterprise_97.py   # MySQL Enterprise 9.7 Audit Script
├── audit_cis_postgresql_16.py         # PostgreSQL 16 Audit Script
├── audit_cis_postgresql_17.py         # PostgreSQL 17 Audit Script
├── audit_cis_postgresql_18.py         # PostgreSQL 18 Audit Script
├── audit_cis_mongodb_7.py             # MongoDB 7 Audit Script
├── audit_cis_mongodb_8.py             # MongoDB 8 Audit Script
├── audit_cis_cassandra_40.py          # Cassandra 4.0 Audit Script
├── audit_cis_cassandra_41.py          # Cassandra 4.1 Audit Script
├── audit_cis_cassandra_50.py          # Cassandra 5.0 Audit Script
├── audit_cis_rhel_8.py                # RHEL 8 CIS/STIG Audit Script
├── audit_cis_rhel_9.py                # RHEL 9 CIS/STIG Audit Script
├── audit_cis_rhel_10.py               # RHEL 10 CIS Audit Script
├── rules/                             # 18 External JSON Rule Specifications (rules/*.json)
├── reports/                           # Generated Audit Reports (HTML, JSON, XML, TXT)
├── docker/                            # Test Container Dockerfiles (16 targets)
├── tests/
│   └── test_evaluate_condition.py     # Automated PSL Unit Test Suite (unittest)
├── scripts/
│   ├── bundle_audit_cis.py            # Automatic Script Bundler
│   ├── pre_commit_checks.py           # 8-Step Quality & Security Pre-Commit Checker
│   ├── run_e2e_tests.py               # Automated E2E Test & Quality Analysis Engine
│   └── start_*.sh                     # Database Container Startup Scripts
├── CIS_DATA/                          # 22 Reference Markdown Specifications
├── VERSION                            # Current Release Version (v1.7.0)
├── ROADMAP.md                         # Strategic Roadmap & Completed Milestones
└── POTENTIAL_ISSUES.md                # Technical Debt & Resolved Backlog
```

---

## 🔒 Security & Architecture Standards

- **PSL Compliance**: Strictly enforces Python 3 Standard Library modules ONLY (`subprocess`, `os`, `sys`, `json`, `ast`, `re`, `html`, `xml`, `unittest`). External packages (`pip`, `jinja2`, `yaml`, `requests`) are prohibited and blocked by pre-commit AST checks.
- **Command Injection Prevention**: All system command executions rely on strict parameter list arguments (`shell=False`) to eliminate command injection vulnerabilities (`python.lang.security.audit.subprocess-shell-true`).
- **Quality Assurance**: Automated 8-step pre-commit validation routine:
  ```bash
  make pre-commit
  ```

---

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

## 📚 References

- [CIS Benchmarks Official Site](https://www.cisecurity.org/cis-benchmarks)
- [Red Hat Enterprise Linux Security Guides](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/)
- [DISA STIG Directives](https://public.cyber.mil/stigs/)