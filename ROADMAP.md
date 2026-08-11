# 🗺️ CIS Benchmarks Tools - Roadmap & Backlog

Ce document présente la feuille de route stratégique, la vision d'architecture et les évolutions prévues pour la suite d'outils d'audit CIS.

---

## 📅 Jalons & Phases de Développement

### Phase 1 : Consolidation & Standardisation (Réalisé ✅)
- [x] Prise en charge des 15 benchmarks bases de données (MariaDB 10.6/10.11, MySQL 8.0/8.4/9.7, PostgreSQL 16/17/18, MongoDB 7/8, Cassandra 4.0/4.1/5.0).
- [x] Dockerfiles et scripts de démarrage standardisés (`scripts/start_*.sh`).
- [x] Cibles unifiées dans le `Makefile` (`make test-all`).
- [x] 15 rapports HTML générés et intégrés au dépôt.
- [x] Intégration des 22 spécifications Markdown dans `CIS_DATA/`.

---

### Phase 2 : Refactorisation de l'Architecture (Backlog court terme 🎯)

#### 1. Moteur d'Audit Unifié (`cis_audit_engine`)
- Mettre en place un module Python centralisé rehaussant la réutilisabilité du code entre les scripts `audit_cis_*.py`.
- Séparer la définition des contrôles (format YAML ou JSON) du moteur d'exécution Python.

#### 2. Sécurisation des Exécutions Subprocess (`shell=False`)
- Remplacer les chaînes de commande brutes par des tableaux d'arguments stricts.
- Valider systématiquement l'existence des binaires clients (`mysql`, `mariadb`, `psql`, `mongosh`, `cqlsh`).

#### 3. Rendu de Rapport via Jinja2
- Migrer du formatage de chaîne natif Python (`str.format`) vers un moteur de template robuste (Jinja2).
- Éliminer totalement les risques d'erreurs de syntaxe CSS (`KeyError`).

---

### Phase 3 : Extensions Système & CI/CD (Backlog long terme 🚀)

#### 1. Extension aux Briques Système & Linux (RHEL 8 / 9 / 10 / STIG)
- Développement des modules d'audit pour Red Hat Enterprise Linux basés sur les spécifications présentes dans `CIS_DATA/`.
- Support d'audit local / SSH à distance.

#### 2. Pipeline CI/CD GitHub Actions
- Automatisation des tests de non-régression (`make test-all`) sur chaque Pull Request.
- Validation automatique de la syntaxe des scripts (`py_compile`) et scan de sécurité (`bandit` / Sourcery).

#### 3. Dashboard Centralisé & Export Multi-Formats
- Génération d'exports JSON / SARIF pour intégration SIEM et outils DevSecOps.
- Vue synthétique consolidée multi-bases et multi-serveurs.
