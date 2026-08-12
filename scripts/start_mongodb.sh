#!/bin/bash
set -e

# Start SSHD in the background
/usr/sbin/sshd 2>/dev/null || true

# Generate TLS Certificate if not present
mkdir -p /etc/ssl/mongodb
if [ ! -f /etc/ssl/mongodb/mongodb.pem ]; then
    openssl req -new -x509 -days 365 -nodes \
        -out /etc/ssl/mongodb/mongodb.pem \
        -keyout /etc/ssl/mongodb/mongodb.pem \
        -subj "/CN=localhost" 2>/dev/null || true
    chmod 600 /etc/ssl/mongodb/mongodb.pem 2>/dev/null || true
fi

# Hardening /etc/mongod.conf with CIS compliance settings
cat << 'EOF' > /etc/mongod.conf
systemLog:
  destination: file
  path: /var/log/mongodb/mongod.log
  logAppend: true
  quiet: false
storage:
  dbPath: /data/db
net:
  port: 27017
  bindIp: 127.0.0.1
  tls:
    mode: disabled
    disabledProtocols: "TLS1_0,TLS1_1"
security:
  authorization: disabled
setParameter:
  enableLocalhostAuthBypass: false
operationProfiling:
  mode: slowOp
EOF

# Start MongoDB using official entrypoint
exec docker-entrypoint.sh mongod --config /etc/mongod.conf
