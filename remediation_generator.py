#!/usr/bin/env python3
"""Deterministic dry-run remediation generator (diff, sql, shell, ansible, json; PSL ONLY)."""
import argparse, difflib, json, sys
from post_execution_publisher import atomic_write_text
from sarif_exporter import _clean, map_compliance_state, normalize_control_results, resolve_rule_spec

SUPPORTED_FORMATS = ("diff", "sql", "shell", "ansible", "json")
FORMAT_EXTENSIONS = {"diff": "diff", "sql": "sql", "shell": "sh", "ansible": "yml", "json": "json"}
_K = ("action_type", "requires_restart", "risk_level", "config_file", "before", "after", "sql", "shell", "verify")


def _t(*a):
    return dict(zip(_K, a))


_MC, _CC, _SC = "/etc/mongod.conf", "/etc/cassandra/cassandra.yaml", "/etc/ssh/sshd_config.d/99-cis.conf"


def _cfg(cfg, bef, aft, sh, ver, rst=False, rsk="low"):
    return _t("config", rst, rsk, cfg, bef, aft, "", sh, ver)


def _ln(cfg, pat, line, bef, aft, ver, rst=False, rsk="low"):
    return _cfg(cfg, bef, aft, f"grep -qE '{pat}' {cfg} 2>/dev/null || printf '{line}\\n' >> {cfg}", ver, rst, rsk)


def _my(v, old, new, persist=False, rst=False, rsk="low", cli="mysql", cv=None, vv=None):
    c, val = "/etc/mysql/conf.d/cis-hardening.cnf", (new if cv is None else cv)
    sql = f"SET {'PERSIST' if persist else 'GLOBAL'} {v} = {new};" if cli else ""
    sh = f"grep -q '^{v}' {c} 2>/dev/null || printf '[mysqld]\\n{v} = {val}\\n' >> {c}"
    return _t("sql_and_config" if sql else "config", rst, rsk, c, f"[mysqld]\n{v} = {old}", f"[mysqld]\n{v} = {val}", sql, sh, f"{cli or 'mysql'} -N -B -e 'SELECT @@{vv or v};'")


def _pg(p, old, new, rst=False, rsk="low"):
    sql = f"ALTER SYSTEM SET {p} = '{new}';{'' if rst else ' SELECT pg_reload_conf();'}"
    return _t("sql_and_config", rst, rsk, "postgresql.auto.conf", f"{p} = '{old}'", f"{p} = '{new}'", sql, f'psql -tAc "{sql}"', f"psql -tAc 'SHOW {p};'")


