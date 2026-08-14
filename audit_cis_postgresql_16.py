import argparse
import subprocess
import json
import os
from datetime import datetime
import re # Pour les expressions régulières
import html # Pour échapper les caractères spéciaux HTML

# --- Structure des Recommandations Automatisées ---
# Cette structure traduit le tableau que tu as fourni en données exploitables par le script.
# Chaque entrée contient le numéro, le nom, le type (Automated/Manual),
# la procédure de test (commande shell), le critère de succès attendu, et la remédiation.
# Pour les contrôles "Manual", la procédure de test et le critère attendu sont juste informatifs
# car le script ne peut pas les exécuter.
RECOMMENDATIONS_DATA = [
    # 1. Installation et correctifs
    {"category": "1. Installation et correctifs", "number": "1.1", "name": "Obtenir les paquets depuis des dépôts autorisés", "type": "Manual", "test_procedure": "Vérifier dnf repolist all ou équivalent (apt-file search /usr/pgsql-*/lib/libpq.so.5) pour s’assurer que seuls les dépôts officiels sont activés.", "expected_output": None, "remediation": "Supprimer/ajouter des dépôts pour n’inclure que les sources valides (p. ex. dnf install -y https://download.postgresql.org/.../pgdg-redhat-repo-latest.noarch.rpm), puis réinstaller."},
    {"category": "1. Installation et correctifs", "number": "1.2", "name": "Installer uniquement les paquets requis", "type": "Manual", "test_procedure": "apt search postgresql ou dnf search postgresql, lister les paquets installés et comparer à la liste d’exigences.", "expected_output": None, "remediation": "Purger/effacer les paquets non désirés : apt purge <pkg> ou dnf erase <pkg>."},
    {"category": "1. Installation et correctifs", "number": "1.3", "name": "Activer le service systemd", "type": "Automated", "test_procedure": "systemctl is-enabled postgresql@16-main.service || systemctl is-enabled postgresql-16.service", "expected_output": {"type": "stdout_equals", "value": "enabled"}, "remediation": "systemctl enable postgresql@16-main || systemctl enable postgresql-16"}, # Added common Ubuntu service name
    # Corrected 1.4: Check service status and data directory permissions/ownership
    {"category": "1. Installation et correctifs", "number": "1.4", "name": "Initialiser correctement le cluster de données", "type": "Automated", "sub_checks": [
        {"test_procedure": "systemctl is-active postgresql@16-main.service || systemctl is-active postgresql-16.service", "expected_output": {"type": "stdout_equals", "value": "active"}}, # Check if service is running
        {"test_procedure": "sudo -u postgres psql -t -c 'SHOW data_directory;'", "expected_output": {"type": "stdout_not_empty"}, "store_output_as": "datadir"}, # Get data directory path and store it
        {"test_procedure_template": "ls -ld {datadir}", "expected_output": {"type": "stdout_regex_match", "pattern": r"^drwx------\s+\d+\s+postgres\s+postgres"}}, # Check ownership and permissions (drwx------ postgres postgres)
    ], "remediation": "Supprimer le répertoire de données et relancer initdb (avec checksums si souhaité), puis démarrer le service. Assurer les bonnes permissions sur le répertoire de données."},
    {"category": "1. Installation et correctifs", "number": "1.5", "name": "Appliquer les derniers correctifs de sécurité", "type": "Manual", "test_procedure": "psql -c 'SHOW server_version' et comparer à la liste des versions disponibles sur la page de news PostgreSQL.", "expected_output": None, "remediation": "sudo apt update && sudo apt upgrade postgresql-16*"}, # Adapted remediation for Ubuntu/apt
    {"category": "1. Installation et correctifs", "number": "1.6", "name": "Vérifier que PGPASSWORD n'est pas défini dans les profils", "type": "Automated", "test_procedure": "! grep -q PGPASSWORD /home/*/.{bashrc,profile,bash_profile} /etc/environment", "expected_output": {"type": "returncode_zero"}, "remediation": "Empêcher le stockage en clair du mot de passe via la variable d’environnement PGPASSWORD.\nSupprimer toute définition de PGPASSWORD dans les scripts de connexion, utiliser ~/.pgpass ou une méthode sécurisée. "}, # Use bash features for grep -q and negation, added description
    {"category": "1. Installation et correctifs", "number": "1.7", "name": "Vérifier que PGPASSWORD n'est pas utilisé par un processus", "type": "Automated", "test_procedure": "! pgrep -a PGPASSWORD", "expected_output": {"type": "returncode_zero"}, "remediation": "S’assurer qu’aucun processus n’utilise la variable PGPASSWORD.\nIdentifier et modifier les scripts/processus pour ne plus utiliser PGPASSWORD."}, # Use pgrep for active processes, added description

    # 2. Permissions de répertoires et fichiers
    {"category": "2. Permissions de répertoires et fichiers", "number": "2.1", "name": "Masque de permissions (umask)", "type": "Manual", "test_procedure": "En tant que postgres, exécuter umask, doit afficher 0077 ou plus restrictif.", "expected_output": None, "remediation": "Configurer le umask de l’utilisateur postgres à 0077 pour restreindre la création de fichiers.\nAjouter umask 077 dans ~postgres/.bash_profile (ou .profile/.bashrc), recharger le profil."}, # Added description
    {"category": "2. Permissions de répertoires et fichiers", "number": "2.2", "name": "Propriétaire et permissions du répertoire d’extensions", "type": "Automated", "path_command": "sudo -u postgres pg_config --sharedir", "test_procedure_template": "ls -ld {path}/extension", "expected_output": {"type": "stdout_regex_match", "pattern": r"^drwxr-xr-x\s+\d+\s+root\s+root"}, "remediation": "Vérifier que $(pg_config --sharedir)/extension appartient à root:root et chmod 0755.\nchown root:root $(sudo -u postgres pg_config --sharedir)/extension && chmod 0755 $(sudo -u postgres pg_config --sharedir)/extension."}, # Corrected remediation command, added description
    {"category": "2. Permissions de répertoires et fichiers", "number": "2.3", "name": "Désactiver l’historique des commandes psql", "type": "Automated", "test_procedure": "! find /home -name .psql_history -print -quit", "expected_output": {"type": "returncode_zero"}, "remediation": "Empêcher la création de ~/.psql_history pour limiter l’exposition de données sensibles.\nSupprimer le fichier .psql_history et ajouter \\set HISTFILE /dev/null dans ~/.psqlrc ou créer un lien symbolique vers /dev/null."}, # Find will return 0 if found, 1 if not found. We want return code 1 (not found) to pass, thus negate., added description
    {"category": "2. Permissions de répertoires et fichiers", "number": "2.4", "name": "Ne pas stocker de mots de passe dans les fichiers de service", "type": "Manual", "test_procedure": "grep -H password /etc/postgresql/.../pg_service.conf et dans les home utilisateurs", "expected_output": None, "remediation": "Vérifier qu’aucun .pg_service.conf ne contient password= en clair.\nSupprimer toutes les lignes password= identifiées."}, # Added description

    # 3. Journalisation et audit
    {"category": "3. Journalisation et audit", "number": "3.1.2", "name": "Configurer log_destination", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW log_destination;'", "expected_output": {"type": "stdout_not_empty"}, "remediation": "Définir la ou les destinations de logs (stderr, csvlog, syslog, jsonlog).\nALTER SYSTEM SET log_destination = 'csvlog'; SELECT pg_reload_conf();"}, # Added description
    {"category": "3. Journalisation et audit", "number": "3.1.3", "name": "Activer logging_collector", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW logging_collector;'", "expected_output": {"type": "stdout_equals", "value": "on"}, "remediation": "Capturer stderr dans des fichiers via le démon collector.\nALTER SYSTEM SET logging_collector = 'on'; puis systemctl restart postgresql@16-main || systemctl restart postgresql-16."}, # Adapted restart command, added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.4", "name": "Définir log_directory", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW log_directory;'", "expected_output": {"type": "stdout_not_empty"}, "remediation": "Spécifier le répertoire de sortie des fichiers de logs (ex. /var/log/postgres).\nALTER SYSTEM SET log_directory = '/var/log/postgres'; SELECT pg_reload_conf();"}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.5", "name": "Définir log_filename", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW log_filename;'", "expected_output": {"type": "stdout_contains", "value": "%Y"}, "remediation": "Choisir un motif de nom de fichier strftime (e.g. postgresql-%Y%m%d.log).\nALTER SYSTEM SET log_filename = 'postgresql-%Y%m%d.log'; SELECT pg_reload_conf();"}, # Checking for %Y as recommended format, added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.6", "name": "Configurer log_file_mode", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW log_file_mode;'", "expected_output": {"type": "stdout_contains_any", "values": ["0600", "0640"]}, "remediation": "Fixer les permissions des fichiers de log à 0600 (ou 0640 selon le groupe).\nALTER SYSTEM SET log_file_mode = '0600'; SELECT pg_reload_conf();"}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.7", "name": "Activer log_truncate_on_rotation", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW log_truncate_on_rotation;'", "expected_output": {"type": "stdout_equals", "value": "on"}, "remediation": "Tronquer les fichiers existants lors de la rotation si même nom.\nALTER SYSTEM SET log_truncate_on_rotation = 'on'; SELECT pg_reload_conf();"}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.8", "name": "Définir log_rotation_age", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW log_rotation_age;'", "expected_output": {"type": "stdout_not_equals", "value": "0"}, "remediation": "Limiter la durée de vie des fichiers de log (ex. 1d).\nALTER SYSTEM SET log_rotation_age = '1d'; SELECT pg_reload_conf();"}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.9", "name": "Définir log_rotation_size", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW log_rotation_size;'", "expected_output": {"type": "stdout_not_equals", "value": "0"}, "remediation": "Limiter la taille des fichiers de log (ex. 1GB).\nALTER SYSTEM SET log_rotation_size = '1GB'; SELECT pg_reload_conf();"}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.10", "name": "Choisir syslog_facility", "type": "Manual", "test_procedure": "SHOW syslog_facility;", "expected_output": None, "remediation": "Définir la facility Syslog (LOCAL0–LOCAL7).\nALTER SYSTEM SET syslog_facility = 'LOCAL1'; SELECT pg_reload_conf();"}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.11", "name": "Activer syslog_split_messages", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW syslog_split_messages;'", "expected_output": {"type": "stdout_equals", "value": "on"}, "remediation": "Couper les messages trop longs (>1024 octets) pour Syslog.\nALTER SYSTEM SET syslog_split_messages = 'on'; SELECT pg_reload_conf();"}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.12", "name": "Prévenir la perte de messages Syslog", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW syslog_split_messages;'", "expected_output": {"type": "stdout_equals", "value": "on"}, "remediation": "Éviter la suppression des messages volumineux dans Syslog.\nMême que 3.1.11."}, # Refers to 3.1.11, added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.13", "name": "Configurer syslog_ident", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW syslog_ident;'", "expected_output": {"type": "stdout_not_empty"}, "remediation": "Définir l’identifiant de programme dans Syslog (ex. postgres).\nALTER SYSTEM SET syslog_ident = 'proddb'; SELECT pg_reload_conf();"}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.14", "name": "Assurer les bons messages dans le log serveur", "type": "Manual", "test_procedure": "Consulter postgresql.conf et SHOW log_statement;/SHOW log_min_messages;.", "expected_output": None, "remediation": "Vérifier que seuls les messages pertinents (erreurs, connexions, requêtes) sont enregistrés.\nALTER SYSTEM SET log_statement = 'all'; ALTER SYSTEM SET log_min_error_statement = 'error'; etc., puis SELECT pg_reload_conf();."}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.15", "name": "Enregistrer les SQL en erreur", "type": "Automated", "sub_checks": [
        {"test_procedure": "sudo -u postgres psql -t -c 'SHOW client_min_messages;'", "expected_output": {"type": "stdout_contains_any", "values": ["error", "log", "warning", "notice", "info", "debug"]}}, # client_min_messages should allow seeing errors.
        {"test_procedure": "sudo -u postgres psql -t -c 'SHOW log_error_verbosity;'", "expected_output": {"type": "stdout_equals", "value": "verbose"}}
    ], "remediation": "Consigner les instructions SQL ayant généré des erreurs.\nALTER SYSTEM SET log_error_verbosity = 'verbose'; puis SELECT pg_reload_conf();."}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.16", "name": "Désactiver debug_print_parse", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW debug_print_parse;'", "expected_output": {"type": "stdout_equals", "value": "off"}, "remediation": "Ne pas afficher les arbres d’analyse SQL dans les logs (réduction du bruit).\nALTER SYSTEM SET debug_print_parse = 'off'; SELECT pg_reload_conf();"}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.17", "name": "Désactiver debug_print_rewritten", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW debug_print_rewritten;'", "expected_output": {"type": "stdout_equals", "value": "off"}, "remediation": "Ne pas afficher les arbres réécrits SQL dans les logs.\nALTER SYSTEM SET debug_print_rewritten = 'off'; SELECT pg_reload_conf();"}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.18", "name": "Désactiver debug_print_plan", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW debug_print_plan;'", "expected_output": {"type": "stdout_equals", "value": "off"}, "remediation": "Ne pas afficher les plans d’exécution SQL dans les logs.\nALTER SYSTEM SET debug_print_plan = 'off'; SELECT pg_reload_conf();"}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.19", "name": "Activer debug_pretty_print", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW debug_pretty_print;'", "expected_output": {"type": "stdout_equals", "value": "on"}, "remediation": "Formater lisiblement les arbres d’analyse/réécriture dans les logs.\nALTER SYSTEM SET debug_pretty_print = 'on'; SELECT pg_reload_conf();."}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.20", "name": "Activer log_connections", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW log_connections;'", "expected_output": {"type": "stdout_equals", "value": "on"}, "remediation": "Enregistrer chaque nouvelle connexion à PostgreSQL.\nALTER SYSTEM SET log_connections = 'on'; SELECT pg_reload_conf();."}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.21", "name": "Activer log_disconnections", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW log_disconnections;'", "expected_output": {"type": "stdout_equals", "value": "on"}, "remediation": "Enregistrer chaque déconnexion de PostgreSQL.\nALTER SYSTEM SET log_disconnections = 'on'; SELECT pg_reload_conf();."}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.22", "name": "Configurer log_error_verbosity", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW log_error_verbosity;'", "expected_output": {"type": "stdout_equals", "value": "verbose"}, "remediation": "Contrôler la verbosité des messages d’erreur (DEFAULT, VERBOSE).\nALTER SYSTEM SET log_error_verbosity = 'verbose'; SELECT pg_reload_conf();."}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.23", "name": "Configurer log_hostname", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW log_hostname;'", "expected_output": {"type": "stdout_equals", "value": "off"}, "remediation": "Indiquer le nom d’hôte ou l’IP dans les logs de connexion.\nALTER SYSTEM SET log_hostname = 'off'; SELECT pg_reload_conf();."}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.24", "name": "Configurer log_line_prefix", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW log_line_prefix;'", "expected_output": {"type": "stdout_contains", "value": "%t"}, "remediation": "Définir le préfixe de ligne (timestamp, utilisateur, base, etc.) dans chaque log.\nALTER SYSTEM SET log_line_prefix = '%m [%p] user=%u db=%d '; SELECT pg_reload_conf();."}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.25", "name": "Configurer log_statement", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW log_statement;'", "expected_output": {"type": "stdout_contains_any", "values": ["ddl", "mod", "all"]}, "remediation": "Choisir le niveau de requêtes à logger (none, ddl, mod, all).\nALTER SYSTEM SET log_statement = 'ddl'; SELECT pg_reload_conf();."}, # Added description
    {"category": "3.1. Journalisation des erreurs serveur", "number": "3.1.26", "name": "Configurer log_timezone", "type": "Automated", "test_procedure": "sudo -u postgres psql -t -c 'SHOW log_timezone;'", "expected_output": {"type": "stdout_equals", "value": "UTC"}, "remediation": "Uniformiser le fuseau horaire des horodatages des logs (ex. UTC).\nALTER SYSTEM SET log_timezone = 'UTC'; SELECT pg_reload_conf();."}, # Added description
    {"category": "3. Journalisation et audit", "number": "3.2", "name": "Activer l’extension pgAudit", "type": "Automated", "test_procedure": "Installer et configurer l’extension d’audit avancé pgAudit pour capturer les activités.\nSELECT * FROM pg_extension WHERE extname = 'pgaudit';", "expected_output": {"type": "stdout_contains", "value": "pgaudit"}, "remediation": "Installer et configurer l’extension d’audit avancé pgAudit pour capturer les activités.\nCREATE EXTENSION pgaudit; ALTER SYSTEM SET pgaudit.log = 'all'; SELECT pg_reload_conf();"}, # Check if query returns 1 (extension exists), added description, changed expected output

    # 4. Accès et autorisations utilisateur
    {"category": "4. Accès et autorisations utilisateur", "number": "4.1", "name": "Désactiver la connexion interactive", "type": "Manual", "test_procedure": "Empêcher les rôles superutilisateurs sans console SSH d’interagir localement.\nVérifier dans pg_hba.conf qu’aucune ligne local .. trust pour les superutilisateurs", "expected_output": None, "remediation": "Empêcher les rôles superutilisateurs sans console SSH d’interagir localement.\nModifier pg_hba.conf, passer à md5 ou peer, puis SELECT pg_reload_conf();."}, # Added description
    {"category": "4. Accès et autorisations utilisateur", "number": "4.2", "name": "Configurer sudo correctement", "type": "Manual", "test_procedure": "Restreindre l’usage de sudo pour l’utilisateur système postgres.\nExaminer /etc/sudoers et fichiers dans /etc/sudoers.d/ pour la section postgres.", "expected_output": None, "remediation": "Restreindre l’usage de sudo pour l’utilisateur système postgres.\nExaminer /etc/sudoers et fichiers dans /etc/sudoers.d/ pour la section postgres.\nAjuster les droits sudo (ex. postgres ALL=(ALL) NOPASSWD: /usr/pgsql-16/bin/pg_*)."}, # Added description
    {"category": "4. Accès et autorisations utilisateur", "number": "4.3", "name": "Révoquer les privilèges administratifs excessifs", "type": "Manual", "test_procedure": "Retirer aux rôles non justifiés les attributs SUPERUSER, CREATEDB, CREATEROLE, REPLICATION.\n\\du+ doit lister uniquement les rôles autorisés avec ces attributs.", "expected_output": None, "remediation": "Retirer aux rôles non justifiés les attributs SUPERUSER, CREATEDB, CREATEROLE, REPLICATION.\n\\du+ doit lister uniquement les rôles autorisés avec ces attributs.\nALTER ROLE <user> NOSUPERUSER NOCREATEDB NOCREATEROLE;."}, # Added description
    {"category": "4. Accès et autorisations utilisateur", "number": "4.4", "name": "Verrouiller les comptes inactifs", "type": "Manual", "test_procedure": "Désactiver les rôles non utilisés depuis un certain temps.\nSELECT rolname, rolvaliduntil FROM pg_authid; vérifier dates d’expiration.", "expected_output": None, "remediation": "Désactiver les rôles non utilisés depuis un certain temps.\nSELECT rolname, rolvaliduntil FROM pg_authid; vérifier dates d’expiration.\nALTER ROLE <user> NOLOGIN; ou définir VALID UNTIL à une date passée."}, # Added description
    {"category": "4. Accès et autorisations utilisateur", "number": "4.5", "name": "Révoquer les privilèges de fonction excessifs", "type": "Manual", "test_procedure": "Restreindre l’EXECUTE sur les fonctions définies aux seuls rôles nécessaires.\nRequête sur pg_proc et has_function_privilege().", "expected_output": None, "remediation": "Restreindre l’EXECUTE sur les fonctions définies aux seuls rôles nécessaires.\nRequête sur pg_proc et has_function_privilege().\nREVOKE EXECUTE ON FUNCTION <schema>.<func>() FROM <role>;."}, # Marked Manual as the test procedure is complex/policy-dependent, added description
    {"category": "4. Accès et autorisations utilisateur", "number": "4.6", "name": "Révoquer les privilèges DML excessifs", "type": "Manual", "test_procedure": "Restreindre INSERT/UPDATE/DELETE aux tables selon le besoin des rôles applicatifs.\nInventaire via has_table_privilege() pour chaque table et utilisateur.", "expected_output": None, "remediation": "Restreindre INSERT/UPDATE/DELETE aux tables selon le besoin des rôles applicatifs.\nInventaire via has_table_privilege() pour chaque table et utilisateur.\nREVOKE INSERT, UPDATE, DELETE ON TABLE <tbl> FROM <role>;."}, # Added description
    {"category": "4. Accès et autorisations utilisateur", "number": "4.7", "name": "Configurer Row Level Security (RLS)", "type": "Manual", "test_procedure": "Activer RLS pour les tables sensibles et définir des politiques restrictives.\n\\d+ <table> doit indiquer Row Level Security: enabled.", "expected_output": None, "remediation": "Activer RLS pour les tables sensibles et définir des politiques restrictives.\n\\d+ <table> doit indiquer Row Level Security: enabled.\nALTER TABLE <tbl> ENABLE ROW LEVEL SECURITY; CREATE POLICY ...;."}, # Added description
    {"category": "4. Accès et autorisations utilisateur", "number": "4.8", "name": "Installer l’extension set_user", "type": "Automated", "test_procedure": "Utiliser set_user pour l’émulation de rôles et la révocabilité de sessions.\nSELECT * FROM pg_extension WHERE extname = 'set_user';", "expected_output": {"type": "stdout_contains", "value": "set_user"}, "remediation": "Utiliser set_user pour l’émulation de rôles et la révocabilité de sessions.\nCREATE EXTENSION set_user;"}, # Added description, changed expected output to check for extension name in output
    {"category": "4. Accès et autorisations utilisateur", "number": "4.9", "name": "Utiliser les rôles prédéfinis", "type": "Manual", "test_procedure": "Favoriser les rôles intégrés (pg_read_all_data, etc.) plutôt que superuser pour les accès.\n\\du+ vérifie la présence et l’usage des rôles prédéfinis.", "expected_output": None, "remediation": "Favoriser les rôles intégrés (pg_read_all_data, etc.) plutôt que superuser pour les accès.\n\\du+ vérifie la présence et l’usage des rôles prédéfinis.\nGRANT pg_read_all_data TO <role>; REVOKE ...."}, # Added description

    # 5. Connexion et authentification
    {"category": "5. Connexion et authentification", "number": "5.1", "name": "Ne pas passer de mot de passe en ligne de commande", "type": "Manual", "test_procedure": "Éviter psql -U user -W password dans les scripts shell.\nExaminer les processus en cours (`ps aux | grep psql`) et scripts automatisés.", "expected_output": None, "remediation": "Éviter psql -U user -W password dans les scripts shell.\nModifier les scripts pour utiliser ~/.pgpass ou une méthode sécurisée."}, # Added description
    {"category": "5. Connexion et authentification", "number": "5.2", "name": "Lier PostgreSQL à une adresse IP", "type": "Manual", "test_procedure": "Restreindre l’écoute à l’interface prévue (listen_addresses).\nSHOW listen_addresses; doit afficher l’IP autorisée ou localhost.", "expected_output": None, "remediation": "Restreindre l’écoute à l’interface prévue (listen_addresses).\nModifier postgresql.conf (listen_addresses = '192.0.2.1' ou '*') et redémarrer le service."}, # Added '*' option, added description
    {"category": "5. Connexion et authentification", "number": "5.3", "name": "Configurer la connexion UNIX locale", "type": "Manual", "test_procedure": "Sécuriser les entrées local dans pg_hba.conf pour n’autoriser que peer ou md5.\nVérifier les lignes local all all trust dans pg_hba.conf.", "expected_output": None, "remediation": "Sécuriser les entrées local dans pg_hba.conf pour n’autoriser que peer ou md5.\nModifier (ou ajouter) local all all peer ou md5 dans pg_hba.conf, puis SELECT pg_reload_conf();."}, # Added md5 option, added description
    {"category": "5. Connexion et authentification", "number": "5.4", "name": "Configurer la connexion TCP/IP", "type": "Manual", "test_procedure": "Sécuriser les entrées host dans pg_hba.conf (CIDR, méthode d’authentification).\nVérifier host all all 10.0.0.0/24 md5.", "expected_output": None, "remediation": "Sécuriser les entrées host dans pg_hba.conf (CIDR, méthode d’authentification).\nModifier pg_hba.conf pour utiliser des CIDR restreints et des méthodes d'authentification fortes (md5, scram-sha-256, cert, etc.), redémarrer ou recharger."}, # More general remediation, added description
    {"category": "5. Connexion et authentification", "number": "5.5", "name": "Limites de connexion par compte", "type": "Manual", "test_procedure": "Empêcher un même rôle d’ouvrir trop de connexions simultanées.\nSELECT rolname, rolconnlimit FROM pg_authid;.", "expected_output": None, "remediation": "Empêcher un même rôle d’ouvrir trop de connexions simultanées.\nALTER ROLE <user> CONNECTION LIMIT 10;."}, # Marked Manual as the pass condition is policy-dependent, added description
    {"category": "5. Connexion et authentification", "number": "5.6", "name": "Configurer la complexité des mots de passe", "type": "Manual", "test_procedure": "Imposer un contrôle de la complexité (extensions passwordcheck, pam, etc.).\nVérifier la présence de password_encryption, modules pam ou passwordcheck.", "expected_output": None, "remediation": "Imposer un contrôle de la complexité (extensions passwordcheck, pam, etc.).\nInstaller/configurer passwordcheck ou pam, définir password_encryption = 'scram-sha-256'."}, # Added description

    # 6. Paramètres PostgreSQL
    {"category": "6. Paramètres PostgreSQL", "number": "6.1", "name": "Comprendre vecteurs d’attaque et paramètres runtime", "type": "Manual", "test_procedure": "Documenter les vecteurs d’attaque possibles et les paramètres ajustables.\nRéviser postgresql.conf pour lister runtime parameters.", "expected_output": None, "remediation": "Documenter les vecteurs d’attaque possibles et les paramètres ajustables.\nMettre à jour la documentation interne, auditer régulièrement."}, # Added description
    {"category": "6. Paramètres PostgreSQL", "number": "6.2", "name": "Configurer les paramètres backend", "type": "Automated", "sub_checks": [ # Check key parameters are set to something reasonable (not 0 or defaults depending on context)
        {"test_procedure": "sudo -u postgres psql -t -c 'SHOW max_connections;'", "expected_output": {"type": "stdout_is_numeric_greater_than", "value": 0}},
        {"test_procedure": "sudo -u postgres psql -t -c 'SHOW shared_buffers;'", "expected_output": {"type": "stdout_not_equals", "value": "128kB"}}, # Default is 128kB, check if changed
        {"test_procedure": "sudo -u postgres psql -t -c 'SHOW work_mem;'", "expected_output": {"type": "stdout_not_equals", "value": "4MB"}} # Default is 4MB, check if changed
    ], "remediation": "Ajuster max_connections, shared_buffers, work_mem, etc., pour limiter l’exposition.\nALTER SYSTEM SET max_connections = 100; ALTER SYSTEM SET shared_buffers = '...'; ALTER SYSTEM SET work_mem = '...'; SELECT pg_reload_conf();"}, # Added description
    {"category": "6. Paramètres PostgreSQL", "number": "6.3", "name": "Configurer Postmaster runtime parameters", "type": "Manual", "test_procedure": "Ajuster data_directory, hba_file, ident_file, etc.\nVérifier SHOW data_directory, hba_file, ident_file;", "expected_output": None, "remediation": "Ajuster data_directory, hba_file, ident_file, etc.\nModifier postgresql.conf puis redémarrer."}, # Added description
    {"category": "6. Paramètres PostgreSQL", "number": "6.4", "name": "Configurer les signaux SIGHUP", "type": "Manual", "test_procedure": "Sécuriser la réaction aux signaux de rechargement de configuration.\nTester SELECT pg_reload_conf();.", "expected_output": None, "remediation": "Sécuriser la réaction aux signaux de rechargement de configuration.\nAucun changement automatique ; documenter le processus."}, # Added description
    {"category": "6. Paramètres PostgreSQL", "number": "6.5", "name": "Configurer les paramètres Superuser", "type": "Manual", "test_procedure": "Restreindre statement_timeout, idle_in_transaction_session_timeout pour les superusers.\nSHOW statement_timeout, idle_in_transaction_session_timeout;.", "expected_output": None, "remediation": "Restreindre statement_timeout, idle_in_transaction_session_timeout pour les superusers.\nALTER SYSTEM SET statement_timeout = '...'; ALTER SYSTEM SET idle_in_transaction_session_timeout = '5min'; puis recharger."}, # Added statement_timeout, added description
    {"category": "6. Paramètres PostgreSQL", "number": "6.6", "name": "Configurer les paramètres User", "type": "Manual", "test_procedure": "Ajuster log_statement, search_path, etc., pour les rôles standards.\nVérifier SHOW search_path;.", "expected_output": None, "remediation": "Ajuster log_statement, search_path, etc., pour les rôles standards.\nALTER ROLE <user> SET search_path TO '$user', public;."}, # Added description
    {"category": "6. Paramètres PostgreSQL", "number": "6.7", "name": "Utiliser la cryptographie FIPS 140-2", "type": "Automated", "test_procedure": "S’assurer qu’OpenSSL FIPS est utilisé si requis.\nSHOW ssl_library; et vérifier la version OpenSSL.", "expected_output": {"type": "stdout_contains", "value": "OpenSSL"}, "remediation": "S’assurer qu’OpenSSL FIPS est utilisé si requis.\nRecompiler PostgreSQL avec FIPS ou configurer la bibliothèque FIPS."}, # Check if OpenSSL is used, FIPS mode is a system/compile-time config, added description
    {"category": "6. Paramètres PostgreSQL", "number": "6.8", "name": "Activer et configurer TLS", "type": "Automated", "sub_checks": [
        {"test_procedure": "sudo -u postgres psql -t -c 'SHOW ssl;'", "expected_output": {"type": "stdout_equals", "value": "on"}},
        {"test_procedure": "sudo -u postgres psql -t -c 'SHOW ssl_cert_file;'", "expected_output": {"type": "stdout_not_empty"}},
        {"test_procedure": "sudo -u postgres psql -t -c 'SHOW ssl_key_file;'", "expected_output": {"type": "stdout_not_empty"}}
    ], "remediation": "Installer certificats TLS et configurer ssl_cert_file, ssl_key_file.\nCopier les certificats, ALTER SYSTEM SET ssl = 'on'; SELECT pg_reload_conf();."}, # Added description
    {"category": "6. Paramètres PostgreSQL", "number": "6.9", "name": "Configurer TLSv1.3+", "type": "Automated", "test_procedure": "Forcer au minimum TLSv1.3.\nSHOW ssl_min_protocol_version; doit être TLSv1.3.", "expected_output": {"type": "stdout_equals", "value": "TLSv1.3"}, "remediation": "Forcer au minimum TLSv1.3.\nALTER SYSTEM SET ssl_min_protocol_version = 'TLSv1.3'; SELECT pg_reload_conf();."}, # Added description
    # Corrected 6.10: Handle potential unrecognized parameter error
    {"category": "6. Paramètres PostgreSQL", "number": "6.10", "name": "Désactiver les cipher suites faibles", "type": "Automated", "test_procedure": "Exclure RC4, DES, etc., dans ssl_cipher_suites.\nSHOW ssl_cipher_suites; vérifier l’absence de ciphers faibles.", "expected_output": {"type": "stdout_not_contains_any", "values": ["RC4", "DES", "3DES", "MD5", "SHA1"]}, "remediation": "Exclure RC4, DES, etc., dans ssl_cipher_suites.\nALTER SYSTEM SET ssl_cipher_suites = 'HIGH:!aNULL'; SELECT pg_reload_conf();.", "possible_errors": ["unrecognized configuration parameter"]}, # Added possible_errors, added description, corrected test procedure
    {"category": "6. Paramètres PostgreSQL", "number": "6.11", "name": "Installer et configurer pgcrypto", "type": "Automated", "test_procedure": "Activer pgcrypto pour fonctions cryptographiques.\nSELECT * FROM pg_extension WHERE extname = 'pgcrypto';", "expected_output": {"type": "stdout_contains", "value": "pgcrypto"}, "remediation": "Activer pgcrypto pour fonctions cryptographiques.\nCREATE EXTENSION pgcrypto;"}, # Check if query returns 1 (extension exists), added description, changed expected output

    # 7. Réplication
    {"category": "7. Réplication", "number": "7.1", "name": "Créer un utilisateur de réplication dédié", "type": "Manual", "test_procedure": "Ne pas réutiliser postgres pour la réplication.\nSELECT rolname, rolreplication FROM pg_roles WHERE rolname = '<user>';", "expected_output": None, "remediation": "Ne pas réutiliser postgres pour la réplication.\nCREATE USER repuser REPLICATION LOGIN ENCRYPTED PASSWORD '…';."}, # Added description
    {"category": "7. Réplication", "number": "7.2", "name": "Journaliser les commandes de réplication", "type": "Automated", "test_procedure": "Activer log_replication_commands pour tracer les actions de réplication.\nSHOW log_replication_commands; doit être on.", "expected_output": {"type": "stdout_equals", "value": "on"}, "remediation": "Activer log_replication_commands pour tracer les actions de réplication.\nALTER SYSTEM SET log_replication_commands = 'on'; SELECT pg_reload_conf();."}, # Added description
    {"category": "7. Réplication", "number": "7.3", "name": "Configurer les sauvegardes de base", "type": "Manual", "test_procedure": "Vérifier que pg_basebackup ou équivalent génère des sauvegardes fonctionnelles.\nExécuter pg_basebackup -h localhost … et vérifier l’intégrité des fichiers.", "expected_output": None, "remediation": "Vérifier que pg_basebackup ou équivalent génère des sauvegardes fonctionnelles.\nMettre en place un script de sauvegarde automatisée avec pg_basebackup."}, # Added description
    {"category": "7. Réplication", "number": "7.4", "name": "Configurer l’archivage WAL", "type": "Automated", "sub_checks": [
        {"test_procedure": "sudo -u postgres psql -t -c 'SHOW archive_mode;'", "expected_output": {"type": "stdout_equals", "value": "on"}},
        {"test_procedure": "sudo -u postgres psql -t -c 'SHOW archive_command;'", "expected_output": {"type": "stdout_not_empty"}} # Check if archive_command is set
    ], "remediation": "Activer archive_mode et archive_command pour conserver les WAL.\nALTER SYSTEM SET archive_mode = 'on'; ALTER SYSTEM SET archive_command = 'cp %p /archive/%f'; SELECT pg_reload_conf();."}, # Added description
    {"category": "7. Réplication", "number": "7.5", "name": "Configurer les paramètres de streaming", "type": "Manual", "test_procedure": "Ajuster primary_conninfo, max_wal_senders, hot_standby.\nSHOW primary_conninfo, max_wal_senders, hot_standby;.", "expected_output": None, "remediation": "Ajuster primary_conninfo, max_wal_senders, hot_standby.\nALTER SYSTEM SET max_wal_senders = 3; ALTER SYSTEM SET hot_standby = 'on'; SELECT pg_reload_conf();."}, # Added description

    # 8. Considérations spéciales de configuration
    {"category": "8. Considérations spéciales de configuration", "number": "8.1", "name": "Emplacements hors du cluster de données", "type": "Manual", "test_procedure": "Placer les répertoires temporaires et de logs en dehors de $PGDATA pour éviter leur inclusion.\nCheck SHOW temp_tablespaces, log_directory;", "expected_output": None, "remediation": "Placer les répertoires temporaires et de logs en dehors de $PGDATA pour éviter leur inclusion.\nSet temp_tablespaces and log_directory on another volume and reload."}, # Added description
    # Corrected 8.2: Handle command not found
    {"category": "8. Considérations spéciales de configuration", "number": "8.2", "name": "Installer/configurer pgBackRest", "type": "Automated", "test_procedure": "sudo pgbackrest info", "expected_output": {"type": "stdout_contains", "value": "stanza:"}, "remediation": "Utiliser pgBackRest pour des sauvegardes et restaurations robustes.\nInstaller le paquet pgbackrest et configurer au moins une stanza (pgbackrest stanza-create)."}, # Check if pgbackrest info shows at least one stanza, improved remediation, added description
    {"category": "8. Considérations spéciales de configuration", "number": "8.3", "name": "Vérifier autres paramètres divers", "type": "Manual", "test_procedure": "Contrôler toute autre configuration (temp_file_limit, temp_tablespaces, …) selon les besoins.\nRevoir postgresql.conf pour paramètres personnalisés.", "expected_output": None, "remediation": "Contrôler toute autre configuration (temp_file_limit, temp_tablespaces, …) selon les besoins.\nAjuster manuellement puis recharger la configuration."} # Added description
]

