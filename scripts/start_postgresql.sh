#!/bin/bash

# Start SSHD in the background
/usr/sbin/sshd

# Initialize PostgreSQL if needed
if [ ! -f "/var/lib/postgresql/17/main/PG_VERSION" ]; then
    echo "Initializing PostgreSQL 17..."
    su - postgres -c "/usr/lib/postgresql/17/bin/initdb -D /var/lib/postgresql/17/main --data-checksums"
fi

# Start PostgreSQL in the foreground
echo "Starting PostgreSQL 17..."
exec su - postgres -c "/usr/lib/postgresql/17/bin/postgres -D /var/lib/postgresql/17/main -c config_file=/etc/postgresql/17/main/postgresql.conf"
