#!/bin/bash
set -e

# Start SSHD in the background
/usr/sbin/sshd 2>/dev/null || true

# Hardening cassandra.yaml if available
CASS_CONF="/etc/cassandra/cassandra.yaml"
if [ -f "$CASS_CONF" ]; then
    sed -i 's/authenticator: AllowAllAuthenticator/authenticator: PasswordAuthenticator/' "$CASS_CONF" 2>/dev/null || true
    sed -i 's/authorizer: AllowAllAuthorizer/authorizer: CassandraAuthorizer/' "$CASS_CONF" 2>/dev/null || true
    sed -i 's/internode_encryption: none/internode_encryption: all/' "$CASS_CONF" 2>/dev/null || true
fi

# Start Cassandra using official entrypoint
exec docker-entrypoint.sh cassandra -f
