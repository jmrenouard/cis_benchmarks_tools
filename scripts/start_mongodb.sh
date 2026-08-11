#!/bin/bash
set -e

# Start SSHD in the background
/usr/sbin/sshd 2>/dev/null || true

# Start MongoDB using official entrypoint
exec docker-entrypoint.sh mongod
