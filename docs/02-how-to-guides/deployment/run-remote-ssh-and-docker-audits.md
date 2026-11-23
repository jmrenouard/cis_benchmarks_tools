# Run Remote SSH and Docker CIS Audits

Read [Reference Index](../../03-reference/index.md) before you start.

## Prerequisites

1. Make sure that Python `3.8+` exists on the controller.
2. Make sure that SSH keys and Docker Engine work.

## Safety Instructions

**CAUTION:** Set mode `0600` on SSH keys before remote execution.
Open permissions fail `BatchMode=yes` checks or expose secrets.

**CAUTION:** Do not pass database passwords on the command line.
Command arguments leak secrets in process listings (`ps aux`).

## Procedure

1. List all 18 target keys:

   ```bash
   python3 audit_cis.py --list-targets
   ```

2. Run a local Docker container audit:

   ```bash
   python3 audit_cis.py -t mariadb106 --docker mariadb106-test -f html -o reports/m106.html
   ```

3. Run a remote SSH audit with `--mode ssh` and `--ssh-key`:

   ```bash
   python3 audit_cis.py -t rhel9 -m ssh -r admin@192.168.1.50 \
     --ssh-port 22 -i ~/.ssh/id_ed25519 --sudo -f json -o reports/rhel9_ssh.json
   ```

4. Run a remote SSH Docker audit for a remote container:

   ```bash
   python3 audit_cis.py -t postgresql17 -r admin@192.168.1.50 \
     --docker prod-pg17 -f html -o reports/pg17_remote.html
   ```

5. Mount `/app/reports` when you run `jmrenouard/cis-benchmarks-tools`:

   ```bash
   docker run --rm -v "$(pwd)/reports:/app/reports" jmrenouard/cis-benchmarks-tools \
     -t mariadb106 -r admin@192.168.1.50 -f html -o /app/reports/audit.html
   ```

**NOTE:** The container runs as non-root `cisuser` (`UID 10001`).

## Verification

1. Confirm exit code `0` from `audit_cis.py`.
2. Inspect JSON output and confirm zero `Error` states:

   ```bash
   python3 -c "import json; d=json.load(open('reports/rhel9_ssh.json')); print(d['target'], d['overall_score'])"
   ```

## Rollback

1. Stop any stuck `audit_cis.py` process.
2. Delete partial files in `reports/`.
3. Test SSH access with `ssh -o BatchMode=yes admin@192.168.1.50 true`.

## Related Documentation

- [Reference Index](../../03-reference/index.md) · [Explanation Index](../../04-explanation/index.md)