# --- Modèle HTML ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CIS Benchmark Audit Report PostgreSQL 16 Benchmark</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    
    <style>
        /* Styles personnalisés si nécessaire */
        .status-pass {{ color: #10B981; }} /* green-500 */
        .status-fail {{ color: #EF4444; }} /* red-500 */
        .status-manual {{ color: #F59E0B; }} /* yellow-500 */
        .status-error {{ color: #6B7280; }} /* gray-500 */
        .status-na {{ color: #9CA3AF; }} /* gray-400 */
        pre {{ white-space: pre-wrap; word-wrap: break-word; }}
        table {{ table-layout: fixed; width: 100%; }} /* Added for better column width control */
        td, th {{ word-break: break-word; }} /* Allow breaking long words */
        .chart-container {{ width: 300px; height: 300px; margin: 20px auto; }} /* Style for chart container */
        .category-chart-container {{ width: 80%; margin: 20px auto; }} /* Style for category chart container */
    </style>
</head>
<body class="font-sans bg-gray-100 text-gray-800 p-6">
    <div class="container mx-auto bg-white p-8 rounded-lg shadow-lg">
        <h1 class="text-3xl font-bold mb-6 text-gray-900">CIS Benchmark Audit Report PostgreSQL 16 Benchmark</h1>
        <p class="text-gray-600 mb-4">Report Date: {report_date}</p>
        <p class="text-gray-600 mb-8">Generated by an automated script based on recommendations from Jean-Marie Renouard (Version 1.0 du 13 Avril 2025).</p>

        <div class="mb-8 p-4 bg-gray-50 rounded-md border border-gray-200">
            <h2 class="text-2xl font-semibold mb-3 text-gray-800">Score Global</h2>
            <p class="text-xl font-bold {overall_score_class}">{overall_score:.2f}%</p>
            <p class="text-gray-700">des contrôles automatisés réussis ({passed_automated}/{total_automated} vérifiés).</p>
             <p class="text-gray-700">{manual_checks} contrôles nécessitent une vérification manuelle.</p>
             <p class="text-gray-700">{error_checks} controls encountered an execution error.</p>
             <p class="text-gray-700">{na_checks} contrôles ne sont pas applicables (paramètre non reconnu, etc.).</p>

             {svg_global_chart_html}
        </div>

        {categories_reports}

    </div>

    <script>
        // Data for the overall pie chart
        const overallChartData = {{
            labels: ['Pass', 'Fail', 'Error', 'N/A'],
            datasets: [{{
                label: 'Résultats des contrôles automatisés',
                data: [{passed_automated_count}, {failed_automated_count}, {error_automated_count}, {na_automated_count}],
                backgroundColor: [
                    '#10B981', // green-500
                    '#EF4444', // red-500
                    '#6B7280', // gray-500
                    '#9CA3AF'  // gray-400
                ],
                hoverOffset: 4
            }}]
        }};

        // Configuration options for the overall pie chart
        const overallChartConfig = {{
            type: 'pie',
            data: overallChartData,
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'top',
                    }},
                    title: {{
                        display: true,
                        text: 'Répartition des contrôles automatisés (Global)'
                    }}
                }}
            }}
        }};

        // Render the overall chart
        const overallScoreChart = new Chart(
            document.getElementById('overallScoreChart'),
            overallChartConfig
        );

        // Data and configuration for category bar charts
        const categoryChartData = {{
            labels: {category_labels}, // List of category names
            datasets: [
                {{
                    label: 'Pass',
                    data: {category_pass_counts},
                    backgroundColor: '#10B981', // green-500
                }},
                {{
                    label: 'Fail',
                    data: {category_fail_counts},
                    backgroundColor: '#EF4444', // red-500
                }},
                {{
                    label: 'Error',
                    data: {category_error_counts},
                    backgroundColor: '#6B7280', // gray-500
                }},
                 {{
                    label: 'N/A',
                    data: {category_na_counts},
                    backgroundColor: '#9CA3AF', // gray-400
                }}
            ]
        }};

        const categoryChartConfig = {{
            type: 'bar',
            data: categoryChartData,
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'top',
                    }},
                    title: {{
                        display: true,
                        text: 'Répartition des contrôles automatisés par catégorie'
                    }}
                }},
                scales: {{
                    x: {{
                        stacked: true,
                    }},
                    y: {{
                        stacked: true,
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Nombre de contrôles'
                        }}
                    }}
                }}
            }}
        }};

        // Render the category bar chart
         const categoryScoreChart = new Chart(
            document.getElementById('categoryChart'),
            categoryChartConfig
        );

    </script>
