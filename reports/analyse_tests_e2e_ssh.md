# 📊 CIS Benchmarks Suite - Analyse Spécifique Mode SSH Remote (-m ssh)

> **Rapport d'Analyse E2E (Mode SSH Remote (-m ssh)) généré le** : `2026-08-12 22:20:16`  
> **Moteur d'Audit** : `CIS Benchmarks Tools Suite v2.0.0` (100% Python Standard Library - PSL ONLY)  
> **Mode d'Exécution** : 🌐 `SSH Remote`  
> **Périmètre** : 10 cibles d'audit évaluées dans ce mode

---

## 📈 Executive Dashboard (Mode SSH Remote (-m ssh))

| Cible / Benchmark | Mode | Date d'Exécution | Score Global | Total | Succès (PASS) | Échecs (FAIL) | Erreurs (ERROR) | Manuels (MANUAL) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MARIADB_1011** | 🌐 `SSH Remote` | 2026-08-12 15:00:14 | 🔴 `27.0%` | 75 | 8 | 27 | 0 | 40 |
| **MARIADB_106** | 🌐 `SSH Remote` | 2026-08-12 14:58:52 | 🔴 `27.0%` | 74 | 8 | 27 | 0 | 39 |
| **MYSQL_80** | 🌐 `SSH Remote` | 2026-08-12 15:01:28 | 🔴 `47.1%` | 70 | 2 | 9 | 0 | 59 |
| **MYSQL_COMMUNITY_84** | 🌐 `SSH Remote` | 2026-08-12 15:02:49 | 🔴 `42.9%` | 79 | 2 | 8 | 0 | 69 |
| **MYSQL_COMMUNITY_97** | 🌐 `SSH Remote` | 2026-08-12 15:05:20 | 🔴 `47.1%` | 70 | 2 | 9 | 0 | 59 |
| **MYSQL_ENTERPRISE_84** | 🌐 `SSH Remote` | 2026-08-12 15:04:03 | 🔴 `47.1%` | 70 | 2 | 9 | 0 | 59 |
| **MYSQL_ENTERPRISE_97** | 🌐 `SSH Remote` | 2026-08-12 15:06:36 | 🔴 `47.1%` | 70 | 2 | 9 | 0 | 59 |
| **POSTGRESQL_16** | 🌐 `SSH Remote` | 2026-08-12 15:07:28 | 🔴 `7.1%` | 71 | 2 | 26 | 0 | 43 |
| **POSTGRESQL_17** | 🌐 `SSH Remote` | 2026-08-12 15:08:18 | 🔴 `7.1%` | 71 | 2 | 26 | 0 | 43 |
| **POSTGRESQL_18** | 🌐 `SSH Remote` | 2026-08-12 15:09:11 | 🔴 `7.1%` | 71 | 2 | 26 | 0 | 43 |

### 📊 Statistiques Consolidées pour ce Mode

- **Nombre total de benchmarks évalués** : `10`
- **Nombre total de règles/contrôles vérifiés** : `721`
- **Score de conformité moyen** : `30.7%`
- **Contrôles en succès (`PASS`)** : `32` (4.4%)
- **Contrôles en échec (`FAIL`)** : `176` (24.4%)
- **Contrôles en erreur (`ERROR`)** : `0` (0.0%)
- **Contrôles manuels (`MANUAL`)** : `513` (71.2%)

---

## ❌ Registre Détaillé des Contrôles en Échec (`FAIL`) & Erreurs (`ERROR`) - Mode SSH Remote (-m ssh)

### 🛑 MARIADB_1011 (`27` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.2** | 🔴 FAIL | Utiliser un compte dédié et privilégié minimal pour MariaDB | 1. Configuration Système d'exploitation | `Stdout:` | Configurer le service MariaDB pour qu'il s'exécute sous un utilisateur dédié (ex: 'mysql') avec les  |
| **1.3** | 🔴 FAIL | Désactiver l'historique des commandes MariaDB | 1. Configuration Système d'exploitation | `Stdout:` | Supprimer les fichiers d'historique, créer un lien symbolique vers /dev/null, ou configurer MYSQL_HI |
| **1.4** | 🔴 FAIL | Vérifier que MYSQL_PWD n'est pas utilisé | 1. Configuration Système d'exploitation | `Stdout:` | Modifier les scripts/utilisateurs pour éviter MYSQL_PWD, utiliser des méthodes d'authentification sé |
| **1.5** | 🔴 FAIL | Désactiver l'accès interactif pour l'utilisateur MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Modifier le shell de l'utilisateur mysql pour utiliser /bin/false ou /sbin/nologin (ex: usermod -s / |
| **1.6** | 🔴 FAIL | Vérifier que MYSQL_PWD n'est pas dans les profils utilisateurs | 1. Configuration Système d'exploitation | `Stdout:` | Nettoyer les fichiers de login des utilisateurs pour supprimer MYSQL_PWD. |
| **2.1.5** | 🔴 FAIL | Point-in-Time Recovery | 2. Installation et Planification | `Stdout:` | Activer les binlogs, configurer binlog_expire_logs_seconds dans mariadb.cnf, tester les restauration |
| **2.6** | 🔴 FAIL | Assurer que password_lifetime <= 365 | 2. Installation et Planification | `Stdout:` | SET GLOBAL default_password_lifetime=365; |
| **2.10** | 🔴 FAIL | Limiter les versions TLS acceptées | 2. Installation et Planification | `Stdout:` | Configurer tls_version=TLSv1.2,TLSv1.3 dans mariadb.cnf. |
| **2.11** | 🔴 FAIL | Exiger des certificats côté client (X.509) | 2. Installation et Planification | `Stdout:` | ALTER USER '<user>'@'<host>' REQUIRE X509; |
| **2.12** | 🔴 FAIL | S'assurer que seuls les chiffrement approuvés sont utilisés | 2. Installation et Planification | `Stdout:` | Configurer ssl_cipher avec une liste de chiffrements approuvés dans mariadb.cnf. |
| **3.7** | 🔴 FAIL | Permissions sur les fichiers de clés SSL | 3. Permissions Fichiers | `Stdout:` | Restreindre l'accès aux clés privées (ex: chmod 600) et s'assurer que le propriétaire est mysql. |
| **3.9** | 🔴 FAIL | Permissions sur 'server_audit_file_path' | 3. Permissions Fichiers | `Stdout:` | Appliquer des permissions restrictives (ex: 640 ou 600). |
| **3.10** | 🔴 FAIL | Permissions sur les fichiers du plugin File Key Management | 3. Permissions Fichiers | `Stdout:` | Restreindre l'accès aux fichiers de clés de chiffrement (chmod 640). |
| **4.4** | 🔴 FAIL | Renforcer l'utilisation de 'local_infile' sur les clients MariaDB | 4. Général | `Stdout:` | Ajouter local-infile=0 à la section [mariadbd] et [client] du fichier de configuration MariaDB. |
| **4.6** | 🔴 FAIL | S'assurer que les liens symboliques sont désactivés | 4. Général | `Stdout:` | Ajouter skip-symbolic-links dans la section [mariadbd] du fichier mariadb.cnf. |
| **4.7** | 🔴 FAIL | S'assurer que 'secure_file_priv' est configuré correctement | 4. Général | `Stdout:` | Configurer secure_file_priv sur NULL (pour désactiver) ou sur un chemin spécifique dans mariadb.cnf. |
| **4.8** | 🔴 FAIL | S'assurer que sql_mode contient STRICT_ALL_TABLES | 4. Général | `Stdout:` | Ajouter STRICT_ALL_TABLES au paramètre sql_mode dans mariadb.cnf. |
| **4.9** | 🔴 FAIL | Activer le chiffrement des données au repos dans MariaDB | 4. Général | `Stdout:` | Configurer file_key_management plugin et innodb_encrypt_tables=ON dans mariadb.cnf. |
| **6.3** | 🔴 FAIL | log_warnings=2 | 6. Audit & Journalisation | `Stdout:` | Ajouter log_warnings=2 dans mariadb.cnf. |
| **6.4** | 🔴 FAIL | Activer la journalisation d'audit (server_audit) | 6. Audit & Journalisation | `Stdout:` | Installer et configurer le plugin server_audit : plugin_load_add=server_audit, server_audit_logging= |
| **6.5** | 🔴 FAIL | Interdire le déchargement du plugin d'audit | 6. Audit & Journalisation | `Stdout:` | Ajouter server_audit=FORCE_PLUS_PERMANENT dans mariadb.cnf. |
| **6.6** | 🔴 FAIL | Chiffrer les Binary et Relay Logs | 6. Audit & Journalisation | `Stdout:` | Ajouter encrypt_binlog=ON dans mariadb.cnf (nécessite un plugin de gestion de clés). |
| **7.1** | 🔴 FAIL | Désactiver mysql_old_password (old_passwords=OFF, secure_auth=ON) | 7. Authentification | `Stdout:` | Configurer old_passwords=0 et secure_auth=ON dans mariadb.cnf et redémarrer. |
| **7.2** | 🔴 FAIL | Aucun mot de passe dans la configuration globale | 7. Authentification | `Stdout:` | Utiliser des fichiers .my.cnf privés ou mysql_config_editor avec permissions restreintes. |
| **7.4** | 🔴 FAIL | Politique de complexité des mots de passe (simple_password_check) | 7. Authentification | `Stdout:` | Installer et configurer simple_password_check et cracklib_password_check. INSTALL SONAME 'simple_pas |
| **8.1** | 🔴 FAIL | Forcer SSL/TLS (require_secure_transport=ON et have_ssl=YES) | 8. Sécurité réseau | `Stdout:` | Configurer les certificats SSL/TLS, puis ajouter require_secure_transport=ON dans mariadb.cnf. |
| **8.2** | 🔴 FAIL | Exiger TLS côté utilisateur (ssl_type) | 8. Sécurité réseau | `Stdout:` | ALTER USER '<user>'@'<host>' REQUIRE SSL; ou REQUIRE X509; |

