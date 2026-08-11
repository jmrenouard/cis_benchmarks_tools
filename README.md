# CIS Benchmarks Tools

> Suite d'outils d'audit automatisés pour les benchmarks CIS (Center for Internet Security) appliqués aux bases de données.

## 📋 Vue d'ensemble

Ce projet fournit des scripts Python d'audit automatisé conformes aux recommandations CIS Benchmarks pour les principales bases de données. Chaque script génère un rapport HTML détaillé avec :

- ✅ Score global de conformité
- 📊 Graphiques par catégorie (Chart.js)
- 🔍 Détails de chaque recommandation (test, résultat, remédiation)
- 📝 Distinction entre contrôles automatisés et manuels

## 🗄️ Bases de données supportées

### MariaDB

| Version | Script d'audit | Dockerfile | CIS Benchmark | Nb Contrôles |
|---------|---------------|------------|----------------|-------------|
| 10.6 | [`audit_cis_mariadb_106.py`](audit_cis_mariadb_106.py) | [`Dockerfile_mariadb106`](Dockerfile_mariadb106) | v1.3.0 | 74 |
| 10.11 | [`audit_cis_mariadb_1011.py`](audit_cis_mariadb_1011.py) | [`Dockerfile_mariadb1011`](Dockerfile_mariadb1011) | v1.0.0 | 75 |

### MySQL

| Version | Script d'audit | Dockerfile | CIS Benchmark | Nb Contrôles |
|---------|---------------|------------|----------------|-------------|
| 8.0 Enterprise | [`audit_cis_mysql_80.py`](audit_cis_mysql_80.py) | [`Dockerfile_mysql80`](Dockerfile_mysql80) | v1.5.0 | ~70 |
| 8.4 Community | [`audit_cis_mysql_community_84.py`](audit_cis_mysql_community_84.py) | [`Dockerfile_mysql_community_84`](Dockerfile_mysql_community_84) | v1.1.0 | ~80 |
| 8.4 Enterprise | [`audit_cis_mysql_enterprise_84.py`](audit_cis_mysql_enterprise_84.py) | [`Dockerfile_mysql_enterprise_84`](Dockerfile_mysql_enterprise_84) | v1.1.0 | ~80 |
| 9.7 Community | [`audit_cis_mysql_community_97.py`](audit_cis_mysql_community_97.py) | [`Dockerfile_mysql_community_97`](Dockerfile_mysql_community_97) | v1.0.0 | ~80 |
| 9.7 Enterprise | [`audit_cis_mysql_enterprise_97.py`](audit_cis_mysql_enterprise_97.py) | [`Dockerfile_mysql_enterprise_97`](Dockerfile_mysql_enterprise_97) | v1.0.0 | ~80 |

### PostgreSQL

| Version | Script d'audit | Dockerfile | CIS Benchmark | Nb Contrôles |
|---------|---------------|------------|----------------|-------------|
| 16 | [`audit_cis_postgresql_16.py`](audit_cis_postgresql_16.py) | [`Dockerfile_postgresql16`](Dockerfile_postgresql16) | v1.1.0 | ~80 |
| 17 | [`audit_cis_postgresql_17.py`](audit_cis_postgresql_17.py) | [`Dockerfile_postgresql17`](Dockerfile_postgresql17) | v1.1.0 | ~80 |
| 18 | [`audit_cis_postgresql_18.py`](audit_cis_postgresql_18.py) | [`Dockerfile_postgresql18`](Dockerfile_postgresql18) | v1.0.0 | ~80 |

### MongoDB

| Version | Script d'audit | Dockerfile | CIS Benchmark | Nb Contrôles |
|---------|---------------|------------|----------------|-------------|
| 7 | [`audit_cis_mongodb_7.py`](audit_cis_mongodb_7.py) | [`Dockerfile_mongodb7`](Dockerfile_mongodb7) | v1.0.0 | ~22 |
| 8 | [`audit_cis_mongodb_8.py`](audit_cis_mongodb_8.py) | [`Dockerfile_mongodb8`](Dockerfile_mongodb8) | v1.0.0 | ~22 |

### Apache Cassandra

| Version | Script d'audit | Dockerfile | CIS Benchmark | Nb Contrôles |
|---------|---------------|------------|----------------|-------------|
| 4.0 | [`audit_cis_cassandra_40.py`](audit_cis_cassandra_40.py) | [`Dockerfile_cassandra40`](Dockerfile_cassandra40) | v1.3.0 | 18 |
| 4.1 | [`audit_cis_cassandra_41.py`](audit_cis_cassandra_41.py) | [`Dockerfile_cassandra41`](Dockerfile_cassandra41) | v1.0.0 | 18 |
| 5.0 | [`audit_cis_cassandra_50.py`](audit_cis_cassandra_50.py) | [`Dockerfile_cassandra50`](Dockerfile_cassandra50) | v1.1.0 | 18 |

## 🚀 Utilisation rapide

### Prérequis

- Python 3.8+
- Docker (pour les environnements de test)
- Accès réseau pour télécharger les images Docker

### Exécution avec Docker (recommandé)

```bash
# 1. Construire l'image Docker
docker build -f Dockerfile_mariadb106 -t cis_mariadb106:audit .

# 2. Lancer le conteneur
docker run -d --name cis_mariadb106_audit cis_mariadb106:audit

# 3. Attendre l'initialisation du service (~30s)
sleep 30

# 4. Exécuter l'audit
docker exec cis_mariadb106_audit python3 /datas/audit_cis_mariadb_106.py

# 5. Récupérer le rapport
docker cp cis_mariadb106_audit:/datas/rapport_cis_mariadb_106.html .

# 6. Nettoyer
docker rm -f cis_mariadb106_audit
```

