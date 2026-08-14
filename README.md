# 🛡️ CIS Benchmarks Tools Suite (v2.3.1)

> **Enterprise-Grade Automated Security Compliance Audit Engine for Databases and Linux Systems (100% Python Standard Library - PSL ONLY).**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![PSL Compliance](https://img.shields.io/badge/Dependencies-Zero%20External%20(PSL%20ONLY)-brightgreen.svg)](https://docs.python.org/3/library/)
[![Release](https://img.shields.io/badge/Release-v2.3.1-success.svg)](https://github.com/jmrenouard/cis_benchmarks_tools/releases)

---

## 📋 Overview

**CIS Benchmarks Tools** is a lightweight, zero-dependency automated security audit suite designed to evaluate system and database configurations against official **CIS (Center for Internet Security) Benchmarks** and **DISA STIG** security guidelines.

### Key Highlights
- 🔒 **100% Python Standard Library (PSL ONLY)**: Zero `pip` dependencies. Runs standalone on any standard Python 3 installation without installing external packages.
- 🎯 **4-Tier Execution Context Engine**: Seamless auto-detection and execution across 4 distinct deployment topologies:
  1. **Local Machine** (`--mode local` / `--local`)
  2. **Remote SSH** (`--mode ssh` / `--remote user@host` / `--ssh user@host`)
  3. **Docker Container (Local)** (`--docker <container_name>`)
  4. **Docker Container (Remote SSH)** (`--remote user@host --docker <container_name>`)
- 📊 **5-State Compliance Taxonomy**:
  - `Pass`: Verified compliant check.
  - `Fail`: Security non-compliance detected.
  - `Error`: Command or environment execution error (guaranteed distinct from security failures).
  - `Manual`: Procedural manual check with structured operational guides and diagnostic commands.
  - `Not Applicable (N/A)`: Variable, plugin, or feature not applicable in the evaluated environment.
- 🔑 **Database Authentication & Credentials Injection**:
  - Full support for `--db-user`, `--db-password`, `--db-host`, `--db-port`, `--db-name`, `--defaults-file`, `--auth-db`, and standard environment variables (`MYSQL_PWD`, `PGPASSWORD`, etc.).
  - Automatic password masking (`***MASKED***`) in audit output logs and HTML reports.
- 🩺 **Zero Command Error & Full Diagnostic Telemetry**: Complete preservation of `stderr` diagnostics without destructive `2>/dev/null` redirection.
- 📈 **100% Offline Pure Inline SVG Charts**: Donut charts and category progress bars generated natively in Python PSL without CDN or external JavaScript dependencies.
- 🗄️ **18 Audit Targets & 887 Controls**: Comprehensive coverage for MariaDB, MySQL, PostgreSQL, MongoDB, Apache Cassandra, and Red Hat Enterprise Linux (RHEL 8 / 9 / 10).
- 🌐 **Multi-Language Support (i18n)**: English (`--lang en`) and French (`--lang fr`) CLI and HTML reports.
- 📄 **Multi-Format Exporters (`--format html|json|xml|txt`)**: HTML, JSON (SIEM/DevSecOps), XML (JUnit/STIG), and TXT text reports.

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

## 🚀 Usage & Execution Examples

### Requirements
- **Python 3.8+** (Standard Installation, PSL only)
- **Docker** (Optional, for containerized audit targets)

### 1. List Available Targets
```bash
python3 audit_cis.py --list-targets
```

### 2. Local Machine Audit (`--mode local` / `--local`)
```bash
# PostgreSQL 16 local audit generating an HTML report
python3 audit_cis.py --target postgresql16 --local --format html

# RHEL 9 local audit exporting to JSON for SIEM ingestion
python3 audit_cis.py --target rhel9 --local --format json -o reports/audit_rhel9.json
```

### 3. Docker Container Audit (`--docker <container_name>`)
```bash
# Audit a running local MySQL 8.0 container directly
python3 audit_cis_mysql_80.py --docker mysql80-test

# Audit a MariaDB container using the unified entrypoint
python3 audit_cis.py --target mariadb106 --docker mariadb106-container --format html
```

### 4. Remote SSH Audit (`--mode ssh` / `--remote user@host`)
```bash
# Remote PostgreSQL 17 audit over SSH
python3 audit_cis.py --target postgresql17 --ssh admin@192.168.1.50 --format html

# Remote Docker audit over SSH (container running on a remote server)
python3 audit_cis.py --target mysql80 --ssh admin@192.168.1.50 --docker prod-mysql-container
```

### 5. Auditing with Database Credentials
```bash
# Provide credentials directly via CLI flags
python3 audit_cis_mysql_80.py --db-user root --db-password 'SecretPass123!' --db-host 127.0.0.1 --db-port 3306

# Pass options file for MySQL / PostgreSQL
python3 audit_cis_mysql_80.py --defaults-file /root/.my.cnf
```

### 6. Auto-Detection & Sequential Suite Execution
```bash
# Automatically detect active database services and audit them
python3 audit_cis.py --auto-detect

# Execute all 18 benchmarks sequentially
python3 audit_cis.py --all
```

---

## 🏗️ Architecture & Strict Design Principles

1. **Python Standard Library (PSL ONLY)**:
   - Absolutely no third-party package dependencies (`requests`, `jinja2`, `yaml`, `paramiko`, etc.).
   - Guaranteed to execute seamlessly in air-gapped, hardened, or restricted enterprise environments.
2. **Decoupled Architecture (`rules/*.json`)**:
   - Every benchmark's check definitions, preconditions, regexes, and remediation steps are stored in standalone JSON files under `rules/`.
3. **Diagnostic Telemetry Integrity**:
   - `stderr` streams are systematically preserved without destructive `2>/dev/null` masking.
4. **Offline First**:
   - Complete visual reports without requiring Internet access or external CDNs.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.