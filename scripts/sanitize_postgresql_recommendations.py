#!/usr/bin/env python3
"""
Sanitize RECOMMENDATIONS_DATA array in audit_cis_postgresql_*.py (PSL ONLY).
"""

import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pg_scripts = ["audit_cis_postgresql_16.py", "audit_cis_postgresql_17.py", "audit_cis_postgresql_18.py"]

for sname in pg_scripts:
    spath = os.path.join(REPO_ROOT, sname)
    with open(spath, "r", encoding="utf-8") as f:
        content = f.read()

    # Rule 3.2
    content = content.replace(
        '"test_procedure": "Installer et configurer l’extension d’audit avancé pgAudit pour capturer les activités.\\nSELECT * FROM pg_extension WHERE extname = \'pgaudit\';"',
        '"test_procedure": "sudo -u postgres psql -t -c \\"SELECT * FROM pg_extension WHERE extname = \'pgaudit\';\\""'
    )
    # Rule 4.8
    content = content.replace(
        '"test_procedure": "Utiliser set_user pour l’émulation de rôles et la révocabilité de sessions.\\nSELECT * FROM pg_extension WHERE extname = \'set_user\';"',
        '"test_procedure": "sudo -u postgres psql -t -c \\"SELECT * FROM pg_extension WHERE extname = \'set_user\';\\""'
    )
    # Rule 6.7
    content = content.replace(
        '"test_procedure": "S’assurer qu’OpenSSL FIPS est utilisé si requis.\\nSHOW ssl_library; et vérifier la version OpenSSL."',
        '"test_procedure": "sudo -u postgres psql -t -c \'SHOW ssl_library;\'"'
    )
    # Rule 6.9
    content = content.replace(
        '"test_procedure": "Forcer au minimum TLSv1.3.\\nSHOW ssl_min_protocol_version; doit être TLSv1.3."',
        '"test_procedure": "sudo -u postgres psql -t -c \'SHOW ssl_min_protocol_version;\'"'
    )
    # Rule 6.10
    content = content.replace(
        '"test_procedure": "Exclure RC4, DES, etc., dans ssl_cipher_suites.\\nSHOW ssl_cipher_suites; vérifier l’absence de ciphers faibles."',
        '"test_procedure": "sudo -u postgres psql -t -c \'SHOW ssl_cipher_suites;\'"'
    )
    # Rule 6.11
    content = content.replace(
        '"test_procedure": "Activer pgcrypto pour fonctions cryptographiques.\\nSELECT * FROM pg_extension WHERE extname = \'pgcrypto\';"',
        '"test_procedure": "sudo -u postgres psql -t -c \\"SELECT * FROM pg_extension WHERE extname = \'pgcrypto\';\\""'
    )
    # Rule 7.2
    content = content.replace(
        '"test_procedure": "Activer log_replication_commands pour tracer les actions de réplication.\\nSHOW log_replication_commands; doit être on."',
        '"test_procedure": "sudo -u postgres psql -t -c \'SHOW log_replication_commands;\'"'
    )

    with open(spath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Sanitized RECOMMENDATIONS_DATA in {sname}")

print("Sanitization complete.")