</body>
</html>
"""

def load_html_template():
    """Load common HTML report template from templates/ or fallback."""
    tmpl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "report_template.html")
    if os.path.exists(tmpl_path):
        try:
            with open(tmpl_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return HTML_TEMPLATE


def load_category_template():
    """Load common category report template from templates/ or fallback."""
    tmpl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "category_report_template.html")
    if os.path.exists(tmpl_path):
        try:
            with open(tmpl_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return CATEGORY_REPORT_TEMPLATE

CATEGORY_REPORT_TEMPLATE = """
        <div class="mb-10 p-4 bg-gray-50 rounded-md border border-gray-200">
            <h2 class="text-2xl font-semibold mb-3 text-gray-800">{category_name}</h2>
            <p class="text-lg font-bold {category_score_class}">{category_score:.2f}%</p>
            <p class="text-gray-700">des contrôles automatisés réussis dans cette catégorie ({passed_automated}/{total_automated} vérifiés).</p>
            <p class="text-gray-700">{manual_checks} contrôles nécessitent une vérification manuelle.</p>
            <p class="text-gray-700">{error_checks} controls encountered an execution error.</p>
            <p class="text-gray-700">{na_checks} contrôles ne sont pas applicables.</p>

            <table class="min-w-full border border-gray-300 divide-y divide-gray-300 mt-6">
                <thead>
                    <tr class="bg-gray-200 text-gray-700 uppercase text-sm leading-normal">
                        <th class="py-3 px-6 text-left w-1/12">Numéro</th>
                        <th class="py-3 px-6 text-left w-2/12">Recommandation</th>
                        <th class="py-3 px-6 text-left w-1/12">Type</th>
                        <th class="py-3 px-6 text-left w-2/12">Test Exécuté</th>
                        <th class="py-3 px-6 text-left w-1/12">Résultat</th>
                        <th class="py-3 px-6 text-left w-3/12">Output / Error / Notes</th>
                        <th class="py-3 px-6 text-left w-2/12">Procédure de Remediation</th>
                    </tr>
                </thead>
                <tbody class="text-gray-600 text-sm font-light divide-y divide-gray-200">
                    {checks_rows}
                </tbody>
            </table>
        </div>
