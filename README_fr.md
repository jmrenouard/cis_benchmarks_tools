# 🛡️ Suite CIS Benchmarks Tools (v2.3.1)

> **Moteur d'Audit de Conformité et de Sécurité Automatisé pour Bases de Données et Systèmes Linux (100% Python Standard Library - PSL ONLY).**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![PSL Compliance](https://img.shields.io/badge/Dependencies-Zero%20External%20(PSL%20ONLY)-brightgreen.svg)](https://docs.python.org/3/library/)
[![Release](https://img.shields.io/badge/Release-v2.3.1-success.svg)](https://github.com/jmrenouard/cis_benchmarks_tools/releases)

---

## 📋 Présentation Générale

**CIS Benchmarks Tools** est une suite d'audit de sécurité automatisée, ultra-légère et sans dépendance externe, conçue pour évaluer la configuration des bases de données et des systèmes Linux selon les référentiels officiels **CIS (Center for Internet Security) Benchmarks** et les guides **DISA STIG**.

### Points Clés & Innovations
- 🔒 **100% Python Standard Library (PSL ONLY)** : Zéro dépendance `pip`. S'exécute de manière autonome sur toute installation Python 3 standard, y compris en environnement cloisonné (Air-Gapped).
- 🎯 **Moteur d'Exécution à 4 Contextes Découplés** :
  1. **Machine Locale** (`--mode local` / `--local`)
  2. **Serveur Distant SSH** (`--mode ssh` / `--remote user@host` / `--ssh user@host`)
  3. **Conteneur Docker Local** (`--docker <nom_conteneur>`)
  4. **Conteneur Docker Distant via SSH** (`--remote user@host --docker <nom_conteneur>`)
- 📊 **Taxonomie de Conformité à 5 États Distincts** :
  - `Pass` : Contrôle conforme validé avec succès.
  - `Fail` : Non-conformité de sécurité avérée.
  - `Error` : Erreur d'exécution technique (distincte des échecs de sécurité).
  - `Manual` : Contrôle procédural avec guide opérationnel et commande diagnostique intégrée.
  - `Not Applicable (N/A)` : Variable ou composant non applicable dans l'environnement cible.
- 🔑 **Gestion des Identifiants & Authentification Base de Données** :
  - Support complet des arguments `--db-user`, `--db-password`, `--db-host`, `--db-port`, `--db-name`, `--defaults-file`, `--auth-db` et des variables d'environnement (`MYSQL_PWD`, `PGPASSWORD`, etc.).
  - Masquage automatique des mots de passe (`***MASKED***`) dans les flux et rapports HTML.
- 🩺 **Garantie Zéro Erreur Commande & Télémétrie `stderr` Intégrale** : Préservation complète sans `2>/dev/null`.
- 📈 **Graphiques SVG 100% Hors-Ligne** : Donut charts et barres de catégories générés nativement sans JavaScript ni CDN.
- 🗄️ **18 Référentiels & 887 Contrôles** : Couverture complète (MariaDB, MySQL, PostgreSQL, MongoDB, Cassandra, RHEL).
- 🌐 **Support Bilingue (i18n)** : Français (`--lang fr`) et Anglais (`--lang en`).
- 📄 **Export Multi-Formats (`--format html|json|xml|txt`)** : HTML Tailwind, JSON (SIEM), XML (JUnit/STIG), TXT.

---

## 🗄️ Cibles Supportées (18 Référentiels / 887 Contrôles)

### Moteurs de Bases de Données (15 Référentiels)

| Clé Cible | Moteur SGBD | Version / Profil | Benchmark CIS | Contrôles | Script d'Audit | Spécification JSON |
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

### Systèmes d'Exploitation Linux & STIG (3 Référentiels)

| Clé Cible | Système d'Exploitation | Profil / STIG | Benchmark CIS | Contrôles | Script d'Audit | Spécification JSON |
|---|---|---|---|:---:|---|---|
| `rhel8` | Red Hat Enterprise Linux | RHEL 8 CIS & STIG | v4.0.0 / v2.0.0 | 20 | [`audit_cis_rhel_8.py`](audit_cis_rhel_8.py) | [`rules/rhel_8.json`](rules/rhel_8.json) |
| `rhel9` | Red Hat Enterprise Linux | RHEL 9 CIS & STIG | v2.0.0 / v1.0.0 | 20 | [`audit_cis_rhel_9.py`](audit_cis_rhel_9.py) | [`rules/rhel_9.json`](rules/rhel_9.json) |
| `rhel10` | Red Hat Enterprise Linux | RHEL 10 CIS | v1.0.1 | 20 | [`audit_cis_rhel_10.py`](audit_cis_rhel_10.py) | [`rules/rhel_10.json`](rules/rhel_10.json) |

---

## 🚀 Guide d'Utilisation & Exemples

### 1. Lister les Référentiels
```bash
python3 audit_cis.py --list-targets
```

### 2. Audit en Mode Local (`--mode local` / `--local`)
```bash
python3 audit_cis.py --target postgresql16 --local --format html
python3 audit_cis.py --target rhel9 --local --format json -o reports/audit_rhel9.json
```

### 3. Audit de Conteneur Docker (`--docker <nom_conteneur>`)
```bash
python3 audit_cis_mysql_80.py --docker mysql80-test
python3 audit_cis.py --target mariadb106 --docker mariadb106-container --format html
```

### 4. Audit Distant par SSH (`--mode ssh` / `--remote user@host`)
```bash
python3 audit_cis.py --target postgresql17 --ssh admin@192.168.1.50 --format html
python3 audit_cis.py --target mysql80 --ssh admin@192.168.1.50 --docker prod-mysql-container
```

### 5. Audit avec Identifiants Base de Données
```bash
python3 audit_cis_mysql_80.py --db-user root --db-password 'SecretPass123!' --db-host 127.0.0.1 --db-port 3306
python3 audit_cis_mysql_80.py --defaults-file /root/.my.cnf
```

### 6. Détection Automatique & Exécution Globale
```bash
python3 audit_cis.py --auto-detect
python3 audit_cis.py --all
```

---

## 🏗️ Architecture & Règles de Conception

1. **100% Python Standard Library (PSL ONLY)** : Aucun recours aux bibliothèques tierces (`pip`, `requests`, `jinja2`, etc.).
2. **Découplage des Règles (`rules/*.json`)** : Contrôles, pré-conditions, regex et remédiations externalisés.
3. **Préservation de la Télémétrie** : Sorties d'erreur `stderr` conservées sans `2>/dev/null`.
4. **Indépendance Réseau (Offline First)** : Rapports HTML complets sans CDN externe.

---

## 📜 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE).
