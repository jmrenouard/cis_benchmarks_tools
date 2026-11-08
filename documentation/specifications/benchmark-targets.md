---
title: Benchmark Targets Specification
date: 2026-11-08
category: specification
---

# CIS Benchmark Targets Specification

## 1. Target Catalog
The suite implements **18 official CIS Benchmarks and DISA STIG targets**, comprising **887 security controls**:

| # | Target Key | Product Name | Benchmark Version | Controls | Script File | Rule Spec JSON | Dockerfile |
|---|------------|--------------|-------------------|----------|-------------|----------------|------------|
| 1 | `mariadb106` | MariaDB 10.6 | CIS v1.1.0 | 74 | `audit_cis_mariadb_106.py` | `rules/mariadb_106.json` | `docker/Dockerfile_mariadb106` |
| 2 | `mariadb1011` | MariaDB 10.11 | CIS v1.0.0 | 75 | `audit_cis_mariadb_1011.py` | `rules/mariadb_1011.json` | `docker/Dockerfile_mariadb1011` |
| 3 | `mysql80` | MySQL Enterprise 8.0 | CIS v1.5.0 | 70 | `audit_cis_mysql_80.py` | `rules/mysql_80.json` | `docker/Dockerfile_mysql80` |
| 4 | `mysql-community84` | MySQL Community 8.4 LTS | CIS v1.1.0 | 79 | `audit_cis_mysql_community_84.py` | `rules/mysql_community_84.json` | `docker/Dockerfile_mysql_community_84` |
| 5 | `mysql-enterprise84` | MySQL Enterprise 8.4 LTS | CIS v1.1.0 | 70 | `audit_cis_mysql_enterprise_84.py` | `rules/mysql_enterprise_84.json` | `docker/Dockerfile_mysql_enterprise_84` |
| 6 | `mysql-community97` | MySQL Community 9.7 | CIS v1.0.0 | 70 | `audit_cis_mysql_community_97.py` | `rules/mysql_community_97.json` | `docker/Dockerfile_mysql_community_97` |
| 7 | `mysql-enterprise97` | MySQL Enterprise 9.7 | CIS v1.0.0 | 70 | `audit_cis_mysql_enterprise_97.py` | `rules/mysql_enterprise_97.json` | `docker/Dockerfile_mysql_enterprise_97` |
| 8 | `postgresql16` | PostgreSQL 16 | CIS v1.1.0 | 71 | `audit_cis_postgresql_16.py` | `rules/postgresql_16.json` | `docker/Dockerfile_postgresql16` |
| 9 | `postgresql17` | PostgreSQL 17 | CIS v1.1.0 | 71 | `audit_cis_postgresql_17.py` | `rules/postgresql_17.json` | `docker/Dockerfile_postgresql17` |
| 10 | `postgresql18` | PostgreSQL 18 | CIS v1.0.0 | 71 | `audit_cis_postgresql_18.py` | `rules/postgresql_18.json` | `docker/Dockerfile_postgresql18` |
| 11 | `mongodb7` | MongoDB 7.0 | CIS v1.2.0 | 23 | `audit_cis_mongodb_7.py` | `rules/mongodb_7.json` | `docker/Dockerfile_mongodb7` |
| 12 | `mongodb8` | MongoDB 8.0 | CIS v1.0.0 | 23 | `audit_cis_mongodb_8.py` | `rules/mongodb_8.json` | `docker/Dockerfile_mongodb8` |
| 13 | `cassandra40` | Apache Cassandra 4.0 | CIS v1.3.0 | 20 | `audit_cis_cassandra_40.py` | `rules/cassandra_40.json` | `docker/Dockerfile_cassandra40` |
| 14 | `cassandra41` | Apache Cassandra 4.1 | CIS v1.0.0 | 20 | `audit_cis_cassandra_41.py` | `rules/cassandra_41.json` | `docker/Dockerfile_cassandra41` |
| 15 | `cassandra50` | Apache Cassandra 5.0 | CIS v1.1.0 | 20 | `audit_cis_cassandra_50.py` | `rules/cassandra_50.json` | `docker/Dockerfile_cassandra50` |
| 16 | `rhel8` | Red Hat Enterprise Linux 8 | CIS v4.0.0 / STIG v2.0.0 | 20 | `audit_cis_rhel_8.py` | `rules/rhel_8.json` | N/A (OS host) |
| 17 | `rhel9` | Red Hat Enterprise Linux 9 | CIS v2.0.0 / STIG v1.0.0 | 20 | `audit_cis_rhel_9.py` | `rules/rhel_9.json` | N/A (OS host) |
| 18 | `rhel10` | Red Hat Enterprise Linux 10 | CIS v1.0.1 | 20 | `audit_cis_rhel_10.py` | `rules/rhel_10.json` | N/A (OS host) |

**Total: 18 Targets, 887 Controls**

## 2. Target Naming Conventions
- **Audit Script Filenames**: `audit_cis_<product>_<version>.py`. RHEL targets use an underscore before the version: `audit_cis_rhel_8.py`, `audit_cis_rhel_9.py`, `audit_cis_rhel_10.py`.
- **Rule Specifications**: `rules/<canonical_name>.json`.
- **Database Test Dockerfiles**: `docker/Dockerfile_<product><version>` or `docker/Dockerfile_<product>_<flavor>_<version>`.