"""

# New template for the category bar chart canvas
CATEGORY_CHART_CANVAS_TEMPLATE = ""


CHECK_ROW_TEMPLATE = """
                    <tr class="border-b border-gray-200 hover:bg-gray-100">
                        <td class="py-3 px-6 text-left align-top">{number}</td>
                        <td class="py-3 px-6 text-left align-top">{name}</td>
                        <td class="py-3 px-6 text-left align-top">{type}</td>
                        <td class="py-3 px-6 text-left align-top"><code>{test_procedure}</code></td>
                        <td class="py-3 px-6 text-left align-top"><span class="{status_class}">{status_icon} {status_text}</span></td>
                        <td class="py-3 px-6 text-left align-top"><pre>{output}</pre></td>
                        <td class="py-3 px-6 text-left align-top">{remediation}</td>
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



def detect_execution_context(mode="local", remote_host=None, docker_container=None, product_hint=None):
    """Detect and categorize execution context into structured dictionary (PSL ONLY)."""
    is_remote = bool(mode == "ssh" or remote_host)
    active_container = docker_container

    if not active_container and product_hint:
        try:
            cmd = "docker ps --format '{{.Names}}'"
            stdout, stderr, ret = run_command(cmd, remote_host=remote_host)
            if ret == 0 and stdout:
                for line in stdout.splitlines():
                    name = line.strip()
                    if product_hint.lower() in name.lower():
                        active_container = name
                        break
        except Exception:
            active_container = None

    is_docker = bool(active_container)

    if is_remote and is_docker:
        ctype = "REMOTE_SSH_DOCKER"
        label = f"Remote SSH + Docker ({remote_host} -> {active_container})"
    elif is_remote:
        ctype = "REMOTE_SSH_BAREMETAL"
        label = f"Remote SSH ({remote_host})"
    elif is_docker:
        ctype = "LOCAL_DOCKER"
        label = f"Local Docker ({active_container})"
    else:
        ctype = "LOCAL_BAREMETAL"
        label = "Local Bare-Metal"

    return {
        "type": ctype,
        "mode": "ssh" if is_remote else "local",
        "remote_host": remote_host if is_remote else None,
        "docker_container": active_container,
        "is_docker": is_docker,
        "is_remote": is_remote,
        "label": label
    }


