# 📋 Rapport de Justification des Contrôles Manuels - MariaDB Benchmark CIS

> **Version Suite** : `v2.2.0`  
> **Périmètre** : CIS MariaDB 10.6 & 10.11 Benchmarks  
> **Objectif** : Documenter les contrôles nécessitant une vérification humaine/organisationnelle, les raisons de la non-automatisation à 100%, la commande d'inspection automatique fournie par l'outil et la procédure pas-à-pas pour l'auditeur.

---

## 📊 Synthèse des Contrôles Manuels Obligatoires

Les contrôles ci-dessous ne peuvent pas être entièrement automatisés de manière déterministe car ils requièrent l'examen de documents de politique organisationnelle, d'infrastructures physiques hors-ligne ou de processus humains.

---

### Catégorie 2 : Installation et Planification

#### 🔴 Contrôle 2.1.1 - Politique de sauvegarde en place
- **Raison de la vérification manuelle** : L'existence d'une politique de sauvegarde formalisée implique la revue de documents d'entreprise (SLA, RPO, RTO) et de procédures d'ordonnancement externes (Veeam, Ansible, Cron, etc.).
- **Commande d'inspection automatique** : `crontab -l 2>/dev/null | grep -E 'mariabackup|mysqldump|xtrabackup' || echo 'AUCUNE_SAUVEGARDE_PLANIFIEE'`
- **Procédure de vérification pas-à-pas** :
  1. Inspecter la présence de crons ou de jobs d'ordonnancement réseau.
  2. Valider le document formalisé de politique de sauvegarde avec l'équipe d'exploitation.
  3. Confirmer que la fréquence couvre les exigences de RPO.

#### 🔴 Contrôle 2.1.2 - Validation des sauvegardes (Tests de Restauration)
- **Raison de la vérification manuelle** : Un fichier de sauvegarde ne garantit pas la restaurabilité des données sans un test de restauration réel sur un serveur hors-production.
- **Commande d'inspection automatique** : `ls -lh /var/backups/mariadb/ /var/lib/mariabackup/ 2>/dev/null || echo 'VÉRIFIER_REPERTOIRE_SAUVEGARDE'`
- **Procédure de vérification pas-à-pas** :
  1. Identifier les derniers rapports d'essais de restauration.
  2. Vérifier la date du dernier test de restauration effectué avec succès.
  3. S'assurer que le processus de validation inclut un contrôle d'intégrité de la base (`CHECK TABLE`).

#### 🔴 Contrôle 2.1.3 - Sécuriser les identifiants de sauvegarde
- **Raison de la vérification manuelle** : Les identifiants peuvent être stockés dans des coffres-forts (Vault, CyberArk) ou des variables d'environnement externes à la machine auditée.
- **Commande d'inspection automatique** : `ls -ld /etc/mysql/debian.cnf /root/.my.cnf 2>/dev/null | awk '{print $1, $3, $4, $9}'`
- **Procédure de vérification pas-à-pas** :
  1. Inspecter les fichiers de configuration de sauvegarde `.my.cnf`.
  2. S'assurer que les permissions sont restreintes à `600` et attribuées à `root` ou `mysql`.
  3. Confirmer l'absence de mots de passe en clair dans les scripts bash.

#### 🔴 Contrôle 2.1.4 - Sécuriser les fichiers de sauvegarde (Chiffrement au repos)
- **Raison de la vérification manuelle** : Le chiffrement peut être géré par le stockage sous-jacent (SAN/NAS chiffré, AWS KMS) non décelable par une simple requête locale.
- **Commande d'inspection automatique** : `file /var/backups/mariadb/* 2>/dev/null | head -n 5`
- **Procédure de vérification pas-à-pas** :
  1. Vérifier si les sauvegardes utilisent `mariabackup --encrypt` ou `gpg`/`openssl`.
  2. Examiner la configuration du stockage externe pour confirmer le chiffrement au repos (AES-256).

#### 🔴 Contrôle 2.1.6 - Plan de reprise d'activité (Disaster Recovery Plan)
- **Raison de la vérification manuelle** : Un plan DR est un document organisationnel global incluant des basculements de sites, Galera Cluster ou réplication hors-site.
- **Commande d'inspection automatique** : `mariadb -N -B -e "SHOW SLAVE STATUS\G" 2>/dev/null | grep -E 'Master_Host|Slave_IO_Running|Slave_SQL_Running' || echo 'REPLICATION_NON_CONFIGURÉE'`
- **Procédure de vérification pas-à-pas** :
  1. Consulter le document officiel du plan de reprise d'activité (PCA/PRA).
  2. Confirmer la présence de nœuds de réplication sur un second centre de données.
  3. Vérifier les dates des derniers exercices de basculement.

