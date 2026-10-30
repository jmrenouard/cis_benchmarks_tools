#!/usr/bin/env python3
"""
Replace raw multiline echo block in MySQL Dockerfiles with a clean single-line echo (PSL ONLY).
"""

import glob
import re

dockerfiles = sorted(glob.glob("docker/Dockerfile_mysql*"))
print(f"Fixing multiline string in {len(dockerfiles)} MySQL Dockerfiles...")

target_single = 'echo -e "[mysqld]\\nskip-symbolic-links=1\\nsecure_file_priv=/var/lib/mysql-files\\nsql_mode=STRICT_ALL_TABLES,NO_ENGINE_SUBSTITUTION\\nlocal_infile=0" > /etc/mysql/conf.d/cis_hardened.cnf'

for fpath in dockerfiles:
    with open(fpath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    skip = False
    for line in lines:
        if 'echo -e "[mysqld]' in line or 'echo "[mysqld]' in line:
            new_lines.append(f"  {target_single} && \\\n")
            skip = True
        elif skip:
            if 'cis_hardened.cnf' in line:
                skip = False
        else:
            new_lines.append(line)

    with open(fpath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

print("✅ Successfully updated all MySQL Dockerfiles to single-line echo!")
