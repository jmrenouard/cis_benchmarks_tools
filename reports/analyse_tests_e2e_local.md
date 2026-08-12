# 📊 CIS Benchmarks Suite - Analyse Spécifique Mode Local (-m local)

> **Rapport d'Analyse E2E (Mode Local (-m local)) généré le** : `2026-08-12 17:11:40`  
> **Moteur d'Audit** : `CIS Benchmarks Tools Suite v2.0.0` (100% Python Standard Library - PSL ONLY)  
> **Mode d'Exécution** : 💻 `Local`  
> **Périmètre** : 19 cibles d'audit évaluées dans ce mode

---

## 📈 Executive Dashboard (Mode Local (-m local))

| Cible / Benchmark | Mode | Date d'Exécution | Score Global | Total | Succès (PASS) | Échecs (FAIL) | Erreurs (ERROR) | Manuels (MANUAL) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **CASSANDRA_40** | 💻 `Local` | 2026-08-12 13:55:04 | 🟡 `50.0%` | 20 | 6 | 6 | 0 | 8 |
| **CASSANDRA_41** | 💻 `Local` | 2026-08-12 13:55:46 | 🔴 `41.7%` | 20 | 5 | 7 | 0 | 8 |
| **CASSANDRA_50** | 💻 `Local` | 2026-08-12 13:56:30 | 🔴 `41.7%` | 20 | 5 | 7 | 0 | 8 |
| **MARIADB_1011** | 💻 `Local` | 2026-08-12 14:59:18 | 🟡 `60.0%` | 75 | 25 | 18 | 0 | 32 |
| **MARIADB_106** | 💻 `Local` | 2026-08-12 14:58:00 | 🟡 `60.0%` | 74 | 25 | 18 | 0 | 31 |
| **MONGODB_7** | 💻 `Local` | 2026-08-12 14:33:12 | 🔴 `9.1%` | 23 | 1 | 10 | 0 | 12 |
| **MONGODB_8** | 💻 `Local` | 2026-08-12 14:33:33 | 🔴 `9.1%` | 23 | 1 | 10 | 0 | 12 |
| **MYSQL_80** | 💻 `Local` | 2026-08-12 15:00:36 | 🟡 `70.6%` | 70 | 6 | 5 | 0 | 59 |
| **MYSQL_80** | 💻 `Local` | 2026-08-11 19:34:32 | 🟡 `70.6%` | 70 | 6 | 5 | 0 | 59 |
| **MYSQL_COMMUNITY_84** | 💻 `Local` | 2026-08-12 15:01:51 | 🟡 `78.6%` | 79 | 7 | 3 | 0 | 69 |
| **MYSQL_COMMUNITY_97** | 💻 `Local` | 2026-08-12 15:04:30 | 🟡 `76.5%` | 70 | 7 | 4 | 0 | 59 |
| **MYSQL_ENTERPRISE_84** | 💻 `Local` | 2026-08-12 15:03:14 | 🟡 `76.5%` | 70 | 7 | 4 | 0 | 59 |
| **MYSQL_ENTERPRISE_97** | 💻 `Local` | 2026-08-12 15:05:46 | 🟡 `76.5%` | 70 | 7 | 4 | 0 | 59 |
| **POSTGRESQL_16** | 💻 `Local` | 2026-08-12 15:06:58 | 🟡 `78.6%` | 71 | 22 | 6 | 0 | 43 |
| **POSTGRESQL_17** | 💻 `Local` | 2026-08-12 15:07:48 | 🟡 `78.6%` | 71 | 22 | 6 | 0 | 43 |
| **POSTGRESQL_18** | 💻 `Local` | 2026-08-12 15:08:40 | 🟡 `78.6%` | 71 | 22 | 6 | 0 | 43 |
| **RHEL_10** | 💻 `Local` | 2026-08-11 19:36:19 | 🔴 `45.0%` | 20 | 9 | 11 | 0 | 0 |
| **RHEL_8** | 💻 `Local` | 2026-08-11 19:36:20 | 🔴 `45.0%` | 20 | 9 | 11 | 0 | 0 |
| **RHEL_9** | 💻 `Local` | 2026-08-11 19:36:22 | 🔴 `45.0%` | 20 | 9 | 11 | 0 | 0 |

### 📊 Statistiques Consolidées pour ce Mode

- **Nombre total de benchmarks évalués** : `19`
- **Nombre total de règles/contrôles vérifiés** : `957`
- **Score de conformité moyen** : `57.5%`
- **Contrôles en succès (`PASS`)** : `201` (21.0%)
- **Contrôles en échec (`FAIL`)** : `152` (15.9%)
- **Contrôles en erreur (`ERROR`)** : `0` (0.0%)
- **Contrôles manuels (`MANUAL`)** : `604` (63.1%)

---

## ❌ Registre Détaillé des Contrôles en Échec (`FAIL`) & Erreurs (`ERROR`) - Mode Local (-m local)

### 🛑 CASSANDRA_40 (`6` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **2.1** | 🔴 FAIL | S'assurer que l'authentification est activée pour les bases de données Cassandra | 2 Authentification et Autorisation | `Stdout:` | Modifier cassandra.yaml pour définir 'authenticator: PasswordAuthenticator' et redémarrer Cassandra. |
| **2.2** | 🔴 FAIL | S'assurer que l'autorisation est activée pour les bases de données Cassandra | 2 Authentification et Autorisation | `Stdout:` | Modifier cassandra.yaml pour définir 'authorizer: CassandraAuthorizer' et redémarrer Cassandra. |
| **3.1** | 🔴 FAIL | S'assurer que les rôles cassandra et superuser sont séparés | 3 Contrôle d'accès | `Stdout:` | Créer un nouveau rôle superuser, se connecter avec ce rôle, puis exécuter ALTER ROLE cassandra WITH  |
| **3.2** | 🔴 FAIL | S'assurer que le mot de passe par défaut du rôle cassandra est changé | 3 Contrôle d'accès | `Stdout:` | Se connecter et exécuter ALTER ROLE cassandra WITH PASSWORD = '<nouveau_mot_de_passe>'; |
| **3.4** | 🔴 FAIL | S'assurer que Cassandra est exécuté sous un compte de service dédié | 3 Contrôle d'accès | `Stdout:` | Configurer le service Cassandra pour qu'il s'exécute sous l'utilisateur 'cassandra'. |
| **5.1** | 🔴 FAIL | Chiffrement inter-nœuds | 5 Chiffrement | `Stdout:` | Configurer server_encryption_options dans cassandra.yaml : internode_encryption: all, et fournir les |

