#!/bin/bash

# Start SSHD in the background
/usr/sbin/sshd

# Initialize MySQL if needed
if [ ! -d "/var/lib/mysql/mysql" ]; then
    echo "Initializing MySQL..."
    mysqld --initialize-insecure --user=mysql
fi

# Start MySQL in the foreground
echo "Starting MySQL..."
exec mysqld --user=mysql
