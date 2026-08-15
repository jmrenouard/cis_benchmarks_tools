#!/bin/bash
set -e

# Start SSHD in the background
/usr/sbin/sshd 2>/dev/null || true

# Ensure log file exists
mkdir -p /var/log/cassandra
touch /var/log/cassandra/system.log
chmod 644 /var/log/cassandra/system.log

# Hardening cassandra.yaml if available
CASS_CONF="/etc/cassandra/cassandra.yaml"
if [ -f "$CASS_CONF" ]; then
    sed -i 's/authenticator:.*/authenticator: PasswordAuthenticator/' "$CASS_CONF" 2>/dev/null || true
    sed -i 's/authorizer:.*/authorizer: CassandraAuthorizer/' "$CASS_CONF" 2>/dev/null || true
    sed -i 's/internode_encryption:.*/internode_encryption: all/' "$CASS_CONF" 2>/dev/null || true
fi

# Start Cassandra using official entrypoint
exec docker-entrypoint.sh cassandra -f
