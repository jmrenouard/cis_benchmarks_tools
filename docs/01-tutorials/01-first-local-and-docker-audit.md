# Tutorial 1: First Local and Docker Audit

> **Goal:** Run your first PSL CIS audit in `/tmp/cis-lab` and verify JSON and offline SVG HTML output.

> [!WARNING]
> **Isolated Lab Only:** Write artifacts under `/tmp/cis-lab` and target disposable containers only.

## Prerequisites

- Python `3.8+` (`python3 audit_cis.py --version` prints `CIS Benchmarks Suite v2.10.0`)
- Optional: Docker Engine for container auditing

## Step 1: List All 18 Targets

```bash
rm -rf /tmp/cis-lab && mkdir -p /tmp/cis-lab
python3 audit_cis.py --list-targets
```

Expected output lists `18 Benchmarks / 887 Controls`.

## Step 2: Run a Local JSON Audit (`--local`)

```bash
python3 audit_cis.py --target rhel9 --local --format json -o /tmp/cis-lab/rhel9.json
python3 -c "import json; d=json.load(open('/tmp/cis-lab/rhel9.json')); print(d['target'], d['overall_score'], d['total_checks'])"
```

## Step 3: Run a Disposable Docker Audit with Offline SVG HTML

```bash
docker build -f docker/Dockerfile_mariadb106 -t cis-lab-mariadb106 .
docker run -d --name cis-lab-mariadb106 cis-lab-mariadb106 && sleep 15
python3 audit_cis.py --target mariadb106 --docker cis-lab-mariadb106 -f html -o /tmp/cis-lab/m106.html
python3 -c "assert '<svg' in open('/tmp/cis-lab/m106.html', encoding='utf-8').read(); print('SVG OK')"
```

## Step 4: Clean Up `/tmp/cis-lab`

```bash
docker rm -f cis-lab-mariadb106 2>/dev/null || true
rm -rf /tmp/cis-lab
```

## Next Steps

- [Tutorial 2: SARIF & Dry-Run Lab](02-sarif-and-dry-run-remediation-lab.md)
- [How-To Guides](../02-how-to-guides/index.md) · [Reference](../03-reference/index.md) · [Explanation](../04-explanation/index.md)
