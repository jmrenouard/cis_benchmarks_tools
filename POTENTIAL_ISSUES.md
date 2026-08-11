# ⚠️ Potential Issues & Technical Debt Backlog

Ce document recense les problèmes potentiels, risques de bugs, remarques de sécurité et retours des revues de code (Pull Requests #17 à #37) identifiés sur le projet **CIS Benchmarks Tools**.

---

## 1. Sécurité et Injections de Commandes (`subprocess`)

> [!WARNING]
> Plusieurs scripts d'audit et utilitaires utilisent `subprocess.run(..., shell=True)` avec interpolation dynamique de chaînes.

### Constats & Recommandations :
- **Risque (`python.lang.security.audit.subprocess-shell-true`)** : L'utilisation de `shell=True` expose à des risques d'injection de commandes si des variables externes ou non assainies y sont transmises.
- **Action Backlog** : Migrer l'ensemble des appels `subprocess.run` vers le format sous forme de liste de paramètres (ex. `['docker', 'exec', container, ...]` avec `shell=False`).

---

## 2. Évaluation des Conditions et Dépendances entre Contrôles

> [!IMPORTANT]
> Les sous-contrôles dépendant de variables stockées (`store_output_as`) nécessitent une exécution séquentielle stricte et un moteur d'évaluation complet.

### Constats & Recommandations :
- **Opérateurs d'évaluation** : L'évaluateur `evaluate_condition` prend désormais en charge `stdout_equals`, `stdout_contains`, `stdout_not_equals`, `stdout_not_contains`, `file_exists`, `file_contains`, `exit_code_equals`.
- **Action Backlog** : Ajouter une suite de tests unitaires automatisés pour valider l'évaluateur de condition sur chaque type d'opérateur sans nécessiter de conteneur en cours d'exécution.

---

## 3. Échappement des Templates HTML / CSS

> [!NOTE]
> Les blocs `<style>` dans les chaînes `HTML_TEMPLATE` doivent obligatoirement utiliser des accolades doubles (`{{` et `}}`).

### Constats & Recommandations :
- **Risque `KeyError`** : Des déclarations CSS avec accolades simples (`.status-pass { color: ... }`) ont provoqué des `KeyError: ' color'` lors des appels à `.format()`.
- **Action Backlog** : Migrer vers le moteur de template Jinja2 au lieu de `str.format()` pour isoler totalement la couche de présentation CSS.

---

## 4. Robustesse des Scripts de Génération de Rapports

> [!TIP]
> Dans `scripts/generate_missing_reports.py`, s'assurer que les échecs de commandes `docker exec` interrompent la génération.

### Constats & Recommandations :
- Éviter la création ou la copie de fichiers rapports partiels ou vides (0 octet) en cas d'erreur de conteneur.
- Valider la taille minimale (> 1 KB) et la validité de la structure HTML après chaque copie de rapport.