TEMPLATES = {
    "mariadb": {
        "1.3": _t("shell", False, "low", "/root/.mysql_history", "# history", "# /dev/null", "",
                  "test -L /root/.mysql_history || ln -sf /dev/null /root/.mysql_history", "readlink -f /root/.mysql_history"),
        "4.4": _my("local_infile", "1", "OFF", False, False, "low", "mariadb", "0"),
        "8.1": _my("require_secure_transport", "OFF", "ON", False, True, "medium", "mariadb"),
    },
    "mysql": {
        "4.4": _my("local_infile", "1", "OFF", True, False, "low", "mysql", "0"),
        "4.6": _my("symbolic-links", "1", "0", False, True, "low", "", None, "have_symlink"),
        "6.3": _my("log_error_verbosity", "1", "2", True),
        "8.1": _my("require_secure_transport", "OFF", "ON", True, True, "medium"),
    },
    "postgresql": {k: _pg(*a) for k, a in (
        ("3.1.2", ("log_destination", "", "stderr")), ("3.1.3", ("logging_collector", "off", "on", True, "medium")),
        ("3.1.20", ("log_connections", "off", "on")), ("3.1.21", ("log_disconnections", "off", "on")),
        ("3.1.22", ("log_error_verbosity", "terse", "default")), ("3.1.23", ("log_hostname", "on", "off")),
    )},
    "mongodb": {
        "2.1": _ln(_MC, "^\\s*authorization:\\s*enabled", "\\nsecurity:\\n  authorization: enabled", "security:\n  authorization: disabled", "security:\n  authorization: enabled", f"grep -E 'authorization:\\s*enabled' {_MC}", True, "medium"),
        "4.3": _ln(_MC, "^\\s*mode:\\s*requireTLS", "\\nnet:\\n  tls:\\n    mode: requireTLS", "net:\n  tls:\n    mode: disabled", "net:\n  tls:\n    mode: requireTLS", f"grep -E 'mode:\\s*requireTLS' {_MC}", True, "medium"),
        "5.4": _ln(_MC, "^\\s*logAppend:\\s*true", "\\nsystemLog:\\n  logAppend: true", "systemLog:\n  logAppend: false", "systemLog:\n  logAppend: true", f"grep -E 'logAppend:\\s*true' {_MC}", True),
    },
    "cassandra": {
        "2.1": _cfg(_CC, "authenticator: AllowAllAuthenticator", "authenticator: PasswordAuthenticator", f"grep -q '^authenticator: PasswordAuthenticator' {_CC} || sed -i 's/^authenticator:.*/authenticator: PasswordAuthenticator/' {_CC}", f"grep -E '^authenticator:\\s*PasswordAuthenticator' {_CC}", True, "medium"),
        "2.2": _cfg(_CC, "authorizer: AllowAllAuthorizer", "authorizer: CassandraAuthorizer", f"grep -q '^authorizer: CassandraAuthorizer' {_CC} || sed -i 's/^authorizer:.*/authorizer: CassandraAuthorizer/' {_CC}", f"grep -E '^authorizer:\\s*CassandraAuthorizer' {_CC}", True, "medium"),
    },
    "rhel": {
        "1.1.1.1": _ln("/etc/modprobe.d/cramfs.conf", "install cramfs /bin/false", "install cramfs /bin/false\\nblacklist cramfs", "# cramfs enabled", "install cramfs /bin/false\nblacklist cramfs", "modprobe -n -v cramfs"),
        "1.3.1.2": _cfg("/etc/selinux/config", "SELINUX=permissive", "SELINUX=enforcing", "grep -q '^SELINUX=enforcing' /etc/selinux/config || sed -i 's/^SELINUX=.*/SELINUX=enforcing/' /etc/selinux/config", "getenforce", True, "medium"),
        "5.2.1": _ln(_SC, "^PermitRootLogin no", "PermitRootLogin no", "PermitRootLogin yes", "PermitRootLogin no", "sshd -T | grep -i permitrootlogin", True, "medium"),
        "5.2.2": _ln(_SC, "^PermitEmptyPasswords no", "PermitEmptyPasswords no", "PermitEmptyPasswords yes", "PermitEmptyPasswords no", "sshd -T | grep -i permitemptypasswords", True),
        "5.3.1": _t("shell", True, "medium", "/etc/crypto-policies/config", "LEGACY", "DEFAULT", "", "update-crypto-policies --show | grep -qE '^(DEFAULT|FUTURE)$' || update-crypto-policies --set DEFAULT", "update-crypto-policies --show"),
    },
}


def resolve_family(target_name):
    s = resolve_rule_spec(target_name)
    return next((f for f in ("mariadb", "mysql", "postgresql", "mongodb", "cassandra", "rhel") if s.startswith(f)), "generic")


def _sort_key(cid):
    return tuple((0, int(p)) if p.isdigit() else (1, p) for p in cid.split(".")), cid