def detect_docker_container(remote_host=None, docker_name=None):
    """Detect active PostgreSQL Docker container name."""
    if docker_name:
        return docker_name
    stdout, stderr, ret = run_command("docker ps --format '{{.Names}}' | grep -iE 'postgres|pg' | head -n 1", remote_host=remote_host)
    if ret == 0 and stdout:
        return stdout.strip()
    return None


def is_valid_executable_command(cmd_str):
    """Check if command string is a valid shell executable command rather than descriptive human text."""
    if not cmd_str or not isinstance(cmd_str, str):
        return False
    s = cmd_str.strip()
    if not s:
        return False
    if s.startswith("!") or s.startswith("[") or s.startswith("(") or s.startswith("/") or s.startswith("."):
        return True
    first_word = s.split()[0].lower()
    known_commands = {
        "cat", "ls", "grep", "egrep", "fgrep", "find", "ps", "awk", "cut", "sed", "head", "tail",
        "echo", "getent", "crontab", "df", "stat", "test", "dpkg", "rpm", "systemctl", "service",
        "mysql", "mariadb", "psql", "cqlsh", "mongo", "mongosh", "python3", "python", "bash", "sh",
        "docker", "curl", "wget", "sshd", "which", "id", "whoami", "uname", "chmod", "chown"
    }
    if first_word in known_commands:
        return True
    if any(token in s for token in ["|", "&&", ";", ">", "||", "$"]):
        return True
    return False


