# Targets, Transport Tiers, Compliance States, and Scoring

Catalog of all 18 benchmarks (887 controls), 4 transports, 5 states, and scoring formula (`v2.10.0`).

## 1. Benchmark Target Matrix (18 Targets / 887 Controls)

| Key | Product | Ctrls | Script | Rule Spec |
| :--- | :--- | :---: | :--- | :--- |
| `mariadb106` | MariaDB 10.6 | 74 | `audit_cis_mariadb_106.py` | `rules/mariadb_106.json` |
| `mariadb1011` | MariaDB 10.11 | 75 | `audit_cis_mariadb_1011.py` | `rules/mariadb_1011.json` |
| `mysql80` | MySQL Enterprise 8.0 | 70 | `audit_cis_mysql_80.py` | `rules/mysql_80.json` |
| `mysql-community84` | MySQL Community 8.4 LTS | 79 | `audit_cis_mysql_community_84.py` | `rules/mysql_community_84.json` |
| `mysql-enterprise84` | MySQL Enterprise 8.4 LTS | 70 | `audit_cis_mysql_enterprise_84.py` | `rules/mysql_enterprise_84.json` |
| `mysql-community97` | MySQL Community 9.7 | 70 | `audit_cis_mysql_community_97.py` | `rules/mysql_community_97.json` |
| `mysql-enterprise97` | MySQL Enterprise 9.7 | 70 | `audit_cis_mysql_enterprise_97.py` | `rules/mysql_enterprise_97.json` |
| `postgresql16` | PostgreSQL 16 | 71 | `audit_cis_postgresql_16.py` | `rules/postgresql_16.json` |
| `postgresql17` | PostgreSQL 17 | 71 | `audit_cis_postgresql_17.py` | `rules/postgresql_17.json` |
| `postgresql18` | PostgreSQL 18 | 71 | `audit_cis_postgresql_18.py` | `rules/postgresql_18.json` |
| `mongodb7` | MongoDB 7.0 | 23 | `audit_cis_mongodb_7.py` | `rules/mongodb_7.json` |
| `mongodb8` | MongoDB 8.0 | 23 | `audit_cis_mongodb_8.py` | `rules/mongodb_8.json` |
| `cassandra40` | Apache Cassandra 4.0 | 20 | `audit_cis_cassandra_40.py` | `rules/cassandra_40.json` |
| `cassandra41` | Apache Cassandra 4.1 | 20 | `audit_cis_cassandra_41.py` | `rules/cassandra_41.json` |
| `cassandra50` | Apache Cassandra 5.0 | 20 | `audit_cis_cassandra_50.py` | `rules/cassandra_50.json` |
| `rhel8` | Red Hat Enterprise Linux 8 | 20 | `audit_cis_rhel_8.py` | `rules/rhel_8.json` |
| `rhel9` | Red Hat Enterprise Linux 9 | 20 | `audit_cis_rhel_9.py` | `rules/rhel_9.json` |
| `rhel10` | Red Hat Enterprise Linux 10 | 20 | `audit_cis_rhel_10.py` | `rules/rhel_10.json` |

## 2. Four-Tier Transports (`execution_drivers.py`)

| Tier | Driver Class | `driver_type` | CLI Trigger |
| :---: | :--- | :--- | :--- |
| 1 | `LocalExecutor` | `LOCAL_BAREMETAL` | `--mode local` / `--local` |
| 2 | `DockerExecutor` | `LOCAL_DOCKER` | `--docker <container>` |
| 3 | `SSHExecutor` | `REMOTE_SSH_BAREMETAL` | `--mode ssh` / `--remote <user@host>` |
| 4 | `RemoteSSHContainerExecutor` | `REMOTE_SSH_DOCKER` | `--remote <user@host> --docker <container>` |

`RuntimeDetector.inspect()` probes `/.dockerenv`, `/run/.containerenv`, `/proc/1/cgroup`, `/proc/self/mountinfo`,
and `id -u` in one batched command.

## 3. Five-State Taxonomy & Standardized Scoring (`cis_core_engine.py`)

| State | SARIF `kind` | SARIF `level` | In Denominator |
| :--- | :--- | :--- | :---: |
| `Pass` (`PASS`, `SUCCÈS`) | `pass` | `none` | Yes |
| `Fail` (`FAIL`, `FAILED`) | `fail` | `error` | Yes |
| `Error` (`ERROR`, `ERREUR`) | `open` | `warning` | No |
| `Manual` (`MANUAL`, `MANUEL`) | `review` | `note` | No |
| `Not Applicable` (`N/A`, `NA`) | `notApplicable` | `none` | No |

$$
\text{Attempted} = \text{Pass} + \text{Fail}
$$

$$
\text{Score}_{\text{compliance}} = \begin{cases} \dfrac{\text{Pass}}{\text{Attempted}} \times 100 & \text{if } \text{Attempted} > 0 \\ 0.0\% & \text{if } \text{Attempted} = 0 \end{cases}
$$

## Related Documentation

- [CLI Flags & Exit Codes](../cli-and-scripts/cli-flags-and-exit-codes.md) · [Error & Alert Matrix](../troubleshooting-codes/error-and-alert-matrix.md)
- [Remote SSH & Docker Audits](../../02-how-to-guides/deployment/run-remote-ssh-and-docker-audits.md)