### 🛑 MARIADB_106 (`27` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.2** | 🔴 FAIL | Utiliser un compte dédié et privilégié minimal pour MariaDB | 1. Configuration Système d'exploitation | `Stdout:` | Configurer le service MariaDB pour qu'il s'exécute sous un utilisateur dédié (ex: 'mysql') avec les  |
| **1.3** | 🔴 FAIL | Désactiver l'historique des commandes MariaDB | 1. Configuration Système d'exploitation | `Stdout:` | Supprimer les fichiers d'historique, créer un lien symbolique vers /dev/null, ou configurer MYSQL_HI |
| **1.4** | 🔴 FAIL | Vérifier que MYSQL_PWD n'est pas utilisé | 1. Configuration Système d'exploitation | `Stdout:` | Modifier les scripts/utilisateurs pour éviter MYSQL_PWD, utiliser des méthodes d'authentification sé |
| **1.5** | 🔴 FAIL | Désactiver l'accès interactif pour l'utilisateur MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Modifier le shell de l'utilisateur mysql pour utiliser /bin/false ou /sbin/nologin (ex: usermod -s / |
| **1.6** | 🔴 FAIL | Vérifier que MYSQL_PWD n'est pas dans les profils utilisateurs | 1. Configuration Système d'exploitation | `Stdout:` | Nettoyer les fichiers de login des utilisateurs pour supprimer MYSQL_PWD. |
| **2.1.5** | 🔴 FAIL | Point-in-Time Recovery | 2. Installation et Planification | `Stdout:` | Activer les binlogs, configurer binlog_expire_logs_seconds dans mariadb.cnf, tester les restauration |
| **2.6** | 🔴 FAIL | Assurer que password_lifetime <= 365 | 2. Installation et Planification | `Stdout:` | SET GLOBAL default_password_lifetime=365; |
| **2.10** | 🔴 FAIL | Limiter les versions TLS acceptées | 2. Installation et Planification | `Stdout:` | Configurer tls_version=TLSv1.2,TLSv1.3 dans mariadb.cnf. |
| **2.11** | 🔴 FAIL | Exiger des certificats côté client (X.509) | 2. Installation et Planification | `Stdout:` | ALTER USER '<user>'@'<host>' REQUIRE X509; |
| **2.12** | 🔴 FAIL | S'assurer que seuls les chiffrement approuvés sont utilisés | 2. Installation et Planification | `Stdout:` | Configurer ssl_cipher avec une liste de chiffrements approuvés dans mariadb.cnf. |
| **3.7** | 🔴 FAIL | Permissions sur les fichiers de clés SSL | 3. Permissions Fichiers | `Stdout:` | Restreindre l'accès aux clés privées (ex: chmod 600) et s'assurer que le propriétaire est mysql. |
| **3.9** | 🔴 FAIL | Permissions sur 'server_audit_file_path' | 3. Permissions Fichiers | `Stdout:` | Appliquer des permissions restrictives (ex: 640 ou 600). |
| **3.10** | 🔴 FAIL | Permissions sur les fichiers du plugin File Key Management | 3. Permissions Fichiers | `Stdout:` | Restreindre l'accès aux fichiers de clés de chiffrement (chmod 640). |
| **4.4** | 🔴 FAIL | Renforcer l'utilisation de 'local_infile' sur les clients MariaDB | 4. Général | `Stdout:` | Ajouter local-infile=0 à la section [mariadbd] et [client] du fichier de configuration MariaDB. |
| **4.6** | 🔴 FAIL | S'assurer que les liens symboliques sont désactivés | 4. Général | `Stdout:` | Ajouter skip-symbolic-links dans la section [mariadbd] du fichier mariadb.cnf. |
| **4.7** | 🔴 FAIL | S'assurer que 'secure_file_priv' est configuré correctement | 4. Général | `Stdout:` | Configurer secure_file_priv sur NULL (pour désactiver) ou sur un chemin spécifique dans mariadb.cnf. |
| **4.8** | 🔴 FAIL | S'assurer que sql_mode contient STRICT_ALL_TABLES | 4. Général | `Stdout:` | Ajouter STRICT_ALL_TABLES au paramètre sql_mode dans mariadb.cnf. |
| **4.9** | 🔴 FAIL | Activer le chiffrement des données au repos dans MariaDB | 4. Général | `Stdout:` | Configurer file_key_management plugin et innodb_encrypt_tables=ON dans mariadb.cnf. |
| **6.3** | 🔴 FAIL | log_warnings=2 | 6. Audit & Journalisation | `Stdout:` | Ajouter log_warnings=2 dans mariadb.cnf. |
| **6.4** | 🔴 FAIL | Activer la journalisation d'audit (server_audit) | 6. Audit & Journalisation | `Stdout:` | Installer et configurer le plugin server_audit : plugin_load_add=server_audit, server_audit_logging= |
| **6.5** | 🔴 FAIL | Interdire le déchargement du plugin d'audit | 6. Audit & Journalisation | `Stdout:` | Ajouter server_audit=FORCE_PLUS_PERMANENT dans mariadb.cnf. |
| **6.6** | 🔴 FAIL | Chiffrer les Binary et Relay Logs | 6. Audit & Journalisation | `Stdout:` | Ajouter encrypt_binlog=ON dans mariadb.cnf (nécessite un plugin de gestion de clés). |
| **7.1** | 🔴 FAIL | Désactiver mysql_old_password (old_passwords=OFF, secure_auth=ON) | 7. Authentification | `Stdout:` | Configurer old_passwords=0 et secure_auth=ON dans mariadb.cnf et redémarrer. |
| **7.2** | 🔴 FAIL | Aucun mot de passe dans la configuration globale | 7. Authentification | `Stdout:` | Utiliser des fichiers .my.cnf privés ou mysql_config_editor avec permissions restreintes. |
| **7.4** | 🔴 FAIL | Politique de complexité des mots de passe (simple_password_check) | 7. Authentification | `Stdout:` | Installer et configurer simple_password_check et cracklib_password_check. INSTALL SONAME 'simple_pas |
| **8.1** | 🔴 FAIL | Forcer SSL/TLS (require_secure_transport=ON et have_ssl=YES) | 8. Sécurité réseau | `Stdout:` | Configurer les certificats SSL/TLS, puis ajouter require_secure_transport=ON dans mariadb.cnf. |
| **8.2** | 🔴 FAIL | Exiger TLS côté utilisateur (ssl_type) | 8. Sécurité réseau | `Stdout:` | ALTER USER '<user>'@'<host>' REQUIRE SSL; ou REQUIRE X509; |

### 🛑 MYSQL_80 (`9` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.2** | 🔴 FAIL | Utiliser un compte dédié et privilégié minimal pour MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Configurer le service MySQL pour qu'il s'exécute sous un utilisateur dédié (ex: 'mysql') avec les pr |
| **1.3** | 🔴 FAIL | Désactiver l'historique des commandes MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Supprimer les fichiers d'historique, créer un lien symbolique vers /dev/null, ou configurer MYSQL_HI |
| **1.4** | 🔴 FAIL | Vérifier que MYSQL_PWD n'est pas utilisé | 1. Configuration Système d'exploitation | `Stdout:` | Modifier les scripts/utilisateurs pour éviter MYSQL_PWD, utiliser mysql_config_editor ou authentific |
| **1.5** | 🔴 FAIL | Désactiver l'accès interactif pour l'utilisateur MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Modifier le shell de l'utilisateur mysql pour utiliser /bin/false ou /sbin/nologin (ex: usermod -s / |
| **1.6** | 🔴 FAIL | Vérifier que MYSQL_PWD n'est pas dans les profils utilisateurs | 1. Configuration Système d'exploitation | `Stdout:` | Nettoyer les fichiers de login des utilisateurs pour supprimer MYSQL_PWD. |
| **1.7** | 🔴 FAIL | Exécuter MySQL dans un environnement sandbox | 1. Configuration Système d'exploitation | `Stdout:` | Configurer chroot, utiliser un service systemd avec un utilisateur spécifique, ou déployer MySQL sou |
| **2.1.1** | 🔴 FAIL | Politique de sauvegarde en place | 2. Installation et Planification | `Stdout:` | Créer une politique de sauvegarde et planifier des sauvegardes automatiques. |
| **6.8** | 🔴 FAIL | Interdire le déchargement du plugin audit | 6. Audit & Journalisation | `Stdout:` | Ajouter audit_log=FORCE_PLUS_PERMANENT dans my.cnf. |
| **7.2** | 🔴 FAIL | Aucun mot de passe dans le my.cnf global | 7. Authentification | `Stdout:` | Utiliser mysql_config_editor ou des fichiers .my.cnf privés avec permissions restreintes. |

### 🛑 MYSQL_COMMUNITY_84 (`8` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.2** | 🔴 FAIL | Utiliser un compte dédié et privilégié minimal pour MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Configurer le service MySQL pour qu'il s'exécute sous un utilisateur dédié (ex: 'mysql') avec les pr |
| **1.3** | 🔴 FAIL | Désactiver l'historique des commandes MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Supprimer les fichiers d'historique, créer un lien symbolique vers /dev/null, ou configurer MYSQL_HI |
| **1.4** | 🔴 FAIL | Vérifier que MYSQL_PWD n'est pas utilisé | 1. Configuration Système d'exploitation | `Stdout:` | Modifier les scripts/utilisateurs pour éviter MYSQL_PWD, utiliser mysql_config_editor ou authentific |
| **1.5** | 🔴 FAIL | Désactiver l'accès interactif pour l'utilisateur MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Modifier le shell de l'utilisateur mysql pour utiliser /bin/false ou /sbin/nologin (ex: usermod -s / |
| **1.6** | 🔴 FAIL | Vérifier que MYSQL_PWD n'est pas dans les profils utilisateurs | 1. Configuration Système d'exploitation | `Stdout:` | Nettoyer les fichiers de login des utilisateurs pour supprimer MYSQL_PWD. |
| **1.7** | 🔴 FAIL | Exécuter MySQL dans un environnement sandbox | 1. Configuration Système d'exploitation | `Stdout:` | Configurer chroot, utiliser un service systemd avec un utilisateur spécifique, ou déployer MySQL sou |
| **2.1.1** | 🔴 FAIL | Politique de sauvegarde en place | 2. Installation et Planification | `Stdout:` | Créer une politique de sauvegarde et planifier des sauvegardes automatiques. |
| **7.2** | 🔴 FAIL | Aucun mot de passe dans le my.cnf global | 7. Authentification | `Stdout:` | Utiliser mysql_config_editor ou des fichiers .my.cnf privés avec permissions restreintes. |

