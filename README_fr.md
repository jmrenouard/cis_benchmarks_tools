# 🛡️ Suite d'Outils CIS Benchmarks (v1.6.0)

> **Moteur d'Audit Automatisé de Conformité de Sécurité pour Bases de Données et Systèmes Linux (100% Python Standard Library - PSL ONLY).**

[![Licence: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Conformité PSL](https://img.shields.io/badge/Dépendances-Zéro%20Externe%20(PSL%20ONLY)-brightgreen.svg)](https://docs.python.org/3/library/)

---

## 📋 Vue d'Ensemble

**CIS Benchmarks Tools** est une suite d'audit de sécurité automatisée, légère et sans dépendance externe, conçue pour évaluer la configuration des systèmes et des bases de données par rapport aux recommandations officielles **CIS (Center for Internet Security) Benchmarks** et aux guides **DISA STIG**.

### Points Forts
- 🔒 **100% Python Standard Library (PSL ONLY)** : Aucune dépendance `pip`. S'exécute de manière autonome sur toute installation standard de Python 3.
- 💻 **Modes d'Exécution Doubles (Local & SSH Distant)** : Auditez des machines/conteneurs locaux (`--mode local` / `--local`) ou des serveurs distants via SSH (`--mode ssh` / `--remote user@hostname` / `--ssh user@hostname`) de manière native sans Paramiko ou Ansible.
- 🗄️ **18 Cibles d'Audit & 887 Contrôles** : Prise en charge de MariaDB, MySQL, PostgreSQL, MongoDB, Apache Cassandra et Red Hat Enterprise Linux (RHEL 8 / 9 / 10).
- ⚡ **CLI d'Exécution Unifiée (`audit_cis.py`)** : Exécutez des audits individuels, l'ensemble des benchmarks ou l'auto-détection des cibles via une interface unique en ligne de commande.
- 🌐 **Support Multi-Langues (i18n)** : Rapports et CLI disponibles en Anglais (`--lang en`) et Français (`--lang fr`).
- 📄 **Exportateurs Multi-Formats (`--format html|json|xml|txt`)** : Génération de rapports visuels HTML, JSON (SIEM/DevSecOps), XML (JUnit/STIG) et TXT clair.
- 📊 **Rapports HTML Interactifs** : Génère des rapports HTML autonomes dans `reports/` avec scores de conformité, graphiques par catégorie et remédiations détaillées.

---

## 🗄️ Cibles d'Audit Supportées (18 Benchmarks / 887 Contrôles)

### Moteurs de Bases de Données (15 Benchmarks)

| Identifiant | Moteur de BD | Version / Profil | CIS Benchmark | Contrôles | Script |
|---|---|---|---|:---:|---|
| `mariadb106` | MariaDB | 10.6 | v1.3.0 | 74 | [`audit_cis_mariadb_106.py`](audit_cis_mariadb_106.py) |
| `mariadb1011` | MariaDB | 10.11 | v1.0.0 | 75 | [`audit_cis_mariadb_1011.py`](audit_cis_mariadb_1011.py) |
| `mysql80` | MySQL Enterprise | 8.0 | v1.5.0 | 70 | [`audit_cis_mysql_80.py`](audit_cis_mysql_80.py) |
| `mysql-community84` | MySQL Community | 8.4 LTS | v1.1.0 | 79 | [`audit_cis_mysql_community_84.py`](audit_cis_mysql_community_84.py) |
| `mysql-enterprise84` | MySQL Enterprise | 8.4 LTS | v1.1.0 | 70 | [`audit_cis_mysql_enterprise_84.py`](audit_cis_mysql_enterprise_84.py) |
| `mysql-community97` | MySQL Community | 9.7 Innovation | v1.0.0 | 70 | [`audit_cis_mysql_community_97.py`](audit_cis_mysql_community_97.py) |
| `mysql-enterprise97` | MySQL Enterprise | 9.7 Innovation | v1.0.0 | 70 | [`audit_cis_mysql_enterprise_97.py`](audit_cis_mysql_enterprise_97.py) |
| `postgresql16` | PostgreSQL | 16 | v1.1.0 | 71 | [`audit_cis_postgresql_16.py`](audit_cis_postgresql_16.py) |
| `postgresql17` | PostgreSQL | 17 | v1.1.0 | 71 | [`audit_cis_postgresql_17.py`](audit_cis_postgresql_17.py) |
| `postgresql18` | PostgreSQL | 18 | v1.0.0 | 71 | [`audit_cis_postgresql_18.py`](audit_cis_postgresql_18.py) |
| `mongodb7` | MongoDB | 7.0 | v1.2.0 | 23 | [`audit_cis_mongodb_7.py`](audit_cis_mongodb_7.py) |
| `mongodb8` | MongoDB | 8.0 | v1.0.0 | 23 | [`audit_cis_mongodb_8.py`](audit_cis_mongodb_8.py) |
| `cassandra40` | Apache Cassandra | 4.0 | v1.3.0 | 20 | [`audit_cis_cassandra_40.py`](audit_cis_cassandra_40.py) |
| `cassandra41` | Apache Cassandra | 4.1 | v1.0.0 | 20 | [`audit_cis_cassandra_41.py`](audit_cis_cassandra_41.py) |
| `cassandra50` | Apache Cassandra | 5.0 | v1.1.0 | 20 | [`audit_cis_cassandra_50.py`](audit_cis_cassandra_50.py) |

### Systèmes d'Exploitation Linux & STIG (3 Benchmarks)

| Identifiant | Système d'Exploitation | Profil / STIG | CIS Benchmark | Contrôles | Script |
|---|---|---|---|:---:|---|
| `rhel8` | Red Hat Enterprise Linux | RHEL 8 CIS & STIG | v4.0.0 / v2.0.0 | 20 | [`audit_cis_rhel_8.py`](audit_cis_rhel_8.py) |
| `rhel9` | Red Hat Enterprise Linux | RHEL 9 CIS & STIG | v2.0.0 / v1.0.0 | 20 | [`audit_cis_rhel_9.py`](audit_cis_rhel_9.py) |
| `rhel10` | Red Hat Enterprise Linux | RHEL 10 CIS | v1.0.1 | 20 | [`audit_cis_rhel_10.py`](audit_cis_rhel_10.py) |

---

## 🚀 Démarrage Rapide

### Prérequis
- **Python 3.8+** (Installation standard)
- **Docker** (Optionnel, pour les environnements de test)

### 1. Lister les Cibles d'Audit Disponibles
```bash
python3 audit_cis.py --list-targets
```

### 2. Exécuter un Audit en Mode Local (`--mode local` / `--local`)
```bash
# Audit local PostgreSQL 16 au format HTML en français
python3 audit_cis.py --target postgresql16 --mode local --format html --lang fr

# Audit local Système RHEL 9 au format JSON pour SIEM
python3 audit_cis.py --target rhel9 --local --format json -o reports/audit_rhel9.json
```

### 3. Exécuter un Audit en Mode SSH Distant (`--mode ssh` / `--remote user@host`)
```bash
# Exécuter l'audit CIS/STIG RHEL 8 à distance via SSH
python3 audit_cis.py --target rhel8 --mode ssh --remote root@192.168.1.50 -f txt

# Exécuter l'audit PostgreSQL 18 à distance via SSH
python3 audit_cis_postgresql_18.py --ssh admin@db-server.domain.com --format json
```

### 4. Exécuter Tous les Audits / Auto-Détection
```bash
# Auto-détecter les conteneurs de bases de données actifs et exécuter les audits
python3 audit_cis.py --auto-detect

# Exécuter les audits des 18 cibles de manière séquentielle
python3 audit_cis.py --all
```

---

## 📁 Structure du Projet

```
cis_benchmarks_tools/
├── .github/
│   └── workflows/
│       └── ci.yml                     # Pipeline CI/CD GitHub Actions (Python 3.8-3.12)
├── README.md                          # Documentation Principale (Anglais)
├── README_fr.md                       # Documentation Synchronisée (Français)
├── audit_cis.py                       # Moteur d'Audit Centralisé (v1.6.0)
├── audit_cis_mariadb_106.py           # Script d'Audit MariaDB 10.6
├── audit_cis_mariadb_1011.py          # Script d'Audit MariaDB 10.11
├── audit_cis_mysql_80.py              # Script d'Audit MySQL Enterprise 8.0
├── audit_cis_mysql_community_84.py    # Script d'Audit MySQL Community 8.4
├── audit_cis_mysql_enterprise_84.py   # Script d'Audit MySQL Enterprise 8.4
├── audit_cis_mysql_community_97.py    # Script d'Audit MySQL Community 9.7
├── audit_cis_mysql_enterprise_97.py   # Script d'Audit MySQL Enterprise 9.7
├── audit_cis_postgresql_16.py         # Script d'Audit PostgreSQL 16
├── audit_cis_postgresql_17.py         # Script d'Audit PostgreSQL 17
├── audit_cis_postgresql_18.py         # Script d'Audit PostgreSQL 18
├── audit_cis_mongodb_7.py             # Script d'Audit MongoDB 7
├── audit_cis_mongodb_8.py             # Script d'Audit MongoDB 8
├── audit_cis_cassandra_40.py          # Script d'Audit Cassandra 4.0
├── audit_cis_cassandra_41.py          # Script d'Audit Cassandra 4.1
├── audit_cis_cassandra_50.py          # Script d'Audit Cassandra 5.0
├── audit_cis_rhel_8.py                # Script d'Audit RHEL 8 CIS/STIG
├── audit_cis_rhel_9.py                # Script d'Audit RHEL 9 CIS/STIG
├── audit_cis_rhel_10.py               # Script d'Audit RHEL 10 CIS
├── reports/                           # Rapports Générés (HTML, JSON, XML, TXT)
├── docker/                            # Dockerfiles de Test (16 cibles)
├── tests/
│   └── test_evaluate_condition.py     # Suite de Tests Unitaires automatisés (unittest)
├── scripts/
│   ├── bundle_audit_cis.py            # Assembler Automatique de Code Python
│   ├── pre_commit_checks.py           # Contrôle de Qualité Pre-Commit (8 étapes)
│   ├── run_e2e_tests.py               # Moteur d'Analyse et de Tests E2E Automatisés
│   └── start_*.sh                     # Scripts de Démarrage des Conteneurs
├── CIS_DATA/                          # 22 Spécifications Markdown de Référence
├── VERSION                            # Version Courante du Produit (v1.6.0)
├── ROADMAP.md                         # Feuille de Route et Jalons Réalisés
└── POTENTIAL_ISSUES.md                # Backlog et Dette Technique Résolue
```

---

## 🔒 Normes de Sécurité & d'Architecture

- **Conformité PSL** : Utilisation exclusive des modules standards Python 3 (`subprocess`, `os`, `sys`, `json`, `ast`, `re`, `html`, `xml`, `unittest`). Aucun paquet tierce partie autorisé (`pip`, `jinja2`, `yaml`).
- **Prévention d'Injection de Commandes** : Exécution stricte avec liste de paramètres (`shell=False`) sur tous les appels système (`python.lang.security.audit.subprocess-shell-true`).
- **Assurance Qualité** : Routine de validation pre-commit automatique en 8 étapes :
  ```bash
  make pre-commit
  ```

---

## 📄 Licence

Ce projet est distribué sous licence **MIT**. Consulter le fichier `LICENSE` pour plus de détails.

## 📚 Références

- [Site Officiel CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
- [Guides de Sécurité Red Hat Enterprise Linux](https://access.redhat.com/documentation/fr-fr/red_hat_enterprise_linux/)
- [Directives DISA STIG](https://public.cyber.mil/stigs/)
