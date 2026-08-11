#!/bin/bash
set -e

# Start SSHD in the background
/usr/sbin/sshd

# Use the official PostgreSQL entrypoint
# The official image handles initialization automatically
exec docker-entrypoint.sh postgres