### 🛑 MYSQL_COMMUNITY_97 (`9` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.2** | 🔴 FAIL | Utiliser un compte dédié et privilégié minimal pour MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Configurer le service MySQL pour qu'il s'exécute sous un utilisateur dédié (ex: 'mysql') avec les pr |
| **1.3** | 🔴 FAIL | Désactiver l'historique des commandes MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Supprimer les fichiers d'historique, créer un lien symbolique vers /dev/null, ou configurer MYSQL_HI |
| **1.4** | 🔴 FAIL | Vérifier que MYSQL_PWD n'est pas utilisé | 1. Configuration Système d'exploitation | `Stdout:` | Modifier les scripts/utilisateurs pour éviter MYSQL_PWD, utiliser mysql_config_editor ou authentific |
| **1.5** | 🔴 FAIL | Désactiver l'accès interactif pour l'utilisateur MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Modifier le shell de l'utilisateur mysql pour utiliser /bin/false ou /sbin/nologin (ex: usermod -s / |
| **1.6** | 🔴 FAIL | Vérifier que MYSQL_PWD n'est pas dans les profils utilisateurs | 1. Configuration Système d'exploitation | `Stdout:` | Nettoyer les fichiers de login des utilisateurs pour supprimer MYSQL_PWD. |
| **1.7** | 🔴 FAIL | Exécuter MySQL dans un environnement sandbox | 1. Configuration Système d'exploitation | `Stdout:` | Configurer chroot, utiliser un service systemd avec un utilisateur spécifique, ou déployer MySQL sou |
| **2.1.1** | 🔴 FAIL | Politique de sauvegarde en place | 2. Installation et Planification | `Stdout:` | Créer une politique de sauvegarde et planifier des sauvegardes automatiques. |
| **6.8** | 🔴 FAIL | Interdire le déchargement du plugin audit | 6. Audit & Journalisation | `Stdout:` | Ajouter audit_log=FORCE_PLUS_PERMANENT dans my.cnf. |
| **7.2** | 🔴 FAIL | Aucun mot de passe dans le my.cnf global | 7. Authentification | `Stdout:` | Utiliser mysql_config_editor ou des fichiers .my.cnf privés avec permissions restreintes. |

### 🛑 MYSQL_ENTERPRISE_84 (`9` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.2** | 🔴 FAIL | Utiliser un compte dédié et privilégié minimal pour MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Configurer le service MySQL pour qu'il s'exécute sous un utilisateur dédié (ex: 'mysql') avec les pr |
| **1.3** | 🔴 FAIL | Désactiver l'historique des commandes MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Supprimer les fichiers d'historique, créer un lien symbolique vers /dev/null, ou configurer MYSQL_HI |
| **1.4** | 🔴 FAIL | Vérifier que MYSQL_PWD n'est pas utilisé | 1. Configuration Système d'exploitation | `Stdout:` | Modifier les scripts/utilisateurs pour éviter MYSQL_PWD, utiliser mysql_config_editor ou authentific |
| **1.5** | 🔴 FAIL | Désactiver l'accès interactif pour l'utilisateur MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Modifier le shell de l'utilisateur mysql pour utiliser /bin/false ou /sbin/nologin (ex: usermod -s / |
| **1.6** | 🔴 FAIL | Vérifier que MYSQL_PWD n'est pas dans les profils utilisateurs | 1. Configuration Système d'exploitation | `Stdout:` | Nettoyer les fichiers de login des utilisateurs pour supprimer MYSQL_PWD. |
| **1.7** | 🔴 FAIL | Exécuter MySQL dans un environnement sandbox | 1. Configuration Système d'exploitation | `Stdout:` | Configurer chroot, utiliser un service systemd avec un utilisateur spécifique, ou déployer MySQL sou |
| **2.1.1** | 🔴 FAIL | Politique de sauvegarde en place | 2. Installation et Planification | `Stdout:` | Créer une politique de sauvegarde et planifier des sauvegardes automatiques. |
| **6.8** | 🔴 FAIL | Interdire le déchargement du plugin audit | 6. Audit & Journalisation | `Stdout:` | Ajouter audit_log=FORCE_PLUS_PERMANENT dans my.cnf. |
| **7.2** | 🔴 FAIL | Aucun mot de passe dans le my.cnf global | 7. Authentification | `Stdout:` | Utiliser mysql_config_editor ou des fichiers .my.cnf privés avec permissions restreintes. |

### 🛑 MYSQL_ENTERPRISE_97 (`9` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.2** | 🔴 FAIL | Utiliser un compte dédié et privilégié minimal pour MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Configurer le service MySQL pour qu'il s'exécute sous un utilisateur dédié (ex: 'mysql') avec les pr |
| **1.3** | 🔴 FAIL | Désactiver l'historique des commandes MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Supprimer les fichiers d'historique, créer un lien symbolique vers /dev/null, ou configurer MYSQL_HI |
| **1.4** | 🔴 FAIL | Vérifier que MYSQL_PWD n'est pas utilisé | 1. Configuration Système d'exploitation | `Stdout:` | Modifier les scripts/utilisateurs pour éviter MYSQL_PWD, utiliser mysql_config_editor ou authentific |
| **1.5** | 🔴 FAIL | Désactiver l'accès interactif pour l'utilisateur MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Modifier le shell de l'utilisateur mysql pour utiliser /bin/false ou /sbin/nologin (ex: usermod -s / |
| **1.6** | 🔴 FAIL | Vérifier que MYSQL_PWD n'est pas dans les profils utilisateurs | 1. Configuration Système d'exploitation | `Stdout:` | Nettoyer les fichiers de login des utilisateurs pour supprimer MYSQL_PWD. |
| **1.7** | 🔴 FAIL | Exécuter MySQL dans un environnement sandbox | 1. Configuration Système d'exploitation | `Stdout:` | Configurer chroot, utiliser un service systemd avec un utilisateur spécifique, ou déployer MySQL sou |
| **2.1.1** | 🔴 FAIL | Politique de sauvegarde en place | 2. Installation et Planification | `Stdout:` | Créer une politique de sauvegarde et planifier des sauvegardes automatiques. |
| **6.8** | 🔴 FAIL | Interdire le déchargement du plugin audit | 6. Audit & Journalisation | `Stdout:` | Ajouter audit_log=FORCE_PLUS_PERMANENT dans my.cnf. |
| **7.2** | 🔴 FAIL | Aucun mot de passe dans le my.cnf global | 7. Authentification | `Stdout:` | Utiliser mysql_config_editor ou des fichiers .my.cnf privés avec permissions restreintes. |

### 🛑 POSTGRESQL_16 (`26` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.3** | 🔴 FAIL | Activer le service systemd | 1. Installation et correctifs | `Stdout:` | systemctl enable postgresql@16-main \|\| systemctl enable postgresql-16 |
| **1.4** | 🔴 FAIL | Initialiser correctement le cluster de données | 1. Installation et correctifs | `--- Command 1: systemctl is-active postgresql@16-main.service \|\| systemctl is-ac` | Supprimer le répertoire de données et relancer initdb (avec checksums si souhaité), puis démarrer le |
| **1.6** | 🔴 FAIL | Vérifier que PGPASSWORD n'est pas défini dans les profils | 1. Installation et correctifs | `Stdout:` | Empêcher le stockage en clair du mot de passe via la variable d’environnement PGPASSWORD. |
| **1.7** | 🔴 FAIL | Vérifier que PGPASSWORD n'est pas utilisé par un processus | 1. Installation et correctifs | `Stdout:` | S’assurer qu’aucun processus n’utilise la variable PGPASSWORD. |
| **2.3** | 🔴 FAIL | Désactiver l’historique des commandes psql | 2. Permissions de répertoires et fichiers | `Stdout:` | Empêcher la création de ~/.psql_history pour limiter l’exposition de données sensibles. |
| **3.1.2** | 🔴 FAIL | Configurer log_destination | 3. Journalisation et audit | `Stdout:` | Définir la ou les destinations de logs (stderr, csvlog, syslog, jsonlog). |
| **3.1.3** | 🔴 FAIL | Activer logging_collector | 3. Journalisation et audit | `Stdout:` | Capturer stderr dans des fichiers via le démon collector. |
| **3.1.4** | 🔴 FAIL | Définir log_directory | 3.1. Journalisation des erreurs serveur | `Stdout:` | Spécifier le répertoire de sortie des fichiers de logs (ex. /var/log/postgres). |
| **3.1.5** | 🔴 FAIL | Définir log_filename | 3.1. Journalisation des erreurs serveur | `Stdout:` | Choisir un motif de nom de fichier strftime (e.g. postgresql-%Y%m%d.log). |
| **3.1.6** | 🔴 FAIL | Configurer log_file_mode | 3.1. Journalisation des erreurs serveur | `Stdout:` | Fixer les permissions des fichiers de log à 0600 (ou 0640 selon le groupe). |
| **3.1.7** | 🔴 FAIL | Activer log_truncate_on_rotation | 3.1. Journalisation des erreurs serveur | `Stdout:` | Tronquer les fichiers existants lors de la rotation si même nom. |
| **3.1.11** | 🔴 FAIL | Activer syslog_split_messages | 3.1. Journalisation des erreurs serveur | `Stdout:` | Couper les messages trop longs (>1024 octets) pour Syslog. |
| **3.1.12** | 🔴 FAIL | Prévenir la perte de messages Syslog | 3.1. Journalisation des erreurs serveur | `Stdout:` | Éviter la suppression des messages volumineux dans Syslog. |
| **3.1.13** | 🔴 FAIL | Configurer syslog_ident | 3.1. Journalisation des erreurs serveur | `Stdout:` | Définir l’identifiant de programme dans Syslog (ex. postgres). |
| **3.1.16** | 🔴 FAIL | Désactiver debug_print_parse | 3.1. Journalisation des erreurs serveur | `Stdout:` | Ne pas afficher les arbres d’analyse SQL dans les logs (réduction du bruit). |
| **3.1.17** | 🔴 FAIL | Désactiver debug_print_rewritten | 3.1. Journalisation des erreurs serveur | `Stdout:` | Ne pas afficher les arbres réécrits SQL dans les logs. |
| **3.1.18** | 🔴 FAIL | Désactiver debug_print_plan | 3.1. Journalisation des erreurs serveur | `Stdout:` | Ne pas afficher les plans d’exécution SQL dans les logs. |
| **3.1.19** | 🔴 FAIL | Activer debug_pretty_print | 3.1. Journalisation des erreurs serveur | `Stdout:` | Formater lisiblement les arbres d’analyse/réécriture dans les logs. |
| **3.1.20** | 🔴 FAIL | Activer log_connections | 3.1. Journalisation des erreurs serveur | `Stdout:` | Enregistrer chaque nouvelle connexion à PostgreSQL. |
| **3.1.21** | 🔴 FAIL | Activer log_disconnections | 3.1. Journalisation des erreurs serveur | `Stdout:` | Enregistrer chaque déconnexion de PostgreSQL. |
| **3.1.22** | 🔴 FAIL | Configurer log_error_verbosity | 3.1. Journalisation des erreurs serveur | `Stdout:` | Contrôler la verbosité des messages d’erreur (DEFAULT, VERBOSE). |
| **3.1.23** | 🔴 FAIL | Configurer log_hostname | 3.1. Journalisation des erreurs serveur | `Stdout:` | Indiquer le nom d’hôte ou l’IP dans les logs de connexion. |
| **3.1.24** | 🔴 FAIL | Configurer log_line_prefix | 3.1. Journalisation des erreurs serveur | `Stdout:` | Définir le préfixe de ligne (timestamp, utilisateur, base, etc.) dans chaque log. |
| **3.1.25** | 🔴 FAIL | Configurer log_statement | 3.1. Journalisation des erreurs serveur | `Stdout:` | Choisir le niveau de requêtes à logger (none, ddl, mod, all). |
| **3.1.26** | 🔴 FAIL | Configurer log_timezone | 3.1. Journalisation des erreurs serveur | `Stdout:` | Uniformiser le fuseau horaire des horodatages des logs (ex. UTC). |
| **8.2** | 🔴 FAIL | Installer/configurer pgBackRest | 8. Considérations spéciales de configuration | `Stdout:` | Utiliser pgBackRest pour des sauvegardes et restaurations robustes. |