### 🛑 CASSANDRA_41 (`7` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.4** | 🔴 FAIL | S'assurer que la dernière version de Cassandra est installée | 1 Installation et Mises à jour | `Stdout:` | Mettre à jour Cassandra vers la dernière version 4.1.x. |
| **2.1** | 🔴 FAIL | S'assurer que l'authentification est activée pour les bases de données Cassandra | 2 Authentification et Autorisation | `Stdout:` | Modifier cassandra.yaml pour définir 'authenticator: PasswordAuthenticator' et redémarrer Cassandra. |
| **2.2** | 🔴 FAIL | S'assurer que l'autorisation est activée pour les bases de données Cassandra | 2 Authentification et Autorisation | `Stdout:` | Modifier cassandra.yaml pour définir 'authorizer: CassandraAuthorizer' et redémarrer Cassandra. |
| **3.1** | 🔴 FAIL | S'assurer que les rôles cassandra et superuser sont séparés | 3 Contrôle d'accès | `Stdout:` | Créer un nouveau rôle superuser, se connecter avec ce rôle, puis exécuter ALTER ROLE cassandra WITH  |
| **3.2** | 🔴 FAIL | S'assurer que le mot de passe par défaut du rôle cassandra est changé | 3 Contrôle d'accès | `Stdout:` | Se connecter et exécuter ALTER ROLE cassandra WITH PASSWORD = '<nouveau_mot_de_passe>'; |
| **3.4** | 🔴 FAIL | S'assurer que Cassandra est exécuté sous un compte de service dédié | 3 Contrôle d'accès | `Stdout:` | Configurer le service Cassandra pour qu'il s'exécute sous l'utilisateur 'cassandra'. |
| **5.1** | 🔴 FAIL | Chiffrement inter-nœuds | 5 Chiffrement | `Stdout:` | Configurer server_encryption_options dans cassandra.yaml : internode_encryption: all, et fournir les |

### 🛑 CASSANDRA_50 (`7` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.4** | 🔴 FAIL | S'assurer que la dernière version de Cassandra est installée | 1 Installation et Mises à jour | `Stdout:` | Mettre à jour Cassandra vers la dernière version 5.0.x. |
| **2.1** | 🔴 FAIL | S'assurer que l'authentification est activée pour les bases de données Cassandra | 2 Authentification et Autorisation | `Stdout:` | Modifier cassandra.yaml pour définir 'authenticator: PasswordAuthenticator' et redémarrer Cassandra. |
| **2.2** | 🔴 FAIL | S'assurer que l'autorisation est activée pour les bases de données Cassandra | 2 Authentification et Autorisation | `Stdout:` | Modifier cassandra.yaml pour définir 'authorizer: CassandraAuthorizer' et redémarrer Cassandra. |
| **3.1** | 🔴 FAIL | S'assurer que les rôles cassandra et superuser sont séparés | 3 Contrôle d'accès | `Stdout:` | Créer un nouveau rôle superuser, se connecter avec ce rôle, puis exécuter ALTER ROLE cassandra WITH  |
| **3.2** | 🔴 FAIL | S'assurer que le mot de passe par défaut du rôle cassandra est changé | 3 Contrôle d'accès | `Stdout:` | Se connecter et exécuter ALTER ROLE cassandra WITH PASSWORD = '<nouveau_mot_de_passe>'; |
| **3.4** | 🔴 FAIL | S'assurer que Cassandra est exécuté sous un compte de service dédié | 3 Contrôle d'accès | `Stdout:` | Configurer le service Cassandra pour qu'il s'exécute sous l'utilisateur 'cassandra'. |
| **5.1** | 🔴 FAIL | Chiffrement inter-nœuds | 5 Chiffrement | `Stdout:` | Configurer server_encryption_options dans cassandra.yaml : internode_encryption: all, et fournir les |

### 🛑 MARIADB_1011 (`18` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.3** | 🔴 FAIL | Désactiver l'historique des commandes MariaDB | 1. Configuration Système d'exploitation | `Stdout:` | Supprimer les fichiers d'historique, créer un lien symbolique vers /dev/null, ou configurer MYSQL_HI |
| **1.5** | 🔴 FAIL | Désactiver l'accès interactif pour l'utilisateur MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Modifier le shell de l'utilisateur mysql pour utiliser /bin/false ou /sbin/nologin (ex: usermod -s / |
| **2.12** | 🔴 FAIL | S'assurer que seuls les chiffrement approuvés sont utilisés | 2. Installation et Planification | `Stdout:` | Configurer ssl_cipher avec une liste de chiffrements approuvés dans mariadb.cnf. |
| **3.2** | 🔴 FAIL | Permissions sur les fichiers 'log_bin_basename' | 3. Permissions Fichiers | `Stdout:` | Appliquer chmod 600 sur les fichiers binaires. |
| **3.4** | 🔴 FAIL | Permissions sur 'slow_query_log' | 3. Permissions Fichiers | `Stdout:` | Limiter l'accès aux utilisateurs autorisés (ex: 640 ou 600). |
| **3.5** | 🔴 FAIL | Permissions sur 'relay_log_basename' | 3. Permissions Fichiers | `Stdout:` | Appliquer chmod 600. |
| **3.6** | 🔴 FAIL | Permissions sur 'general_log_file' | 3. Permissions Fichiers | `Stdout:` | Restreindre les droits d'accès (ex: 640 ou 600). |
| **3.7** | 🔴 FAIL | Permissions sur les fichiers de clés SSL | 3. Permissions Fichiers | `Stdout:` | Restreindre l'accès aux clés privées (ex: chmod 600) et s'assurer que le propriétaire est mysql. |
| **3.9** | 🔴 FAIL | Permissions sur 'server_audit_file_path' | 3. Permissions Fichiers | `Stdout:` | Appliquer des permissions restrictives (ex: 640 ou 600). |
| **3.10** | 🔴 FAIL | Permissions sur les fichiers du plugin File Key Management | 3. Permissions Fichiers | `Stdout:` | Restreindre l'accès aux fichiers de clés de chiffrement (chmod 640). |
| **4.9** | 🔴 FAIL | Activer le chiffrement des données au repos dans MariaDB | 4. Général | `Stdout:` | Configurer file_key_management plugin et innodb_encrypt_tables=ON dans mariadb.cnf. |
| **6.2** | 🔴 FAIL | Journal hors partition système | 6. Audit & Journalisation | `Stdout:` | Déplacer les répertoires des journaux (log-bin, log-error) hors des partitions système. |
| **6.4** | 🔴 FAIL | Activer la journalisation d'audit (server_audit) | 6. Audit & Journalisation | `Stdout:` | Installer et configurer le plugin server_audit : plugin_load_add=server_audit, server_audit_logging= |
| **6.5** | 🔴 FAIL | Interdire le déchargement du plugin d'audit | 6. Audit & Journalisation | `Stdout:` | Ajouter server_audit=FORCE_PLUS_PERMANENT dans mariadb.cnf. |
| **6.6** | 🔴 FAIL | Chiffrer les Binary et Relay Logs | 6. Audit & Journalisation | `Stdout:` | Ajouter encrypt_binlog=ON dans mariadb.cnf (nécessite un plugin de gestion de clés). |
| **7.3** | 🔴 FAIL | Authentification forte pour tous les comptes | 7. Authentification | `Stdout:` | Migrer les comptes vers ed25519, unix_socket ou d'autres plugins d'authentification forte. |
| **7.4** | 🔴 FAIL | Politique de complexité des mots de passe (simple_password_check) | 7. Authentification | `Stdout:` | Installer et configurer simple_password_check et cracklib_password_check. INSTALL SONAME 'simple_pas |
| **8.1** | 🔴 FAIL | Forcer SSL/TLS (require_secure_transport=ON et have_ssl=YES) | 8. Sécurité réseau | `Stdout:` | Configurer les certificats SSL/TLS, puis ajouter require_secure_transport=ON dans mariadb.cnf. |

