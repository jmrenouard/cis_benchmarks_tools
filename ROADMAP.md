# 🗺️ CIS Benchmarks Tools - Roadmap & Backlog (v1.2.2)

Ce document présente la feuille de route stratégique, la vision d'architecture et les évolutions prévues pour la suite d'outils d'audit CIS.

---

## 🔒 Contrainte Globale d'Architecture & Processus de Release

> [!IMPORTANT]
> 1. **Utiliser uniquement les modules standards Python 3 (PSL ONLY)** : L'ensemble du code Python (moteur d'exécution, scripts d'audit `audit_cis_*.py`, script unifié `audit_cis.py`, génération de rapports, routine pre-commit) utilise **EXCLUSIVEMENT la bibliothèque standard Python 3**. Aucune dépendance externe (`jinja2`, `yaml`, `requests`) n'est autorisée.
> 2. **Mise à Jour Systématique** : À chaque modification de code Python, le numéro de version (`VERSION`), la `ROADMAP.md` et `POTENTIAL_ISSUES.md` sont **automatiquement mis à jour et validés**.

---

## 📅 Jalons & Phases de Développement

### Phase 1 : Consolidation & Standardisation (Réalisé ✅)
- [x] Prise en charge des 15 benchmarks bases de données (MariaDB 10.6/10.11, MySQL 8.0/8.4/9.7, PostgreSQL 16/17/18, MongoDB 7/8, Cassandra 4.0/4.1/5.0).
- [x] Dockerfiles et scripts de démarrage standardisés (`scripts/start_*.sh`).
- [x] Cibles unifiées dans le `Makefile` (`make test-all`).
- [x] 15 rapports HTML générés et intégrés au dépôt dans `reports/`.
- [x] Intégration des 22 spécifications Markdown dans `CIS_DATA/`.

---

### Phase 2 : Moteur Unifié, Modularisation PSL & Arborescence (Réalisé ✅ - v1.2.2)

#### 1. Moteur d'Audit Unifié (`audit_cis.py`)
- CLI centralisée d'exécution autonome avec gestion des versions (`python3 audit_cis.py --version`, `--target <target>`, `--all`, `--auto-detect`, `--list-targets`).
- API Python programmatique native (`from audit_cis import run_single_audit, list_targets, get_target_info, TARGET_MAP`).
- Affichage synthétique des statistiques (827 contrôles d'audit répartis sur les 15 cibles bases de données).
- Création dynamique automatique du sous-dossier de sortie des rapports HTML/JSON.
- Moteur d'exécution 100% PSL.

#### 2. Routine Pre-Commit Python (`scripts/pre_commit_checks.py` & `make pre-commit`)
- Routine d'assemblage automatique Python (`scripts/bundle_audit_cis.py`) concaténant et synchronisant `audit_cis.py` à chaque commit.
- Validation automatique de la syntaxe Python (`py_compile`).
- Contrôle de conformité de l'AST pour bloquer tout import non-PSL.
- Validation de la syntaxe des scripts shell (`bash -n`).
- Contrôle d'intégrité de la structure du projet (`reports/`, `docker/`, `scripts/`, `CIS_DATA/`) et de la validité des fichiers rapports (> 1 KB).

#### 3. Réorganisation Structurée des Répertoires
- `reports/` : Sous-dossier dédié regroupant l'ensemble des rapports HTML d'audit.
- `docker/` : Sous-dossier dédié regroupant l'ensemble des 16 Dockerfiles.
- `scripts/` : Scripts shell de démarrage (`start_*.sh`) et routines pre-commit.
- `CIS_DATA/` : Contient l'ensemble des 22 spécifications Markdown de référence.

---

### Phase 3 : Extensions Système & CI/CD (Backlog long terme 🚀)

#### 1. Extension aux Briques Système & Linux (RHEL 8 / 9 / 10 / STIG)
- Développement des modules d'audit pour Red Hat Enterprise Linux basés sur les spécifications présentes dans `CIS_DATA/` en utilisant la PSL.
- Support d'audit local / SSH à distance.

#### 2. Sécurisation des Exécutions Subprocess (`shell=False`)
- Remplacer l'ensemble des chaînes de commande brutes par des tableaux d'arguments stricts (`shell=False`).

#### 3. Pipeline CI/CD GitHub Actions
- Automatisation de la routine `make pre-commit` et `make test-all` sur chaque Pull Request.
- Validation automatique de la syntaxe et du scan de sécurité.