### 🛑 POSTGRESQL_17 (`26` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.3** | 🔴 FAIL | Activer le service systemd | 1. Installation et correctifs | `Stdout:` | systemctl enable postgresql@17-main \|\| systemctl enable postgresql-17 |
| **1.4** | 🔴 FAIL | Initialiser correctement le cluster de données | 1. Installation et correctifs | `--- Command 1: systemctl is-active postgresql@17-main.service \|\| systemctl is-ac` | Supprimer le répertoire de données et relancer initdb (avec checksums si souhaité), puis démarrer le |
| **1.6** | 🔴 FAIL | Vérifier que PGPASSWORD n'est pas défini dans les profils | 1. Installation et correctifs | `Stdout:` | Empêcher le stockage en clair du mot de passe via la variable d’environnement PGPASSWORD. |
| **1.7** | 🔴 FAIL | Vérifier que PGPASSWORD n'est pas utilisé par un processus | 1. Installation et correctifs | `Stdout:` | S’assurer qu’aucun processus n’utilise la variable PGPASSWORD. |
| **2.3** | 🔴 FAIL | Désactiver l’historique des commandes psql | 2. Permissions de répertoires et fichiers | `Stdout:` | Empêcher la création de ~/.psql_history pour limiter l’exposition de données sensibles. |
| **3.1.2** | 🔴 FAIL | Configurer log_destination | 3. Journalisation et audit | `Stdout:` | Définir la ou les destinations de logs (stderr, csvlog, syslog, jsonlog). |
| **3.1.3** | 🔴 FAIL | Activer logging_collector | 3. Journalisation et audit | `Stdout:` | Capturer stderr dans des fichiers via le démon collector. |
| **3.1.4** | 🔴 FAIL | Définir log_directory | 3.1. Journalisation des erreurs serveur | `Stdout:` | Spécifier le répertoire de sortie des fichiers de logs (ex. /var/log/postgres). |
| **3.1.5** | 🔴 FAIL | Définir log_filename | 3.1. Journalisation des erreurs serveur | `Stdout:` | Choisir un motif de nom de fichier strftime (e.g. postgresql-%Y%m%d.log). |
| **3.1.6** | 🔴 FAIL | Configurer log_file_mode | 3.1. Journalisation des erreurs serveur | `Stdout:` | Fixer les permissions des fichiers de log à 0600 (ou 0640 selon le groupe). |
| **3.1.7** | 🔴 FAIL | Activer log_truncate_on_rotation | 3.1. Journalisation des erreurs serveur | `Stdout:` | Tronquer les fichiers existants lors de la rotation si même nom. |
| **3.1.11** | 🔴 FAIL | Activer syslog_split_messages | 3.1. Journalisation des erreurs serveur | `Stdout:` | Couper les messages trop longs (>1024 octets) pour Syslog. |
| **3.1.12** | 🔴 FAIL | Prévenir la perte de messages Syslog | 3.1. Journalisation des erreurs serveur | `Stdout:` | Éviter la suppression des messages volumineux dans Syslog. |
| **3.1.13** | 🔴 FAIL | Configurer syslog_ident | 3.1. Journalisation des erreurs serveur | `Stdout:` | Définir l’identifiant de programme dans Syslog (ex. postgres). |
| **3.1.16** | 🔴 FAIL | Désactiver debug_print_parse | 3.1. Journalisation des erreurs serveur | `Stdout:` | Ne pas afficher les arbres d’analyse SQL dans les logs (réduction du bruit). |
| **3.1.17** | 🔴 FAIL | Désactiver debug_print_rewritten | 3.1. Journalisation des erreurs serveur | `Stdout:` | Ne pas afficher les arbres réécrits SQL dans les logs. |
| **3.1.18** | 🔴 FAIL | Désactiver debug_print_plan | 3.1. Journalisation des erreurs serveur | `Stdout:` | Ne pas afficher les plans d’exécution SQL dans les logs. |
| **3.1.19** | 🔴 FAIL | Activer debug_pretty_print | 3.1. Journalisation des erreurs serveur | `Stdout:` | Formater lisiblement les arbres d’analyse/réécriture dans les logs. |
| **3.1.20** | 🔴 FAIL | Activer log_connections | 3.1. Journalisation des erreurs serveur | `Stdout:` | Enregistrer chaque nouvelle connexion à PostgreSQL. |
| **3.1.21** | 🔴 FAIL | Activer log_disconnections | 3.1. Journalisation des erreurs serveur | `Stdout:` | Enregistrer chaque déconnexion de PostgreSQL. |
| **3.1.22** | 🔴 FAIL | Configurer log_error_verbosity | 3.1. Journalisation des erreurs serveur | `Stdout:` | Contrôler la verbosité des messages d’erreur (DEFAULT, VERBOSE). |
| **3.1.23** | 🔴 FAIL | Configurer log_hostname | 3.1. Journalisation des erreurs serveur | `Stdout:` | Indiquer le nom d’hôte ou l’IP dans les logs de connexion. |
| **3.1.24** | 🔴 FAIL | Configurer log_line_prefix | 3.1. Journalisation des erreurs serveur | `Stdout:` | Définir le préfixe de ligne (timestamp, utilisateur, base, etc.) dans chaque log. |
| **3.1.25** | 🔴 FAIL | Configurer log_statement | 3.1. Journalisation des erreurs serveur | `Stdout:` | Choisir le niveau de requêtes à logger (none, ddl, mod, all). |
| **3.1.26** | 🔴 FAIL | Configurer log_timezone | 3.1. Journalisation des erreurs serveur | `Stdout:` | Uniformiser le fuseau horaire des horodatages des logs (ex. UTC). |
| **8.2** | 🔴 FAIL | Installer/configurer pgBackRest | 8. Considérations spéciales de configuration | `Stdout:` | Utiliser pgBackRest pour des sauvegardes et restaurations robustes. |

### 🛑 POSTGRESQL_18 (`26` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.3** | 🔴 FAIL | Activer le service systemd | 1. Installation et correctifs | `Stdout:` | systemctl enable postgresql@18-main \|\| systemctl enable postgresql-18 |
| **1.4** | 🔴 FAIL | Initialiser correctement le cluster de données | 1. Installation et correctifs | `--- Command 1: systemctl is-active postgresql@18-main.service \|\| systemctl is-ac` | Supprimer le répertoire de données et relancer initdb (avec checksums si souhaité), puis démarrer le |
| **1.6** | 🔴 FAIL | Vérifier que PGPASSWORD n'est pas défini dans les profils | 1. Installation et correctifs | `Stdout:` | Empêcher le stockage en clair du mot de passe via la variable d’environnement PGPASSWORD. |
| **1.7** | 🔴 FAIL | Vérifier que PGPASSWORD n'est pas utilisé par un processus | 1. Installation et correctifs | `Stdout:` | S’assurer qu’aucun processus n’utilise la variable PGPASSWORD. |
| **2.3** | 🔴 FAIL | Désactiver l’historique des commandes psql | 2. Permissions de répertoires et fichiers | `Stdout:` | Empêcher la création de ~/.psql_history pour limiter l’exposition de données sensibles. |
| **3.1.2** | 🔴 FAIL | Configurer log_destination | 3. Journalisation et audit | `Stdout:` | Définir la ou les destinations de logs (stderr, csvlog, syslog, jsonlog). |
| **3.1.3** | 🔴 FAIL | Activer logging_collector | 3. Journalisation et audit | `Stdout:` | Capturer stderr dans des fichiers via le démon collector. |
| **3.1.4** | 🔴 FAIL | Définir log_directory | 3.1. Journalisation des erreurs serveur | `Stdout:` | Spécifier le répertoire de sortie des fichiers de logs (ex. /var/log/postgres). |
| **3.1.5** | 🔴 FAIL | Définir log_filename | 3.1. Journalisation des erreurs serveur | `Stdout:` | Choisir un motif de nom de fichier strftime (e.g. postgresql-%Y%m%d.log). |
| **3.1.6** | 🔴 FAIL | Configurer log_file_mode | 3.1. Journalisation des erreurs serveur | `Stdout:` | Fixer les permissions des fichiers de log à 0600 (ou 0640 selon le groupe). |
| **3.1.7** | 🔴 FAIL | Activer log_truncate_on_rotation | 3.1. Journalisation des erreurs serveur | `Stdout:` | Tronquer les fichiers existants lors de la rotation si même nom. |
| **3.1.11** | 🔴 FAIL | Activer syslog_split_messages | 3.1. Journalisation des erreurs serveur | `Stdout:` | Couper les messages trop longs (>1024 octets) pour Syslog. |
| **3.1.12** | 🔴 FAIL | Prévenir la perte de messages Syslog | 3.1. Journalisation des erreurs serveur | `Stdout:` | Éviter la suppression des messages volumineux dans Syslog. |
| **3.1.13** | 🔴 FAIL | Configurer syslog_ident | 3.1. Journalisation des erreurs serveur | `Stdout:` | Définir l’identifiant de programme dans Syslog (ex. postgres). |
| **3.1.16** | 🔴 FAIL | Désactiver debug_print_parse | 3.1. Journalisation des erreurs serveur | `Stdout:` | Ne pas afficher les arbres d’analyse SQL dans les logs (réduction du bruit). |
| **3.1.17** | 🔴 FAIL | Désactiver debug_print_rewritten | 3.1. Journalisation des erreurs serveur | `Stdout:` | Ne pas afficher les arbres réécrits SQL dans les logs. |
| **3.1.18** | 🔴 FAIL | Désactiver debug_print_plan | 3.1. Journalisation des erreurs serveur | `Stdout:` | Ne pas afficher les plans d’exécution SQL dans les logs. |
| **3.1.19** | 🔴 FAIL | Activer debug_pretty_print | 3.1. Journalisation des erreurs serveur | `Stdout:` | Formater lisiblement les arbres d’analyse/réécriture dans les logs. |
| **3.1.20** | 🔴 FAIL | Activer log_connections | 3.1. Journalisation des erreurs serveur | `Stdout:` | Enregistrer chaque nouvelle connexion à PostgreSQL. |
| **3.1.21** | 🔴 FAIL | Activer log_disconnections | 3.1. Journalisation des erreurs serveur | `Stdout:` | Enregistrer chaque déconnexion de PostgreSQL. |
| **3.1.22** | 🔴 FAIL | Configurer log_error_verbosity | 3.1. Journalisation des erreurs serveur | `Stdout:` | Contrôler la verbosité des messages d’erreur (DEFAULT, VERBOSE). |
| **3.1.23** | 🔴 FAIL | Configurer log_hostname | 3.1. Journalisation des erreurs serveur | `Stdout:` | Indiquer le nom d’hôte ou l’IP dans les logs de connexion. |
| **3.1.24** | 🔴 FAIL | Configurer log_line_prefix | 3.1. Journalisation des erreurs serveur | `Stdout:` | Définir le préfixe de ligne (timestamp, utilisateur, base, etc.) dans chaque log. |
| **3.1.25** | 🔴 FAIL | Configurer log_statement | 3.1. Journalisation des erreurs serveur | `Stdout:` | Choisir le niveau de requêtes à logger (none, ddl, mod, all). |
| **3.1.26** | 🔴 FAIL | Configurer log_timezone | 3.1. Journalisation des erreurs serveur | `Stdout:` | Uniformiser le fuseau horaire des horodatages des logs (ex. UTC). |
| **8.2** | 🔴 FAIL | Installer/configurer pgBackRest | 8. Considérations spéciales de configuration | `Stdout:` | Utiliser pgBackRest pour des sauvegardes et restaurations robustes. |

