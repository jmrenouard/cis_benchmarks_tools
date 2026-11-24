# Explications architecturales (FR)

Architecture en 4 couches 100 % Python Standard Library (`PSL ONLY`) sans dépendances tierces :

1. **CLI (`audit_cis.py`)** : analyse les arguments et assemble la suite autonome zéro-dépendance.
2. **Orchestration (`audit_orchestrator.py`)** : gère `--auto-detect`, `--all`, horodatage et diagnostics.
3. **Transports (`execution_drivers.py`, `docker_transport.py`)** : exécute en local, SSH (`--sudo`) ou Docker (`-c`).
4. **Moteurs & exports (`cis_core_engine.py`, `sarif_exporter.py`, `remediation_generator.py`)** : score pondéré, SVG hors ligne, SARIF v2.1.0 et plans `--remediate-dry-run`.

- [Architecture PSL 4 couches (EN)](../../04-explanation/architecture-overview/four-tier-psl-audit-architecture.md)
- [Vue d'ensemble complète (`README_fr.md`)](../../../README_fr.md)
- [Référence](../03-reference/index.md) · [Guides pratiques](../02-guides-pratiques/index.md) · [Accueil FR](../index.md)
