# -*- coding: utf-8 -*-
import argparse
import subprocess
import json
import os
from datetime import datetime
import re # Pour les expressions régulières
import html # Pour échapper les caractères spéciaux HTML

# --- Configuration ---
# Adapte cette commande si nécessaire pour te connecter à MariaDB
# Par exemple, ajoute -u <user> -p<password> ou utilise un fichier de configuration
# Pour l'instant, on suppose que la connexion fonctionne sans mot de passe
# ou via un fichier de configuration (ex: /root/.my.cnf)
MYSQL_CMD = "mysql -N -B" # -N: skip headers, -B: batch mode (tab separated)

# --- Structure des Recommandations (Adaptée pour MariaDB 10.6) ---
# Basée sur le CIS MariaDB 10.6 Benchmark v1.1.0
RECOMMENDATIONS_DATA = [
    # Category 1: Configuration Système d'exploitation
    {"category": "1. Configuration Système d'exploitation", "number": "1.1", "name": "Placer les bases de données sur des partitions non-système", "type": "Automated", "path_command": f"{MYSQL_CMD} -e \"SELECT @@datadir;\"", "test_procedure_template": "df -P {path} | awk 'NR==2 {{print $6}}'", "expected_output": {"type": "stdout_not_equals", "value": "/"}, "remediation": "Sauvegarder la base, déplacer les fichiers de données vers une partition dédiée, mettre à jour datadir dans la configuration MariaDB, redémarrer le service."},
    {"category": "1. Configuration Système d'exploitation", "number": "1.2", "name": "Utiliser un compte dédié et privilégié minimal pour MariaDB", "type": "Automated", "test_procedure": "ps -ef | grep -E 'mysqld|mariadbd' | grep -v grep | awk '{print $1}' | head -n 1", "expected_output": {"type": "stdout_equals", "value": "mysql"}, "remediation": "Configurer le service MariaDB pour qu'il s'exécute sous un utilisateur dédié (ex: 'mysql') avec les privilèges minimaux."},
    {"category": "1. Configuration Système d'exploitation", "number": "1.3", "name": "Désactiver l'historique des commandes MariaDB", "type": "Automated", "test_procedure": "! find /home /root -name .mysql_history -print -quit 2>/dev/null", "expected_output": {"type": "returncode_zero"}, "remediation": "Supprimer les fichiers d'historique, créer un lien symbolique vers /dev/null, ou configurer MYSQL_HISTFILE."},
    {"category": "1. Configuration Système d'exploitation", "number": "1.4", "name": "Vérifier que MYSQL_PWD n'est pas utilisé", "type": "Automated", "test_procedure": "! grep -qs MYSQL_PWD /proc/*/environ", "expected_output": {"type": "returncode_zero"}, "remediation": "Modifier les scripts/utilisateurs pour éviter MYSQL_PWD, utiliser des méthodes d'authentification sécurisées."},
    {"category": "1. Configuration Système d'exploitation", "number": "1.5", "name": "Désactiver l'accès interactif pour l'utilisateur MySQL", "type": "Automated", "test_procedure": "getent passwd mysql | cut -d: -f7", "expected_output": {"type": "stdout_contains_any", "values": ["/bin/false", "/sbin/nologin"]}, "remediation": "Modifier le shell de l'utilisateur mysql pour utiliser /bin/false ou /sbin/nologin (ex: usermod -s /sbin/nologin mysql)."},
    {"category": "1. Configuration Système d'exploitation", "number": "1.6", "name": "Vérifier que MYSQL_PWD n'est pas dans les profils utilisateurs", "type": "Automated", "test_procedure": "! grep -qs MYSQL_PWD /home/*/.{bashrc,profile,bash_profile} /root/.{bashrc,profile,bash_profile} /etc/environment 2>/dev/null", "expected_output": {"type": "returncode_zero"}, "remediation": "Nettoyer les fichiers de login des utilisateurs pour supprimer MYSQL_PWD."},
    {"category": "1. Configuration Système d'exploitation", "number": "1.7", "name": "Exécuter MariaDB dans un environnement sandbox", "type": "Manual", "test_procedure": "[[ -f /.dockerenv ]] && echo 'DOCKER' || echo 'NOT_SANDBOX'", "expected_output": None, "remediation": "Configurer chroot, utiliser un service systemd avec un utilisateur spécifique, ou déployer MariaDB sous Docker.", "manual_steps": ["Vérifier si MariaDB utilise chroot.", "Vérifier si MariaDB est géré par systemd.", "Vérifier si MariaDB fonctionne dans un conteneur Docker."]},

    # Category 2: Installation et Planification
    {"category": "2. Installation et Planification", "number": "2.1.1", "name": "Politique de sauvegarde en place", "type": "Manual", "test_procedure": "crontab -l 2>/dev/null | grep -E 'mariabackup|mysqldump|xtrabackup' || echo 'AUCUNE_SAUVEGARDE_PLANIFIEE'", "expected_output": None, "remediation": "Créer une politique de sauvegarde et planifier des sauvegardes automatiques.", "manual_steps": ["Vérifier la présence d'un cron de sauvegarde.", "Confirmer l'utilisation de mariabackup ou mysqldump.", "Documenter la politique de sauvegarde."]},
    {"category": "2. Installation et Planification", "number": "2.1.2", "name": "Validation des sauvegardes", "type": "Manual", "test_procedure": "Analyser les rapports de tests de restauration.", "expected_output": None, "remediation": "Planifier et documenter les tests de restauration périodiques.", "manual_steps": ["Identifier les fichiers de sauvegarde récents.", "Restaurer une base de test à partir de ces fichiers.", "Vérifier l'intégrité des données.", "Documenter la date et le résultat du test."]},
    {"category": "2. Installation et Planification", "number": "2.1.3", "name": "Sécuriser les identifiants de sauvegarde", "type": "Manual", "test_procedure": "Inspecter les permissions des fichiers contenant les credentials de sauvegarde.", "expected_output": None, "remediation": "Restreindre les droits fichiers, utiliser des keystores ou du chiffrement.", "manual_steps": ["Rechercher les scripts de sauvegarde.", "Vérifier si les mots de passe sont en clair.", "S'assurer que les fichiers de config (.my.cnf) ont des droits 600."]},
    {"category": "2. Installation et Planification", "number": "2.1.4", "name": "Sécuriser les fichiers de sauvegarde", "type": "Manual", "test_procedure": "Examiner les permissions et la présence de chiffrement sur les fichiers de sauvegarde.", "expected_output": None, "remediation": "Utiliser le chiffrement des sauvegardes (mariabackup + openssl enc).", "manual_steps": ["Localiser le stockage des sauvegardes.", "Vérifier les ACLs.", "Confirmer que les fichiers sont chiffrés au repos (AES-256/GPG)."]},
    {"category": "2. Installation et Planification", "number": "2.1.5", "name": "Point-in-Time Recovery", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT VARIABLE_VALUE FROM information_schema.global_variables WHERE variable_name = 'binlog_expire_logs_seconds';\"", "expected_output": {"type": "stdout_is_numeric_greater_than", "value": 0}, "remediation": "Activer les binlogs, configurer binlog_expire_logs_seconds dans mariadb.cnf, tester les restaurations PITR."},
    {"category": "2. Installation et Planification", "number": "2.1.6", "name": "Plan de reprise d'activité (DR)", "type": "Manual", "test_procedure": "Vérifier l'existence et la validité du plan DR.", "expected_output": None, "remediation": "Documenter et tester un plan DR incluant réplication Galera, backups offsite.", "manual_steps": ["Consulter la documentation technique.", "Vérifier la présence d'une procédure de basculement.", "Confirmer la réplication hors-site."]},
    {"category": "2. Installation et Planification", "number": "2.1.7", "name": "Sauvegarde des fichiers de configuration", "type": "Manual", "test_procedure": "Contrôler la liste des fichiers inclus dans la sauvegarde (mariadb.cnf, clés SSL, etc.).", "expected_output": None, "remediation": "Ajouter tous les fichiers essentiels à la stratégie de sauvegarde.", "manual_steps": ["Lister le contenu d'une sauvegarde complète.", "Vérifier la présence de /etc/mysql/mariadb.cnf et des certificats SSL."]},
    {"category": "2. Installation et Planification", "number": "2.2", "name": "Dédier la machine à MariaDB", "type": "Manual", "test_procedure": "Vérifier les services actifs sur la machine.", "expected_output": None, "remediation": "Utiliser un serveur dédié ou un conteneur pour MariaDB.", "manual_steps": ["Lister les services actifs (systemctl list-units --type=service).", "S'assurer qu'aucun autre service de base de données ou applicatif majeur ne tourne."]},
    {"category": "2. Installation et Planification", "number": "2.3", "name": "Ne pas spécifier de mots de passe en ligne de commande", "type": "Manual", "test_procedure": "ps -ef | grep -E 'mysql|mariadb' | grep -v grep | grep -E '\\-p[^ ]'", "expected_output": None, "remediation": "Utiliser des fichiers d'options (.my.cnf) ou des méthodes d'authentification alternatives.", "manual_steps": ["Vérifier les processus en cours.", "Inspecter les scripts de démarrage et crontab.", "S'assurer que -p<password> n'apparaît nulle part."]},
    {"category": "2. Installation et Planification", "number": "2.4", "name": "Ne pas réutiliser les noms d'utilisateurs", "type": "Manual", "test_procedure": f"{MYSQL_CMD} -e \"SELECT host, user, plugin FROM mysql.user WHERE user NOT IN ('mysql.infoschema', 'mysql.session', 'mysql.sys', 'mariadb.sys') ORDER BY user;\"", "expected_output": None, "remediation": "Ajouter/Supprimer les utilisateurs pour que chaque compte soit dédié à un usage spécifique.", "manual_steps": ["Lister les utilisateurs MariaDB.", "Vérifier que chaque nom de compte n'est utilisé que pour un seul rôle."]},
    {"category": "2. Installation et Planification", "number": "2.5", "name": "S'assurer que le matériel cryptographique est unique et non par défaut", "type": "Manual", "test_procedure": "Vérifier les certificats SSL utilisés par MariaDB.", "expected_output": None, "remediation": "Générer de nouveaux certificats, clés et autre matériel cryptographique pour chaque instance.", "manual_steps": ["Examiner les certificats via openssl x509 -in server-cert.pem -subject -noout.", "Vérifier qu'ils ne contiennent pas 'Auto_Generated'."]},
    {"category": "2. Installation et Planification", "number": "2.6", "name": "Assurer que password_lifetime <= 365", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT @@default_password_lifetime;\"", "expected_output": {"type": "stdout_is_numeric_less_equal", "value": 365}, "remediation": "SET GLOBAL default_password_lifetime=365;"},
    {"category": "2. Installation et Planification", "number": "2.7", "name": "Verrouiller les comptes inutilisés", "type": "Manual", "test_procedure": f"{MYSQL_CMD} -e \"SELECT CONCAT(user, '@', host) FROM mysql.global_priv;\"", "expected_output": None, "remediation": "ALTER USER 'user'@'host' ACCOUNT LOCK; pour chaque compte inutilisé.", "manual_steps": ["Lister les comptes.", "Identifier les comptes dormants.", "Verrouiller les comptes non utilisés."]},
    {"category": "2. Installation et Planification", "number": "2.8", "name": "Utilisation appropriée de l'authentification Socket Peer-Credential", "type": "Manual", "test_procedure": f"{MYSQL_CMD} -e \"SELECT PLUGIN_NAME, PLUGIN_STATUS FROM INFORMATION_SCHEMA.PLUGINS WHERE PLUGIN_NAME = 'unix_socket';\"", "expected_output": None, "remediation": "Configurer unix_socket=ON/OFF selon les besoins. ALTER USER ... IDENTIFIED VIA unix_socket.", "manual_steps": ["Vérifier si unix_socket est activé.", "Lister les utilisateurs configurés avec unix_socket.", "S'assurer que seuls les accès locaux autorisés l'utilisent."]},
    {"category": "2. Installation et Planification", "number": "2.9", "name": "S'assurer que MariaDB est lié à une adresse IP", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT VARIABLE_VALUE FROM information_schema.global_variables WHERE VARIABLE_NAME = 'bind_address';\"", "expected_output": {"type": "stdout_not_contains_any", "values": ["*", "::"]}, "remediation": "Configurer bind_address=<adresse_IP_spécifique> dans mariadb.cnf."},
    {"category": "2. Installation et Planification", "number": "2.10", "name": "Limiter les versions TLS acceptées", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT VARIABLE_VALUE FROM information_schema.global_variables WHERE VARIABLE_NAME = 'tls_version';\"", "expected_output": {"type": "stdout_contains", "value": "TLSv1.2"}, "remediation": "Configurer tls_version=TLSv1.2,TLSv1.3 dans mariadb.cnf."},
    {"category": "2. Installation et Planification", "number": "2.11", "name": "Exiger des certificats côté client (X.509)", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT count(*) FROM mysql.user WHERE host NOT IN ('localhost', '127.0.0.1', '::1') AND ssl_type NOT IN ('ANY', 'X509', 'SPECIFIED');\"", "expected_output": {"type": "stdout_equals", "value": "0"}, "remediation": "ALTER USER '<user>'@'<host>' REQUIRE X509;"},
    {"category": "2. Installation et Planification", "number": "2.12", "name": "S'assurer que seuls les chiffrement approuvés sont utilisés", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT VARIABLE_VALUE FROM information_schema.global_variables WHERE VARIABLE_NAME = 'ssl_cipher';\"", "expected_output": {"type": "stdout_not_empty"}, "remediation": "Configurer ssl_cipher avec une liste de chiffrements approuvés dans mariadb.cnf."},

    # Category 3: Permissions Fichiers
    {"category": "3. Permissions Fichiers", "number": "3.1", "name": "Permissions adéquates sur 'datadir'", "type": "Automated", "path_command": f"{MYSQL_CMD} -e \"SELECT @@datadir;\"", "test_procedure_template": "stat -c '%U:%G %a' {path}", "expected_output": {"type": "stdout_regex_match", "pattern": r"^mysql:mysql\s+7[05][05]$"}, "remediation": "chown -R mysql:mysql <datadir> && chmod 700 <datadir>"},
    {"category": "3. Permissions Fichiers", "number": "3.2", "name": "Permissions sur les fichiers 'log_bin_basename'", "type": "Automated", "path_command": f"{MYSQL_CMD} -e \"SELECT @@log_bin_basename;\"", "test_procedure_template": "ls -l {path}* | awk '{{print $1}}' | uniq", "expected_output": {"type": "stdout_regex_match", "pattern": r"^-rw-------$"}, "remediation": "Appliquer chmod 600 sur les fichiers binaires."},
    {"category": "3. Permissions Fichiers", "number": "3.3", "name": "Permissions sur 'log_error'", "type": "Automated", "path_command": f"{MYSQL_CMD} -e \"SELECT @@log_error;\"", "test_procedure_template": "stat -c '%a' {path}", "expected_output": {"type": "stdout_regex_match", "pattern": r"^6[04]0$"}, "remediation": "Appliquer des permissions restrictives (ex: 640 ou 600)."},
    {"category": "3. Permissions Fichiers", "number": "3.4", "name": "Permissions sur 'slow_query_log'", "type": "Automated", "path_command": f"{MYSQL_CMD} -e \"SELECT @@slow_query_log_file;\"", "test_procedure_template": "stat -c '%a' {path}", "expected_output": {"type": "stdout_regex_match", "pattern": r"^6[04]0$"}, "remediation": "Limiter l'accès aux utilisateurs autorisés (ex: 640 ou 600)."},
    {"category": "3. Permissions Fichiers", "number": "3.5", "name": "Permissions sur 'relay_log_basename'", "type": "Automated", "path_command": f"{MYSQL_CMD} -e \"SELECT @@relay_log_basename;\"", "test_procedure_template": "ls -l {path}* | awk '{{print $1}}' | uniq", "expected_output": {"type": "stdout_regex_match", "pattern": r"^-rw-------$"}, "remediation": "Appliquer chmod 600."},
    {"category": "3. Permissions Fichiers", "number": "3.6", "name": "Permissions sur 'general_log_file'", "type": "Automated", "path_command": f"{MYSQL_CMD} -e \"SELECT @@general_log_file;\"", "test_procedure_template": "stat -c '%a' {path}", "expected_output": {"type": "stdout_regex_match", "pattern": r"^6[04]0$"}, "remediation": "Restreindre les droits d'accès (ex: 640 ou 600)."},
    {"category": "3. Permissions Fichiers", "number": "3.7", "name": "Permissions sur les fichiers de clés SSL", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SHOW VARIABLES LIKE 'ssl_key';\" | awk '{{print $2}}' | xargs stat -c '%a'", "expected_output": {"type": "stdout_equals", "value": "600"}, "remediation": "Restreindre l'accès aux clés privées (ex: chmod 600) et s'assurer que le propriétaire est mysql."},
    {"category": "3. Permissions Fichiers", "number": "3.8", "name": "Permissions sur le répertoire des plugins", "type": "Automated", "path_command": f"{MYSQL_CMD} -e \"SELECT @@plugin_dir;\"", "test_procedure_template": "stat -c '%U:%G %a' {path}", "expected_output": {"type": "stdout_regex_match", "pattern": r"^(mysql|root):(mysql|root)\s+7[57]5$"}, "remediation": "chown -R mysql:mysql <plugin_dir> && chmod 755 <plugin_dir>"},
    {"category": "3. Permissions Fichiers", "number": "3.9", "name": "Permissions sur 'server_audit_file_path'", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SHOW VARIABLES LIKE 'server_audit_file_path';\" | awk '{{print $2}}' | xargs stat -c '%a'", "expected_output": {"type": "stdout_regex_match", "pattern": r"^6[04]0$"}, "remediation": "Appliquer des permissions restrictives (ex: 640 ou 600)."},
    {"category": "3. Permissions Fichiers", "number": "3.10", "name": "Permissions sur les fichiers du plugin File Key Management", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SHOW VARIABLES LIKE 'file_key_management_filename';\" | awk '{{print $2}}' | xargs stat -c '%a'", "expected_output": {"type": "stdout_regex_match", "pattern": r"^6[04]0$"}, "remediation": "Restreindre l'accès aux fichiers de clés de chiffrement (chmod 640)."},

    # Category 4: Général
    {"category": "4. Général", "number": "4.1", "name": "S'assurer que les derniers correctifs de sécurité sont appliqués", "type": "Manual", "test_procedure": f"{MYSQL_CMD} -e \"SELECT @@version;\"", "expected_output": None, "remediation": "Installez les derniers correctifs pour votre version ou mettez à niveau vers la dernière version.", "manual_steps": ["Relever la version affichée.", "Comparer avec les Release Notes MariaDB 10.6.", "Vérifier les CVE critiques."]},
    {"category": "4. Général", "number": "4.2", "name": "S'assurer que les bases de test ne sont pas installées en production", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME IN ('employees', 'world', 'world_x', 'sakila', 'airportdb', 'menagerie', 'test');\"", "expected_output": {"type": "stdout_is_empty"}, "remediation": "Exécutez DROP DATABASE <database name>; pour supprimer une base de données d'exemple."},
    {"category": "4. Général", "number": "4.3", "name": "S'assurer que 'allow-suspicious-udfs' est à 'OFF'", "type": "Automated", "test_procedure": "my_print_defaults mysqld 2>/dev/null | grep -q 'allow-suspicious-udfs' && echo 'FOUND' || echo 'NOT FOUND'", "expected_output": {"type": "stdout_equals", "value": "NOT FOUND"}, "remediation": "Supprimer --allow-suspicious-udfs de la ligne de commande ou du fichier de configuration."},
    {"category": "4. Général", "number": "4.4", "name": "Renforcer l'utilisation de 'local_infile' sur les clients MariaDB", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT @@local_infile;\"", "expected_output": {"type": "stdout_equals", "value": "0"}, "remediation": "Ajouter local-infile=0 à la section [mariadbd] et [client] du fichier de configuration MariaDB."},
    {"category": "4. Général", "number": "4.5", "name": "S'assurer que mariadb n'est pas démarré avec '--skip-grant-tables'", "type": "Automated", "test_procedure": "ps -ef | grep -E 'mysqld|mariadbd' | grep -v grep | grep -q 'skip-grant-tables' && echo 'FOUND' || echo 'NOT FOUND'", "expected_output": {"type": "stdout_equals", "value": "NOT FOUND"}, "remediation": "Supprimer l'option --skip-grant-tables de la ligne de commande ou du fichier de configuration."},
    {"category": "4. Général", "number": "4.6", "name": "S'assurer que les liens symboliques sont désactivés", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT @@have_symlink;\"", "expected_output": {"type": "stdout_equals", "value": "DISABLED"}, "remediation": "Ajouter skip-symbolic-links dans la section [mariadbd] du fichier mariadb.cnf."},
    {"category": "4. Général", "number": "4.7", "name": "S'assurer que 'secure_file_priv' est configuré correctement", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SHOW GLOBAL VARIABLES WHERE Variable_name = 'secure_file_priv';\" | awk '{{print $2}}'", "expected_output": {"type": "stdout_not_empty"}, "remediation": "Configurer secure_file_priv sur NULL (pour désactiver) ou sur un chemin spécifique dans mariadb.cnf."},
    {"category": "4. Général", "number": "4.8", "name": "S'assurer que sql_mode contient STRICT_ALL_TABLES", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT @@sql_mode;\"", "expected_output": {"type": "stdout_contains", "value": "STRICT_ALL_TABLES"}, "remediation": "Ajouter STRICT_ALL_TABLES au paramètre sql_mode dans mariadb.cnf."},
    {"category": "4. Général", "number": "4.9", "name": "Activer le chiffrement des données au repos dans MariaDB", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT VARIABLE_VALUE FROM information_schema.global_variables WHERE variable_name = 'innodb_encrypt_tables';\"", "expected_output": {"type": "stdout_equals", "value": "ON"}, "remediation": "Configurer file_key_management plugin et innodb_encrypt_tables=ON dans mariadb.cnf."},

    # Category 5 - Permissions MariaDB
    {"category": "5. Permissions MariaDB", "number": "5.1", "name": "Limiter l'accès complet à mysql.* aux seuls administrateurs", "type": "Manual", "test_procedure": f"{MYSQL_CMD} -e \"SELECT GRANTEE, PRIVILEGE_TYPE FROM information_schema.user_privileges WHERE grantee NOT LIKE ('\\\\'mysql.%localhost\\\\'');\"", "expected_output": None, "remediation": "Révoquer les privilèges excessifs sur la base 'mysql' pour les utilisateurs non-administrateurs.", "manual_steps": ["Examiner les utilisateurs retournés.", "Vérifier que seuls les administrateurs ont un accès complet.", "REVOKE les privilèges excessifs."]},
    {"category": "5. Permissions MariaDB", "number": "5.2", "name": "Retirer le droit FILE aux non-admins", "type": "Manual", "test_procedure": f"{MYSQL_CMD} -e \"SELECT GRANTEE FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE PRIVILEGE_TYPE = 'FILE';\"", "expected_output": None, "remediation": "REVOKE FILE ON *.* FROM '<user>'@'<host>';", "manual_steps": ["Vérifier les utilisateurs ayant le droit FILE.", "S'assurer que seuls les administrateurs l'ont."]},
    {"category": "5. Permissions MariaDB", "number": "5.3", "name": "Retirer le droit PROCESS aux non-admins", "type": "Manual", "test_procedure": f"{MYSQL_CMD} -e \"SELECT GRANTEE FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE PRIVILEGE_TYPE = 'PROCESS';\"", "expected_output": None, "remediation": "REVOKE PROCESS ON *.* FROM '<user>'@'<host>';", "manual_steps": ["Vérifier les utilisateurs ayant le droit PROCESS.", "S'assurer que seuls les administrateurs l'ont."]},
    {"category": "5. Permissions MariaDB", "number": "5.4", "name": "Retirer le droit SUPER aux non-admins", "type": "Manual", "test_procedure": f"{MYSQL_CMD} -e \"SELECT GRANTEE FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE PRIVILEGE_TYPE = 'SUPER';\"", "expected_output": None, "remediation": "REVOKE SUPER ON *.* FROM '<user>'@'<host>';", "manual_steps": ["Vérifier les utilisateurs ayant le droit SUPER.", "S'assurer que seuls les administrateurs l'ont."]},
    {"category": "5. Permissions MariaDB", "number": "5.5", "name": "Retirer le droit SHUTDOWN aux non-admins", "type": "Manual", "test_procedure": f"{MYSQL_CMD} -e \"SELECT GRANTEE FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE PRIVILEGE_TYPE = 'SHUTDOWN';\"", "expected_output": None, "remediation": "REVOKE SHUTDOWN ON *.* FROM '<user>'@'<host>';", "manual_steps": ["Vérifier les utilisateurs ayant le droit SHUTDOWN.", "S'assurer que seuls les administrateurs l'ont."]},
    {"category": "5. Permissions MariaDB", "number": "5.6", "name": "Retirer CREATE USER aux non-admins", "type": "Manual", "test_procedure": f"{MYSQL_CMD} -e \"SELECT GRANTEE FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE PRIVILEGE_TYPE = 'CREATE USER';\"", "expected_output": None, "remediation": "REVOKE CREATE USER ON *.* FROM '<user>'@'<host>';", "manual_steps": ["Vérifier les utilisateurs ayant le droit CREATE USER.", "S'assurer que seuls les administrateurs l'ont."]},
    {"category": "5. Permissions MariaDB", "number": "5.7", "name": "Retirer GRANT OPTION aux non-admins", "type": "Manual", "test_procedure": f"{MYSQL_CMD} -e \"SELECT GRANTEE FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE IS_GRANTABLE = 'YES';\"", "expected_output": None, "remediation": "REVOKE GRANT OPTION ON *.* FROM '<user>'@'<host>';", "manual_steps": ["Vérifier les utilisateurs ayant GRANT OPTION.", "S'assurer que seuls les administrateurs l'ont."]},
    {"category": "5. Permissions MariaDB", "number": "5.8", "name": "Limiter REPLICATION SLAVE aux comptes de réplication", "type": "Manual", "test_procedure": f"{MYSQL_CMD} -e \"SELECT GRANTEE FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE PRIVILEGE_TYPE = 'REPLICATION SLAVE';\"", "expected_output": None, "remediation": "REVOKE REPLICATION SLAVE ON *.* FROM les comptes non dédiés à la réplication.", "manual_steps": ["Vérifier les utilisateurs ayant REPLICATION SLAVE.", "S'assurer que seuls les comptes de réplication l'ont."]},
    {"category": "5. Permissions MariaDB", "number": "5.9", "name": "Limiter les droits DML/DDL à des BD/comptes précis", "type": "Manual", "test_procedure": f"{MYSQL_CMD} -e \"SELECT GRANTEE, PRIVILEGE_TYPE FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE PRIVILEGE_TYPE IN ('SELECT','INSERT','UPDATE','DELETE','CREATE','DROP','ALTER');\"", "expected_output": None, "remediation": "Révoquer les droits superflus par base de données/compte.", "manual_steps": ["Vérifier les droits DML/DDL par utilisateur.", "S'assurer du principe du moindre privilège."]},
    {"category": "5. Permissions MariaDB", "number": "5.10", "name": "Définir proprement DEFINER/INVOKER des SP/Functions", "type": "Manual", "test_procedure": f"{MYSQL_CMD} -e \"SELECT ROUTINE_SCHEMA, ROUTINE_NAME, DEFINER, SECURITY_TYPE FROM information_schema.ROUTINES WHERE DEFINER NOT IN ('root@localhost', 'mariadb.sys@localhost');\"", "expected_output": None, "remediation": "Recréer les routines avec un DEFINER minimal ou utiliser SQL SECURITY INVOKER.", "manual_steps": ["Lister les routines et leurs DEFINER.", "Vérifier que les DEFINER sont appropriés."]},

    # Category 6 - Audit & Journalisation
    {"category": "6. Audit & Journalisation", "number": "6.1", "name": "Configurer log_error correctement", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SHOW VARIABLES LIKE 'log_error';\" | awk '{{print $2}}'", "expected_output": {"type": "stdout_not_contains", "value": "stderr"}, "remediation": "Définir log-error=/chemin/vers/mariadb.err dans mariadb.cnf."},
    {"category": "6. Audit & Journalisation", "number": "6.2", "name": "Journal hors partition système", "type": "Automated", "path_command": f"{MYSQL_CMD} -e \"SELECT @@log_bin_basename;\"", "test_procedure_template": "df -P {path} | awk 'NR==2 {{print $6}}'", "expected_output": {"type": "stdout_not_equals", "value": "/"}, "remediation": "Déplacer les répertoires des journaux (log-bin, log-error) hors des partitions système."},
    {"category": "6. Audit & Journalisation", "number": "6.3", "name": "log_warnings=2", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT @@log_warnings;\"", "expected_output": {"type": "stdout_equals", "value": "2"}, "remediation": "Ajouter log_warnings=2 dans mariadb.cnf."},
    {"category": "6. Audit & Journalisation", "number": "6.4", "name": "Activer la journalisation d'audit (server_audit)", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT PLUGIN_STATUS FROM information_schema.plugins WHERE PLUGIN_NAME = 'SERVER_AUDIT';\"", "expected_output": {"type": "stdout_equals", "value": "ACTIVE"}, "remediation": "Installer et configurer le plugin server_audit : plugin_load_add=server_audit, server_audit_logging=ON dans mariadb.cnf."},
    {"category": "6. Audit & Journalisation", "number": "6.5", "name": "Interdire le déchargement du plugin d'audit", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT LOAD_OPTION FROM information_schema.plugins WHERE PLUGIN_NAME='SERVER_AUDIT';\"", "expected_output": {"type": "stdout_equals", "value": "FORCE_PLUS_PERMANENT"}, "remediation": "Ajouter server_audit=FORCE_PLUS_PERMANENT dans mariadb.cnf."},
    {"category": "6. Audit & Journalisation", "number": "6.6", "name": "Chiffrer les Binary et Relay Logs", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT VARIABLE_VALUE FROM information_schema.global_variables WHERE variable_name = 'encrypt_binlog';\"", "expected_output": {"type": "stdout_equals", "value": "ON"}, "remediation": "Ajouter encrypt_binlog=ON dans mariadb.cnf (nécessite un plugin de gestion de clés)."},

    # Category 7 - Authentification
    {"category": "7. Authentification", "number": "7.1", "name": "Désactiver mysql_old_password (old_passwords=OFF, secure_auth=ON)", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT @@old_passwords;\"", "expected_output": {"type": "stdout_equals", "value": "0"}, "remediation": "Configurer old_passwords=0 et secure_auth=ON dans mariadb.cnf et redémarrer."},
    {"category": "7. Authentification", "number": "7.2", "name": "Aucun mot de passe dans la configuration globale", "type": "Automated", "test_procedure": "! grep -riE 'password|pwd|pass' /etc/mysql/ /etc/my.cnf 2>/dev/null | grep -v '#' | grep -v 'password_lifetime' | grep -v 'password_check' | grep -v 'validate_password' | grep -v 'strict_password' | grep -v 'old_passwords' | grep -v 'default_password_lifetime' | grep -v 'password_last_changed'", "expected_output": {"type": "returncode_zero"}, "remediation": "Utiliser des fichiers .my.cnf privés ou mysql_config_editor avec permissions restreintes."},
    {"category": "7. Authentification", "number": "7.3", "name": "Authentification forte pour tous les comptes", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT User, host FROM mysql.user WHERE (plugin IN('mysql_native_password', 'mysql_old_password','') AND NOT (User = 'root' AND authentication_string = 'invalid') AND NOT (User = 'mysql' AND authentication_string = 'invalid'));\"", "expected_output": {"type": "stdout_is_empty"}, "remediation": "Migrer les comptes vers ed25519, unix_socket ou d'autres plugins d'authentification forte."},
    {"category": "7. Authentification", "number": "7.4", "name": "Politique de complexité des mots de passe (simple_password_check)", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT PLUGIN_STATUS FROM information_schema.plugins WHERE PLUGIN_NAME = 'simple_password_check';\"", "expected_output": {"type": "stdout_equals", "value": "ACTIVE"}, "remediation": "Installer et configurer simple_password_check et cracklib_password_check. INSTALL SONAME 'simple_password_check';"},
    {"category": "7. Authentification", "number": "7.5", "name": "Pas de wildcard '%' dans host", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT user, host FROM mysql.user WHERE host = '%';\"", "expected_output": {"type": "stdout_is_empty"}, "remediation": "ALTER USER '<user>'@'%' ... ou supprimer le compte."},
    {"category": "7. Authentification", "number": "7.6", "name": "Supprimer les comptes anonymes", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT user, host FROM mysql.user WHERE user = '';\"", "expected_output": {"type": "stdout_is_empty"}, "remediation": "DROP USER ''@'<host>'; ou utiliser mariadb-secure-installation."},

    # Category 8 - Sécurité réseau
    {"category": "8. Sécurité réseau", "number": "8.1", "name": "Forcer SSL/TLS (require_secure_transport=ON et have_ssl=YES)", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT @@require_secure_transport;\"", "expected_output": {"type": "stdout_equals", "value": "1"}, "remediation": "Configurer les certificats SSL/TLS, puis ajouter require_secure_transport=ON dans mariadb.cnf."},
    {"category": "8. Sécurité réseau", "number": "8.2", "name": "Exiger TLS côté utilisateur (ssl_type)", "type": "Automated", "test_procedure": f"{MYSQL_CMD} -e \"SELECT count(*) FROM mysql.user WHERE host NOT IN ('localhost', '127.0.0.1', '::1') AND ssl_type = '';\"", "expected_output": {"type": "stdout_equals", "value": "0"}, "remediation": "ALTER USER '<user>'@'<host>' REQUIRE SSL; ou REQUIRE X509;"},
    {"category": "8. Sécurité réseau", "number": "8.3", "name": "Limiter le nombre de connexions", "type": "Manual", "test_procedure": f"{MYSQL_CMD} -e \"SELECT VARIABLE_NAME, VARIABLE_VALUE FROM information_schema.global_variables WHERE VARIABLE_NAME LIKE 'max_%connections';\"", "expected_output": None, "remediation": "Ajuster max_connections et max_user_connections dans mariadb.cnf selon les besoins.", "manual_steps": ["Vérifier les valeurs de max_connections et max_user_connections.", "S'assurer que des limites raisonnables sont définies."]},

    # Category 9 - Réplication
    {"category": "9. Réplication", "number": "9.1", "name": "Chiffrer le trafic de réplication", "type": "Manual", "pre_condition": f"{MYSQL_CMD} -e \"SHOW REPLICA STATUS;\" | grep -q .", "test_procedure": f"{MYSQL_CMD} -e \"SHOW REPLICA STATUS\\G\" | grep 'Master_SSL_Allowed'", "expected_output": None, "remediation": "STOP REPLICA; CHANGE MASTER TO MASTER_SSL=1; START REPLICA;", "manual_steps": ["Vérifier si la réplication est active.", "Vérifier Master_SSL_Allowed.", "Configurer TLS pour la réplication si nécessaire."]},
    {"category": "9. Réplication", "number": "9.2", "name": "MASTER_SSL_VERIFY_SERVER_CERT activé", "type": "Automated", "pre_condition": f"{MYSQL_CMD} -e \"SHOW REPLICA STATUS;\" | grep -q .", "test_procedure": f"{MYSQL_CMD} -e \"SHOW REPLICA STATUS\\G\" | grep 'Master_SSL_Verify_Server_Cert'", "expected_output": {"type": "stdout_contains", "value": "Yes"}, "remediation": "STOP REPLICA; CHANGE MASTER TO MASTER_SSL_VERIFY_SERVER_CERT=1; START REPLICA;"},
    {"category": "9. Réplication", "number": "9.3", "name": "Pas de SUPER pour les utilisateurs de réplication", "type": "Automated", "pre_condition": f"{MYSQL_CMD} -e \"SELECT count(*) FROM mysql.user WHERE user LIKE '%repl%';\" | grep -q '[1-9]'", "test_procedure": f"{MYSQL_CMD} -e \"SELECT count(*) FROM mysql.user WHERE user LIKE '%repl%' AND Super_priv = 'Y';\"", "expected_output": {"type": "stdout_equals", "value": "0"}, "remediation": "REVOKE SUPER ON *.* FROM '<repl_user>'@'<repl_host>';"},
    {"category": "9. Réplication", "number": "9.4", "name": "Chiffrement approuvé pour la réplication", "type": "Manual", "pre_condition": f"{MYSQL_CMD} -e \"SHOW REPLICA STATUS;\" | grep -q .", "test_procedure": f"{MYSQL_CMD} -e \"SHOW REPLICA STATUS\\G\" | grep 'Master_SSL_Cipher'", "expected_output": None, "remediation": "STOP REPLICA; CHANGE MASTER TO MASTER_SSL_CIPHER='ECDHE-ECDSA-AES128-GCM-SHA256'; START REPLICA;", "manual_steps": ["Vérifier le cipher utilisé pour la réplication.", "S'assurer qu'un cipher fort est configuré."]},
    {"category": "9. Réplication", "number": "9.5", "name": "TLS mutuel activé pour la réplication", "type": "Manual", "pre_condition": f"{MYSQL_CMD} -e \"SHOW REPLICA STATUS;\" | grep -q .", "test_procedure": f"{MYSQL_CMD} -e \"SHOW REPLICA STATUS\\G\" | grep -E 'Master_SSL_Cert|Master_SSL_Key'", "expected_output": None, "remediation": "STOP REPLICA; CHANGE MASTER TO MASTER_SSL_CERT='...', MASTER_SSL_KEY='...'; START REPLICA; ALTER USER <repl_user> REQUIRE X509;", "manual_steps": ["Vérifier Master_SSL_Cert et Master_SSL_Key sur le replica.", "Vérifier ssl_type=X509 pour les utilisateurs de réplication sur le primary."]},
]