---

## ⚠️ Registre Détaillé des Contrôles Manuels (`MANUAL`) - Mode SSH Remote (-m ssh)

### 📋 MARIADB_1011 (`40` contrôles manuels)

| ID Règle | Nom du Contrôle | Catégorie | Note de Vérification |
| :---: | :--- | :--- | :--- |
| **1.1** | Placer les bases de données sur des partitions non-système | 1. Configuration Système d'exploitation | Vérification visuelle / politique organisationnelle requise |
| **1.7** | Exécuter MariaDB dans un environnement sandbox | 1. Configuration Système d'exploitation | Vérification visuelle / politique organisationnelle requise |
| **2.1.1** | Politique de sauvegarde en place | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.2** | Validation des sauvegardes | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.3** | Sécuriser les identifiants de sauvegarde | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.4** | Sécuriser les fichiers de sauvegarde | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.6** | Plan de reprise d'activité (DR) | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.7** | Sauvegarde des fichiers de configuration | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.2** | Dédier la machine à MariaDB | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.3** | Ne pas spécifier de mots de passe en ligne de commande | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.4** | Ne pas réutiliser les noms d'utilisateurs | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.5** | S'assurer que le matériel cryptographique est unique et non par défaut | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.7** | Verrouiller les comptes inutilisés | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.8** | Utilisation appropriée de l'authentification Socket Peer-Credential | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **3.1** | Permissions adéquates sur 'datadir' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.2** | Permissions sur les fichiers 'log_bin_basename' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.3** | Permissions sur 'log_error' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.4** | Permissions sur 'slow_query_log' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.5** | Permissions sur 'relay_log_basename' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.6** | Permissions sur 'general_log_file' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.8** | Permissions sur le répertoire des plugins | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **4.1** | S'assurer que les derniers correctifs de sécurité sont appliqués | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **5.1** | Limiter l'accès complet à mysql.* aux seuls administrateurs | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **5.2** | Retirer le droit FILE aux non-admins | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **5.3** | Retirer le droit PROCESS aux non-admins | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **5.4** | Retirer le droit SUPER aux non-admins | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **5.5** | Retirer le droit SHUTDOWN aux non-admins | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **5.6** | Retirer CREATE USER aux non-admins | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **5.7** | Retirer GRANT OPTION aux non-admins | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **5.8** | Limiter REPLICATION SLAVE aux comptes de réplication | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **5.9** | Limiter les droits DML/DDL à des BD/comptes précis | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **5.10** | Définir proprement DEFINER/INVOKER des SP/Functions | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **6.2** | Journal hors partition système | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **7.7** | Empêcher la réutilisation des mots de passe (password_reuse_check) | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **8.3** | Limiter le nombre de connexions | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **9.1** | Chiffrer le trafic de réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.2** | MASTER_SSL_VERIFY_SERVER_CERT activé | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.3** | Pas de SUPER pour les utilisateurs de réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.4** | Chiffrement approuvé pour la réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.5** | TLS mutuel activé pour la réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |

### 📋 MARIADB_106 (`39` contrôles manuels)

| ID Règle | Nom du Contrôle | Catégorie | Note de Vérification |
| :---: | :--- | :--- | :--- |
| **1.1** | Placer les bases de données sur des partitions non-système | 1. Configuration Système d'exploitation | Vérification visuelle / politique organisationnelle requise |
| **1.7** | Exécuter MariaDB dans un environnement sandbox | 1. Configuration Système d'exploitation | Vérification visuelle / politique organisationnelle requise |
| **2.1.1** | Politique de sauvegarde en place | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.2** | Validation des sauvegardes | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.3** | Sécuriser les identifiants de sauvegarde | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.4** | Sécuriser les fichiers de sauvegarde | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.6** | Plan de reprise d'activité (DR) | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.7** | Sauvegarde des fichiers de configuration | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.2** | Dédier la machine à MariaDB | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.3** | Ne pas spécifier de mots de passe en ligne de commande | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.4** | Ne pas réutiliser les noms d'utilisateurs | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.5** | S'assurer que le matériel cryptographique est unique et non par défaut | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.7** | Verrouiller les comptes inutilisés | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.8** | Utilisation appropriée de l'authentification Socket Peer-Credential | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **3.1** | Permissions adéquates sur 'datadir' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.2** | Permissions sur les fichiers 'log_bin_basename' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.3** | Permissions sur 'log_error' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.4** | Permissions sur 'slow_query_log' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.5** | Permissions sur 'relay_log_basename' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.6** | Permissions sur 'general_log_file' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.8** | Permissions sur le répertoire des plugins | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **4.1** | S'assurer que les derniers correctifs de sécurité sont appliqués | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **5.1** | Limiter l'accès complet à mysql.* aux seuls administrateurs | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **5.2** | Retirer le droit FILE aux non-admins | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **5.3** | Retirer le droit PROCESS aux non-admins | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **5.4** | Retirer le droit SUPER aux non-admins | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **5.5** | Retirer le droit SHUTDOWN aux non-admins | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **5.6** | Retirer CREATE USER aux non-admins | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **5.7** | Retirer GRANT OPTION aux non-admins | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **5.8** | Limiter REPLICATION SLAVE aux comptes de réplication | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **5.9** | Limiter les droits DML/DDL à des BD/comptes précis | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **5.10** | Définir proprement DEFINER/INVOKER des SP/Functions | 5. Permissions MariaDB | Vérification visuelle / politique organisationnelle requise |
| **6.2** | Journal hors partition système | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **8.3** | Limiter le nombre de connexions | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **9.1** | Chiffrer le trafic de réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.2** | MASTER_SSL_VERIFY_SERVER_CERT activé | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.3** | Pas de SUPER pour les utilisateurs de réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.4** | Chiffrement approuvé pour la réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.5** | TLS mutuel activé pour la réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |

### 📋 MYSQL_80 (`59` contrôles manuels)

| ID Règle | Nom du Contrôle | Catégorie | Note de Vérification |
| :---: | :--- | :--- | :--- |
| **1.1** | Placer les bases de données sur des partitions non-système | 1. Configuration Système d'exploitation | Vérification visuelle / politique organisationnelle requise |
| **2.1.2** | Validation des sauvegardes | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.3** | Sécuriser les identifiants de sauvegarde | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.4** | Sécuriser les fichiers de sauvegarde | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.5** | Point-in-Time Recovery | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.6** | Plan de reprise d'activité (DR) | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.7** | Sauvegarde des fichiers de configuration | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **3.1** | Permissions adéquates sur 'datadir' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.2** | Permissions sur les fichiers 'log_bin_basename' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.3** | Permissions sur 'log_error' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.4** | Permissions sur 'slow_query_log' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.5** | Permissions sur 'relay_log_basename' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.6** | Permissions sur 'general_log_file' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.7** | Permissions sur les fichiers de clés SSL | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.8** | Permissions sur le répertoire des plugins | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.9** | Permissions sur 'audit_log_file' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.10** | Sécuriser le Keyring MySQL | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **4.1** | Ensure the Latest Security Patches are Applied | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.2** | Ensure Example or Test Databases are Not Installed on Production Servers | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.4** | Harden Usage for 'local_infile' on MySQL Clients | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.6** | Ensure Symbolic Links are Disabled | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.7** | Ensure the 'daemon_memcached' Plugin is Disabled | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.8** | Ensure the 'secure_file_priv' is Configured Correctly | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.9** | Ensure 'sql_mode' Contains 'STRICT_ALL_TABLES' | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.10** | Use MySQL TDE for At-Rest Data Encryption | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **5.1** | Limiter l'accès complet à mysql.* aux seuls administrateurs | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.2** | Retirer le droit FILE aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.3** | Retirer le droit PROCESS aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.4** | Retirer le droit SUPER (prérogative obsolète) | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.5** | Retirer le droit SHUTDOWN | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.6** | Retirer CREATE USER aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.7** | Retirer GRANT OPTION aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.8** | Limiter REPLICATION SLAVE aux comptes de réplication | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.9** | Limiter les droits DML/DDL à des BD/comptes précis | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.10** | Définir proprement DEFINER/INVOKER des SP/Functions | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.11** | Restreindre le droit SET_ANY_DEFINER | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.12** | Restreindre ALLOW_NONEXISTENT_DEFINER | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **6.1** | Configurer log_error | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.2** | Journal hors partition système | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.3** | log_error_verbosity=2 | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.4** | log-raw OFF | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.5** | Filtrer et journaliser les connexions | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.6** | Filtre << tout journaliser >> | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.7** | audit_log_strategy = (S)SYNC | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **7.1** | Plugin d'authentification sûr (caching_sha2_password) | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.3** | Tous les comptes ont un mot de passe | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.4** | Expiration annuelle des mots de passe | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.5** | Politique de complexité forte | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.6** | Pas de wildcard '%' dans host | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.7** | Supprimer les comptes anonymes | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **8.1** | Forcer SSL/TLS (require_secure_transport=ON) | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **8.2** | Exiger TLS côté utilisateur (ssl_type) | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **8.3** | Limiter le nombre de connexions | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **9.1** | Chiffrer le trafic de réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.2** | SOURCE_SSL_VERIFY_SERVER_CERT = 1 | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.3** | master_info_repository TABLE | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.4** | Retirer SUPER aux comptes de réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **10.1** | Chiffrer le trafic Group Replication | 10. InnoDB Cluster / Group Replication | Vérification visuelle / politique organisationnelle requise |
| **10.2** | Définir une allow-list de nœuds | 10. InnoDB Cluster / Group Replication | Vérification visuelle / politique organisationnelle requise |

