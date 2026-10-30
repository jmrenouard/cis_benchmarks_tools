#!/usr/bin/env python3
"""
Add CIS hardening config to MySQL Dockerfiles using single-line echo -e (PSL ONLY).
"""

import glob
import re

dockerfiles = sorted(glob.glob("docker/Dockerfile_mysql*"))
print(f"Fixing {len(dockerfiles)} MySQL Dockerfiles...")

cnf_single_line = 'echo -e "[mysqld]\\nskip-symbolic-links=1\\nsecure_file_priv=/var/lib/mysql-files\\nsql_mode=STRICT_ALL_TABLES,NO_ENGINE_SUBSTITUTION\\nlocal_infile=0" > /etc/mysql/conf.d/cis_hardened.cnf'

for fpath in dockerfiles:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace broken multiline echo in Dockerfile
    pattern = r'echo "\[mysqld\].*?cis_hardened\.cnf'
    content = re.sub(pattern, cnf_single_line, content, flags=re.DOTALL)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Successfully fixed all MySQL Dockerfiles!")