#### 🔴 Contrôle 2.1.7 - Sauvegarde des fichiers de configuration et matériel cryptographique
- **Raison de la vérification manuelle** : La sauvegarde des fichiers de configuration (`mariadb.cnf`) et des clés SSL (`server-key.pem`) dépend des règles d'inclusion du logiciel de sauvegarde.
- **Commande d'inspection automatique** : `ls -l /etc/mysql/mariadb.conf.d/ /etc/mysql/ssl/ 2>/dev/null`
- **Procédure de vérification pas-à-pas** :
  1. Vérifier la liste des répertoires inclus dans la sauvegarde système.
  2. S'assurer que `/etc/mysql/` et les certificats TLS/SSL sont inclus.

#### 🔴 Contrôle 2.2 - Dédier la machine à l'instance MariaDB
- **Raison de la vérification manuelle** : L'évaluation de la colocalisation d'applications nécessite une analyse contextuelle des services métier exécutés sur le serveur.
- **Commande d'inspection automatique** : `ps aux | grep -v -E 'root|mysql|systemd|ssh|grep' | head -n 20`
- **Procédure de vérification pas-à-pas** :
  1. Analyser la liste des processus actifs.
  2. Vérifier qu'aucun serveur Web (Apache/Nginx) ou autre SGDB ne tourne sur le même serveur physique/virtuel.

#### 🔴 Contrôle 2.3 - Ne pas spécifier de mots de passe en ligne de commande
- **Raison de la vérification manuelle** : Les mots de passe peuvent être transmis temporairement par des sous-processus ou des tâches crontab applicatives.
- **Commande d'inspection automatique** : `ps -ef | grep -E 'mysql|mariadb' | grep -v grep | grep -E '\-p[^ ]'`
- **Procédure de vérification pas-à-pas** :
  1. Inspecter l'historique des processus et la crontab.
  2. S'assurer qu'aucun script n'invoque `mysql -pPASSWORD`.

#### 🔴 Contrôle 2.5 - S'assurer que le matériel cryptographique est unique et non par défaut
- **Raison de la vérification manuelle** : Nécessite la vérification de l'autorité de certification (CA) et de la date d'émission des certificats X.509.
- **Commande d'inspection automatique** : `mariadb -N -B -e "SHOW VARIABLES LIKE 'ssl_key';" 2>/dev/null | awk '{print $2}' | xargs -I{} openssl x509 -in {} -subject -issuer -noout 2>/dev/null`
- **Procédure de vérification pas-à-pas** :
  1. Inspecter le sujet et l'émetteur du certificat TLS.
  2. Vérifier que le certificat n'est pas le certificat auto-généré par défaut du paquetier.

#### 🔴 Contrôle 2.7 - Verrouiller les comptes inutilisés
- **Raison de la vérification manuelle** : La définition d'un compte "inutilisé" ou "dormant" dépend des mouvements de personnel RH et des applications métier.
- **Commande d'inspection automatique** : `mariadb -N -B -e "SELECT user, host, account_locked FROM mysql.user WHERE account_locked='N';" 2>/dev/null`
- **Procédure de vérification pas-à-pas** :
  1. Comparer la liste des utilisateurs actifs avec l'annuaire de l'entreprise.
  2. Verrouiller les comptes sans propriétaire actif via `ALTER USER 'user'@'host' ACCOUNT LOCK;`.

---

### Catégorie 4 : Général

#### 🔴 Contrôle 4.1 - S'assurer que les derniers correctifs de sécurité sont appliqués
- **Raison de la vérification manuelle** : L'application des correctifs nécessite de croiser la version exacte installée avec la matrice de vulnérabilités CVE de l'éditeur.
- **Commande d'inspection automatique** : `mariadb -N -B -e "SELECT @@version;" 2>/dev/null`
- **Procédure de vérification pas-à-pas** :
  1. Relever la version exacte retournée.
  2. Consulter les Release Notes MariaDB relatives à la branche (10.6 / 10.11).
  3. Confirmer la mise à jour vers le dernier package de maintenance.
