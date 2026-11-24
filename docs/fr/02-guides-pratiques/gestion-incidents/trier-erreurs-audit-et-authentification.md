# Trier les erreurs d'audit et d'authentification

Ce guide classe les échecs retournés par `CommandFailureClassifier` pour séparer les erreurs d'environnement des écarts CIS.

## Prérequis

- Gardez la sortie CLI ou le rapport JSON de l'audit en échec.
- Consultez la table des catégories dans la [matrice d'erreurs (EN)](../../../03-reference/troubleshooting-codes/error-and-alert-matrix.md).

## Procédure

1. Examinez le code de sortie retourné par `audit_cis.py`.


2. Si la catégorie est `TIMEOUT` ou `CONNECTION_ERROR`, testez l'accès réseau et le port cible.

```bash
ssh -o ConnectTimeout=5 -p 22 admin@db-host "echo ok"
```

3. Si la catégorie est `MISSING_BINARY` (`rc == 127`), installez le client manquant ou vérifiez `$PATH`.

4. Si la catégorie est `AUTH_FAILURE`, vérifiez la variable `CIS_DB_PASSWORD` et les droits du fichier `.my.cnf` ou `.pgpass`.

5. **ATTENTION :** Corrigez la configuration d'accès avant de redémarrer l'audit sur une base active. Des tentatives répétées déclenchent le verrouillage du compte de service.

6. Si la catégorie est `PERMISSION_DENIED` (`rc == 126`), lancez avec `--sudo` lorsque la politique système l'autorise.

7. Si la catégorie est `SYNTAX_ERROR`, exécutez `python3 audit_cis.py --help` et corrigez les options CLI.

## Vérification

1. Lancez de nouveau l'audit sur la cible corrigée et vérifiez un code de retour égal à `0`.
2. Confirmez que le rapport JSON ne signale plus de catégorie d'erreur d'environnement.

## Retour arrière

1. Si un changement temporaire de `$PATH` ou de profil shell bloque un autre outil, ouvrez une nouvelle session.
2. Restaurez les permissions initiales des fichiers de configuration modifiés (`chmod 600 ~/.my.cnf`).

---

Références : [Guides pratiques](../index.md) · [Référence FR](../../03-reference/index.md) · [Explications FR](../../04-explications/index.md) · [Matrice d'erreurs (EN)](../../../03-reference/troubleshooting-codes/error-and-alert-matrix.md)