### 📋 MYSQL_COMMUNITY_84 (`69` contrôles manuels)

| ID Règle | Nom du Contrôle | Catégorie | Note de Vérification |
| :---: | :--- | :--- | :--- |
| **1.1** | Placer les bases de données sur des partitions non-système | 1. Configuration Système d'exploitation | Vérification visuelle / politique organisationnelle requise |
| **2.1.2** | Validation des sauvegardes | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.3** | Sécuriser les identifiants de sauvegarde | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.4** | Point-in-Time Recovery | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.5** | Plan de reprise d'activité (DR) | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.6** | Sauvegarde des fichiers de configuration | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.2.1** | Chiffrer les binary et relay logs | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.3** | Dédier la machine MySQL | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.4** | Ne pas spécifier de mots de passe en ligne de commande | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.5** | Ne pas réutiliser les noms d'utilisateurs | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.6** | Matériel cryptographique unique et non-par-défaut | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.7** | Durée de vie des mots de passe ≤ 365 jours | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.8** | Exiger des mots de passe forts lors de la réinitialisation | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.9** | Exiger le mot de passe actuel pour changer le mot de passe | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.10** | Utiliser les mots de passe doubles pour rotation fréquente | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.11** | Verrouiller les comptes inutilisés | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.12** | Configurer le mode de chiffrement AES | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.13** | Authentification socket peer-credential appropriée | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.14** | MySQL est lié à une adresse IP spécifique | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.15** | Limiter les versions TLS acceptées | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.16** | Exiger les certificats côté client (X.509) | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.17** | Utiliser uniquement des ciphers approuvés | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.18** | Délais de connexion pour limiter les tentatives échouées | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.19** | Utiliser le chiffrement OpenSSL FIPS 140-2 | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **3.1** | Permissions adéquates sur 'datadir' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.2** | Permissions sur les fichiers 'log_bin_basename' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.3** | Permissions sur 'log_error' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.4** | Permissions sur 'slow_query_log' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.5** | Permissions sur 'relay_log_basename' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.6** | Permissions sur 'general_log_file' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.7** | Permissions sur les fichiers de clés SSL | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.8** | Permissions sur le répertoire des plugins | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **4.1** | Appliquer les derniers correctifs de sécurité | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.2** | S'assurer que les bases de test ne sont pas installées en production | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.4** | Renforcer l'utilisation de 'local_infile' sur les clients MySQL | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.6** | Désactiver les liens symboliques | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.7** | Configurer 'secure_file_priv' correctement | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.8** | S'assurer que 'sql_mode' contient 'STRICT_ALL_TABLES' | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.9** | Chiffrement des données au repos avec TDE | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **5.1** | Limiter l'accès complet à mysql.* aux seuls administrateurs | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.2** | Retirer le droit FILE aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.3** | Retirer le droit PROCESS aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.4** | Retirer le droit SUPER | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.5** | Retirer le droit SHUTDOWN | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.6** | Retirer CREATE USER aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.7** | Retirer GRANT OPTION aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.8** | Limiter REPLICATION SLAVE aux comptes de réplication | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.9** | Limiter les droits DML/DDL à des BD/comptes précis | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.10** | Définir proprement DEFINER/INVOKER des SP/Functions | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.11** | Restreindre le droit SET_ANY_DEFINER | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.12** | Restreindre ALLOW_NONEXISTENT_DEFINER | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **6.1** | Configurer log_error | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.2** | Journal hors partition système | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.3** | log_error_verbosity=2 | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.4** | log-raw OFF | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **7.1** | Politique d'authentification sécurisée (authentication_policy) | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.3** | Tous les comptes ont un mot de passe | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.4** | Expiration annuelle des mots de passe | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.5** | Politique de complexité forte | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.6** | Pas de wildcard '%' dans host | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.7** | Supprimer les comptes anonymes | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **8.1** | Forcer SSL/TLS (require_secure_transport=ON) | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **8.2** | Exiger TLS côté utilisateur (ssl_type) | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **8.3** | Limiter le nombre de connexions | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **9.1** | Chiffrer le trafic de réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.2** | SOURCE_SSL_VERIFY_SERVER_CERT = YES | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.3** | Retirer SUPER aux comptes de réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **10.1** | Chiffrer le trafic Group Replication | 10. InnoDB Cluster / Group Replication | Vérification visuelle / politique organisationnelle requise |
| **10.2** | Définir une allow-list de nœuds | 10. InnoDB Cluster / Group Replication | Vérification visuelle / politique organisationnelle requise |

### 📋 MYSQL_COMMUNITY_97 (`59` contrôles manuels)

| ID Règle | Nom du Contrôle | Catégorie | Note de Vérification |
| :---: | :--- | :--- | :--- |
| **1.1** | Placer les bases de données sur des partitions non-système | 1. Configuration Système d'exploitation | Vérification visuelle / politique organisationnelle requise |
| **2.1.2** | Validation des sauvegardes | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.3** | Sécuriser les identifiants de sauvegarde | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.4** | Sécuriser les fichiers de sauvegarde | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.5** | Point-in-Time Recovery | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.6** | Plan de reprise d'activité (DR) | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.7** | Sauvegarde des fichiers de configuration | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **3.1** | Permissions adéquates sur 'datadir' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.2** | Permissions sur les fichiers 'log_bin_basename' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.3** | Permissions sur 'log_error' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.4** | Permissions sur 'slow_query_log' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.5** | Permissions sur 'relay_log_basename' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.6** | Permissions sur 'general_log_file' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.7** | Permissions sur les fichiers de clés SSL | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.8** | Permissions sur le répertoire des plugins | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.9** | Permissions sur 'audit_log_file' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.10** | Sécuriser le Keyring MySQL | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **4.1** | Ensure the Latest Security Patches are Applied | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.2** | Ensure Example or Test Databases are Not Installed on Production Servers | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.4** | Harden Usage for 'local_infile' on MySQL Clients | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.6** | Ensure Symbolic Links are Disabled | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.7** | Ensure the 'daemon_memcached' Plugin is Disabled | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.8** | Ensure the 'secure_file_priv' is Configured Correctly | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.9** | Ensure 'sql_mode' Contains 'STRICT_ALL_TABLES' | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.10** | Use MySQL TDE for At-Rest Data Encryption | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **5.1** | Limiter l'accès complet à mysql.* aux seuls administrateurs | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.2** | Retirer le droit FILE aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.3** | Retirer le droit PROCESS aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.4** | Retirer le droit SUPER (prérogative obsolète) | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.5** | Retirer le droit SHUTDOWN | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.6** | Retirer CREATE USER aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.7** | Retirer GRANT OPTION aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.8** | Limiter REPLICATION SLAVE aux comptes de réplication | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.9** | Limiter les droits DML/DDL à des BD/comptes précis | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.10** | Définir proprement DEFINER/INVOKER des SP/Functions | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.11** | Restreindre le droit SET_ANY_DEFINER | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.12** | Restreindre ALLOW_NONEXISTENT_DEFINER | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **6.1** | Configurer log_error | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.2** | Journal hors partition système | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.3** | log_error_verbosity=2 | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.4** | log-raw OFF | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.5** | Filtrer et journaliser les connexions | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.6** | Filtre << tout journaliser >> | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.7** | audit_log_strategy = (S)SYNC | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **7.1** | Plugin d'authentification sûr (caching_sha2_password) | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.3** | Tous les comptes ont un mot de passe | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.4** | Expiration annuelle des mots de passe | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.5** | Politique de complexité forte | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.6** | Pas de wildcard '%' dans host | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.7** | Supprimer les comptes anonymes | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **8.1** | Forcer SSL/TLS (require_secure_transport=ON) | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **8.2** | Exiger TLS côté utilisateur (ssl_type) | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **8.3** | Limiter le nombre de connexions | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **9.1** | Chiffrer le trafic de réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.2** | SOURCE_SSL_VERIFY_SERVER_CERT = 1 | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.3** | master_info_repository TABLE | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.4** | Retirer SUPER aux comptes de réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **10.1** | Chiffrer le trafic Group Replication | 10. InnoDB Cluster / Group Replication | Vérification visuelle / politique organisationnelle requise |
| **10.2** | Définir une allow-list de nœuds | 10. InnoDB Cluster / Group Replication | Vérification visuelle / politique organisationnelle requise |

### 📋 MYSQL_ENTERPRISE_84 (`59` contrôles manuels)

