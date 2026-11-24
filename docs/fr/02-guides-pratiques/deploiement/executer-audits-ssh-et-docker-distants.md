# Exécuter des audits SSH et Docker distants

Ce guide décrit l'audit CIS en lecture seule par SSH vers un hôte distant ou un conteneur Docker.

## Prérequis

- Installez Python `3.10` ou une version plus récente sur le poste contrôleur.
- Configurez une clé SSH avec un accès lecture seule sur la machine cible.
- Si vous ciblez un conteneur distant, vérifiez le droit d'accès au socket Docker.

## Procédure

1. Vérifiez l'accès SSH vers la machine distante avant tout audit.

```bash
ssh -i ~/.ssh/id_ed25519 -p 22 admin@db-host "docker --version"
```

2. **ATTENTION :** Limitez les droits SSH du compte de supervision au strict nécessaire. Un compte `root` sans restriction expose le serveur cible aux erreurs de manipulation.

3. Exécutez l'audit CIS MariaDB 10.6 sur le conteneur distant avec SSH.

```bash
python3 audit_cis.py -t mariadb106 -m ssh -r admin@db-host \
  --ssh-port 22 -i ~/.ssh/id_ed25519 -c mariadb-prod -l fr \
  -f html -o reports/mariadb_remote.html -j reports/mariadb_remote.json
```

4. Si le moteur exige une élévation locale sur l'hôte distant, ajoutez `--sudo`.

```bash
python3 audit_cis.py -t rhel9 -m ssh -r admin@linux-host --sudo \
  -l fr -f json -o reports/rhel9_remote.json
```

## Vérification

1. Vérifiez le code de retour et l'absence de fichier temporaire sur l'hôte distant.
2. Ouvrez `reports/mariadb_remote.json` et confirmez la présence des résultats.

## Retour arrière

1. Supprimez les rapports locaux si vous voulez annuler la collecte.

```bash
rm -f reports/mariadb_remote.html reports/mariadb_remote.json reports/rhel9_remote.json
```

2. Si vous avez ajouté un compte SSH temporaire, révoquez sa clé publique dans `~/.ssh/authorized_keys`.

---

Références : [Guides pratiques](../index.md) · [Référence FR](../../03-reference/index.md) · [Explications FR](../../04-explications/index.md) · [Matrice CLI (EN)](../../../03-reference/cli-and-scripts/cli-flags-and-exit-codes.md)