### Exécution directe

```bash
# Sur un serveur MariaDB 10.6 existant
python3 audit_cis_mariadb_106.py

# Le rapport HTML est généré dans le répertoire courant
# Ouvrir rapport_cis_mariadb_106.html dans un navigateur
```

## 📁 Structure du projet

```
cis_benchmarks_tools/
├── README.md                          # Ce fichier
├── audit_cis_mariadb_106.py           # Audit MariaDB 10.6
├── audit_cis_mariadb_1011.py          # Audit MariaDB 10.11
├── audit_cis_mysql_80.py              # Audit MySQL 8.0
├── audit_cis_mysql_community_84.py    # Audit MySQL Community 8.4
├── audit_cis_mysql_enterprise_84.py   # Audit MySQL Enterprise 8.4
├── audit_cis_mysql_community_97.py    # Audit MySQL Community 9.7
├── audit_cis_mysql_enterprise_97.py   # Audit MySQL Enterprise 9.7
├── audit_cis_postgresql_16.py         # Audit PostgreSQL 16
├── audit_cis_postgresql_17.py         # Audit PostgreSQL 17
├── audit_cis_postgresql_18.py         # Audit PostgreSQL 18
├── audit_cis_mongodb_7.py             # Audit MongoDB 7
├── audit_cis_mongodb_8.py             # Audit MongoDB 8
├── audit_cis_cassandra_40.py          # Audit Cassandra 4.0
├── audit_cis_cassandra_41.py          # Audit Cassandra 4.1
├── audit_cis_cassandra_50.py          # Audit Cassandra 5.0
├── Dockerfile_mariadb106              # Env test MariaDB 10.6
├── Dockerfile_mariadb1011             # Env test MariaDB 10.11
├── Dockerfile_mysql80                 # Env test MySQL 8.0
├── Dockerfile_mysql_community_84      # Env test MySQL Community 8.4
├── Dockerfile_mysql_enterprise_84     # Env test MySQL Enterprise 8.4
├── Dockerfile_mysql_community_97      # Env test MySQL Community 9.7
├── Dockerfile_mysql_enterprise_97     # Env test MySQL Enterprise 9.7
├── Dockerfile_postgresql16            # Env test PostgreSQL 16
├── Dockerfile_postgresql17            # Env test PostgreSQL 17
├── Dockerfile_postgresql18            # Env test PostgreSQL 18
├── Dockerfile_mongodb7                # Env test MongoDB 7
├── Dockerfile_mongodb8                # Env test MongoDB 8
├── Dockerfile_cassandra40             # Env test Cassandra 4.0
├── Dockerfile_cassandra41             # Env test Cassandra 4.1
├── Dockerfile_cassandra50             # Env test Cassandra 5.0
├── scripts/
│   ├── start_mariadb.sh               # Script de démarrage MariaDB
│   ├── start_mysql.sh                 # Script de démarrage MySQL
│   └── start_postgresql.sh            # Script de démarrage PostgreSQL
└── CIS_DATA/                          # Spécifications CIS (PDF/MD)
```

## 🔧 Architecture des scripts

Chaque script d'audit suit la même architecture :

1. **Configuration** : Commande CLI de la base de données, chemin du fichier de configuration
2. **RECOMMENDATIONS_DATA** : Liste structurée de toutes les recommandations CIS
   - `category` : Catégorie CIS (ex: "1 Installation et Patching")
   - `number` : Numéro de la recommandation (ex: "1.1")
   - `name` : Description en français
   - `type` : `Automated` ou `Manual`
   - `test_procedure` : Commande shell à exécuter
   - `expected_output` : Résultat attendu (regex, valeur exacte, etc.)
   - `remediation` : Correction à appliquer
3. **HTML_TEMPLATE** : Modèle HTML avec graphiques Chart.js
4. **Fonctions d'exécution** : Exécution des tests, évaluation, génération du rapport

### Types de validation

| Type | Description |
|------|------------|
| `stdout_equals` | La sortie doit correspondre exactement |
| `stdout_not_equals` | La sortie ne doit pas correspondre |
| `stdout_contains` | La sortie doit contenir la valeur |
| `stdout_not_contains` | La sortie ne doit pas contenir la valeur |
| `stdout_regex_match` | La sortie doit correspondre au pattern regex |
| `stdout_not_empty` | La sortie ne doit pas être vide |
| `returncode_zero` | Le code de retour doit être 0 |
| `all_lines_match_regex` | Toutes les lignes doivent correspondre |

## 📊 Rapports

Les rapports HTML générés incluent :

- **Score global** avec graphique camembert
- **Score par catégorie** avec graphiques en barres
- **Tableau détaillé** pour chaque recommandation :
  - Statut : ✅ Pass / ❌ Fail / ⚠️ Manual / 🔘 N/A
  - Commande exécutée
  - Sortie obtenue
  - Remédiation proposée

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feat/new-benchmark`)
3. Commit les changements (`git commit -am 'feat: Add new benchmark'`)
4. Push la branche (`git push origin feat/new-benchmark`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est distribué sous licence MIT.

## 📚 Références

- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
- [MariaDB Security](https://mariadb.com/kb/en/securing-mariadb/)
- [MySQL Security](https://dev.mysql.com/doc/refman/8.4/en/security.html)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/security.html)
- [MongoDB Security](https://www.mongodb.com/docs/manual/security/)
- [Cassandra Security](https://cassandra.apache.org/doc/latest/cassandra/operating/security.html)