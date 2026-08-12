# 📋 Rapport de Justification des Contrôles Manuels - PostgreSQL Benchmark CIS

> **Version Suite** : `v2.3.0`  
> **Périmètre** : CIS PostgreSQL 16, 17 & 18 Benchmarks  
> **Objectif** : Documenter les contrôles nécessitant une vérification humaine/organisationnelle, la commande d'inspection et la procédure d'audit.

---

## 📊 Synthèse des Contrôles Manuels Obligatoires

#### 🔴 Contrôle 2.1.1 - Politique de sauvegarde en place
- **Raison** : Validation des SLA organisationnels et des scripts d'archivage WAL (pg_backrest, Barman, WAL-G).
- **Commande d'inspection** : `crontab -l 2>/dev/null | grep -E 'pg_dump|pg_backrest|barman' || echo 'AUCUNE_SAUVEGARDE_PLANIFIEE'`
- **Procédure** : Inspecter l'archivage WAL et valider les fenêtres de restauration RPO.

#### 🔴 Contrôle 2.1.2 - Validation des sauvegardes (Tests de Restauration PITR)
- **Raison** : La restaurabilité des fichiers WAL nécessite un essai de restauration sur un cluster de qualification.
- **Commande d'inspection** : `ls -lh /var/lib/pgsql/backups/ 2>/dev/null || echo 'VÉRIFIER_REPERTOIRE'`
- **Procédure** : Vérifier le dernier rapport de test PITR et valider l'intégrité des bases.

#### 🔴 Contrôle 2.1.6 - Plan de reprise d'activité (DR Plan)
- **Raison** : Stratégie globale de réplication (Streaming Replication, Patroni, pg_auto_failover).
- **Commande d'inspection** : `psql -U postgres -c "SELECT * FROM pg_stat_replication;" 2>/dev/null || echo 'PAS_DE_RÉPLICATION'`
- **Procédure** : Valider le document DR et la présence de standby répliqués.