| ID Règle | Nom du Contrôle | Catégorie | Note de Vérification |
| :---: | :--- | :--- | :--- |
| **1.1** | Placer les bases de données sur des partitions non-système | 1. Configuration Système d'exploitation | Vérification visuelle / politique organisationnelle requise |
| **2.1.2** | Validation des sauvegardes | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.3** | Sécuriser les identifiants de sauvegarde | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.4** | Sécuriser les fichiers de sauvegarde | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.5** | Point-in-Time Recovery | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.6** | Plan de reprise d'activité (DR) | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.7** | Sauvegarde des fichiers de configuration | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **3.1** | Permissions adéquates sur 'datadir' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.2** | Permissions sur les fichiers 'log_bin_basename' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.3** | Permissions sur 'log_error' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.4** | Permissions sur 'slow_query_log' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.5** | Permissions sur 'relay_log_basename' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.6** | Permissions sur 'general_log_file' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.7** | Permissions sur les fichiers de clés SSL | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.8** | Permissions sur le répertoire des plugins | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.9** | Permissions sur 'audit_log_file' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.10** | Sécuriser le Keyring MySQL | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **4.1** | Ensure the Latest Security Patches are Applied | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.2** | Ensure Example or Test Databases are Not Installed on Production Servers | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.4** | Harden Usage for 'local_infile' on MySQL Clients | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.6** | Ensure Symbolic Links are Disabled | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.7** | Ensure the 'daemon_memcached' Plugin is Disabled | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.8** | Ensure the 'secure_file_priv' is Configured Correctly | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.9** | Ensure 'sql_mode' Contains 'STRICT_ALL_TABLES' | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.10** | Use MySQL TDE for At-Rest Data Encryption | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **5.1** | Limiter l'accès complet à mysql.* aux seuls administrateurs | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.2** | Retirer le droit FILE aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.3** | Retirer le droit PROCESS aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.4** | Retirer le droit SUPER (prérogative obsolète) | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.5** | Retirer le droit SHUTDOWN | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.6** | Retirer CREATE USER aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.7** | Retirer GRANT OPTION aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.8** | Limiter REPLICATION SLAVE aux comptes de réplication | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.9** | Limiter les droits DML/DDL à des BD/comptes précis | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.10** | Définir proprement DEFINER/INVOKER des SP/Functions | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.11** | Restreindre le droit SET_ANY_DEFINER | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.12** | Restreindre ALLOW_NONEXISTENT_DEFINER | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **6.1** | Configurer log_error | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.2** | Journal hors partition système | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.3** | log_error_verbosity=2 | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.4** | log-raw OFF | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.5** | Filtrer et journaliser les connexions | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.6** | Filtre << tout journaliser >> | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.7** | audit_log_strategy = (S)SYNC | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **7.1** | Plugin d'authentification sûr (caching_sha2_password) | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.3** | Tous les comptes ont un mot de passe | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.4** | Expiration annuelle des mots de passe | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.5** | Politique de complexité forte | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.6** | Pas de wildcard '%' dans host | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.7** | Supprimer les comptes anonymes | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **8.1** | Forcer SSL/TLS (require_secure_transport=ON) | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **8.2** | Exiger TLS côté utilisateur (ssl_type) | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **8.3** | Limiter le nombre de connexions | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **9.1** | Chiffrer le trafic de réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.2** | SOURCE_SSL_VERIFY_SERVER_CERT = 1 | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.3** | master_info_repository TABLE | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.4** | Retirer SUPER aux comptes de réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **10.1** | Chiffrer le trafic Group Replication | 10. InnoDB Cluster / Group Replication | Vérification visuelle / politique organisationnelle requise |
| **10.2** | Définir une allow-list de nœuds | 10. InnoDB Cluster / Group Replication | Vérification visuelle / politique organisationnelle requise |

### 📋 MYSQL_ENTERPRISE_97 (`59` contrôles manuels)

| ID Règle | Nom du Contrôle | Catégorie | Note de Vérification |
| :---: | :--- | :--- | :--- |
| **1.1** | Placer les bases de données sur des partitions non-système | 1. Configuration Système d'exploitation | Vérification visuelle / politique organisationnelle requise |
| **2.1.2** | Validation des sauvegardes | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.3** | Sécuriser les identifiants de sauvegarde | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.4** | Sécuriser les fichiers de sauvegarde | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.5** | Point-in-Time Recovery | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.6** | Plan de reprise d'activité (DR) | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **2.1.7** | Sauvegarde des fichiers de configuration | 2. Installation et Planification | Vérification visuelle / politique organisationnelle requise |
| **3.1** | Permissions adéquates sur 'datadir' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.2** | Permissions sur les fichiers 'log_bin_basename' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.3** | Permissions sur 'log_error' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.4** | Permissions sur 'slow_query_log' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.5** | Permissions sur 'relay_log_basename' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.6** | Permissions sur 'general_log_file' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.7** | Permissions sur les fichiers de clés SSL | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.8** | Permissions sur le répertoire des plugins | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.9** | Permissions sur 'audit_log_file' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.10** | Sécuriser le Keyring MySQL | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
| **4.1** | Ensure the Latest Security Patches are Applied | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.2** | Ensure Example or Test Databases are Not Installed on Production Servers | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.4** | Harden Usage for 'local_infile' on MySQL Clients | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.6** | Ensure Symbolic Links are Disabled | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.7** | Ensure the 'daemon_memcached' Plugin is Disabled | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.8** | Ensure the 'secure_file_priv' is Configured Correctly | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.9** | Ensure 'sql_mode' Contains 'STRICT_ALL_TABLES' | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **4.10** | Use MySQL TDE for At-Rest Data Encryption | 4. Général | Vérification visuelle / politique organisationnelle requise |
| **5.1** | Limiter l'accès complet à mysql.* aux seuls administrateurs | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.2** | Retirer le droit FILE aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.3** | Retirer le droit PROCESS aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.4** | Retirer le droit SUPER (prérogative obsolète) | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.5** | Retirer le droit SHUTDOWN | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.6** | Retirer CREATE USER aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.7** | Retirer GRANT OPTION aux non-admins | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.8** | Limiter REPLICATION SLAVE aux comptes de réplication | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.9** | Limiter les droits DML/DDL à des BD/comptes précis | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.10** | Définir proprement DEFINER/INVOKER des SP/Functions | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.11** | Restreindre le droit SET_ANY_DEFINER | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **5.12** | Restreindre ALLOW_NONEXISTENT_DEFINER | 5. Gestion des privilèges | Vérification visuelle / politique organisationnelle requise |
| **6.1** | Configurer log_error | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.2** | Journal hors partition système | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.3** | log_error_verbosity=2 | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.4** | log-raw OFF | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.5** | Filtrer et journaliser les connexions | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.6** | Filtre << tout journaliser >> | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **6.7** | audit_log_strategy = (S)SYNC | 6. Audit & Journalisation | Vérification visuelle / politique organisationnelle requise |
| **7.1** | Plugin d'authentification sûr (caching_sha2_password) | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.3** | Tous les comptes ont un mot de passe | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.4** | Expiration annuelle des mots de passe | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.5** | Politique de complexité forte | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.6** | Pas de wildcard '%' dans host | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **7.7** | Supprimer les comptes anonymes | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **8.1** | Forcer SSL/TLS (require_secure_transport=ON) | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **8.2** | Exiger TLS côté utilisateur (ssl_type) | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **8.3** | Limiter le nombre de connexions | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **9.1** | Chiffrer le trafic de réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.2** | SOURCE_SSL_VERIFY_SERVER_CERT = 1 | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.3** | master_info_repository TABLE | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.4** | Retirer SUPER aux comptes de réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **10.1** | Chiffrer le trafic Group Replication | 10. InnoDB Cluster / Group Replication | Vérification visuelle / politique organisationnelle requise |
| **10.2** | Définir une allow-list de nœuds | 10. InnoDB Cluster / Group Replication | Vérification visuelle / politique organisationnelle requise |

### 📋 POSTGRESQL_16 (`43` contrôles manuels)

| ID Règle | Nom du Contrôle | Catégorie | Note de Vérification |
| :---: | :--- | :--- | :--- |
| **1.1** | Obtenir les paquets depuis des dépôts autorisés | 1. Installation et correctifs | Vérification visuelle / politique organisationnelle requise |
| **1.2** | Installer uniquement les paquets requis | 1. Installation et correctifs | Vérification visuelle / politique organisationnelle requise |
| **1.5** | Appliquer les derniers correctifs de sécurité | 1. Installation et correctifs | Vérification visuelle / politique organisationnelle requise |
| **2.1** | Masque de permissions (umask) | 2. Permissions de répertoires et fichiers | Vérification visuelle / politique organisationnelle requise |
| **2.2** | Propriétaire et permissions du répertoire d’extensions | 2. Permissions de répertoires et fichiers | Vérification visuelle / politique organisationnelle requise |
| **2.4** | Ne pas stocker de mots de passe dans les fichiers de service | 2. Permissions de répertoires et fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.2** | Activer l’extension pgAudit | 3. Journalisation et audit | Vérification visuelle / politique organisationnelle requise |
| **3.1.10** | Choisir syslog_facility | 3.1. Journalisation des erreurs serveur | Vérification visuelle / politique organisationnelle requise |
| **3.1.14** | Assurer les bons messages dans le log serveur | 3.1. Journalisation des erreurs serveur | Vérification visuelle / politique organisationnelle requise |
| **3.1.15** | Enregistrer les SQL en erreur | 3.1. Journalisation des erreurs serveur | Vérification visuelle / politique organisationnelle requise |
| **4.1** | Désactiver la connexion interactive | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.2** | Configurer sudo correctement | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.3** | Révoquer les privilèges administratifs excessifs | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.4** | Verrouiller les comptes inactifs | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.5** | Révoquer les privilèges de fonction excessifs | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.6** | Révoquer les privilèges DML excessifs | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.7** | Configurer Row Level Security (RLS) | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.8** | Installer l’extension set_user | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.9** | Utiliser les rôles prédéfinis | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **5.1** | Ne pas passer de mot de passe en ligne de commande | 5. Connexion et authentification | Vérification visuelle / politique organisationnelle requise |
| **5.2** | Lier PostgreSQL à une adresse IP | 5. Connexion et authentification | Vérification visuelle / politique organisationnelle requise |
| **5.3** | Configurer la connexion UNIX locale | 5. Connexion et authentification | Vérification visuelle / politique organisationnelle requise |
| **5.4** | Configurer la connexion TCP/IP | 5. Connexion et authentification | Vérification visuelle / politique organisationnelle requise |
| **5.5** | Limites de connexion par compte | 5. Connexion et authentification | Vérification visuelle / politique organisationnelle requise |
| **5.6** | Configurer la complexité des mots de passe | 5. Connexion et authentification | Vérification visuelle / politique organisationnelle requise |
| **6.1** | Comprendre vecteurs d’attaque et paramètres runtime | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.2** | Configurer les paramètres backend | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.3** | Configurer Postmaster runtime parameters | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.4** | Configurer les signaux SIGHUP | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.5** | Configurer les paramètres Superuser | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.6** | Configurer les paramètres User | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.7** | Utiliser la cryptographie FIPS 140-2 | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.8** | Activer et configurer TLS | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.9** | Configurer TLSv1.3+ | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.10** | Désactiver les cipher suites faibles | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.11** | Installer et configurer pgcrypto | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **7.1** | Créer un utilisateur de réplication dédié | 7. Réplication | Vérification visuelle / politique organisationnelle requise |
| **7.2** | Journaliser les commandes de réplication | 7. Réplication | Vérification visuelle / politique organisationnelle requise |
| **7.3** | Configurer les sauvegardes de base | 7. Réplication | Vérification visuelle / politique organisationnelle requise |
| **7.4** | Configurer l’archivage WAL | 7. Réplication | Vérification visuelle / politique organisationnelle requise |
| **7.5** | Configurer les paramètres de streaming | 7. Réplication | Vérification visuelle / politique organisationnelle requise |
| **8.1** | Emplacements hors du cluster de données | 8. Considérations spéciales de configuration | Vérification visuelle / politique organisationnelle requise |
| **8.3** | Vérifier autres paramètres divers | 8. Considérations spéciales de configuration | Vérification visuelle / politique organisationnelle requise |

