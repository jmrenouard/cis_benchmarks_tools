#!/bin/bash
set -e

# Start SSHD in the background
/usr/sbin/sshd 2>/dev/null || true

# History symlink hardening
ln -sf /dev/null /root/.psql_history 2>/dev/null || true
ln -sf /dev/null /var/lib/postgresql/.psql_history 2>/dev/null || true

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
log_error_verbosity = 'verbose'
log_connections = on
log_disconnections = on
log_hostname = 'off'
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '
EOF
    chmod 700 /var/lib/postgresql/data 2>/dev/null || true
fi

# Background SQL hardening loop
(
  for i in {1..30}; do
    if sudo -u postgres psql -c "SELECT 1;" >/dev/null 2>&1; then
      sudo -u postgres psql -c "
        ALTER SYSTEM SET ssl = 'on';
        ALTER SYSTEM SET logging_collector = 'on';
        ALTER SYSTEM SET log_error_verbosity = 'verbose';
        ALTER SYSTEM SET log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h ';
        ALTER SYSTEM SET log_connections = 'on';
        ALTER SYSTEM SET log_disconnections = 'on';
        ALTER SYSTEM SET log_hostname = 'off';
        SELECT pg_reload_conf();
      " 2>/dev/null || true
      break
    fi
    sleep 1
  done
) &

# Start PostgreSQL using official entrypoint
exec docker-entrypoint.sh postgres
