# syntax=docker/dockerfile:1
FROM python:3.12-slim

LABEL org.opencontainers.image.title="CIS Benchmarks Tools Suite" \
      org.opencontainers.image.source="https://github.com/jmrenouard/cis_benchmarks_tools" \
      org.opencontainers.image.licenses="GPL-3.0-or-later"

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PATH="/app:${PATH}"

RUN groupadd -g 10001 cisgroup && \
    useradd -u 10001 -g cisgroup -s /sbin/nologin -M -d /app cisuser && \
    mkdir -p /app/reports && chown -R cisuser:cisgroup /app

WORKDIR /app

COPY --chown=cisuser:cisgroup audit_cis*.py execution_drivers.py audit_diagnostics.py \
     audit_orchestrator.py cis_core_engine.py docker_transport.py in_container_inspector.py \
     docker_e2e_engine.py temporal_metadata.py post_execution_publisher.py \
     VERSION README.md LICENSE ./
COPY --chown=cisuser:cisgroup rules/ ./rules/
COPY --chown=cisuser:cisgroup templates/ ./templates/

USER cisuser
VOLUME ["/app/reports"]
HEALTHCHECK --interval=30s --timeout=5s --retries=1 CMD python3 audit_cis.py --version || exit 1
ENTRYPOINT ["python3", "audit_cis.py"]
CMD ["--help"]
