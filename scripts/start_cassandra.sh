#!/bin/bash
set -e

# Start SSHD in the background
/usr/sbin/sshd 2>/dev/null || true

# Start Cassandra using official entrypoint
exec docker-entrypoint.sh cassandra -f
