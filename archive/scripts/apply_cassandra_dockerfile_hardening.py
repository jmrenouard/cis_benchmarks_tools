#!/usr/bin/env python3
"""
Add Cassandra security hardening to Cassandra Dockerfiles (PSL ONLY).
"""

import glob

dockerfiles = sorted(glob.glob("docker/Dockerfile_cassandra*"))
print(f"Hardening {len(dockerfiles)} Cassandra Dockerfiles...")

yaml_init_block = '''RUN sed -i 's/authenticator: AllowAllAuthenticator/authenticator: PasswordAuthenticator/' /etc/cassandra/cassandra.yaml 2>/dev/null || true && \\
  sed -i 's/authorizer: AllowAllAuthorizer/authorizer: CassandraAuthorizer/' /etc/cassandra/cassandra.yaml 2>/dev/null || true && \\
  sed -i 's/internode_encryption: none/internode_encryption: all/' /etc/cassandra/cassandra.yaml 2>/dev/null || true

'''

for fpath in dockerfiles:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    if "PasswordAuthenticator" in content:
        continue

    content = content.replace("# Copy the audit script for testing", yaml_init_block + "# Copy the audit script for testing")
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Successfully updated all Cassandra Dockerfiles!")
