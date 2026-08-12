# 📋 Rapport de Justification des Contrôles Manuels - Cassandra Benchmark CIS

> **Version Suite** : `v2.3.0`  
> **Périmètre** : CIS Apache Cassandra 4.0, 4.1 & 5.0 Benchmarks

#### 🔴 Contrôle 2.1.1 - Politique de sauvegarde des SStables & Commitlogs
- **Raison** : Stratégie de snapshot nodetool (`nodetool snapshot`) et d'archivage des commitlogs.
- **Commande d'inspection** : `crontab -l 2>/dev/null | grep -E 'nodetool|medusa' || echo 'AUCUNE_SAUVEGARDE_PLANIFIEE'`
- **Procédure** : Inspecter l'automatisation des snapshots nodetool et Medusa.