def run_command(command, remote_host=None, docker_container=None, db_user=None, db_password=None, db_host=None, db_port=None, db_name=None, defaults_file=None, auth_db=None):
    """Execute command safely locally, over SSH, or inside Docker container (PSL ONLY)."""
    try:
        env = os.environ.copy()
        docker_env = []
        if db_password:
            env["MYSQL_PWD"] = str(db_password)
            env["PGPASSWORD"] = str(db_password)
            docker_env.extend(["-e", f"MYSQL_PWD={db_password}", "-e", f"PGPASSWORD={db_password}"])
        if db_user:
            env["MYSQL_USER"] = str(db_user)
            env["PGUSER"] = str(db_user)
            docker_env.extend(["-e", f"MYSQL_USER={db_user}", "-e", f"PGUSER={db_user}"])
        if db_host:
            env["MYSQL_HOST"] = str(db_host)
            env["PGHOST"] = str(db_host)
            docker_env.extend(["-e", f"MYSQL_HOST={db_host}", "-e", f"PGHOST={db_host}"])
        if db_port:
            env["MYSQL_TCP_PORT"] = str(db_port)
            env["PGPORT"] = str(db_port)
            docker_env.extend(["-e", f"MYSQL_TCP_PORT={db_port}", "-e", f"PGPORT={db_port}"])
        if db_name:
            env["PGDATABASE"] = str(db_name)
            docker_env.extend(["-e", f"PGDATABASE={db_name}"])
        if isinstance(command, str):
            if docker_container and not command.startswith("docker exec"):
                env_flags = " ".join(docker_env) if docker_env else ""
                command = f"docker exec -i {env_flags} {docker_container} /bin/bash -c {json.dumps(command)}".replace("  ", " ")
            elif "systemctl" in command and (os.path.exists("/.dockerenv") or not os.path.exists("/run/systemd/system")):
                if "postgresql" in command:
                    command = "pg_isready -h localhost -p 5432 || ps aux | grep -v grep | grep postgres"
            cmd_args = ["/bin/bash", "-c", command]
        else:
            cmd_args = list(command)

        if remote_host:
            cmd_args = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", "-i", "/root/.ssh/id_rsa", remote_host] + cmd_args

        process = subprocess.run(cmd_args, check=False, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10, env=env)
        stdout_text = process.stdout.strip()
        stderr_text = process.stderr.strip()

        if stderr_text:
            filtered_lines = [
                line for line in stderr_text.splitlines()
                if not line.startswith("Warning: Permanently added")
                and "pseudo-terminal" not in line
            ]
            stderr_text = chr(10).join(filtered_lines).strip()

        return stdout_text, stderr_text, process.returncode
    except subprocess.TimeoutExpired:
        return "", "Command execution timed out after 10 seconds", -1
    except Exception as e:
        return "", str(e), -1



def evaluate_condition(condition, stdout, stderr, returncode):
    """Évalue si le résultat de la commande correspond à la condition attendue."""
    if not condition:
        return False
    if stdout is None:
        stdout = ""
    if stderr is None:
        stderr = "" # Aucune condition définie pour un test automatisé ? Ne devrait pas arriver avec la structure actuelle.

    condition_type = condition.get("type")
    expected_value = condition.get("value")
    expected_values = condition.get("values")
    regex_pattern = condition.get("pattern")

    if condition_type == "returncode_zero":
        return returncode == 0
    elif condition_type == "returncode_equals":
        return returncode == expected_value
    elif condition_type == "stdout_equals":
        return stdout == expected_value
    elif condition_type == "stdout_not_equals":
        return stdout != expected_value
    elif condition_type == "stdout_not_contains":
        return expected_value not in stdout
    elif condition_type == "stdout_contains":
        return expected_value in stdout
    elif condition_type == "stdout_is_empty":
        return stdout.strip() == ""
    elif condition_type == "stdout_not_empty":
        return stdout != "" and stdout is not None
    elif condition_type == "stdout_contains_any":
        if expected_values is None: return False # Should not happen with current data
        return any(value in stdout for value in expected_values)
    elif condition_type == "stdout_not_contains_any":
        if expected_values is None: return True # Should not happen with current data
        return not any(value in stdout for value in expected_values)
    elif condition_type == "stdout_regex_match":
        if regex_pattern is None: return False # Should not happen
        return re.search(regex_pattern, stdout) is not None
    elif condition_type == "stdout_is_numeric_greater_than":
        try:
            # Extract potential number from string like '100' or '8GB' (take the number part)
            numeric_value_match = re.match(r'^(\d+)', stdout)
            if numeric_value_match:
                 numeric_value = int(numeric_value_match.group(1))
                 return numeric_value > expected_value
            return False
        except ValueError:
            return False # Not a valid number
    # Ajouter d'autres types de conditions au besoin
    return False # Type de condition inconnu