### 🛑 MARIADB_106 (`18` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.3** | 🔴 FAIL | Désactiver l'historique des commandes MariaDB | 1. Configuration Système d'exploitation | `Stdout:` | Supprimer les fichiers d'historique, créer un lien symbolique vers /dev/null, ou configurer MYSQL_HI |
| **1.5** | 🔴 FAIL | Désactiver l'accès interactif pour l'utilisateur MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Modifier le shell de l'utilisateur mysql pour utiliser /bin/false ou /sbin/nologin (ex: usermod -s / |
| **2.12** | 🔴 FAIL | S'assurer que seuls les chiffrement approuvés sont utilisés | 2. Installation et Planification | `Stdout:` | Configurer ssl_cipher avec une liste de chiffrements approuvés dans mariadb.cnf. |
| **3.2** | 🔴 FAIL | Permissions sur les fichiers 'log_bin_basename' | 3. Permissions Fichiers | `Stdout:` | Appliquer chmod 600 sur les fichiers binaires. |
| **3.4** | 🔴 FAIL | Permissions sur 'slow_query_log' | 3. Permissions Fichiers | `Stdout:` | Limiter l'accès aux utilisateurs autorisés (ex: 640 ou 600). |
| **3.5** | 🔴 FAIL | Permissions sur 'relay_log_basename' | 3. Permissions Fichiers | `Stdout:` | Appliquer chmod 600. |
| **3.6** | 🔴 FAIL | Permissions sur 'general_log_file' | 3. Permissions Fichiers | `Stdout:` | Restreindre les droits d'accès (ex: 640 ou 600). |
| **3.7** | 🔴 FAIL | Permissions sur les fichiers de clés SSL | 3. Permissions Fichiers | `Stdout:` | Restreindre l'accès aux clés privées (ex: chmod 600) et s'assurer que le propriétaire est mysql. |
| **3.9** | 🔴 FAIL | Permissions sur 'server_audit_file_path' | 3. Permissions Fichiers | `Stdout:` | Appliquer des permissions restrictives (ex: 640 ou 600). |
| **3.10** | 🔴 FAIL | Permissions sur les fichiers du plugin File Key Management | 3. Permissions Fichiers | `Stdout:` | Restreindre l'accès aux fichiers de clés de chiffrement (chmod 640). |
| **4.9** | 🔴 FAIL | Activer le chiffrement des données au repos dans MariaDB | 4. Général | `Stdout:` | Configurer file_key_management plugin et innodb_encrypt_tables=ON dans mariadb.cnf. |
| **6.2** | 🔴 FAIL | Journal hors partition système | 6. Audit & Journalisation | `Stdout:` | Déplacer les répertoires des journaux (log-bin, log-error) hors des partitions système. |
| **6.4** | 🔴 FAIL | Activer la journalisation d'audit (server_audit) | 6. Audit & Journalisation | `Stdout:` | Installer et configurer le plugin server_audit : plugin_load_add=server_audit, server_audit_logging= |
| **6.5** | 🔴 FAIL | Interdire le déchargement du plugin d'audit | 6. Audit & Journalisation | `Stdout:` | Ajouter server_audit=FORCE_PLUS_PERMANENT dans mariadb.cnf. |
| **6.6** | 🔴 FAIL | Chiffrer les Binary et Relay Logs | 6. Audit & Journalisation | `Stdout:` | Ajouter encrypt_binlog=ON dans mariadb.cnf (nécessite un plugin de gestion de clés). |
| **7.3** | 🔴 FAIL | Authentification forte pour tous les comptes | 7. Authentification | `Stdout:` | Migrer les comptes vers ed25519, unix_socket ou d'autres plugins d'authentification forte. |
| **7.4** | 🔴 FAIL | Politique de complexité des mots de passe (simple_password_check) | 7. Authentification | `Stdout:` | Installer et configurer simple_password_check et cracklib_password_check. INSTALL SONAME 'simple_pas |
| **8.1** | 🔴 FAIL | Forcer SSL/TLS (require_secure_transport=ON et have_ssl=YES) | 8. Sécurité réseau | `Stdout:` | Configurer les certificats SSL/TLS, puis ajouter require_secure_transport=ON dans mariadb.cnf. |

