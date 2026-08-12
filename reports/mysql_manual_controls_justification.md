# 📋 Rapport de Justification des Contrôles Manuels - MySQL Benchmark CIS

> **Version Suite** : `v2.3.0`  
> **Périmètre** : CIS MySQL 8.0, 8.4 & 9.7 Benchmarks  
> **Objectif** : Documenter les contrôles nécessitant une vérification humaine/organisationnelle, les raisons de la non-automatisation à 100%, la commande d'inspection automatique et la procédure pas-à-pas.

---

## 📊 Synthèse des Contrôles Manuels Obligatoires

#### 🔴 Contrôle 2.1.1 - Politique de sauvegarde en place
- **Raison** : Nécessite la revue de documents d'entreprise (SLA, RPO, RTO) et de processus d'ordonnancement externes (Veeam, Ansible, Cron).
- **Commande d'inspection** : `crontab -l 2>/dev/null | grep -E 'mysqldump|mysqlbackup' || echo 'AUCUNE_SAUVEGARDE_PLANIFIEE'`
- **Procédure** : Inspecter les tâches planifiées et valider le document officiel de sauvegarde.

#### 🔴 Contrôle 2.1.2 - Validation des sauvegardes (Tests de Restauration)
- **Raison** : La validité d'une sauvegarde nécessite un test de restauration physique sur environnement hors-production.
- **Commande d'inspection** : `ls -lh /var/backups/mysql/ 2>/dev/null || echo 'VÉRIFIER_REPERTOIRE'`
- **Procédure** : Examiner le dernier procès-verbal de test de restauration et vérifier l'intégrité des tables.

#### 🔴 Contrôle 2.1.3 - Sécuriser les identifiants de sauvegarde
- **Raison** : Les credentials peuvent résider dans des coffres-forts réseau (Vault, CyberArk).
- **Commande d'inspection** : `ls -ld /root/.my.cnf 2>/dev/null`
- **Procédure** : S'assurer que `.my.cnf` a les permissions 600 et que les mots de passe sont chiffrés.

#### 🔴 Contrôle 2.1.6 - Plan de reprise d'activité (DR Plan)
- **Raison** : Document organisationnel décrivant l'architecture de haute disponibilité (InnoDB Cluster, Replica).
- **Commande d'inspection** : `mysql -N -B -e "SHOW REPLICA STATUS\G" 2>/dev/null || echo 'PAS_DE_RÉPLICATION'`
- **Procédure** : Consulter la documentation DR et valider les procédures de basculement.

#### 🔴 Contrôle 2.2 - Dédier la machine à MySQL
- **Raison** : Évaluation contextuelle de la colocalisation d'applications tierces.
- **Commande d'inspection** : `ps aux | grep -v -E 'root|mysql|systemd|ssh|grep' | head -n 20`
- **Procédure** : S'assurer qu'aucun serveur applicatif majeur (Apache/Nginx/SGDB) ne partage le serveur.
