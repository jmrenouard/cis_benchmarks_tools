#!/bin/bash
set -e

# Start SSHD in the background
/usr/sbin/sshd 2>/dev/null || true

# History symlink hardening
ln -sf /dev/null /root/.mysql_history 2>/dev/null || true
ln -sf /dev/null /root/.bash_history 2>/dev/null || true

# Set up client configuration for seamless root CLI auditing
cat << 'EOF' > /root/.my.cnf
[client]
user=root
password=rootpass
host=localhost
EOF
chmod 600 /root/.my.cnf

# Background SQL hardening loop
(
  for i in {1..40}; do
    if mysql -u root -prootpass -e "SELECT 1;" >/dev/null 2>&1; then
      mysql -u root -prootpass --connect-expired-password -e "
        DELETE FROM mysql.user WHERE User='';
        DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
        SET GLOBAL default_password_lifetime = 365;
        SET GLOBAL local_infile = 0;
        FLUSH PRIVILEGES;
      " 2>/dev/null || true
      break
    fi
    sleep 1
  done
) &

# Start MySQL using official entrypoint
exec docker-entrypoint.sh mysqld