### 🛑 MONGODB_7 (`10` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **2.1** | 🔴 FAIL | S'assurer que l'authentification est configurée | 2 Authentification | `Stdout:` | Démarrer l'instance sans authentification, créer un utilisateur administrateur, configurer 'security |
| **2.2** | 🔴 FAIL | S'assurer que MongoDB ne contourne pas l'authentification via l'exception localhost | 2 Authentification | `Stdout:` | Définir 'setParameter.enableLocalhostAuthBypass: false' dans le fichier de configuration ou exécuter |
| **2.3** | 🔴 FAIL | S'assurer que l'authentification est activée dans le cluster sharded | 2 Authentification | `Stdout:` | Configurer 'net.tls.mode: requireSSL', 'net.tls.PEMKeyFile', 'net.tls.CAFile', 'net.tls.clusterFile' |
| **4.1** | 🔴 FAIL | S'assurer que les protocoles TLS hérités sont désactivés | 4 Data Encryption | `Stdout:` | Définir 'net.tls.disabledProtocols: [TLS1_0, TLS1_1]' (ou équivalent) dans le fichier de configurati |
| **4.2** | 🔴 FAIL | S'assurer que les protocoles faibles sont désactivés | 4 Data Encryption | `Stdout:` | Définir 'net.ssl.disabledProtocols: TLS1_0, TLS1_1' dans le fichier de configuration et redémarrer. |
| **4.3** | 🔴 FAIL | S'assurer du chiffrement des données en transit TLS ou SSL (chiffrement de transport) | 4 Data Encryption | `Stdout:` | Définir 'net.tls.mode: requireTLS', 'net.tls.certificateKeyFile', 'net.tls.CAFile' dans le fichier d |
| **4.4** | 🔴 FAIL | S'assurer que la norme FIPS (Federal Information Processing Standard) est activée | 4 Data Encryption | `Stdout:` | Définir 'net.tls.FIPSMode: true' dans le fichier de configuration et redémarrer. |
| **5.1** | 🔴 FAIL | S'assurer que l'activité du système est auditée | 5 Audit Logging | `Stdout:` | Définir 'auditLog.destination' sur 'syslog', 'console' ou 'file' dans le fichier de configuration. |
| **5.3** | 🔴 FAIL | S'assurer que la journalisation capture autant d'informations que possible | 5 Audit Logging | `Stdout:` | Définir 'systemLog.quiet: false' dans le fichier de configuration. |
| **6.1** | 🔴 FAIL | S'assurer que MongoDB utilise un port non-standard | 6 Operating System Hardening | `Stdout:` | Changer le port 'net.port' dans le fichier de configuration pour un numéro autre que 27017. |

### 🛑 MONGODB_8 (`10` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **2.1** | 🔴 FAIL | S'assurer que l'authentification est configurée | 2 Authentification | `Stdout:` | Démarrer l'instance sans authentification, créer un utilisateur administrateur, configurer 'security |
| **2.2** | 🔴 FAIL | S'assurer que MongoDB ne contourne pas l'authentification via l'exception localhost | 2 Authentification | `Stdout:` | Définir 'setParameter.enableLocalhostAuthBypass: false' dans le fichier de configuration ou exécuter |
| **2.3** | 🔴 FAIL | S'assurer que l'authentification est activée dans le cluster sharded | 2 Authentification | `Stdout:` | Configurer 'net.tls.mode: requireSSL', 'net.tls.PEMKeyFile', 'net.tls.CAFile', 'net.tls.clusterFile' |
| **4.1** | 🔴 FAIL | S'assurer que les protocoles TLS hérités sont désactivés | 4 Data Encryption | `Stdout:` | Définir 'net.tls.disabledProtocols: [TLS1_0, TLS1_1]' (ou équivalent) dans le fichier de configurati |
| **4.2** | 🔴 FAIL | S'assurer que les protocoles faibles sont désactivés | 4 Data Encryption | `Stdout:` | Définir 'net.ssl.disabledProtocols: TLS1_0, TLS1_1' dans le fichier de configuration et redémarrer. |
| **4.3** | 🔴 FAIL | S'assurer du chiffrement des données en transit TLS ou SSL (chiffrement de transport) | 4 Data Encryption | `Stdout:` | Définir 'net.tls.mode: requireTLS', 'net.tls.certificateKeyFile', 'net.tls.CAFile' dans le fichier d |
| **4.4** | 🔴 FAIL | S'assurer que la norme FIPS (Federal Information Processing Standard) est activée | 4 Data Encryption | `Stdout:` | Définir 'net.tls.FIPSMode: true' dans le fichier de configuration et redémarrer. |
| **5.1** | 🔴 FAIL | S'assurer que l'activité du système est auditée | 5 Audit Logging | `Stdout:` | Définir 'auditLog.destination' sur 'syslog', 'console' ou 'file' dans le fichier de configuration. |
| **5.3** | 🔴 FAIL | S'assurer que la journalisation capture autant d'informations que possible | 5 Audit Logging | `Stdout:` | Définir 'systemLog.quiet: false' dans le fichier de configuration. |
| **6.1** | 🔴 FAIL | S'assurer que MongoDB utilise un port non-standard | 6 Operating System Hardening | `Stdout:` | Changer le port 'net.port' dans le fichier de configuration pour un numéro autre que 27017. |

### 🛑 MYSQL_80 (`5` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.3** | 🔴 FAIL | Désactiver l'historique des commandes MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Supprimer les fichiers d'historique, créer un lien symbolique vers /dev/null, ou configurer MYSQL_HI |
| **1.5** | 🔴 FAIL | Désactiver l'accès interactif pour l'utilisateur MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Modifier le shell de l'utilisateur mysql pour utiliser /bin/false ou /sbin/nologin (ex: usermod -s / |
| **2.1.1** | 🔴 FAIL | Politique de sauvegarde en place | 2. Installation et Planification | `Stdout:` | Créer une politique de sauvegarde et planifier des sauvegardes automatiques. |
| **6.8** | 🔴 FAIL | Interdire le déchargement du plugin audit | 6. Audit & Journalisation | `Stdout:` | Ajouter audit_log=FORCE_PLUS_PERMANENT dans my.cnf. |
| **7.2** | 🔴 FAIL | Aucun mot de passe dans le my.cnf global | 7. Authentification | `Stdout:` | Utiliser mysql_config_editor ou des fichiers .my.cnf privés avec permissions restreintes. |

