#!/usr/bin/env python3
"""
Add CIS hardening config to MySQL Dockerfiles (PSL ONLY).
"""

import glob
import re

dockerfiles = sorted(glob.glob("docker/Dockerfile_mysql*"))
print(f"Hardening {len(dockerfiles)} MySQL Dockerfiles...")

cnf_block = '''  mkdir -p /var/lib/mysql-files && \\
  chmod 750 /var/lib/mysql-files && \\
  chown mysql:mysql /var/lib/mysql-files && \\
  mkdir -p /etc/mysql/conf.d && \\
  echo "[mysqld]\\nskip-symbolic-links=1\\nsecure_file_priv=/var/lib/mysql-files\\nsql_mode=STRICT_ALL_TABLES,NO_ENGINE_SUBSTITUTION\\nlocal_infile=0" > /etc/mysql/conf.d/cis_hardened.cnf && \\
'''

for fpath in dockerfiles:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    if "cis_hardened.cnf" in content:
        continue

    pattern = r'(RUN echo \'root:rootpass\' \| chpasswd && \\\n)'
    replacement = r'\1' + cnf_block

    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)

print("✅ Successfully updated all MySQL Dockerfiles!")
