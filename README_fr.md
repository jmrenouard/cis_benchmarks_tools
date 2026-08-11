# 🛡️ Suite d'Outils CIS Benchmarks (v1.5.0)

> **Moteur d'Audit Automatisé de Conformité de Sécurité pour Bases de Données et Systèmes Linux (100% Python Standard Library - PSL ONLY).**

[![Licence: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Conformité PSL](https://img.shields.io/badge/Dépendances-Zéro%20Externe%20(PSL%20ONLY)-brightgreen.svg)](https://docs.python.org/3/library/)

---

## 📋 Vue d'Ensemble

**CIS Benchmarks Tools** est une suite d'audit de sécurité automatisée, légère et sans dépendance externe, conçue pour évaluer la configuration des systèmes et des bases de données par rapport aux recommandations officielles **CIS (Center for Internet Security) Benchmarks** et aux guides **DISA STIG**.

### Points Forts
- 🔒 **100% Python Standard Library (PSL ONLY)** : Aucune dépendance `pip`. S'exécute de manière autonome sur toute installation standard de Python 3.
- 🗄️ **18 Cibles d'Audit & 887 Contrôles** : Prise en charge de MariaDB, MySQL, PostgreSQL, MongoDB, Apache Cassandra et Red Hat Enterprise Linux (RHEL 8 / 9 / 10).
- ⚡ **CLI d'Exécution Unifiée (`audit_cis.py`)** : Exécutez des audits individuels, l'ensemble des benchmarks ou l'auto-détection des cibles via une interface unique en ligne de commande.
- 🌐 **Audit SSH à Distance** : Support natif de l'audit de serveurs distants via SSH (`--remote user@hostname`) sans nécessiter Paramiko ou Ansible.
- 🌐 **Support Multi-Langues (i18n)** : Rapports et CLI disponibles en Anglais (`--lang en`) et Français (`--lang fr`).
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

### 2. Exécuter l'Audit d'une Cible Unique
```bash
# Audit PostgreSQL 16 en français
python3 audit_cis.py --target postgresql16 --lang fr

# Audit Système RHEL 9 en français
python3 audit_cis.py --target rhel9 --lang fr
```

### 3. Audit d'un Serveur Distant via SSH
```bash
# Exécuter l'audit CIS/STIG RHEL 8 à distance via SSH
python3 audit_cis_rhel_8.py --remote root@192.168.1.50 --lang fr -o reports/rapport_remote_rhel8_fr.html
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
├── README.md                          # Documentation Principale (Anglais)
├── README_fr.md                       # Documentation Synchronisée (Français)
├── audit_cis.py                       # Moteur d'Audit Centralisé (v1.5.0)
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
├── reports/                           # Rapports HTML Générés
├── docker/                            # Dockerfiles de Test (16 cibles)
├── scripts/
│   ├── bundle_audit_cis.py            # Assembler Automatique de Code Python
│   ├── pre_commit_checks.py           # Contrôle de Qualité Pre-Commit (7 étapes)
│   └── start_*.sh                     # Scripts de Démarrage des Conteneurs
├── CIS_DATA/                          # 22 Spécifications Markdown de Référence
├── VERSION                            # Version Courante du Produit (v1.5.0)
├── ROADMAP.md                         # Feuille de Route et Jalons Réalisés
└── POTENTIAL_ISSUES.md                # Backlog et Dette Technique Résolue
```

---

## 🔒 Normes de Sécurité & d'Architecture

- **Conformité PSL** : Utilisation exclusive des modules standards Python 3 (`subprocess`, `os`, `sys`, `json`, `ast`, `re`, `html`). Aucun paquet tierce partie autorisé (`pip`, `jinja2`, `yaml`).
- **Prévention d'Injection de Commandes** : Exécution stricte avec liste de paramètres (`shell=False`) sur tous les appels système (`python.lang.security.audit.subprocess-shell-true`).
- **Assurance Qualité** : Routine de validation pre-commit automatique en 7 étapes :
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