### 🛑 MYSQL_80 (`5` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.2** | 🔴 FAIL | Utiliser un compte dédié et privilégié minimal pour MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Configurer le service MySQL pour qu'il s'exécute sous un utilisateur dédié (ex: 'mysql') avec les pr |
| **1.5** | 🔴 FAIL | Désactiver l'accès interactif pour l'utilisateur MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Modifier le shell de l'utilisateur mysql pour utiliser /bin/false ou /sbin/nologin (ex: usermod -s / |
| **1.7** | 🔴 FAIL | Exécuter MySQL dans un environnement sandbox | 1. Configuration Système d'exploitation | `Stdout:` | Configurer chroot, utiliser un service systemd avec un utilisateur spécifique, ou déployer MySQL sou |
| **2.1.1** | 🔴 FAIL | Politique de sauvegarde en place | 2. Installation et Planification | `Stdout:` | Créer une politique de sauvegarde et planifier des sauvegardes automatiques. |
| **6.8** | 🔴 FAIL | Interdire le déchargement du plugin audit | 6. Audit & Journalisation | `Stdout:` | Ajouter audit_log=FORCE_PLUS_PERMANENT dans my.cnf. |

### 🛑 MYSQL_COMMUNITY_84 (`3` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.3** | 🔴 FAIL | Désactiver l'historique des commandes MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Supprimer les fichiers d'historique, créer un lien symbolique vers /dev/null, ou configurer MYSQL_HI |
| **1.5** | 🔴 FAIL | Désactiver l'accès interactif pour l'utilisateur MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Modifier le shell de l'utilisateur mysql pour utiliser /bin/false ou /sbin/nologin (ex: usermod -s / |
| **2.1.1** | 🔴 FAIL | Politique de sauvegarde en place | 2. Installation et Planification | `Stdout:` | Créer une politique de sauvegarde et planifier des sauvegardes automatiques. |

### 🛑 MYSQL_COMMUNITY_97 (`4` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.3** | 🔴 FAIL | Désactiver l'historique des commandes MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Supprimer les fichiers d'historique, créer un lien symbolique vers /dev/null, ou configurer MYSQL_HI |
| **1.5** | 🔴 FAIL | Désactiver l'accès interactif pour l'utilisateur MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Modifier le shell de l'utilisateur mysql pour utiliser /bin/false ou /sbin/nologin (ex: usermod -s / |
| **2.1.1** | 🔴 FAIL | Politique de sauvegarde en place | 2. Installation et Planification | `Stdout:` | Créer une politique de sauvegarde et planifier des sauvegardes automatiques. |
| **6.8** | 🔴 FAIL | Interdire le déchargement du plugin audit | 6. Audit & Journalisation | `Stdout:` | Ajouter audit_log=FORCE_PLUS_PERMANENT dans my.cnf. |

### 🛑 MYSQL_ENTERPRISE_84 (`4` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.3** | 🔴 FAIL | Désactiver l'historique des commandes MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Supprimer les fichiers d'historique, créer un lien symbolique vers /dev/null, ou configurer MYSQL_HI |
| **1.5** | 🔴 FAIL | Désactiver l'accès interactif pour l'utilisateur MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Modifier le shell de l'utilisateur mysql pour utiliser /bin/false ou /sbin/nologin (ex: usermod -s / |
| **2.1.1** | 🔴 FAIL | Politique de sauvegarde en place | 2. Installation et Planification | `Stdout:` | Créer une politique de sauvegarde et planifier des sauvegardes automatiques. |
| **6.8** | 🔴 FAIL | Interdire le déchargement du plugin audit | 6. Audit & Journalisation | `Stdout:` | Ajouter audit_log=FORCE_PLUS_PERMANENT dans my.cnf. |