def build_remediation_plan(results, target_name="CIS Target", dry_run=True):
    """Build deterministic dry-run remediation plan (executes zero commands)."""
    if not dry_run:
        raise ValueError("Direct mutating execution is disabled; use dry_run=True.")
    spec, fam = resolve_rule_spec(target_name), resolve_family(target_name)
    tpls, items = TEMPLATES.get(fam, {}), []
    for c in sorted(normalize_control_results(results), key=lambda x: _sort_key(x["control_id"])):
        st, _, _ = map_compliance_state(c["status"], c["type"])
        if st not in ("Fail", "Manual"):
            continue
        cid = c["control_id"]
        t = tpls.get(cid) if st == "Fail" and c["type"].lower() != "manual" else None
        it = {"dry_run": True, "control_id": cid, "title": _clean(c["title"]), "compliance_state": st, "idempotent": True,
              "action_type": "manual_only", "requires_restart": False, "risk_level": "review",
              "config_file": "", "sql": "", "shell": "", "diff": "", "verification_command": _clean(c["command"])}
        if t:
            cf = t["config_file"].lstrip("/")
            bl, al = [ln + "\n" for ln in t["before"].splitlines()], [ln + "\n" for ln in t["after"].splitlines()]
            d = "".join(difflib.unified_diff(bl, al, f"a/{cf}", f"b/{cf}", lineterm="\n")).rstrip("\n")
            it.update({k: t[k] for k in ("action_type", "requires_restart", "risk_level", "config_file", "sql", "shell")},
                      diff=d, verification_command=t["verify"])
        else:
            it["manual_guidance"] = _clean(c["remediation"] or f"Review CIS {cid} manually.")
        items.append(it)
    return {"dry_run": True, "target": _clean(target_name), "rule_spec": spec, "family": fam, "total_items": len(items), "items": items}


def render_remediation(plan, fmt="diff"):
    """Render deterministic diff, sql, shell, ansible, or json output."""
    f = (fmt or "diff").strip().lower()
    if f not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format: {fmt}")
    if f == "json":
        return json.dumps(plan, indent=2, sort_keys=True) + "\n"
    tgt, items = plan.get("target", "CIS Target"), plan.get("items", [])
    hdr = f"{tgt} / {plan.get('family', 'generic')}"
    if f != "ansible":
        pfx, ol = ("--" if f == "sql" else "#"), lambda s: " ".join(str(s or "").splitlines())
        out = [*(["#!/usr/bin/env bash", "set -euo pipefail"] if f == "shell" else []), f"{pfx} DRY-RUN {f.upper()} ({ol(hdr)})"]
        for it in items:
            b, cid, ttl = it.get(f, ""), ol(it["control_id"]), ol(it["title"])
            out.extend([f"{pfx} CIS {cid} - {ttl}", b] if b else [f"{pfx} CIS {cid} [manual_only]: {ol(it.get('manual_guidance', ttl))}"])
        return "\n".join(out).rstrip("\n") + "\n"
    out = ["---", f"- name: {json.dumps(f'CIS Dry-Run Remediation ({tgt})')}", "  hosts: all", "  become: true", "  tasks:"]
    for it in items:
        cid, ttl = it["control_id"], it["title"]
        if it["action_type"] == "manual_only":
            out.extend([f"    - name: {json.dumps(f'CIS {cid} [manual_only] {ttl}')}", "      ansible.builtin.debug:", f"        msg: {json.dumps(_clean(it.get('manual_guidance', ttl)))}"])
        else:
            out.extend([f"    - name: {json.dumps(f'CIS {cid} {ttl}')}", "      ansible.builtin.shell:", f"        cmd: {json.dumps(it['shell'] or it['sql'])}", "      check_mode: true", "      changed_when: false"])
    return "\n".join(out) + "\n"


def generate_from_report_file(report_path, fmt="diff", output_path=None, target_name=None, dry_run=True):
    with open(report_path, "r", encoding="utf-8") as fp:
        data = json.load(fp)
    t = target_name or (data.get("target") or data.get("benchmark") if isinstance(data, dict) else None) or "CIS Target"
    raw = data.get("results", data) if isinstance(data, dict) else (data if isinstance(data, list) else [])
    plan = build_remediation_plan(raw, target_name=t, dry_run=dry_run)
    txt = render_remediation(plan, fmt=fmt)
    if output_path:
        atomic_write_text(output_path, txt)
    return plan, txt


def main(argv=None):
    p = argparse.ArgumentParser(description="PSL Dry-Run Remediation Generator")
    p.add_argument("--from-report", required=True)
    p.add_argument("-t", "--target")
    p.add_argument("-f", "--format", choices=list(SUPPORTED_FORMATS), default="diff")
    p.add_argument("-o", "--output")
    a = p.parse_args(argv)
    _, txt = generate_from_report_file(a.from_report, a.format, a.output, a.target, True)
    if not a.output:
        sys.stdout.write(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
