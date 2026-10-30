#!/usr/bin/env python3
"""
Add PostgreSQL hardening init SQL and history symlinks to PostgreSQL Dockerfiles (PSL ONLY).
"""

import glob

dockerfiles = sorted(glob.glob("docker/Dockerfile_postgresql*"))
print(f"Hardening {len(dockerfiles)} PostgreSQL Dockerfiles...")

sql_init_block = '''RUN mkdir -p /docker-entrypoint-initdb.d && \\
  ln -sf /dev/null /root/.psql_history && \\
  echo "ALTER SYSTEM SET logging_collector = 'on';" > /docker-entrypoint-initdb.d/001_hardening.sql && \\
  echo "ALTER SYSTEM SET log_truncate_on_rotation = 'on';" >> /docker-entrypoint-initdb.d/001_hardening.sql && \\
  echo "ALTER SYSTEM SET log_connections = 'on';" >> /docker-entrypoint-initdb.d/001_hardening.sql && \\
  echo "ALTER SYSTEM SET log_disconnections = 'on';" >> /docker-entrypoint-initdb.d/001_hardening.sql && \\
  echo "ALTER SYSTEM SET log_error_verbosity = 'default';" >> /docker-entrypoint-initdb.d/001_hardening.sql && \\
  echo "ALTER SYSTEM SET log_line_prefix = '%m [%p] %q%u@%d ';" >> /docker-entrypoint-initdb.d/001_hardening.sql && \\
  echo "ALTER SYSTEM SET log_statement = 'ddl';" >> /docker-entrypoint-initdb.d/001_hardening.sql && \\
  echo "ALTER SYSTEM SET log_timezone = 'UTC';" >> /docker-entrypoint-initdb.d/001_hardening.sql && \\
  echo "SELECT pg_reload_conf();" >> /docker-entrypoint-initdb.d/001_hardening.sql

'''

for fpath in dockerfiles:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    if "001_hardening.sql" in content:
        continue

    content = content.replace("# Copy the audit script for testing", sql_init_block + "# Copy the audit script for testing")
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Successfully updated all PostgreSQL Dockerfiles!")
