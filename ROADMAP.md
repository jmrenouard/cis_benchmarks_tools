# 🗺️ CIS Benchmarks Tools - Roadmap & Backlog (v1.4.1)

Ce document présente la feuille de route stratégique, la vision d'architecture et les évolutions prévues pour la suite d'outils d'audit CIS.

---

## 🔒 Contrainte Globale d'Architecture & Processus de Release

> [!IMPORTANT]
> 1. **Utiliser uniquement les modules standards Python 3 (PSL ONLY)** : L'ensemble du code Python (moteur d'exécution, scripts d'audit `audit_cis_*.py`, script unifié `audit_cis.py`, génération de rapports, routine pre-commit) utilise **EXCLUSIVEMENT la bibliothèque standard Python 3**. Aucune dépendance externe (`jinja2`, `yaml`, `requests`) n'est autorisée.
> 2. **Mise à Jour Systématique** : À chaque modification de code Python, le numéro de version (`VERSION`), la `ROADMAP.md` et `POTENTIAL_ISSUES.md` sont **automatiquement mis à jour et validés**.
> 3. **Règle de Nommage Git** : Le numéro de version est embarqué dans le nom de la branche (`feat/vX.Y.Z-...`), de l'Issue et de la PR (`[vX.Y.Z] ...`).

---

## 📅 Jalons & Phases de Développement

### Phase 1 : Consolidation & Standardisation (Réalisé ✅)
- [x] Prise en charge des 15 benchmarks bases de données (MariaDB 10.6/10.11, MySQL 8.0/8.4/9.7, PostgreSQL 16/17/18, MongoDB 7/8, Cassandra 4.0/4.1/5.0).
- [x] Dockerfiles et scripts de démarrage standardisés (`scripts/start_*.sh`).
- [x] Cibles unifiées dans le `Makefile` (`make test-all`).
- [x] 15 rapports HTML générés et intégrés au dépôt dans `reports/`.
- [x] Intégration des 22 spécifications Markdown dans `CIS_DATA/`.

---

### Phase 2 : Moteur Unifié, Modularisation PSL & Arborescence (Réalisé ✅ - v1.2.5)

#### 1. Moteur d'Audit Unifié (`audit_cis.py`)
- [x] CLI centralisée d'exécution autonome avec gestion des versions (`python3 audit_cis.py --version`, `--target <target>`, `--all`, `--auto-detect`, `--list-targets`).
- [x] API Python programmatique native (`from audit_cis import run_single_audit, list_targets, get_target_info, TARGET_MAP`).
- [x] Affichage synthétique des statistiques (887 contrôles d'audit répartis sur 18 cibles).
- [x] Moteur d'exécution 100% PSL.

#### 2. Routine Pre-Commit Python (`scripts/pre_commit_checks.py` & `make pre-commit`)
- [x] Routine d'assemblage automatique Python (`scripts/bundle_audit_cis.py`) concaténant et synchronisant `audit_cis.py` à chaque commit.
- [x] Validation automatique de la syntaxe Python (`py_compile`).
- [x] Contrôle de conformité de l'AST pour bloquer tout import non-PSL.
- [x] Validation de la syntaxe des scripts shell (`bash -n`).
- [x] Contrôle d'intégrité de la structure du projet (`reports/`, `docker/`, `scripts/`, `CIS_DATA/`) et de la validité des fichiers rapports (> 1 KB).
- [x] Validation de l'intégrité des 22 spécifications Markdown dans `CIS_DATA/` et des permissions d'exécution (`chmod +x`).

---

### Phase 3 : Extensions Système Linux & Sécurisation Subprocess (Réalisé ✅ - v1.4.1)

#### 1. Extension aux Briques Système & Linux (RHEL 8 / 9 / 10 / STIG)
- [x] Développement des modules d'audit Python PSL pour Red Hat Enterprise Linux 8 (`audit_cis_rhel_8.py`), RHEL 9 (`audit_cis_rhel_9.py`) et RHEL 10 (`audit_cis_rhel_10.py`).
- [x] Support d'audit local direct et d'audit à distance SSH via `--remote user@hostname` (sans dépendance externe).

#### 2. Sécurisation des Exécutions Subprocess (`shell=False` / Liste de Paramètres)
- [x] Migration de 100% des appels `subprocess.run` vers le format sous forme de liste de paramètres stricts (`['/bin/bash', '-c', command]`, `['docker', ...]`).
- [x] Élimination totale de `shell=True` dans l'ensemble des scripts Python pour éradiquer les risques d'injection de commandes.

#### 3. Pipeline CI/CD GitHub Actions (Backlog long terme 🚀)
- [ ] Automatisation de la routine `make pre-commit` et `make test-all` sur chaque Pull Request.
- [ ] Validation automatique de la syntaxe et du scan de sécurité.