### 📋 POSTGRESQL_17 (`43` contrôles manuels)

| ID Règle | Nom du Contrôle | Catégorie | Note de Vérification |
| :---: | :--- | :--- | :--- |
| **1.1** | Obtenir les paquets depuis des dépôts autorisés | 1. Installation et correctifs | Vérification visuelle / politique organisationnelle requise |
| **1.2** | Installer uniquement les paquets requis | 1. Installation et correctifs | Vérification visuelle / politique organisationnelle requise |
| **1.5** | Appliquer les derniers correctifs de sécurité | 1. Installation et correctifs | Vérification visuelle / politique organisationnelle requise |
| **2.1** | Masque de permissions (umask) | 2. Permissions de répertoires et fichiers | Vérification visuelle / politique organisationnelle requise |
| **2.2** | Propriétaire et permissions du répertoire d’extensions | 2. Permissions de répertoires et fichiers | Vérification visuelle / politique organisationnelle requise |
| **2.4** | Ne pas stocker de mots de passe dans les fichiers de service | 2. Permissions de répertoires et fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.2** | Activer l’extension pgAudit | 3. Journalisation et audit | Vérification visuelle / politique organisationnelle requise |
| **3.1.10** | Choisir syslog_facility | 3.1. Journalisation des erreurs serveur | Vérification visuelle / politique organisationnelle requise |
| **3.1.14** | Assurer les bons messages dans le log serveur | 3.1. Journalisation des erreurs serveur | Vérification visuelle / politique organisationnelle requise |
| **3.1.15** | Enregistrer les SQL en erreur | 3.1. Journalisation des erreurs serveur | Vérification visuelle / politique organisationnelle requise |
| **4.1** | Désactiver la connexion interactive | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.2** | Configurer sudo correctement | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.3** | Révoquer les privilèges administratifs excessifs | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.4** | Verrouiller les comptes inactifs | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.5** | Révoquer les privilèges de fonction excessifs | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.6** | Révoquer les privilèges DML excessifs | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.7** | Configurer Row Level Security (RLS) | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.8** | Installer l’extension set_user | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.9** | Utiliser les rôles prédéfinis | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **5.1** | Ne pas passer de mot de passe en ligne de commande | 5. Connexion et authentification | Vérification visuelle / politique organisationnelle requise |
| **5.2** | Lier PostgreSQL à une adresse IP | 5. Connexion et authentification | Vérification visuelle / politique organisationnelle requise |
| **5.3** | Configurer la connexion UNIX locale | 5. Connexion et authentification | Vérification visuelle / politique organisationnelle requise |
| **5.4** | Configurer la connexion TCP/IP | 5. Connexion et authentification | Vérification visuelle / politique organisationnelle requise |
| **5.5** | Limites de connexion par compte | 5. Connexion et authentification | Vérification visuelle / politique organisationnelle requise |
| **5.6** | Configurer la complexité des mots de passe | 5. Connexion et authentification | Vérification visuelle / politique organisationnelle requise |
| **6.1** | Comprendre vecteurs d’attaque et paramètres runtime | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.2** | Configurer les paramètres backend | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.3** | Configurer Postmaster runtime parameters | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.4** | Configurer les signaux SIGHUP | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.5** | Configurer les paramètres Superuser | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.6** | Configurer les paramètres User | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.7** | Utiliser la cryptographie FIPS 140-2 | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.8** | Activer et configurer TLS | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.9** | Configurer TLSv1.3+ | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.10** | Désactiver les cipher suites faibles | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.11** | Installer et configurer pgcrypto | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **7.1** | Créer un utilisateur de réplication dédié | 7. Réplication | Vérification visuelle / politique organisationnelle requise |
| **7.2** | Journaliser les commandes de réplication | 7. Réplication | Vérification visuelle / politique organisationnelle requise |
| **7.3** | Configurer les sauvegardes de base | 7. Réplication | Vérification visuelle / politique organisationnelle requise |
| **7.4** | Configurer l’archivage WAL | 7. Réplication | Vérification visuelle / politique organisationnelle requise |
| **7.5** | Configurer les paramètres de streaming | 7. Réplication | Vérification visuelle / politique organisationnelle requise |
| **8.1** | Emplacements hors du cluster de données | 8. Considérations spéciales de configuration | Vérification visuelle / politique organisationnelle requise |
| **8.3** | Vérifier autres paramètres divers | 8. Considérations spéciales de configuration | Vérification visuelle / politique organisationnelle requise |

### 📋 POSTGRESQL_18 (`43` contrôles manuels)

| ID Règle | Nom du Contrôle | Catégorie | Note de Vérification |
| :---: | :--- | :--- | :--- |
| **1.1** | Obtenir les paquets depuis des dépôts autorisés | 1. Installation et correctifs | Vérification visuelle / politique organisationnelle requise |
| **1.2** | Installer uniquement les paquets requis | 1. Installation et correctifs | Vérification visuelle / politique organisationnelle requise |
| **1.5** | Appliquer les derniers correctifs de sécurité | 1. Installation et correctifs | Vérification visuelle / politique organisationnelle requise |
| **2.1** | Masque de permissions (umask) | 2. Permissions de répertoires et fichiers | Vérification visuelle / politique organisationnelle requise |
| **2.2** | Propriétaire et permissions du répertoire d’extensions | 2. Permissions de répertoires et fichiers | Vérification visuelle / politique organisationnelle requise |
| **2.4** | Ne pas stocker de mots de passe dans les fichiers de service | 2. Permissions de répertoires et fichiers | Vérification visuelle / politique organisationnelle requise |
| **3.2** | Activer l’extension pgAudit | 3. Journalisation et audit | Vérification visuelle / politique organisationnelle requise |
| **3.1.10** | Choisir syslog_facility | 3.1. Journalisation des erreurs serveur | Vérification visuelle / politique organisationnelle requise |
| **3.1.14** | Assurer les bons messages dans le log serveur | 3.1. Journalisation des erreurs serveur | Vérification visuelle / politique organisationnelle requise |
| **3.1.15** | Enregistrer les SQL en erreur | 3.1. Journalisation des erreurs serveur | Vérification visuelle / politique organisationnelle requise |
| **4.1** | Désactiver la connexion interactive | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.2** | Configurer sudo correctement | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.3** | Révoquer les privilèges administratifs excessifs | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.4** | Verrouiller les comptes inactifs | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.5** | Révoquer les privilèges de fonction excessifs | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.6** | Révoquer les privilèges DML excessifs | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.7** | Configurer Row Level Security (RLS) | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.8** | Installer l’extension set_user | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **4.9** | Utiliser les rôles prédéfinis | 4. Accès et autorisations utilisateur | Vérification visuelle / politique organisationnelle requise |
| **5.1** | Ne pas passer de mot de passe en ligne de commande | 5. Connexion et authentification | Vérification visuelle / politique organisationnelle requise |
| **5.2** | Lier PostgreSQL à une adresse IP | 5. Connexion et authentification | Vérification visuelle / politique organisationnelle requise |
| **5.3** | Configurer la connexion UNIX locale | 5. Connexion et authentification | Vérification visuelle / politique organisationnelle requise |
| **5.4** | Configurer la connexion TCP/IP | 5. Connexion et authentification | Vérification visuelle / politique organisationnelle requise |
| **5.5** | Limites de connexion par compte | 5. Connexion et authentification | Vérification visuelle / politique organisationnelle requise |
| **5.6** | Configurer la complexité des mots de passe | 5. Connexion et authentification | Vérification visuelle / politique organisationnelle requise |
| **6.1** | Comprendre vecteurs d’attaque et paramètres runtime | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.2** | Configurer les paramètres backend | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.3** | Configurer Postmaster runtime parameters | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.4** | Configurer les signaux SIGHUP | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.5** | Configurer les paramètres Superuser | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.6** | Configurer les paramètres User | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.7** | Utiliser la cryptographie FIPS 140-2 | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.8** | Activer et configurer TLS | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.9** | Configurer TLSv1.3+ | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.10** | Désactiver les cipher suites faibles | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **6.11** | Installer et configurer pgcrypto | 6. Paramètres PostgreSQL | Vérification visuelle / politique organisationnelle requise |
| **7.1** | Créer un utilisateur de réplication dédié | 7. Réplication | Vérification visuelle / politique organisationnelle requise |
| **7.2** | Journaliser les commandes de réplication | 7. Réplication | Vérification visuelle / politique organisationnelle requise |
| **7.3** | Configurer les sauvegardes de base | 7. Réplication | Vérification visuelle / politique organisationnelle requise |
| **7.4** | Configurer l’archivage WAL | 7. Réplication | Vérification visuelle / politique organisationnelle requise |
| **7.5** | Configurer les paramètres de streaming | 7. Réplication | Vérification visuelle / politique organisationnelle requise |
| **8.1** | Emplacements hors du cluster de données | 8. Considérations spéciales de configuration | Vérification visuelle / politique organisationnelle requise |
| **8.3** | Vérifier autres paramètres divers | 8. Considérations spéciales de configuration | Vérification visuelle / politique organisationnelle requise |