def perform_checks(recommendations, remote_host=None, docker_container=None, db_user=None, db_password=None, db_host=None, db_port=None, db_name=None, defaults_file=None, auth_db=None):
    """Exécute tous les contrôles et stocke les résultats."""
    results = {}
    for rec in recommendations:
        category = rec["category"]
        if category not in results:
            results[category] = []

        # Ensure 'number' key exists before accessing it
        check_number = rec.get("number", "N/A") # Use .get() with a default value

        check_result = {
            "number": check_number,
            "name": rec["name"],
            "type": rec["type"],
            "test_procedure": rec.get("test_procedure", ""),
            "remediation": rec.get("remediation", ""),
            "status": "Not Applicable", # Default status
            "output": "",
            "error": ""
        }

        if rec["type"] == "Manual":
            check_result["status"] = "Manual"
            tp = rec.get("test_procedure", "").strip()
            if tp and is_valid_executable_command(tp):
                diag_out, diag_err, diag_ret = run_command(
                    tp, remote_host=remote_host, docker_container=docker_container,
                    db_user=db_user, db_password=db_password, db_host=db_host,
                    db_port=db_port, db_name=db_name, defaults_file=defaults_file, auth_db=auth_db
                )
                diag_disp = diag_out if diag_out else (diag_err or "")
                if diag_disp:
                    check_result["output"] = f"--- [Contrôle Manuel - Diagnostic Système] ---\nCommande: {tp}\n\nRésultat capturé:\n{diag_disp}\n\nNote: L'auditeur doit valider la conformité selon la politique de sécurité de l'organisation."
                else:
                    check_result["output"] = f"--- [Contrôle Manuel - Diagnostic Système] ---\nCommande: {tp}\n\n(Aucune sortie retournée)\n\nNote: L'auditeur doit valider la conformité selon la politique de sécurité de l'organisation."
            else:
                check_result["output"] = "This control requires manual verification.\nConsulter la politique de sécurité et les procédures organisationnelles."
        elif rec["type"] == "Automated":
            all_sub_checks_passed = True
            aggregated_output = []
            aggregated_error = []
            command_executed_display = check_result.get("test_procedure", rec.get("test_procedure", ""))
            stored_outputs = {} # To store outputs for templates

            # Handle checks that require getting a path first (like 2.2) or storing output for later sub-checks
            if "path_command" in rec or ("sub_checks" in rec and any("store_output_as" in sc for sc in rec["sub_checks"])):
                 # If it's a path_command or any sub_check needs output stored
                 # For path_command, run it first
                 if rec.get("path_command"):
                     path_cmd = rec["path_command"]
                     path_cmd_output, path_cmd_error, path_cmd_returncode = run_command(path_cmd, remote_host=remote_host)
                     aggregated_output.append(f"--- Command pour obtenir le chemin: {path_cmd} ---\nStdout:\n{path_cmd_output}\nStderr:\n{path_cmd_error}\nReturn Code: {path_cmd_returncode}\n---")
                     aggregated_error.append(path_cmd_error)

                     if path_cmd_returncode != 0:
                         check_result["status"] = "Error"
                         check_result["output"] = "\n\n".join(aggregated_output)
                         check_result["error"] = "\n\n".join(aggregated_error)
                         all_sub_checks_passed = False # Mark as failed due to setup error
                     else:
                         stored_outputs["path"] = path_cmd_output.strip() # Store the fetched path

                 # Now process sub_checks if pre-checks passed and there are sub_checks
                 if "sub_checks" in rec and all_sub_checks_passed:
                     command_executed_display = "Multiple commandes (voir Sortie)"
                     overall_sub_checks_status = "Pass" # Assume pass unless a sub-check fails or errors

                     for i, sub_check in enumerate(rec["sub_checks"]):
                        cmd_to_run = sub_check.get("test_procedure")

                        # If template exists, format it using stored outputs
                        if "test_procedure_template" in sub_check:
                             try:
                                 cmd_to_run = sub_check["test_procedure_template"].format(**stored_outputs)
                                 sub_check["test_procedure"] = cmd_to_run # Store formatted command back
                             except KeyError as e:
                                 aggregated_output.append(f"--- Error: Template for sub-control {i+1} invalid ---")
                                 aggregated_error.append(f"Internal error: Missing key for sub-control template {i+1}: {e}.")
                                 overall_sub_checks_status = "Error"
                                 all_sub_checks_passed = False
                                 break # Cannot proceed with this sub-check

                        # Check if command is defined after template formatting (if applicable)
                        if cmd_to_run is None:
                             aggregated_output.append(f"--- Error: Command for sub-control {i+1} undefined ---")
                             aggregated_error.append(f"Internal error: Command for sub-control {i+1} undefined.")
                             overall_sub_checks_status = "Error"
                             all_sub_checks_passed = False
                             break # Cannot proceed with this sub-check


                        stdout, stderr, returncode = run_command(cmd_to_run, remote_host=remote_host)
                        aggregated_output.append(f"--- Command {i+1}: {cmd_to_run} ---\nStdout:\n{stdout}\nStderr:\n{stderr}\nReturn Code: {returncode}\n---")
                        aggregated_error.append(stderr)

                        # Store output if requested
                        if "store_output_as" in sub_check:
                            stored_outputs[sub_check["store_output_as"]] = stdout.strip()


                        condition = sub_check.get("expected_output")
                        sub_check_passed = False
                        if condition:
                            if evaluate_condition(condition, stdout, stderr, returncode):
                                sub_check_passed = True
                            else:
                                # Sub-check failed the condition
                                overall_sub_checks_status = "Fail"
                                aggregated_output[-1] += "\nCondition de succès non remplie." # Add failure reason to output
                                break # If any sub-check fails, the overall check fails
                        else:
                             # Sub-check has no condition, consider it passed if no execution error
                             sub_check_passed = True


                        # Check for specific known errors that should mark as N/A
                        if rec.get("possible_errors"):
                             if any(err in stderr for err in rec["possible_errors"]):
                                  check_result["status"] = "Not Applicable" # Mark the main check as N/A
                                  overall_sub_checks_status = "Not Applicable" # Propagate status
                                  # No break here, still run other sub-checks to collect info

                        # Check for command not found errors for the sub-check
                        if returncode == 127:
                             overall_sub_checks_status = "Error" # Mark the main check as Error
                             aggregated_output[-1] = f"--- Command {i+1}: {cmd_to_run} ---\nExecution error: Command not found.\n{aggregated_output[-1]}"
                             break # Stop if a command is not found

                        # If a sub-check had an execution error (other than 127)
                        if returncode != 0 and stderr and overall_sub_checks_status not in ["Not Applicable", "Error"]:
                             overall_sub_checks_status = "Error" # Mark the main check as Error
                             aggregated_output[-1] = f"--- Command {i+1}: {cmd_to_run} ---\nExecution error:\n{aggregated_output[-1]}"
                             # No break here, still run other sub-checks to collect info


                     check_result["output"] = "\n\n".join(aggregated_output)
                     check_result["error"] = "\n\n".join(aggregated_error)
                     check_result["test_procedure"] = command_executed_display # Display the general description
                     check_result["status"] = overall_sub_checks_status # Set the final status based on sub-checks

                 elif all_sub_checks_passed and "sub_checks" in rec: # No path_command, but sub_checks defined
                      command_executed_display = "Multiple commandes (voir Sortie)"
                      overall_sub_checks_status = "Pass" # Assume pass unless a sub-check fails or errors

                      for i, sub_check in enumerate(rec["sub_checks"]):
                         cmd_to_run = sub_check.get("test_procedure")
                         # No template formatting needed here as no path_command

                         if cmd_to_run is None:
                              aggregated_output.append(f"--- Error: Command for sub-control {i+1} undefined ---")
                              aggregated_error.append(f"Internal error: Command for sub-control {i+1} undefined.")
                              overall_sub_checks_status = "Error"
                              all_sub_checks_passed = False
                              break # Cannot proceed with this sub-check

                         stdout, stderr, returncode = run_command(cmd_to_run, remote_host=remote_host)
                         aggregated_output.append(f"--- Command {i+1}: {cmd_to_run} ---\nStdout:\n{stdout}\nStderr:\n{stderr}\nReturn Code: {returncode}\n---")
                         aggregated_error.append(stderr)

                         # Store output if requested
                         if "store_output_as" in sub_check:
                             stored_outputs[sub_check["store_output_as"]] = stdout.strip()

                         condition = sub_check.get("expected_output")
                         sub_check_passed = False
                         if condition:
                             if evaluate_condition(condition, stdout, stderr, returncode):
                                 sub_check_passed = True
                             else:
                                 # Sub-check failed the condition
                                 overall_sub_checks_status = "Fail"
                                 aggregated_output[-1] += "\nCondition de succès non remplie." # Add failure reason to output
                                 break # If any sub-check fails, the overall check fails
                         else:
                              # Sub-check has no condition, consider it passed if no execution error
                              sub_check_passed = True

                         # Check for specific known errors that should mark as N/A
                         if rec.get("possible_errors"):
                              if any(err in stderr for err in rec["possible_errors"]):
                                   check_result["status"] = "Not Applicable" # Mark the main check as N/A
                                   overall_sub_checks_status = "Not Applicable" # Propagate status
                                   # No break here, still run other sub-checks to collect info

                         # Check for command not found errors for the sub-check
                         if returncode == 127:
                              overall_sub_checks_status = "Error" # Mark the main check as Error
                              aggregated_output[-1] = f"--- Command {i+1}: {cmd_to_run} ---\nExecution error: Command not found.\n{aggregated_output[-1]}"
                              break # Stop if a command is not found

                         # If a sub-check had an execution error (other than 127)
                         if returncode != 0 and stderr and overall_sub_checks_status not in ["Not Applicable", "Error"]:
                              overall_sub_checks_status = "Error" # Mark the main check as Error
                              aggregated_output[-1] = f"--- Command {i+1}: {cmd_to_run} ---\nExecution error:\n{aggregated_output[-1]}"
                              # No break here, still run other sub-checks to collect info

                      check_result["output"] = "\n\n".join(aggregated_output)
                      check_result["error"] = "\n\n".join(aggregated_error)
                      check_result["test_procedure"] = command_executed_display # Display the general description
                      check_result["status"] = overall_sub_checks_status # Set the final status based on sub-checks


            elif all_sub_checks_passed: # Run single test procedure if no sub_checks or sub_checks setup passed
                cmd = check_result.get("test_procedure", rec.get("test_procedure", "")) # Use the formatted procedure if available
                command_executed_display = cmd
                stdout, stderr, returncode = run_command(cmd, remote_host=remote_host)
                check_result["output"] = f"Stdout:\n{stdout}\nStderr:\n{stderr}\nReturn Code: {returncode}"
                check_result["error"] = stderr
                check_result["test_procedure"] = command_executed_display # Store the command that was run

                condition = rec.get("expected_output")
                if condition:
                    if evaluate_condition(condition, stdout, stderr, returncode):
                        check_result["status"] = "Pass"
                    else:
                        check_result["status"] = "Fail"
                        check_result["output"] += "\n\nCondition de succès non remplie."

                # Check for specific known errors that should mark as N/A
                if rec.get("possible_errors"):
                     if any(err in stderr for err in rec["possible_errors"]):
                          check_result["status"] = "Not Applicable"

                # Check for command not found errors
                if returncode == 127:
                     check_result["status"] = "Error"
                     check_result["output"] = f"Execution error: Command not found.\n{check_result['output']}" # Add specific error message


            # If status is still Not Applicable (e.g., error during sub_check handling or no condition defined)
            if check_result["status"] == "Not Applicable" and rec.get("expected_output") is not None:
                 # If it was marked N/A due to a possible_error, keep that status
                 pass # Keep Not Applicable status if set by possible_errors check
            elif check_result["status"] == "Not Applicable" and (rec.get("expected_output") is None and not rec.get("sub_checks")):
                 # If it's automated but no condition/sub_checks, mark as Error (misconfiguration in script)
                 check_result["status"] = "Error"
                 check_result["output"] = check_result.get("output", "") + "\n\nError interne du script : Automated control with no condition defined."
            elif check_result["status"] == "Fail" and check_result["error"] and check_result["output"].startswith("Stdout:\n\nStderr:\n\nReturn Code:"):
                 # If it failed but there was an execution error (not just condition not met)
                 check_result["status"] = "Error"
                 check_result["output"] = f"Execution error:\n{check_result['output']}"


        results[category].append(check_result)

    return results