### 🛑 MYSQL_ENTERPRISE_97 (`4` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.3** | 🔴 FAIL | Désactiver l'historique des commandes MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Supprimer les fichiers d'historique, créer un lien symbolique vers /dev/null, ou configurer MYSQL_HI |
| **1.5** | 🔴 FAIL | Désactiver l'accès interactif pour l'utilisateur MySQL | 1. Configuration Système d'exploitation | `Stdout:` | Modifier le shell de l'utilisateur mysql pour utiliser /bin/false ou /sbin/nologin (ex: usermod -s / |
| **2.1.1** | 🔴 FAIL | Politique de sauvegarde en place | 2. Installation et Planification | `Stdout:` | Créer une politique de sauvegarde et planifier des sauvegardes automatiques. |
| **6.8** | 🔴 FAIL | Interdire le déchargement du plugin audit | 6. Audit & Journalisation | `Stdout:` | Ajouter audit_log=FORCE_PLUS_PERMANENT dans my.cnf. |

### 🛑 POSTGRESQL_16 (`6` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.3** | 🔴 FAIL | Activer le service systemd | 1. Installation et correctifs | `Stdout:` | systemctl enable postgresql@16-main \|\| systemctl enable postgresql-16 |
| **1.4** | 🔴 FAIL | Initialiser correctement le cluster de données | 1. Installation et correctifs | `--- Command 1: systemctl is-active postgresql@16-main.service \|\| systemctl is-ac` | Supprimer le répertoire de données et relancer initdb (avec checksums si souhaité), puis démarrer le |
| **2.3** | 🔴 FAIL | Désactiver l’historique des commandes psql | 2. Permissions de répertoires et fichiers | `Stdout:` | Empêcher la création de ~/.psql_history pour limiter l’exposition de données sensibles. |
| **3.1.22** | 🔴 FAIL | Configurer log_error_verbosity | 3.1. Journalisation des erreurs serveur | `Stdout:` | Contrôler la verbosité des messages d’erreur (DEFAULT, VERBOSE). |
| **3.1.24** | 🔴 FAIL | Configurer log_line_prefix | 3.1. Journalisation des erreurs serveur | `Stdout:` | Définir le préfixe de ligne (timestamp, utilisateur, base, etc.) dans chaque log. |
| **8.2** | 🔴 FAIL | Installer/configurer pgBackRest | 8. Considérations spéciales de configuration | `Stdout:` | Utiliser pgBackRest pour des sauvegardes et restaurations robustes. |

### 🛑 POSTGRESQL_17 (`6` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.3** | 🔴 FAIL | Activer le service systemd | 1. Installation et correctifs | `Stdout:` | systemctl enable postgresql@17-main \|\| systemctl enable postgresql-17 |
| **1.4** | 🔴 FAIL | Initialiser correctement le cluster de données | 1. Installation et correctifs | `--- Command 1: systemctl is-active postgresql@17-main.service \|\| systemctl is-ac` | Supprimer le répertoire de données et relancer initdb (avec checksums si souhaité), puis démarrer le |
| **2.3** | 🔴 FAIL | Désactiver l’historique des commandes psql | 2. Permissions de répertoires et fichiers | `Stdout:` | Empêcher la création de ~/.psql_history pour limiter l’exposition de données sensibles. |
| **3.1.22** | 🔴 FAIL | Configurer log_error_verbosity | 3.1. Journalisation des erreurs serveur | `Stdout:` | Contrôler la verbosité des messages d’erreur (DEFAULT, VERBOSE). |
| **3.1.24** | 🔴 FAIL | Configurer log_line_prefix | 3.1. Journalisation des erreurs serveur | `Stdout:` | Définir le préfixe de ligne (timestamp, utilisateur, base, etc.) dans chaque log. |
| **8.2** | 🔴 FAIL | Installer/configurer pgBackRest | 8. Considérations spéciales de configuration | `Stdout:` | Utiliser pgBackRest pour des sauvegardes et restaurations robustes. |

### 🛑 POSTGRESQL_18 (`6` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.3** | 🔴 FAIL | Activer le service systemd | 1. Installation et correctifs | `Stdout:` | systemctl enable postgresql@18-main \|\| systemctl enable postgresql-18 |
| **1.4** | 🔴 FAIL | Initialiser correctement le cluster de données | 1. Installation et correctifs | `--- Command 1: systemctl is-active postgresql@18-main.service \|\| systemctl is-ac` | Supprimer le répertoire de données et relancer initdb (avec checksums si souhaité), puis démarrer le |
| **2.3** | 🔴 FAIL | Désactiver l’historique des commandes psql | 2. Permissions de répertoires et fichiers | `Stdout:` | Empêcher la création de ~/.psql_history pour limiter l’exposition de données sensibles. |
| **3.1.22** | 🔴 FAIL | Configurer log_error_verbosity | 3.1. Journalisation des erreurs serveur | `Stdout:` | Contrôler la verbosité des messages d’erreur (DEFAULT, VERBOSE). |
| **3.1.24** | 🔴 FAIL | Configurer log_line_prefix | 3.1. Journalisation des erreurs serveur | `Stdout:` | Définir le préfixe de ligne (timestamp, utilisateur, base, etc.) dans chaque log. |
| **8.2** | 🔴 FAIL | Installer/configurer pgBackRest | 8. Considérations spéciales de configuration | `Stdout:` | Utiliser pgBackRest pour des sauvegardes et restaurations robustes. |

### 🛑 RHEL_10 (`11` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.1.1.1** | 🔴 FAIL | Ensure cramfs kernel module is not available | Initial Setup | `insmod /lib/modules/6.18.33.2-microsoft-standard-WSL2/kernel/fs/cramfs/cramfs.ko` | N/A |
| **1.3.1.1** | 🔴 FAIL | Ensure SELinux is installed and active | Initial Setup | `Aucune sortie` | N/A |
| **1.3.1.2** | 🔴 FAIL | Ensure SELinux state is enforcing | Initial Setup | `Aucune sortie` | N/A |
| **1.4.1** | 🔴 FAIL | Ensure AIDE is installed | Initial Setup | `Aucune sortie` | N/A |
| **2.1.1** | 🔴 FAIL | Ensure xinetd is not installed | Services | `Aucune sortie` | N/A |
| **2.2.1** | 🔴 FAIL | Ensure telnet server is not installed | Services | `Aucune sortie` | N/A |
| **3.1.1** | 🔴 FAIL | Ensure IP forwarding is disabled | Network Configuration | `net.ipv4.ip_forward = 1` | N/A |
| **3.1.2** | 🔴 FAIL | Ensure packet redirect sending is disabled | Network Configuration | `net.ipv4.conf.all.send_redirects = 1` | N/A |
| **5.2.1** | 🔴 FAIL | Ensure SSH PermitRootLogin is disabled | Access Control | `Aucune sortie` | N/A |
| **5.2.2** | 🔴 FAIL | Ensure SSH PermitEmptyPasswords is disabled | Access Control | `Aucune sortie` | N/A |
| **5.3.1** | 🔴 FAIL | Ensure crypto policy is DEFAULT or FUTURE | System Cryptography | `Aucune sortie` | N/A |

### 🛑 RHEL_8 (`11` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.1.1.1** | 🔴 FAIL | Ensure cramfs kernel module is not available | Initial Setup | `insmod /lib/modules/6.18.33.2-microsoft-standard-WSL2/kernel/fs/cramfs/cramfs.ko` | N/A |
| **1.3.1.1** | 🔴 FAIL | Ensure SELinux is installed and active | Initial Setup | `Aucune sortie` | N/A |
| **1.3.1.2** | 🔴 FAIL | Ensure SELinux state is enforcing | Initial Setup | `Aucune sortie` | N/A |
| **1.4.1** | 🔴 FAIL | Ensure AIDE is installed | Initial Setup | `Aucune sortie` | N/A |
| **2.1.1** | 🔴 FAIL | Ensure xinetd is not installed | Services | `Aucune sortie` | N/A |
| **2.2.1** | 🔴 FAIL | Ensure telnet server is not installed | Services | `Aucune sortie` | N/A |
| **3.1.1** | 🔴 FAIL | Ensure IP forwarding is disabled | Network Configuration | `net.ipv4.ip_forward = 1` | N/A |
| **3.1.2** | 🔴 FAIL | Ensure packet redirect sending is disabled | Network Configuration | `net.ipv4.conf.all.send_redirects = 1` | N/A |
| **5.2.1** | 🔴 FAIL | Ensure SSH PermitRootLogin is disabled | Access Control | `Aucune sortie` | N/A |
| **5.2.2** | 🔴 FAIL | Ensure SSH PermitEmptyPasswords is disabled | Access Control | `Aucune sortie` | N/A |
| **5.3.1** | 🔴 FAIL | Ensure password hashing algorithm is SHA-512 | Access Control | `Aucune sortie` | N/A |

### 🛑 RHEL_9 (`11` échecs / erreurs)

| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1.1.1.1** | 🔴 FAIL | Ensure cramfs kernel module is not available | Initial Setup | `insmod /lib/modules/6.18.33.2-microsoft-standard-WSL2/kernel/fs/cramfs/cramfs.ko` | N/A |
| **1.3.1.1** | 🔴 FAIL | Ensure SELinux is installed and active | Initial Setup | `Aucune sortie` | N/A |
| **1.3.1.2** | 🔴 FAIL | Ensure SELinux state is enforcing | Initial Setup | `Aucune sortie` | N/A |
| **1.4.1** | 🔴 FAIL | Ensure AIDE is installed | Initial Setup | `Aucune sortie` | N/A |
| **2.1.1** | 🔴 FAIL | Ensure xinetd is not installed | Services | `Aucune sortie` | N/A |
| **2.2.1** | 🔴 FAIL | Ensure telnet server is not installed | Services | `Aucune sortie` | N/A |
| **3.1.1** | 🔴 FAIL | Ensure IP forwarding is disabled | Network Configuration | `net.ipv4.ip_forward = 1` | N/A |
| **3.1.2** | 🔴 FAIL | Ensure packet redirect sending is disabled | Network Configuration | `net.ipv4.conf.all.send_redirects = 1` | N/A |
| **5.2.1** | 🔴 FAIL | Ensure SSH PermitRootLogin is disabled | Access Control | `Aucune sortie` | N/A |
| **5.2.2** | 🔴 FAIL | Ensure SSH PermitEmptyPasswords is disabled | Access Control | `Aucune sortie` | N/A |
| **5.3.1** | 🔴 FAIL | Ensure crypto policy is DEFAULT or FUTURE | System Cryptography | `Aucune sortie` | N/A |

---

## ⚠️ Registre Détaillé des Contrôles Manuels (`MANUAL`) - Mode Local (-m local)

### 📋 CASSANDRA_40 (`8` contrôles manuels)

| ID Règle | Nom du Contrôle | Catégorie | Note de Vérification |
| :---: | :--- | :--- | :--- |
| **1.1** | S'assurer qu'un utilisateur et un groupe dédiés existent pour Cassandra | 1 Installation et Mises à jour | Vérification visuelle / politique organisationnelle requise |
| **1.6** | S'assurer que les horloges sont synchronisées sur tous les nœuds | 1 Installation et Mises à jour | Vérification visuelle / politique organisationnelle requise |
| **3.3** | S'assurer qu'il n'y a pas de rôles ou privilèges excessifs | 3 Contrôle d'accès | Vérification visuelle / politique organisationnelle requise |
| **3.5** | S'assurer que Cassandra n'écoute que sur les interfaces autorisées | 3 Contrôle d'accès | Vérification visuelle / politique organisationnelle requise |
| **3.6** | S'assurer que les autorisations Data Center sont activées | 3 Contrôle d'accès | Vérification visuelle / politique organisationnelle requise |
| **3.7** | Réviser les rôles définis par l'utilisateur | 3 Contrôle d'accès | Vérification visuelle / politique organisationnelle requise |
| **3.8** | Réviser les rôles superuser/administrateur | 3 Contrôle d'accès | Vérification visuelle / politique organisationnelle requise |
| **4.2** | S'assurer que l'audit est activé | 4 Audit et Journalisation | Vérification visuelle / politique organisationnelle requise |

### 📋 CASSANDRA_41 (`8` contrôles manuels)

| ID Règle | Nom du Contrôle | Catégorie | Note de Vérification |
| :---: | :--- | :--- | :--- |
| **1.1** | S'assurer qu'un utilisateur et un groupe dédiés existent pour Cassandra | 1 Installation et Mises à jour | Vérification visuelle / politique organisationnelle requise |
| **1.6** | S'assurer que les horloges sont synchronisées sur tous les nœuds | 1 Installation et Mises à jour | Vérification visuelle / politique organisationnelle requise |
| **3.3** | S'assurer qu'il n'y a pas de rôles ou privilèges excessifs | 3 Contrôle d'accès | Vérification visuelle / politique organisationnelle requise |
| **3.5** | S'assurer que Cassandra n'écoute que sur les interfaces autorisées | 3 Contrôle d'accès | Vérification visuelle / politique organisationnelle requise |
| **3.6** | S'assurer que les autorisations Data Center sont activées | 3 Contrôle d'accès | Vérification visuelle / politique organisationnelle requise |
| **3.7** | Réviser les rôles définis par l'utilisateur | 3 Contrôle d'accès | Vérification visuelle / politique organisationnelle requise |
| **3.8** | Réviser les rôles superuser/administrateur | 3 Contrôle d'accès | Vérification visuelle / politique organisationnelle requise |
| **4.2** | S'assurer que l'audit est activé | 4 Audit et Journalisation | Vérification visuelle / politique organisationnelle requise |

### 📋 CASSANDRA_50 (`8` contrôles manuels)

| ID Règle | Nom du Contrôle | Catégorie | Note de Vérification |
| :---: | :--- | :--- | :--- |
| **1.1** | S'assurer qu'un utilisateur et un groupe dédiés existent pour Cassandra | 1 Installation et Mises à jour | Vérification visuelle / politique organisationnelle requise |
| **1.6** | S'assurer que les horloges sont synchronisées sur tous les nœuds | 1 Installation et Mises à jour | Vérification visuelle / politique organisationnelle requise |
| **3.3** | S'assurer qu'il n'y a pas de rôles ou privilèges excessifs | 3 Contrôle d'accès | Vérification visuelle / politique organisationnelle requise |
| **3.5** | S'assurer que Cassandra n'écoute que sur les interfaces autorisées | 3 Contrôle d'accès | Vérification visuelle / politique organisationnelle requise |
| **3.6** | S'assurer que les autorisations Data Center sont activées | 3 Contrôle d'accès | Vérification visuelle / politique organisationnelle requise |
| **3.7** | Réviser les rôles définis par l'utilisateur | 3 Contrôle d'accès | Vérification visuelle / politique organisationnelle requise |
| **3.8** | Réviser les rôles superuser/administrateur | 3 Contrôle d'accès | Vérification visuelle / politique organisationnelle requise |
| **4.2** | S'assurer que l'audit est activé | 4 Audit et Journalisation | Vérification visuelle / politique organisationnelle requise |

### 📋 MARIADB_1011 (`32` contrôles manuels)

| ID Règle | Nom du Contrôle | Catégorie | Note de Vérification |
| :---: | :--- | :--- | :--- |
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
| **3.3** | Permissions sur 'log_error' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
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
| **7.7** | Empêcher la réutilisation des mots de passe (password_reuse_check) | 7. Authentification | Vérification visuelle / politique organisationnelle requise |
| **8.3** | Limiter le nombre de connexions | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **9.1** | Chiffrer le trafic de réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.2** | MASTER_SSL_VERIFY_SERVER_CERT activé | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.3** | Pas de SUPER pour les utilisateurs de réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.4** | Chiffrement approuvé pour la réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.5** | TLS mutuel activé pour la réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |

### 📋 MARIADB_106 (`31` contrôles manuels)

| ID Règle | Nom du Contrôle | Catégorie | Note de Vérification |
| :---: | :--- | :--- | :--- |
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
| **3.3** | Permissions sur 'log_error' | 3. Permissions Fichiers | Vérification visuelle / politique organisationnelle requise |
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
| **8.3** | Limiter le nombre de connexions | 8. Sécurité réseau | Vérification visuelle / politique organisationnelle requise |
| **9.1** | Chiffrer le trafic de réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.2** | MASTER_SSL_VERIFY_SERVER_CERT activé | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.3** | Pas de SUPER pour les utilisateurs de réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.4** | Chiffrement approuvé pour la réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |
| **9.5** | TLS mutuel activé pour la réplication | 9. Réplication | Vérification visuelle / politique organisationnelle requise |

### 📋 MONGODB_7 (`12` contrôles manuels)

| ID Règle | Nom du Contrôle | Catégorie | Note de Vérification |
| :---: | :--- | :--- | :--- |
| **1.1** | S'assurer que la version/les correctifs appropriés de MongoDB sont installés | 1 Installation et Patching | Vérification visuelle / politique organisationnelle requise |
| **3.1** | S'assurer du moindre privilège pour les comptes de base de données | 3 Authorization | Vérification visuelle / politique organisationnelle requise |
| **3.2** | S'assurer que le contrôle d'accès basé sur les rôles est activé et configuré correctement | 3 Authorization | Vérification visuelle / politique organisationnelle requise |
| **3.3** | S'assurer que MongoDB est exécuté en utilisant un compte de service dédié et non privilégié | 3 Authorization | Vérification visuelle / politique organisationnelle requise |
| **3.4** | S'assurer que chaque rôle pour chaque base de données MongoDB est nécessaire et n'accorde que les privilèges nécessaires | 3 Authorization | Vérification visuelle / politique organisationnelle requise |
| **3.5** | Réviser les rôles de superutilisateur/administrateur | 3 Authorization | Vérification visuelle / politique organisationnelle requise |
| **4.5** | S'assurer du chiffrement des données au repos | 4 Data Encryption | Vérification visuelle / politique organisationnelle requise |
| **5.2** | S'assurer que les filtres d'audit sont configurés correctement | 5 Audit Logging | Vérification visuelle / politique organisationnelle requise |
| **6.2** | S'assurer que les limites de ressources du système d'exploitation sont définies pour MongoDB | 6 Operating System Hardening | Vérification visuelle / politique organisationnelle requise |
| **6.3** | S'assurer que le script côté serveur est désactivé si non nécessaire | 6 Operating System Hardening | Vérification visuelle / politique organisationnelle requise |
| **7.1** | S'assurer que les permissions appropriées du fichier de clés sont définies | 7 File Permissions | Vérification visuelle / politique organisationnelle requise |
| **7.2** | S'assurer que les permissions appropriées du fichier de base de données sont définies | 7 File Permissions | Vérification visuelle / politique organisationnelle requise |

### 📋 MONGODB_8 (`12` contrôles manuels)

| ID Règle | Nom du Contrôle | Catégorie | Note de Vérification |
| :---: | :--- | :--- | :--- |
| **1.1** | S'assurer que la version/les correctifs appropriés de MongoDB sont installés | 1 Installation et Patching | Vérification visuelle / politique organisationnelle requise |
| **3.1** | S'assurer du moindre privilège pour les comptes de base de données | 3 Authorization | Vérification visuelle / politique organisationnelle requise |
| **3.2** | S'assurer que le contrôle d'accès basé sur les rôles est activé et configuré correctement | 3 Authorization | Vérification visuelle / politique organisationnelle requise |
| **3.3** | S'assurer que MongoDB est exécuté en utilisant un compte de service dédié et non privilégié | 3 Authorization | Vérification visuelle / politique organisationnelle requise |
| **3.4** | S'assurer que chaque rôle pour chaque base de données MongoDB est nécessaire et n'accorde que les privilèges nécessaires | 3 Authorization | Vérification visuelle / politique organisationnelle requise |
| **3.5** | Réviser les rôles de superutilisateur/administrateur | 3 Authorization | Vérification visuelle / politique organisationnelle requise |
| **4.5** | S'assurer du chiffrement des données au repos | 4 Data Encryption | Vérification visuelle / politique organisationnelle requise |
| **5.2** | S'assurer que les filtres d'audit sont configurés correctement | 5 Audit Logging | Vérification visuelle / politique organisationnelle requise |
| **6.2** | S'assurer que les limites de ressources du système d'exploitation sont définies pour MongoDB | 6 Operating System Hardening | Vérification visuelle / politique organisationnelle requise |
| **6.3** | S'assurer que le script côté serveur est désactivé si non nécessaire | 6 Operating System Hardening | Vérification visuelle / politique organisationnelle requise |
| **7.1** | S'assurer que les permissions appropriées du fichier de clés sont définies | 7 File Permissions | Vérification visuelle / politique organisationnelle requise |
| **7.2** | S'assurer que les permissions appropriées du fichier de base de données sont définies | 7 File Permissions | Vérification visuelle / politique organisationnelle requise |

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
