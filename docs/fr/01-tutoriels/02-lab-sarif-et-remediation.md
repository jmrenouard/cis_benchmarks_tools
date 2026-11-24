# Tutoriel 2 : Lab SARIF et remédiation dry-run

Ce tutoriel produit un export SARIF v2.1.0 et génère des plans de remédiation déterministes en lecture seule à partir d'un rapport JSON existant.

```mermaid
flowchart LR
    A["Rapport JSON CIS"] --> B["Export SARIF v2.1.0"]
    A --> C["Rejoue --from-report"]
    C --> D["Plans diff, sql et ansible"]
```

## Prérequis isolés

- Python `3.10` ou supérieur (`python3 --version`).
- Avoir terminé le [Tutoriel 1](01-premier-audit-local-et-docker.md) ou disposer du répertoire du projet.

## Étape 1 — Préparer un rapport JSON de démonstration

Créez un espace temporaire et un exemple minimal de rapport JSON :

```bash
mkdir -p /tmp/cis-sarif-fr
cat <<'EOF' > /tmp/cis-sarif-fr/sample_report.json
{
  "target": "mariadb106",
  "version": "1.1.0",
  "host": "tut-mariadb",
  "timestamp": "2026-11-24T00:00:00Z",
  "controls": [
    {
      "id": "4.3",
      "title": "Ensure allow-nonexistent-definer is OFF",
      "status": "FAIL",
      "severity": "HIGH",
      "remediation": "SET GLOBAL local_infile = OFF;"
    }
  ]
}
EOF
```

## Étape 2 — Générer un plan de remédiation dry-run

Rejouez le rapport hors ligne avec `--remediate-dry-run` :

```bash
python3 audit_cis.py --remediate-dry-run \
  --from-report /tmp/cis-sarif-fr/sample_report.json \
  --remediation-format diff \
  --remediation-output /tmp/cis-sarif-fr/plan.diff
```

Résultat attendu : `plan.diff` contient le plan de modification sans aucune exécution sur une base réelle. Changez `--remediation-format` pour `sql`, `shell`, `ansible` ou `json` selon votre outillage.

## Étape 3 — Valider le format SARIF v2.1.0

Convertissez et vérifiez le schéma SARIF avec la bibliothèque standard :

```bash
python3 -c "import json, sarif_exporter; doc = sarif_exporter.build_sarif_from_audit('mariadb106', [], tool_version='2.10.0'); errs = sarif_exporter.validate_sarif_document(doc); print('SARIF errors:', errs)"
```

Résultat attendu : `SARIF errors: []`.

## Nettoyage

```bash
rm -rf /tmp/cis-sarif-fr
```

## Aller plus loin

- Consultez les [Guides pratiques](../02-guides-pratiques/index.md) pour intégrer SARIF dans GitHub Actions.
- Vérifiez les options exactes dans la [Référence](../03-reference/index.md) et l'[Architecture PSL](../04-explications/index.md).
- Retour à l'[Accueil FR](../index.md).