def calculate_scores(results):
    """Calcule les scores globaux et par catégorie."""
    overall = {"total_automated": 0, "passed_automated": 0, "failed_automated": 0, "manual": 0, "error": 0, "na": 0}
    categories_scores = {}
    # Initialize category counts
    for category in list(dict.fromkeys(rec["category"] for rec in RECOMMENDATIONS_DATA)):
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
        for check in checks:
            if check["type"] == "Automated":
                overall["total_automated"] += 1
                categories_scores[category]["total_automated"] += 1 # Count attempted automated checks per category

                if check["status"] == "Pass":
                    overall["passed_automated"] += 1
                    categories_scores[category]["passed_automated"] += 1
                    categories_scores[category]["pass_count"] += 1
                elif check["status"] == "Fail":
                    overall["failed_automated"] += 1
                    categories_scores[category]["failed_automated"] += 1
                    categories_scores[category]["fail_count"] += 1
                elif check["status"] == "Error":
                     overall["error"] += 1
                     categories_scores[category]["error_checks"] += 1
                     categories_scores[category]["error_count"] += 1
                elif check["status"] == "Not Applicable":
                     overall["na"] += 1
                     categories_scores[category]["na_checks"] += 1
                     categories_scores[category]["na_count"] += 1
             # Manual checks are just counted
            elif check["type"] == "Manual":
                overall["manual"] += 1
                categories_scores[category]["manual_checks"] += 1


        # Calculate category score based on attempted automated checks (Pass + Fail)
        cat_attempted_automated = categories_scores[category]["passed_automated"] + categories_scores[category]["failed_automated"]
        categories_scores[category]["total_automated"] = cat_attempted_automated # Update total_automated to be attempted
        categories_scores[category]["score"] = (categories_scores[category]["passed_automated"] / cat_attempted_automated * 100) if cat_attempted_automated > 0 else 0


    overall_attempted_automated = overall["passed_automated"] + overall["failed_automated"] # Only count Pass and Fail for the percentage base
    overall_score = (overall["passed_automated"] / overall_attempted_automated * 100) if overall_attempted_automated > 0 else 0

    # Prepare data for category bar chart
    category_labels = json.dumps(list(categories_scores.keys()))
    category_pass_counts = json.dumps([cat_info["pass_count"] for cat_info in categories_scores.values()])
    category_fail_counts = json.dumps([cat_info["fail_count"] for cat_info in categories_scores.values()])
    category_error_counts = json.dumps([cat_info["error_count"] for cat_info in categories_scores.values()])
    category_na_counts = json.dumps([cat_info["na_count"] for cat_info in categories_scores.values()])


    # Return counts for chart
    return overall_score, categories_scores, overall["manual"], overall["error"], overall["na"], overall["passed_automated"], overall["failed_automated"], overall["error"], overall["na"], category_labels, category_pass_counts, category_fail_counts, category_error_counts, category_na_counts

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
        return "❓", status, "status-error" # Fallback for unexpected status








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
            test_proc = r.get("test_procedure", r.get("audit", ""))
            if test_proc:
                cmd_elem = ET.SubElement(tc, "system-out")
                cmd_elem.text = f"Test Command: {str(test_proc).strip()}"
            rem = r.get("remediation", "")
            if rem:
                rem_elem = ET.SubElement(tc, "remediation")
                rem_elem.text = str(rem).strip()
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
            "=" * 90,
            f"               CIS BENCHMARK AUDIT REPORT - {target_name.upper()}",
            "=" * 90,
            f"Report Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Global Score  : {overall_score:.1f}%",
            f"Total Controls: {len(flat_results)}",
            "-" * 90,
            " CATEGORY BREAKDOWN & COMPLIANCE SUMMARY TABLE",
            "-" * 90,
            f"  {'ID':<6} {'Category Name':<45} {'Pass':<6} {'Fail':<6} {'Manual':<8} {'Score':<8}",
            f"  {'-'*6} {'-'*45} {'-'*6} {'-'*6} {'-'*8} {'-'*8}",
        ]
        if isinstance(categories_scores, dict):
            for cat_id, data in categories_scores.items():
                name = str(data.get('name', cat_id))[:44]
                p = data.get('passed_automated', 0)
                f = data.get('failed_automated', 0)
                m = data.get('manual_checks', 0)
                sc = data.get('score', 0.0)
                lines.append(f"  {str(cat_id):<6} {name:<45} {p:<6} {f:<6} {m:<8} {sc:>6.1f}%")
        lines.extend([
            "=" * 90,
            " DETAILED CONTROL RESULTS",
            "=" * 90,
            ""
        ])
        for r in flat_results:
            status = r.get("status", "")
            status_icon = "[PASS]" if status in ["PASS", "Pass"] else ("[FAIL]" if status in ["FAIL", "Fail"] else "[MANUAL]")
            rec_id = r.get("number", r.get("id", ""))
            rec_name = r.get("name", r.get("title", ""))
            lines.append(f"{status_icon} {rec_id} - {rec_name}")
            lines.append(f"  Category: {r.get('category')}")
            test_proc = r.get("test_procedure", r.get("audit", ""))
            if test_proc:
                lines.append(f"  Commande de test: {str(test_proc).strip()}")
            out = r.get('output', r.get('stdout', ''))
            if out:
                lines.append(f"  Output: {str(out).strip()}")
            rem = r.get('remediation', '')
            if rem:
                lines.append(f"  Procédure de remédiation: {str(rem).strip()}")
            lines.append("-" * 90)
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"📄 TXT Report successfully generated: {filename}")

    else:
        try:
            generate_html_report(results, overall_score, categories_scores, filename=filename, lang=lang)
        except TypeError:
            try:
                generate_html_report(results, overall_score, categories_scores, filename=filename)
            except TypeError:
                # Legacy positional args fallback
                generate_html_report(results, overall_score, categories_scores, 0, 0, 0, 0, 0, 0, 0, [], [], [], [], [], filename)



def generate_html_report(results, overall_score, categories_scores, filename=None, lang="en", execution_context=None):
    if not filename:
        filename = "reports/rapport_cis_postgresql_16.html"

    report_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    overall_score_class = get_score_class(overall_score)
    categories_html = ""
    sidebar_links_html = ""

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

    for category in category_order:
        checks = results.get(category, [])
        cat_info = categories_scores.get(category, {})
        category_score = cat_info.get("score", 0)
        cat_score_class = get_score_class(category_score)
        cat_total_automated = cat_info.get("total_automated", 0) # This is now attempted automated
        cat_passed_automated = cat_info.get("passed_automated", 0)
        cat_manual_checks = cat_info.get("manual_checks", 0)
        cat_error_checks = cat_info.get("error_checks", 0)
        cat_na_checks = cat_info.get("na_checks", 0)


        checks_rows_html = ""
        # Sort checks within the category by number for consistent report order
        sorted_checks = sorted(checks, key=lambda x: tuple(map(int, x['number'].replace('.', '_').split('_'))))

        for check in sorted_checks:
            status_icon, status_text, status_class = get_status_info(check["status"])

            # Escape HTML special characters in text fields
            escaped_name = html.escape(check["name"])
            escaped_test_procedure = html.escape(check["test_procedure"])
            escaped_output = html.escape(check["output"])
            escaped_remediation = html.escape(check["remediation"])


            checks_rows_html += CHECK_ROW_TEMPLATE.format(
                number=check["number"],
                name=escaped_name,
                type=check["type"],
                test_procedure=escaped_test_procedure,
                status_icon=status_icon,
                status_text=status_text,
                status_class=status_class,
                output=escaped_output,
                remediation=escaped_remediation if escaped_remediation else "N/A"
            )

        categories_html += CATEGORY_REPORT_TEMPLATE.format(
            category_name=category,
            category_score=category_score,
            category_score_class=cat_score_class,
            passed_automated=cat_passed_automated,
            total_automated=cat_total_automated, # Display attempted automated checks
            manual_checks=cat_manual_checks,
            error_checks=cat_error_checks,
            na_checks=cat_na_checks,
            checks_rows=checks_rows_html
        )
    # Add the category chart canvas after all category reports
    categories_html += CATEGORY_CHART_CANVAS_TEMPLATE
    class SafeDict(dict):
        def __missing__(self, key):
            return f"{{{key}}}"

    ctx_label = execution_context if execution_context else "Local Bare-Metal"
    html_output = load_html_template().format_map(SafeDict(
        product_title="PostgreSQL 16",
        benchmark_title="PostgreSQL 16",
        benchmark_version="1.0.0",
        suite_version="2.3.0",
        execution_context=ctx_label,
        lang=lang if 'lang' in locals() else "en",
        report_date=report_date,
        overall_score=overall_score,
        overall_score_class=overall_score_class,
        passed_automated_count=passed_auto_count if 'passed_auto_count' in locals() else 0,
        failed_automated_count=failed_auto_count if 'failed_auto_count' in locals() else 0,
        passed_automated=passed_auto_count if 'passed_auto_count' in locals() else 0,
        total_automated=(passed_auto_count + failed_auto_count) if 'passed_auto_count' in locals() else 0,
        manual_checks=total_manual if 'total_manual' in locals() else 0,
        error_checks=total_errors if 'total_errors' in locals() else 0,
        error_count=total_errors if 'total_errors' in locals() else 0,
        na_checks=total_na if 'total_na' in locals() else 0,
        sidebar_links=sidebar_links_html if 'sidebar_links_html' in locals() else "",
        categories_reports=categories_html,
        donut_svg=svg_global_chart_html if 'svg_global_chart_html' in locals() else "",
        bar_svg=build_inline_svg_category_chart(categories_scores) if 'categories_scores' in locals() else "",
        svg_global_chart_html=svg_global_chart_html if 'svg_global_chart_html' in locals() else ""
    ))

    if os.path.dirname(filename):
            os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_output)

    print(f"Report successfully generated: {filename}")


# --- Main Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CIS Audit Benchmark (Local & SSH Remote Modes)",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-c", "--docker", "--container", dest="docker_container", default=None, help="Target Docker container name or ID")
    parser.add_argument("-m", "--mode", choices=["local", "ssh"], default="local", help="Audit execution mode (local or ssh)")
    parser.add_argument("-r", "--remote", "--ssh", dest="remote_host", default=None, help="Remote SSH server target (e.g. user@hostname)")
    parser.add_argument("--ssh-port", type=int, default=22, help="SSH port for remote execution (default: 22)")
    parser.add_argument("-i", "--ssh-key", dest="ssh_key", default=None, help="Path to SSH private key file")
    parser.add_argument("--sudo", action="store_true", help="Execute remote/local commands with sudo privileges")
    parser.add_argument("-H", "--host", "--db-host", dest="db_host", default="localhost", help="Database host address (default: localhost)")
    parser.add_argument("-P", "--port", "--db-port", dest="db_port", type=int, default=None, help="Database port number")
    parser.add_argument("-u", "--user", "--db-user", dest="db_user", default=None, help="Database username")
    parser.add_argument("-p", "--password", "--db-password", dest="db_password", default=None, help="Database password")
    parser.add_argument("-D", "-d", "--database", "--db-name", dest="db_name", default=None, help="Database name")
    parser.add_argument("--defaults-file", "--config-file", dest="defaults_file", default=None, help="Path to database option/configuration file (.my.cnf, .pgpass, cqlshrc)")
    parser.add_argument("--auth-db", dest="auth_db", default=None, help="Authentication database (MongoDB)")
    parser.add_argument("--local", action="store_true", help="Force local audit execution mode")
    parser.add_argument("-f", "--format", choices=["html", "json", "xml", "txt"], default="html", help="Report output format (html/json/xml/txt)")
    parser.add_argument("-l", "--lang", choices=["en", "fr"], default="en", help="Report language choice (en/fr)")
    parser.add_argument("-o", "--output", dest="output", default=None, help="Custom output report file path")
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

    rules_data = load_recommendations("postgresql_16")
    docker_target = detect_docker_container(remote_host=remote_target, docker_name=args.docker_container)
    check_results = perform_checks(rules_data, remote_host=remote_target, docker_container=docker_target)
    (overall_score, categories_scores, *rest) = calculate_scores(check_results)
    export_results(check_results, overall_score, categories_scores, target_name="postgresql_16", filename=args.output, fmt=args.format, lang=args.lang)