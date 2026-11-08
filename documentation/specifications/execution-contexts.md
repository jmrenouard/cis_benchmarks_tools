---
title: Execution Contexts & Transports Specification
date: 2026-11-08
category: specification
---

# Execution Contexts & Transports Specification

## 1. 4-Tier Polymorphic Execution Transports
Auditing commands must execute reliably across four operational tiers managed by `execution_drivers.py`:

1. **Local Mode (`LocalExecutor`, `driver_type="LOCAL"`)**:
   - Executes commands directly on the host using `/bin/bash -c`.
   - Used for bare-metal databases, local system audits, and CI/CD runners.
2. **Local Docker Mode (`DockerExecutor`, `driver_type="LOCAL_DOCKER"`)**:
   - Executes commands inside a container via `docker exec -i <container> /bin/bash -c <cmd>`.
   - Used for local containerized databases and automated Docker verification.
3. **Remote SSH Mode (`SSHExecutor`, `driver_type="REMOTE_SSH"`)**:
   - Executes commands on remote hosts via `ssh -o BatchMode=yes -o StrictHostKeyChecking=no -p <port> -i <key> <host> <cmd>`.
   - Used for remote bare-metal servers, VMs, and cloud instances.
4. **Remote SSH Docker Mode (`RemoteSSHContainerExecutor`, `driver_type="REMOTE_SSH_DOCKER"`)**:
   - Hybrid transport: Connects over SSH to a remote Docker daemon host and executes inside a remote container via `docker exec -i`.

## 2. Zero-Credential Exposure & Process Table Security
- **No Command-Line Passwords**: Database passwords must **never** be passed as CLI arguments (e.g., `mysql -psecret`, `psql -W`). Doing so exposes credentials in `ps aux` and `/proc` process listings (Ponytail Finding 6).
- **Environment Variable Injection**:
   - MySQL / MariaDB: `MYSQL_PWD` passed in execution environment.
   - PostgreSQL: `PGPASSWORD` passed in execution environment.
   - Unified CLI: `CIS_DB_PASSWORD` passed via internal environment.
- **Log & Stderr Scrubbing**: `SecretSanitizer` automatically masks password patterns (`-p`, `--password`, `MYSQL_PWD=`, `PGPASSWORD=`, `token`, `secret`) in command strings and logs before display or storage.

## 3. Rejection of OpenSSH `ControlMaster` (`IMP-006`)
- Connection multiplexing via `ControlMaster` was explicitly evaluated and rejected in `docs/RCA_REGISTER.md` (`IMP-006`).
- **Rationale**: Lack of Windows AF_UNIX socket support, orphaned control sockets causing unrecoverable hangs in CI/CD, and head-of-line blocking during concurrent multi-threaded audits.
- Invocations remain stateless, independent, and resilient, with standardized timeouts and keepalive options.