# --- Modèle HTML (Adapté pour MariaDB 10.6) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CIS Benchmark Audit Report MariaDB 10.6 Benchmark</title>
    <script src="https://cdn.tailwindcss.com"></script>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        body {{ font-family: 'Inter', sans-serif; }}
        .status-pass {{ background-color: #DEF7EC; color: #03543F; }}
        .status-fail {{ background-color: #FDE8E8; color: #9B1C1C; }}
        .status-manual {{ background-color: #FEF3C7; color: #92400E; }}
        .status-error {{ background-color: #F3F4F6; color: #1F2937; }}
        .status-na {{ background-color: #E5E7EB; color: #4B5563; }}
        pre {{ white-space: pre-wrap; word-wrap: break-word; font-size: 0.75rem; }}
        .sidebar-link.active {{ background-color: #3B82F6; color: white; }}
    </style>
</head>
<body class="bg-gray-50 flex">
    <!-- Sidebar -->
    <aside class="w-64 h-screen bg-white border-r border-gray-200 sticky top-0 overflow-y-auto hidden lg:block">
        <div class="p-6">
            <h2 class="text-xl font-bold text-blue-600"><i class="fas fa-shield-halved mr-2"></i>CIS MariaDB 10.6</h2>
            <p class="text-xs text-gray-500 mt-1">Audit Security Report</p>
        </div>
        <nav class="px-4 pb-6">
            <a href="#summary" class="sidebar-link flex items-center p-3 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors mb-1">
                <i class="fas fa-chart-pie w-5 mr-3"></i> Synthèse
            </a>
            <div class="mt-4 mb-2 text-xs font-semibold text-gray-400 uppercase px-3">Categorys</div>
            {sidebar_links}
        </nav>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 min-w-0">
        <!-- Header -->
        <header class="bg-white border-b border-gray-200 p-6 flex justify-between items-center">
            <div>
                <h1 class="text-2xl font-bold text-gray-900">Benchmark CIS MariaDB 10.6</h1>
                <p class="text-sm text-gray-500">Report Date: {report_date}</p>
            </div>
            <div class="flex space-x-2">
                <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">MariaDB 10.6.x</span>
                <span class="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-xs font-medium border border-gray-200">v1.1.0</span>
            </div>
        </header>

        <div class="p-8 max-w-7xl mx-auto">
            <!-- Summary Dashboard -->
            <section id="summary" class="mb-12">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col items-center">
                        <span class="text-sm font-medium text-gray-500 uppercase tracking-wider mb-2">Score Global</span>
                        <div class="relative flex items-center justify-center">
                            <svg class="w-24 h-24">
                                <circle class="text-gray-100" stroke-width="8" stroke="currentColor" fill="transparent" r="40" cx="48" cy="48" />
                                <circle class="{overall_score_class}" stroke-width="8" stroke-dasharray="251.2" stroke-dashoffset="{overall_score_offset}" stroke-linecap="round" stroke="currentColor" fill="transparent" r="40" cx="48" cy="48" />
                            </svg>
                            <span class="absolute text-xl font-bold">{overall_score:.1f}%</span>
                        </div>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 border-l-4 border-l-green-500">
                        <span class="text-xs font-bold text-green-600 uppercase tracking-widest">Succès</span>
                        <div class="text-3xl font-bold text-gray-900 mt-1">{passed_automated_count}</div>
                        <p class="text-xs text-gray-500 mt-1">Vérifications conformes</p>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 border-l-4 border-l-red-500">
                        <span class="text-xs font-bold text-red-600 uppercase tracking-widest">Échecs</span>
                        <div class="text-3xl font-bold text-gray-900 mt-1">{failed_automated_count}</div>
                        <p class="text-xs text-gray-500 mt-1">Non-conformités détectées</p>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 border-l-4 border-l-amber-500">
                        <span class="text-xs font-bold text-amber-600 uppercase tracking-widest">Manuels</span>
                        <div class="text-3xl font-bold text-gray-900 mt-1">{manual_checks}</div>
                        <p class="text-xs text-gray-500 mt-1">À vérifier manuellement</p>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 border-l-4 border-l-gray-500">
                        <span class="text-xs font-bold text-gray-600 uppercase tracking-widest">Errors / N/A</span>
                        <div class="text-3xl font-bold text-gray-900 mt-1">{total_other}</div>
                        <p class="text-xs text-gray-500 mt-1">{error_automated_count} Errors, {na_automated_count} N/A</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200 lg:col-span-1 h-80 flex flex-col">
                        <h3 class="font-bold text-gray-800 mb-4 tracking-tight text-center">Répartition Automatisée</h3>
                        <div class="flex-1 min-h-0 relative">
                            <canvas id="overallScoreChart"></canvas>
                        </div>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200 lg:col-span-2 h-80 flex flex-col">
                        <h3 class="font-bold text-gray-800 mb-4 tracking-tight">Analyse par Category</h3>
                        <div class="flex-1 min-h-0 relative">
                            <canvas id="categoryChart"></canvas>
                        </div>
                    </div>
                </div>
            </section>

            <div class="space-y-12">
                {categories_reports}
            </div>
        </div>

        <footer class="bg-white border-t border-gray-200 p-8 mt-12 text-center">
            <p class="text-sm text-gray-500 italic">Rapport généré automatiquement par CIS MariaDB 10.6 Auditor.</p>
            <p class="text-xs text-gray-400 mt-2">Basé sur CIS MariaDB 10.6 Benchmark v1.1.0.</p>
        </footer>
    </main>

    <script>
        // Pie Chart
        const overallScoreChartCtx = document.getElementById('overallScoreChart').getContext('2d');
        new Chart(overallScoreChartCtx, {{
            type: 'doughnut',
            data: {{
                labels: ['Pass', 'Fail', 'Error', 'N/A'],
                datasets: [{{
                    data: [{passed_automated_count}, {failed_automated_count}, {error_automated_count}, {na_automated_count}],
                    backgroundColor: ['#10B981', '#EF4444', '#374151', '#9CA3AF'],
                    borderWidth: 0,
                    cutout: '70%'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ position: 'bottom', labels: {{ usePointStyle: true, padding: 20 }} }} }}
            }}
        }});

        // Bar Chart
        const categoryScoreChartCtx = document.getElementById('categoryChart').getContext('2d');
        new Chart(categoryScoreChartCtx, {{
            type: 'bar',
            data: {{
                labels: {category_labels},
                datasets: [
                    {{ label: 'Pass', data: {category_pass_counts}, backgroundColor: '#10B981' }},
                    {{ label: 'Fail', data: {category_fail_counts}, backgroundColor: '#EF4444' }},
                    {{ label: 'Manual', data: {category_manual_counts}, backgroundColor: '#F59E0B' }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{ x: {{ stacked: true, grid: {{ display: false }} }}, y: {{ stacked: true }} }},
                plugins: {{ legend: {{ position: 'bottom', labels: {{ usePointStyle: true }} }} }}
            }}
        }});
    </script>
</body>
</html>
"""

CATEGORY_REPORT_TEMPLATE = """
            <section id="cat-{category_id}" class="scroll-mt-24">
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mb-8">
                    <div class="p-6 border-b border-gray-100 flex flex-col md:flex-row md:items-center justify-between gap-4">
                        <div>
                            <h2 class="text-xl font-bold text-gray-900">{category_name}</h2>
                            <p class="text-sm text-gray-500 mt-1">Détails des recommandations et résultats pour cette section.</p>
                        </div>
                        <div class="flex flex-wrap gap-2">
                            <span class="flex items-center px-3 py-1 rounded-full text-xs font-bold status-pass bg-opacity-20 border border-green-200"><i class="fas fa-check-circle mr-1.5"></i>{passed_automated} Pass</span>
                            <span class="flex items-center px-3 py-1 rounded-full text-xs font-bold status-fail bg-opacity-20 border border-red-200"><i class="fas fa-times-circle mr-1.5"></i>{failed_automated} Fail</span>
                            <span class="flex items-center px-3 py-1 rounded-full text-xs font-bold status-manual bg-opacity-20 border border-amber-200"><i class="fas fa-hand-paper mr-1.5"></i>{manual_checks} Manuel</span>
                            <span class="flex items-center px-3 py-1 rounded-full text-xs font-bold bg-gray-100 text-gray-600 border border-gray-200"><i class="fas fa-exclamation-triangle mr-1.5"></i>{error_checks} Error</span>
                            <span class="flex items-center px-3 py-1 rounded-full text-xs font-bold bg-gray-50 text-gray-400 border border-gray-100"><i class="fas fa-minus-circle mr-1.5"></i>{na_checks} N/A</span>
                            <div class="ml-2 pl-4 border-l border-gray-200 flex items-center">
                                <span class="text-lg font-black {category_score_class}">{category_score:.0f}%</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="w-16 py-3 px-4 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">ID</th>
                                    <th class="py-3 px-4 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Recommandation</th>
                                    <th class="w-32 py-3 px-4 text-center text-[10px] font-bold text-gray-400 uppercase tracking-widest">Status</th>
                                    <th class="py-3 px-4 text-left text-[10px] font-bold text-gray-400 uppercase tracking-widest">Analyse & Remediation</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200 bg-white text-sm">
                                {checks_rows}
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>
"""

CHECK_ROW_TEMPLATE = """
                            <tr class="hover:bg-gray-50 transition-colors">
                                <td class="py-4 px-4 text-sm font-medium text-gray-400 align-top">{number}</td>
                                <td class="py-4 px-4 align-top">
                                    <div class="text-sm font-bold text-gray-900 mb-1">{name}</div>
                                    <div class="text-xs text-gray-500 italic font-mono bg-gray-100 p-1 rounded inline-block truncate max-w-xs">{test_procedure}</div>
                                </td>
                                <td class="py-4 px-4 align-top text-center">
                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider {status_class}">
                                        {status_icon} {status_text}
                                    </span>
                                </td>
                                <td class="py-4 px-4 text-sm align-top">
                                    {manual_steps_html}
                                    <div class="mb-3">
                                        <div class="text-[10px] font-bold text-gray-400 uppercase mb-1">Résultat de l'audit:</div>
                                        <div class="bg-gray-900 text-gray-100 p-3 rounded-lg border border-gray-700">
                                            <pre class="overflow-x-auto">{output}</pre>
                                        </div>
                                    </div>
                                    <div class="p-3 bg-blue-50 border-l-4 border-blue-400 rounded-r-lg">
                                        <div class="text-[10px] font-bold text-blue-600 uppercase mb-1"><i class="fas fa-wrench mr-1"></i> Remediation:</div>
                                        <div class="text-xs text-blue-800 leading-relaxed font-medium">{remediation}</div>
                                    </div>
                                </td>
                            </tr>
"""

# --- Execution and evaluation functions ---


def build_inline_svg_donut_chart(passed, failed, errors, na, score):
    """Generate 100% self-contained Inline SVG Donut Chart (PSL ONLY, Zero JS)."""
    total = passed + failed + errors + na
    p_pass = (passed / total * 100) if total > 0 else 0
    p_fail = (failed / total * 100) if total > 0 else 0
    p_err = (errors / total * 100) if total > 0 else 0
    p_na = (na / total * 100) if total > 0 else 0

    offset_pass = 25
    offset_fail = 25 - p_pass
    offset_err = offset_fail - p_fail
    offset_na = offset_err - p_err

    return f"""
    <div style="display: flex; align-items: center; justify-content: center; gap: 40px; margin: 20px 0; flex-wrap: wrap;">
      <div style="position: relative; width: 170px; height: 170px;">
        <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg);">
          <path stroke-dasharray="100 100" stroke="#e5e7eb" stroke-width="3.8" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          <path stroke-dasharray="{p_na:.1f} 100" stroke-dashoffset="{offset_na:.1f}" stroke="#9ca3af" stroke-width="3.8" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          <path stroke-dasharray="{p_err:.1f} 100" stroke-dashoffset="{offset_err:.1f}" stroke="#6b7280" stroke-width="3.8" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          <path stroke-dasharray="{p_fail:.1f} 100" stroke-dashoffset="{offset_fail:.1f}" stroke="#ef4444" stroke-width="3.8" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          <path stroke-dasharray="{p_pass:.1f} 100" stroke-dashoffset="{offset_pass:.1f}" stroke="#10b981" stroke-width="3.8" stroke-linecap="round" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
        </svg>
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
          <span style="font-size: 24px; font-weight: 800; color: #111827;">{score:.1f}%</span>
          <span style="font-size: 11px; color: #6b7280; font-weight: 600;">Score Global</span>
        </div>
      </div>
      <div style="display: flex; flex-direction: column; gap: 8px; font-size: 13px;">
        <div style="display: flex; align-items: center; gap: 8px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #10b981; display: inline-block;"></span> <strong>Réussi (PASS) :</strong> {passed}</div>
        <div style="display: flex; align-items: center; gap: 8px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #ef4444; display: inline-block;"></span> <strong>Échoué (FAIL) :</strong> {failed}</div>
        <div style="display: flex; align-items: center; gap: 8px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #6b7280; display: inline-block;"></span> <strong>Erreur (Error) :</strong> {errors}</div>
        <div style="display: flex; align-items: center; gap: 8px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #9ca3af; display: inline-block;"></span> <strong>Non Applicable (N/A) :</strong> {na}</div>
      </div>
    </div>
    """


def build_inline_svg_category_chart(categories_scores):
    """Generate 100% self-contained Inline SVG/HTML5 Horizontal Stacked Bar Charts per category (PSL ONLY, Zero JS)."""
    if not categories_scores or not isinstance(categories_scores, dict):
        return ""
    items_html = []
    for label, cat in categories_scores.items():
        p = cat.get("passed_automated", cat.get("passed", 0))
        f = cat.get("failed_automated", cat.get("failed", 0))
        e = cat.get("error_checks", cat.get("errors", 0))
        n = cat.get("na_checks", cat.get("na", 0))
        cat_total = p + f + e + n
        cat_score = cat.get("score", (p / cat_total * 100) if cat_total > 0 else 0)

        p_pass = (p / cat_total * 100) if cat_total > 0 else 0
        p_fail = (f / cat_total * 100) if cat_total > 0 else 0
        p_err = (e / cat_total * 100) if cat_total > 0 else 0
        p_na = (n / cat_total * 100) if cat_total > 0 else 0

        badge_color = "#10b981" if cat_score >= 80 else ("#f59e0b" if cat_score >= 50 else "#ef4444")

        bar_segments = []
        if p > 0: bar_segments.append(f'<div style="width: {p_pass:.1f}%; background: #10b981;" title="Réussi: {p}"></div>')
        if f > 0: bar_segments.append(f'<div style="width: {p_fail:.1f}%; background: #ef4444;" title="Échoué: {f}"></div>')
        if e > 0: bar_segments.append(f'<div style="width: {p_err:.1f}%; background: #6b7280;" title="Error: {e}"></div>')
        if n > 0: bar_segments.append(f'<div style="width: {p_na:.1f}%; background: #9ca3af;" title="N/A: {n}"></div>')
        if not bar_segments:
            bar_segments.append('<div style="width: 100%; background: #e5e7eb;" title="Aucun contrôle"></div>')

        items_html.append(f"""
        <div style="margin-bottom: 16px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-weight: 600; font-size: 14px; color: #374151;">{label}</span>
            <span style="font-weight: 700; font-size: 13px; color: {badge_color};">{cat_score:.1f}% ({p}/{cat_total})</span>
          </div>
          <div style="display: flex; height: 16px; width: 100%; border-radius: 8px; overflow: hidden; background: #f3f4f6; border: 1px solid #e5e7eb;">
            {''.join(bar_segments)}
          </div>
        </div>
        """)

    legend_html = """
    <div style="display: flex; gap: 20px; justify-content: center; margin-bottom: 20px; font-size: 13px;">
      <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #10b981; display: inline-block;"></span> Réussi</div>
      <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #ef4444; display: inline-block;"></span> Échoué</div>
      <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #6b7280; display: inline-block;"></span> Erreur</div>
      <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #9ca3af; display: inline-block;"></span> N/A</div>
    </div>
    """

    return f"""
    <div style="background: #ffffff; padding: 24px; border-radius: 12px; border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-top: 24px;">
      <h3 style="font-size: 18px; font-weight: 700; color: #111827; margin-bottom: 16px; text-align: center;">Répartition des contrôles automatisés par catégorie</h3>
      {legend_html}
      {''.join(items_html)}
    </div>
    """


def load_recommendations(target_key):
    """Load audit control specifications from rules/<target_key>.json with inline fallback (PSL ONLY)."""
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rules", f"{target_key}.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Warning: Could not load rule spec '{json_path}': {e}", file=sys.stderr)
    return RECOMMENDATIONS_DATA



def run_command(command, remote_host=None):
    """Execute command locally or via SSH remote execution without shell=True (PSL ONLY)."""
    try:
        if isinstance(command, str):
            cmd_args = ["/bin/bash", "-c", command]
        else:
            cmd_args = list(command)

        if remote_host:
            cmd_args = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", remote_host] + cmd_args

        process = subprocess.run(cmd_args, check=False, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10)
        return process.stdout.strip(), process.stderr.strip(), process.returncode
    except subprocess.TimeoutExpired:
        return "", "Command execution timed out after 10 seconds", -1
    except Exception as e:
        return "", str(e), -1



def evaluate_condition(condition, stdout, stderr, returncode):
    """Évalue si le résultat de la commande correspond à la condition attendue."""
    if not condition:
        return False

    condition_type = condition.get("type")
    expected_value = condition.get("value")
    expected_values = condition.get("values")
    regex_pattern = condition.get("pattern")

    if "No such file or directory" in stderr or "Permission denied" in stderr:
        return False

    if condition_type == "returncode_zero":
        return returncode == 0
    elif condition_type == "returncode_equals":
         return returncode == expected_value
    elif condition_type == "stdout_equals":
        return stdout.strip() == str(expected_value)
    elif condition_type == "stdout_not_equals":
        return stdout.strip() != str(expected_value)
    elif condition_type == "stdout_contains":
        return str(expected_value) in stdout
    elif condition_type == "stdout_not_contains":
        return str(expected_value) not in stdout
    elif condition_type == "stdout_not_empty":
        return stdout.strip() != "" and stdout is not None
    elif condition_type == "stdout_is_empty":
        return stdout.strip() == "" or stdout is None
    elif condition_type == "stdout_contains_any":
        if expected_values is None: return False
        return any(str(value) in stdout for value in expected_values)
    elif condition_type == "stdout_not_contains_any":
        if expected_values is None: return True
        return not any(str(value) in stdout for value in expected_values)
    elif condition_type == "stdout_regex_match":
        if regex_pattern is None: return False
        return re.search(regex_pattern, stdout) is not None
    elif condition_type == "stdout_is_numeric_greater_than":
        try:
            numeric_value_match = re.search(r'(\d+)', stdout)
            if numeric_value_match:
                 numeric_value = int(numeric_value_match.group(1))
                 return numeric_value > expected_value
            return False
        except (ValueError, TypeError):
            return False
    elif condition_type == "stdout_is_numeric_less_equal":
         try:
             numeric_value_match = re.search(r'(\d+)', stdout)
             if numeric_value_match:
                  numeric_value = int(numeric_value_match.group(1))
                  if numeric_value == 0:
                      return False # 0 (infinite) is not <= 365
                  return numeric_value <= expected_value
             return False
         except (ValueError, TypeError):
             return False

    print(f"WARN: Unknown condition type '{condition_type}'")
    return False

def perform_checks(recommendations, remote_host=None):
    """Exécute tous les contrôles et stocke les résultats."""
    results = {}
    stored_outputs = {}

    for rec in recommendations:
        category = rec["category"]
        if category not in results:
            results[category] = []

        check_number = rec.get("number", "N/A")

        check_result = {
            "number": check_number,
            "name": rec["name"],
            "type": rec["type"],
            "test_procedure": rec.get("test_procedure", ""),
            "remediation": rec.get("remediation", ""),
            "manual_steps": rec.get("manual_steps", []),
            "status": "Not Applicable",
            "output": "",
            "error": ""
        }

        should_run = False
        cmd_to_run = None
        command_executed_display = "N/A"

        if rec["type"] == "Automated":
            if "pre_condition" in rec:
                pc_stdout, pc_stderr, pc_returncode = run_command(rec["pre_condition"])
                if pc_returncode != 0 or not pc_stdout or pc_stdout == "0":
                    check_result["status"] = "Not Applicable"
                    check_result["output"] = f"Check non applicable dans cet environnement (Pré-condition non remplie).\nCommand de vérification: {rec['pre_condition']}"
                    results[category].append(check_result)
                    continue
            should_run = True
        elif rec["type"] == "Manual" and "test_procedure" in rec and ("mysql" in rec["test_procedure"].lower() or "mariadb" in rec["test_procedure"].lower() or "crontab" in rec["test_procedure"].lower() or "ps" in rec["test_procedure"].lower()):
            should_run = True

        if should_run:
            try:
                if "path_command" in rec:
                    path_cmd = rec["path_command"]
                    path_stdout, path_stderr, path_returncode = run_command(path_cmd, remote_host=remote_host)

                    if path_returncode != 0 or not path_stdout:
                        if "Unknown system variable" in path_stderr or "ERROR 1193" in path_stderr:
                             check_result["status"] = "Not Applicable"
                             check_result["output"] = f"Variable/Plugin non disponible (N/A).\nStderr:\n{path_stderr}"
                        else:
                             check_result["status"] = "Error"
                             check_result["output"] = f"Error lors de l'obtention du chemin via:\n`{path_cmd}`\nStdout:\n{path_stdout}\nStderr:\n{path_stderr}"
                             check_result["error"] = path_stderr
                        results[category].append(check_result)
                        continue

                    dynamic_path = path_stdout.strip()
                    stored_outputs[check_number + "_path"] = dynamic_path

                    if "test_procedure_template" in rec:
                        cmd_to_run = rec["test_procedure_template"].format(path=dynamic_path)
                        command_executed_display = cmd_to_run
                elif "test_procedure" in rec:
                    cmd_to_run = rec["test_procedure"]
                    command_executed_display = cmd_to_run

                if cmd_to_run:
                    stdout, stderr, returncode = run_command(cmd_to_run, remote_host=remote_host)
                    check_result["output"] = f"Stdout:\n{stdout}\nStderr:\n{stderr}\nReturn Code: {returncode}"
                    check_result["error"] = stderr
                    check_result["test_procedure"] = command_executed_display

                    if "Unknown system variable" in stderr or "Unknown command" in stderr or "ERROR 1193" in stderr:
                         check_result["status"] = "Not Applicable"
                         check_result["output"] = f"Variable ou plugin non installé/activé.\n{check_result['output']}"
                         results[category].append(check_result)
                         continue

                    condition = rec.get("expected_output")

                    if rec["type"] == "Manual":
                        check_result["status"] = "Manual"
                        check_result["output"] = "This control requires manual verification.\n\nRésultat de l'extraction automatique pour aide:\n" + check_result["output"]
                    elif returncode == 127:
                        check_result["status"] = "Error"
                        check_result["output"] = f"Error: Command not found.\n{check_result['output']}"
                    elif returncode == 124:
                        check_result["status"] = "Error"
                        check_result["output"] = f"Error: Timeout.\n{check_result['output']}"
                    elif "command not found" in stderr.lower() and not cmd_to_run.strip().startswith('!'):
                         check_result["status"] = "Error"
                         check_result["output"] = f"Error: Command not found (détecté dans stderr).\n{check_result['output']}"
                    elif "ERROR 1045 (28000): Access denied" in stderr:
                         check_result["status"] = "Error"
                         check_result["output"] = f"Error: Accès refusé. Vérifiez les identifiants/privilèges MariaDB.\n{check_result['output']}"
                    elif "ERROR 2002 (HY000): Can't connect" in stderr:
                         check_result["status"] = "Error"
                         check_result["output"] = f"Error: Impossible de se connecter à MariaDB (serveur arrêté ou mauvais socket).\n{check_result['output']}"
                    elif condition:
                        is_pass = evaluate_condition(condition, stdout, stderr, returncode)
                        if is_pass and returncode != 0 and condition.get("type") not in ["returncode_zero", "returncode_equals"] and not cmd_to_run.strip().startswith('!'):
                             is_pass = False
                             check_result["output"] += f"\n\nÉchec car la commande a retourné une erreur (code {returncode})."
                        
                        if is_pass:
                            check_result["status"] = "Pass"
                        else:
                            check_result["status"] = "Fail"
                            check_result["output"] += "\n\nCondition de succès non remplie."
                    elif returncode == 0:
                         check_result["status"] = "Pass"
                         check_result["output"] += "\n\nNote: Command exécutée avec succès."
                    else:
                         check_result["status"] = "Fail"
                         check_result["output"] += f"\n\nLa commande a échoué (code {returncode})."
                else:
                     check_result["status"] = "Error"
                     check_result["output"] = f"Configuration d'audit invalid pour {check_number}."

            except Exception as e:
                 check_result["status"] = "Error"
                 check_result["output"] = f"Error interne lors du contrôle {check_number}: {e}"
                 check_result["error"] = str(e)
        else:
            check_result["status"] = "Manual"
            check_result["output"] = "This control requires manual verification.\n\nProcédure suggérée:\n" + rec.get('test_procedure', 'N/A')

        results[category].append(check_result)

    return results

def calculate_scores(results):
    """Calcule les scores globaux et par catégorie."""
    overall = {"total_automated": 0, "passed_automated": 0, "failed_automated": 0, "manual": 0, "error": 0, "na": 0}
    categories_scores = {}
    category_order = list(dict.fromkeys(rec["category"] for rec in RECOMMENDATIONS_DATA))
    for category in category_order:
        categories_scores[category] = {
            "score": 0,
            "total_automated": 0,
            "passed_automated": 0,
            "failed_automated": 0,
            "manual_checks": 0,
            "error_checks": 0,
            "na_checks": 0,
            "pass_count": 0,
            "fail_count": 0,
            "error_count": 0,
            "na_count": 0
        }

    for category, checks in results.items():
        if category not in categories_scores:
             print(f"WARN: Category '{category}' found in results but not pre-initialized. Skipping.")
             continue
        for check in checks:
            cat_stats = categories_scores[category]
            if check["type"] == "Automated":
                if check["status"] == "Pass":
                    overall["passed_automated"] += 1
                    cat_stats["passed_automated"] += 1
                    cat_stats["pass_count"] += 1
                elif check["status"] == "Fail":
                    overall["failed_automated"] += 1
                    cat_stats["failed_automated"] += 1
                    cat_stats["fail_count"] += 1
                elif check["status"] == "Error":
                    overall["error"] += 1
                    cat_stats["error_checks"] += 1
                    cat_stats["error_count"] += 1
                elif check["status"] == "Not Applicable":
                    overall["na"] += 1
                    cat_stats["na_checks"] += 1
                    cat_stats["na_count"] += 1
            elif check["type"] == "Manual":
                overall["manual"] += 1
                cat_stats["manual_checks"] += 1

    overall_attempted_automated = overall["passed_automated"] + overall["failed_automated"] + overall["na"]
    overall_score = ((overall["passed_automated"] + overall["na"]) / overall_attempted_automated * 100) if overall_attempted_automated > 0 else 0

    for category in category_order:
         cat_stats = categories_scores[category]
         cat_attempted_automated = cat_stats["passed_automated"] + cat_stats["failed_automated"] + cat_stats["na_checks"]
         cat_stats["total_automated"] = cat_attempted_automated
         cat_stats["score"] = ((cat_stats["passed_automated"] + cat_stats["na_checks"]) / cat_attempted_automated * 100) if cat_attempted_automated > 0 else 0

    category_labels = json.dumps(category_order)
    category_pass_counts = json.dumps([categories_scores[cat]["pass_count"] for cat in category_order])
    category_fail_counts = json.dumps([categories_scores[cat]["fail_count"] for cat in category_order])
    category_error_counts = json.dumps([categories_scores[cat]["error_count"] for cat in category_order])
    category_na_counts = json.dumps([categories_scores[cat]["na_count"] for cat in category_order])

    return (overall_score, categories_scores,
            overall["manual"], overall["error"], overall["na"],
            overall["passed_automated"], overall["failed_automated"], overall["error"], overall["na"],
            category_labels, category_pass_counts, category_fail_counts, category_error_counts, category_na_counts)

def get_score_class(score):
    """Retourne la classe CSS pour la couleur du score."""
    if score >= 80:
        return "text-green-600"
    elif score >= 50:
        return "text-yellow-600"
    else:
        return "text-red-600"

def get_status_info(status):
    """Retourne l'icône et le texte pour un statut."""
    if status == "Pass":
        return "✅", "Pass", "status-pass"
    elif status == "Fail":
        return "❌", "Fail", "status-fail"
    elif status == "Manual":
        return "⚠️", "Manuel", "status-manual"
    elif status == "Error":
        return "❓", "Error", "status-error"
    elif status == "Not Applicable":
        return "➖", "N/A", "status-na"
    else:
        return "❓", status, "status-error"



def export_results(results, overall_score, categories_scores, target_name, filename, fmt="html", lang="en"):
    """Export audit results into HTML, JSON, XML, or TXT formats using PSL ONLY."""
    import json
    import os
    import xml.etree.ElementTree as ET
    from datetime import datetime

    if not filename:
        ext = "html" if fmt == "html" else fmt
        target_slug = target_name.lower().replace(" ", "_").replace(".", "")
        filename = f"reports/rapport_cis_{target_slug}.{ext}"

    if os.path.dirname(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Flatten results if dictionary categorized
    flat_results = []
    if isinstance(results, dict):
        for cat, checks in results.items():
            for c in checks:
                c_copy = dict(c)
                c_copy["category"] = cat
                flat_results.append(c_copy)
    else:
        flat_results = results

    if fmt == "json":
        data = {
            "benchmark": target_name,
            "report_date": datetime.now().isoformat(),
            "overall_score": overall_score,
            "total_checks": len(flat_results),
            "results": flat_results
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"📄 JSON Report successfully generated: {filename}")

    elif fmt == "xml":
        root = ET.Element("testsuite", name=target_name, tests=str(len(flat_results)), failures=str(sum(1 for r in flat_results if r.get("status") in ["FAIL", "Fail"])), timestamp=datetime.now().isoformat())
        for r in flat_results:
            tc = ET.SubElement(root, "testcase", id=str(r.get("number", r.get("id", ""))), name=str(r.get("name", r.get("title", ""))), classname=str(r.get("category", "")))
            if r.get("status") in ["FAIL", "Fail"]:
                failure = ET.SubElement(tc, "failure", message="Control failed")
                failure.text = str(r.get("output", r.get("stdout", "")))
            elif r.get("status") in ["ERROR", "Error"]:
                err = ET.SubElement(tc, "error", message="Control execution error")
                err.text = str(r.get("output", r.get("stderr", "")))
        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        print(f"📄 XML Report successfully generated: {filename}")

    elif fmt == "txt":
        lines = [
            "=" * 70,
            f"🛡️  {target_name} - CIS Benchmark Audit Report",
            f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Global Score: {overall_score:.1f}%",
            "=" * 70,
            ""
        ]
        for r in flat_results:
            status = r.get("status", "")
            status_icon = "[PASS]" if status in ["PASS", "Pass"] else ("[FAIL]" if status in ["FAIL", "Fail"] else "[MANUAL]")
            rec_id = r.get("number", r.get("id", ""))
            rec_name = r.get("name", r.get("title", ""))
            lines.append(f"{status_icon} {rec_id} - {rec_name}")
            lines.append(f"  Category: {r.get('category')}")
            out = r.get('output', r.get('stdout', ''))
            if out:
                lines.append(f"  Output: {str(out).strip()}")
            rem = r.get('remediation', '')
            if rem and status in ["FAIL", "Fail"]:
                lines.append(f"  Remediation: {str(rem).strip()}")
            lines.append("-" * 70)
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"📄 TXT Report successfully generated: {filename}")

    else:
        generate_html_report(results, overall_score, categories_scores, filename=filename, lang=lang)



def generate_html_report(results, overall_score, categories_scores, filename=None, lang="en"):
    if not filename:
        filename = "reports/rapport_cis_mariadb_106.html"

    report_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    overall_score_class = get_score_class(overall_score)
    categories_html = ""

    flat_results = []
    if isinstance(results, dict):
        for cat, checks in results.items():
            for c in checks:
                flat_results.append(c)
    else:
        flat_results = results

    passed_auto_count = sum(1 for c in flat_results if c.get("status") in ["PASS", "Pass"])
    failed_auto_count = sum(1 for c in flat_results if c.get("status") in ["FAIL", "Fail"])
    error_auto_count = sum(1 for c in flat_results if c.get("status") in ["ERROR", "Error"])
    na_auto_count = sum(1 for c in flat_results if c.get("status") in ["N/A", "NA"])
    total_manual = sum(1 for c in flat_results if c.get("status") in ["MANUAL", "Manual"])
    total_errors = error_auto_count
    total_na = na_auto_count

    svg_global_chart_html = build_inline_svg_donut_chart(passed_auto_count, failed_auto_count, error_auto_count, na_auto_count, overall_score)

    category_order = list(dict.fromkeys(rec["category"] for rec in RECOMMENDATIONS_DATA))

    for idx, category in enumerate(category_order):
        category_id = str(idx + 1)
        checks = results.get(category, [])
        cat_info = categories_scores.get(category, {})
        category_score = cat_info.get("score", 0)
        cat_score_class = get_score_class(category_score)
        
        sidebar_links_html += f'<a href="#cat-{category_id}" class="sidebar-link flex items-center p-3 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors mb-1"><span class="w-5 text-xs font-bold mr-3">{category_id}.</span> <span class="truncate text-sm font-medium">{category.split(". ", 1)[-1]}</span></a>'

        checks_rows_html = ""
        def sort_key(check):
            parts = re.split(r'[._-]', check['number'])
            return [int(p) if p.isdigit() else p for p in parts]

        try:
             sorted_checks = sorted(checks, key=sort_key)
        except:
             sorted_checks = checks

        for check in sorted_checks:
            status_icon, status_text, status_class = get_status_info(check["status"])
            tw_status_class = ""
            if check["status"] == "Pass": tw_status_class = "status-pass"
            elif check["status"] == "Fail": tw_status_class = "status-fail"
            elif check["status"] == "Manual": tw_status_class = "status-manual"
            elif check["status"] == "Error": tw_status_class = "status-error"
            else: tw_status_class = "status-na"

            manual_steps_html = ""
            if check.get("manual_steps"):
                steps_list = "".join([f"<li>{html.escape(step)}</li>" for step in check["manual_steps"]])
                manual_steps_html = f"""
                <div class="mb-3 p-3 bg-amber-50 border-l-4 border-amber-400 rounded-r-lg">
                    <div class="text-[10px] font-bold text-amber-600 uppercase mb-1"><i class="fas fa-list-check mr-1"></i> Guide de Validation Manuelle:</div>
                    <ul class="list-decimal list-inside text-xs text-amber-800 space-y-1 font-medium">
                        {steps_list}
                    </ul>
                </div>
                """

            checks_rows_html += CHECK_ROW_TEMPLATE.format(
                number=check["number"],
                name=html.escape(check["name"]),
                test_procedure=html.escape(check["test_procedure"]),
                status_icon=status_icon,
                status_text=status_text,
                status_class=tw_status_class,
                output=html.escape(check["output"]),
                remediation=html.escape(check["remediation"]) if check["remediation"] else "N/A",
                manual_steps_html=manual_steps_html
            )

        categories_html += CATEGORY_REPORT_TEMPLATE.format(
            category_id=category_id,
            category_name=html.escape(category),
            category_score=category_score,
            category_score_class=cat_score_class,
            passed_automated=cat_info.get("passed_automated", 0),
            failed_automated=cat_info.get("failed_automated", 0),
            manual_checks=cat_info.get("manual_checks", 0),
            error_checks=cat_info.get("error_checks", 0),
            na_checks=cat_info.get("na_checks", 0),
            checks_rows=checks_rows_html
        )

    category_manual_counts = json.dumps([categories_scores[cat]["manual_checks"] for cat in category_order])
    total_other = error_auto_count + na_auto_count
    html_output = HTML_TEMPLATE.format(
        report_date=report_date,
        overall_score=overall_score,
        overall_score_class=overall_score_class,
        passed_automated=passed_auto_count,
        total_automated=passed_auto_count + failed_auto_count,
        manual_checks=total_manual,
        error_checks=total_errors,
        na_checks=total_na,
        categories_reports=categories_html,
        svg_global_chart_html=svg_global_chart_html
    )

    try:
        if os.path.dirname(filename):
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_output)
        print(f"Report successfully generated: {filename}")
    except IOError as e:
        print(f"Error writing report file '{filename}': {e}")


# --- Main Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CIS Audit Benchmark (Local & SSH Remote Modes)")
    parser.add_argument("-m", "--mode", choices=["local", "ssh"], default="local", help="Audit execution mode (local or ssh)")
    parser.add_argument("-r", "--remote", "--ssh", dest="remote_host", default=None, help="Remote SSH server target (e.g. user@hostname)")
    parser.add_argument("--local", action="store_true", help="Force local audit execution mode")
    parser.add_argument("-f", "--format", choices=["html", "json", "xml", "txt"], default="html", help="Report output format")
    parser.add_argument("-l", "--lang", choices=["en", "fr"], default="en", help="Report language choice (en/fr)")
    parser.add_argument("-o", "--output", default=None, help="Custom output report file path")
    args = parser.parse_args()

    remote_target = None
    if args.mode == "ssh" or args.remote_host:
        remote_target = args.remote_host
        if not remote_target:
            print("❌ SSH mode requires a remote host target via --remote user@hostname or --ssh user@hostname", file=sys.stderr)
            sys.exit(1)
        print(f"🌐 Running Audit in SSH Remote Mode on host: '{remote_target}'...")
    else:
        print("🖥️  Running Audit in Local Mode on local machine...")

    rules_data = load_recommendations("mariadb_106")
    check_results = perform_checks(rules_data, remote_host=remote_target)
    (overall_score, categories_scores, *rest) = calculate_scores(check_results)
    export_results(check_results, overall_score, categories_scores, target_name="mariadb_106", filename=args.output, fmt=args.format, lang=args.lang)