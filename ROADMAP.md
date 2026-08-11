# 🗺️ CIS Benchmarks Tools - Roadmap & Backlog

Ce document présente la feuille de route stratégique, la vision d'architecture et les évolutions prévues pour la suite d'outils d'audit CIS.

---

## 🔒 Contrainte Globale d'Architecture : Python Standard Library (PSL ONLY)

> [!IMPORTANT]
> L'ensemble du code de la suite d'audit CIS (moteur d'exécution, scripts d'audit `audit_cis_*.py`, script unifié `audit_cis.py`, génération de rapports HTML/JSON) utilise **EXCLUSIVEMENT les modules de la bibliothèque standard Python (Python Standard Library - PSL)**.
> **Aucune dépendance externe tierce** (ex. `jinja2`, `yaml`, `requests`) n'est autorisée, garantissant une exécution nomade, sans installation de paquets `pip`, dans n'importe quel environnement Linux / Docker.

---

## 📅 Jalons & Phases de Développement

### Phase 1 : Consolidation & Standardisation (Réalisé ✅)
- [x] Prise en charge des 15 benchmarks bases de données (MariaDB 10.6/10.11, MySQL 8.0/8.4/9.7, PostgreSQL 16/17/18, MongoDB 7/8, Cassandra 4.0/4.1/5.0).
- [x] Dockerfiles et scripts de démarrage standardisés (`scripts/start_*.sh`).
- [x] Cibles unifiées dans le `Makefile` (`make test-all`).
- [x] 15 rapports HTML générés et intégrés au dépôt.
- [x] Intégration des 22 spécifications Markdown dans `CIS_DATA/`.

---

### Phase 2 : Refactorisation de l'Architecture & Script Unifié (Réalisé ✅)

#### 1. Script d'Audit Unifié (`audit_cis.py`)
- Moteur d'audit centralisé permettant d'exécuter n'importe quel benchmark CIS via une CLI unique (`python3 audit_cis.py --target <target>`).
- Auto-détection des bases de données (`--auto-detect`) et exécution globale (`--all`).
- Respect strict de la PSL (modules `argparse`, `json`, `subprocess`, `os`, `sys`, `re`, `html`, `datetime`).

#### 2. Routine Pre-Commit (`scripts/pre-commit.sh` & `make pre-commit`)
- Validation automatique de la syntaxe Python (`py_compile`).
- Vérification stricte du non-usage de dépendances tierces (PSL compliance check).
- Validation de la syntaxe des scripts shell (`bash -n`).

#### 3. Sécurisation des Exécutions Subprocess (`shell=False`)
- Remplacer les chaînes de commande brutes par des tableaux d'arguments stricts dans les prochains modules.

---

### Phase 3 : Extensions Système & CI/CD (Backlog long terme 🚀)

#### 1. Extension aux Briques Système & Linux (RHEL 8 / 9 / 10 / STIG)
- Développement des modules d'audit pour Red Hat Enterprise Linux basés sur les spécifications présentes dans `CIS_DATA/` en utilisant la PSL.
- Support d'audit local / SSH à distance.

#### 2. Pipeline CI/CD GitHub Actions
- Automatisation de la routine `make pre-commit` et `make test-all` sur chaque Pull Request.
- Scan de sécurité statique de code.
