#!/bin/bash
set -e

# Start SSHD in the background
/usr/sbin/sshd 2>/dev/null || true

# Prepare SSL Certificates and Data Directory Hardening if PGDATA exists or initdb is run
mkdir -p /var/lib/postgresql/certs
if [ ! -f /var/lib/postgresql/certs/server.key ]; then
    openssl req -new -x509 -days 365 -nodes \
        -out /var/lib/postgresql/certs/server.crt \
        -keyout /var/lib/postgresql/certs/server.key \
        -subj "/CN=localhost" 2>/dev/null || true
    chown -R postgres:postgres /var/lib/postgresql/certs 2>/dev/null || true
    chmod 600 /var/lib/postgresql/certs/server.key 2>/dev/null || true
fi

# Hardening PostgreSQL configuration file if available
PG_CONF="/var/lib/postgresql/data/postgresql.conf"
if [ -f "$PG_CONF" ]; then
    grep -q "ssl = on" "$PG_CONF" || cat << 'EOF' >> "$PG_CONF"
ssl = on
ssl_cert_file = '/var/lib/postgresql/certs/server.crt'
ssl_key_file = '/var/lib/postgresql/certs/server.key'
logging_collector = on
log_destination = 'csvlog'
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_min_messages = 'warning'
log_min_error_statement = 'error'
log_connections = on
log_disconnections = on
log_line_prefix = '%m [%p] %q%u@%d '
EOF
    chmod 700 /var/lib/postgresql/data 2>/dev/null || true
fi

# Start PostgreSQL using official entrypoint
exec docker-entrypoint.sh postgres
