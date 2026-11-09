# PyPI Packaging & Release Publishing Guide

This guide details packaging architecture, build verification, and automated GitHub Actions PyPI publishing for the **CIS Benchmarks Tools Suite** (`cis-benchmarks-tools`).

---

## 1. Packaging Architecture & Standards

- **PyPA Standard**: Setuptools build backend (`setuptools.build_meta`) in `pyproject.toml`.
- **PSL ONLY**: Strictly zero third-party dependencies (`dependencies = []`).
- **Dynamic Versioning**: Resolved from root `VERSION` file; fallback via `importlib.metadata.version("cis-benchmarks-tools")` for installed wheels.
- **Data Bundling**: 18 JSON rules (`rules/*.json`) and 2 HTML templates (`templates/*.html`) packaged into wheels via `packages = ["rules", "templates"]` and `[tool.setuptools.package-data]`.
- **Console Entrypoints**: `audit-cis = "audit_cis:main"` and `audit_cis = "audit_cis:main"`.

---

## 2. Local Distribution Build & Verification

Build distribution archives (`sdist` and `wheel`) locally:

```bash
python -m pip install --upgrade build twine
python -m build
```

Verify wheel data assets using Python Standard Library:

```bash
python -c "import glob, zipfile; z = zipfile.ZipFile(glob.glob('dist/*.whl')[0]); assert len([n for n in z.namelist() if n.startswith('rules/') and n.endswith('.json')]) == 18; assert len([n for n in z.namelist() if n.startswith('templates/') and n.endswith('.html')]) == 2; print('Wheel data assets verified successfully!')"
```

---

## 3. Preflight Distribution Validation (`twine check`)

Validate metadata rendering and distribution integrity before PyPI upload:

```bash
python -m twine check --strict dist/*
```

Verifies `README.md` CommonMark syntax, metadata schema, and archive integrity with zero warnings.

---

## 4. Automated GitHub Actions Publishing Workflow

Automated publication is orchestrated by `.github/workflows/pypi-publish.yml`:

- **Triggers**: Exclusively `release: types: [published]` and `workflow_dispatch`. Tag pushes (`push: tags:`) are excluded to prevent premature publishing.
- **Concurrency**: `cancel-in-progress: false` ensures active uploads are never aborted mid-transmission.
- **Preflight Twine Check**: Executes `python -m twine check --strict dist/*` right after `python -m build`.
- **Authentication Modes**:
  1. **PyPI Trusted Publishing (OIDC)**: Passwordless OpenID Connect token minting via `id-token: write` and `pypa/gh-action-pypi-publish@release/v1`.
  2. **API Token (`PYPI_API_TOKEN`)**: Repository secret using `twine upload --non-interactive --skip-existing dist/*`.
  3. **Graceful Notice**: Emits an informational notice if neither credential method is configured.

---

## 5. Release Publication Procedure

1. **Local Validation**: Run `python scripts/pre_commit_checks.py` and `python -m unittest discover -s tests -v`.
2. **Publish GitHub Release**:
   ```bash
   gh release create v2.10.0 --title "v2.10.0" --notes-file docs/RELEASE_NOTES_v2.10.0.md
   ```
3. **Workflow Execution**: Monitor **Actions** → **Publish to PyPI**.
4. **PyPI Verification**: Verify live installation via `pip install --upgrade cis-benchmarks-tools`.

---

## 6. Docker Hub Container Packaging & Release Publishing

Multi-platform container published to Docker Hub at [`jmrenouard/cis-benchmarks-tools`](https://hub.docker.com/r/jmrenouard/cis-benchmarks-tools).

### Architecture & Standards
- **Base Image**: `python:3.12-slim`.
- **Non-Root**: `cisuser:cisgroup` (UID/GID 10001).
- **PSL ONLY**: Zero external dependencies.
- **Assets**: Bundles 18 CIS rule specs (`rules/*.json`) and HTML templates (`templates/*.html`).
- **Volume**: `/app/reports`.

### Local Container Build & Verification
```bash
docker build -t jmrenouard/cis-benchmarks-tools:latest .
docker run --rm jmrenouard/cis-benchmarks-tools --list-targets
docker run --rm -v $(pwd)/reports:/app/reports jmrenouard/cis-benchmarks-tools --target mariadb106 -o /app/reports/audit.html
```

### Automated GitHub Actions Workflow
Orchestrated by `.github/workflows/docker-publish.yml`:
- **Triggers**: `release: types: [published]` and manual `workflow_dispatch`.
- **Platforms**: `linux/amd64` and `linux/arm64` (Buildx/QEMU).
- **Tags**: `latest`, `vX.Y.Z`, and `X.Y.Z`.
- **Secrets**: `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`.


