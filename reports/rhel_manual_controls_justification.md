# 📋 Rapport de Justification des Contrôles Manuels - Red Hat Enterprise Linux (RHEL) Benchmark CIS

> **Version Suite** : `v2.3.0`  
> **Périmètre** : CIS Red Hat Enterprise Linux 8, 9 & 10 Benchmarks

#### 🔴 Contrôle 1.1 - Partitionnement physique dédié (/tmp, /var, /var/log, /var/log/audit, /home)
- **Raison** : Validation de la politique d'isolation disque système et des besoins applicatifs.
- **Commande d'inspection** : `df -hP | grep -E '/tmp|/var|/home'`
- **Procédure** : Inspecter le schéma de partitionnement physique avec les équipes d'infrastructure.

#### 🔴 Contrôle 6.1 - Politique de mise à jour des packages (Yum / Dnf)
- **Raison** : Matrice de mise à jour et validation des dépôts Satellite / RHUI.
- **Commande d'inspection** : `dnf check-update --security 2>/dev/null || echo 'CHECK_SECURITY_ERR'`
- **Procédure** : Valider les fenêtres de maintenance et les répertoires de paquets Red Hat.
