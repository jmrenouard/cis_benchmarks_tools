# 📋 Rapport de Justification des Contrôles Manuels - MongoDB Benchmark CIS

> **Version Suite** : `v2.3.0`  
> **Périmètre** : CIS MongoDB 7 & 8 Benchmarks

#### 🔴 Contrôle 2.1.1 - Politique de sauvegarde en place
- **Raison** : Validation des procédures de sauvegardes à chaud (mongodump, Ops Manager, Cloud Manager, LVM snapshot).
- **Commande d'inspection** : `crontab -l 2>/dev/null | grep -E 'mongodump|ops-manager' || echo 'AUCUNE_SAUVEGARDE_PLANIFIEE'`
- **Procédure** : Inspecter la planification des sauvegardes et le paramétrage d'oplog tailing.
