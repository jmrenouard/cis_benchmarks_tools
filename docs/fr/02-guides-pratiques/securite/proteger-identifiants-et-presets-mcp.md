# Protéger les identifiants et exécuter les presets MCP

Ce guide verrouille la transmission des secrets et encadre les presets en lecture seule du contrat MCP.

## Prérequis

- Consultez le fichier [mcp_api_executor_presets.json](../../../../conf/mcp_api_executor_presets.json).
- Utilisez Python `3.10` ou une version plus récente.

## Procédure

1. **ATTENTION :** Ne passez jamais un mot de passe avec `-p` ou `--db-password` en ligne de commande. La table des processus expose les arguments en clair aux utilisateurs locaux.

2. Injectez le secret de base avec la variable d'environnement `CIS_DB_PASSWORD` ou avec `--defaults-file`.

```bash
export CIS_DB_PASSWORD="votre_secret_temporaire"
chmod 600 ~/.my.cnf
python3 audit_cis.py -t mysql80 --defaults-file ~/.my.cnf -f json -o reports/mysql80.json
```

3. Effacez la variable de session juste après la fin de l'audit.

```bash
unset CIS_DB_PASSWORD
```

4. Pour une automatisation agentique, sélectionnez uniquement les presets `read_only` (`cis_list_targets`, `cis_audit_json`, `cis_audit_sarif`, `cis_remediate_dry_run`).

5. Refusez tout preset ou appel qui contient les options interdites `--apply`, `--force`, `--sync-cis`, `--all` ou `--auto-detect`.

## Vérification

1. Vérifiez l'absence de secret en clair dans `reports/mysql80.json` grâce au filtre `SecretSanitizer`.
2. Vérifiez l'état `read_only: true` dans `conf/mcp_api_executor_presets.json`.

## Retour arrière

1. Exécutez `unset CIS_DB_PASSWORD` si la variable reste active dans le shell courant.
2. Si un mot de passe a fui dans l'historique shell ou les journaux, révoquez le secret immédiatement.

---

Références : [Guides pratiques](../index.md) · [Référence FR](../../03-reference/index.md) · [Explications FR](../../04-explications/index.md) · [Contrat MCP (EN)](../../../MCP_API_EXECUTOR_CONTRACT.md)
