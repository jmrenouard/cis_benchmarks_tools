# ⚠️ Potential Issues & Technical Debt Backlog (v1.4.3)

Ce document recense les problèmes potentiels, risques de bugs, remarques de sécurité et retours des revues de code (Pull Requests #17 à #103) identifiés sur le projet **CIS Benchmarks Tools**.

---

## 🔒 Contrainte Globale : Python Standard Library (PSL ONLY)

> [!IMPORTANT]
> L'ensemble du projet respecte la règle **Python Standard Library (PSL ONLY)**. Aucune bibliothèque externe (telle que `jinja2`, `yaml`, `requests`) ne doit être introduite.
> Cette contrainte est consignée dans `.agents/AGENTS.md` et est automatiquement vérifiée lors du `make pre-commit` via l'analyse d'AST dans `scripts/pre_commit_checks.py`.

---

## 1. Résolus dans les versions v1.2.0 - v1.4.3 ✅

- [x] **Élimination de `shell=True` & Sécurisation `subprocess`** : Migration de 100% des exécutions `subprocess` vers le format liste de paramètres stricts (`['/bin/bash', '-c', command]` et tableaux `['docker', ...]`). Risque d'injection de commande éradiqué sur l'ensemble des scripts d'audit et utilitaires (`python.lang.security.audit.subprocess-shell-true`).
- [x] **Extension Système RHEL & Audit SSH à Distance** : Implémentation des modules `audit_cis_rhel_8.py`, `audit_cis_rhel_9.py`, et `audit_cis_rhel_10.py` basés sur les spécifications `CIS_DATA/` avec support SSH natif `--remote user@host`.
- [x] **Documentation README.md en Anglais** : Réécriture intégrale du `README.md` en anglais décrivant les 18 cibles (887 contrôles), l'utilisation CLI `audit_cis.py` et les règles PSL.
- [x] **Échappement des templates HTML/CSS** : Correction des accolades simples dans les blocs `<style>` de tous les templates d'audit.
- [x] **Contrainte PSL vérifiée** : Suppression de toute référence à Jinja2/PyYAML et intégration d'un vérificateur d'imports PSL dans la routine pre-commit.
- [x] **Règles Workspace AGENTS.md** : Consignation explicite de la contrainte PSL, du versioning dans le nom de branche (`feat/vX.Y.Z-...`) et des PRs dans `.agents/AGENTS.md`.
- [x] **Organisation de l'arborescence** : Déplacement de tous les rapports dans `reports/` et des Dockerfiles dans `docker/`.
- [x] **Moteur d'Audit Unifié & Bundler** : Implémentation du script `audit_cis.py` alimenté par `scripts/bundle_audit_cis.py` (18 cibles bases de données & système).
- [x] **Validation d'Intégrité des Rapports & Specs** : Contrôle systématique des tailles de rapports HTML (> 1 KB), de l'arborescence, des spécifications `CIS_DATA/` et des permissions d'exécution (`chmod +x`) dans la routine pre-commit (7 étapes).

---

## 2. Évaluation des Conditions et Dépendances entre Contrôles

> [!IMPORTANT]
> Les sous-contrôles dépendant de variables stockées (`store_output_as`) nécessitent une exécution séquentielle stricte et un moteur d'évaluation complet.

### Constats & Recommandations :
- **Opérateurs d'évaluation** : L'évaluateur `evaluate_condition` prend en charge `stdout_equals`, `stdout_contains`, `stdout_not_equals`, `stdout_not_contains`, `file_exists`, `file_contains`, `exit_code_equals`.
- **Action Backlog** : Ajouter une suite de tests unitaires automatisés basés sur le module `unittest` de la PSL pour valider l'évaluateur de condition sur chaque type d'opérateur sans nécessiter de conteneur en cours d'exécution.

---

## 3. Robustesse des Scripts de Génération de Rapports

> [!TIP]
> Dans `scripts/generate_missing_reports.py`, s'assurer que les échecs de commandes `docker exec` interrompent la génération.

### Constats & Recommandations :
- Éviter la création ou la copie de fichiers rapports partiels ou vides (0 octet) en cas d'erreur de conteneur.
- Valider la taille minimale (> 1 KB) et la validité de la structure HTML après chaque copie de rapport.
