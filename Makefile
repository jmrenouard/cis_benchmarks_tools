# Makefile for CIS Benchmark Tools

# Variables for PostgreSQL 16
POSTGRESQL16_DOCKERFILE = Dockerfile_postgresql16
POSTGRESQL16_IMAGE = postgresql16-audit
POSTGRESQL16_CONTAINER = postgresql16-test
POSTGRESQL16_SCRIPT = audit_cis_postgresql_16.py
POSTGRESQL16_REPORT = rapport_cis_postgresql_16.html

.PHONY: help build-postgresql16 run-postgresql16 audit-postgresql16 report-postgresql16 clean-postgresql16 test-postgresql16

help:
	@echo "Available commands for PostgreSQL 16:"
	@echo "  make test-postgresql16    - Complete cycle: build, run, audit, get report, and clean"
	@echo "  make build-postgresql16   - Build the Docker image"
	@echo "  make run-postgresql16     - Start the Docker container"
	@echo "  make audit-postgresql16   - Run the audit script inside the container"
	@echo "  make report-postgresql16  - Copy the report from the container to the host"
	@echo "  make clean-postgresql16   - Remove the Docker container"

build-postgresql16:
	docker build -f $(POSTGRESQL16_DOCKERFILE) -t $(POSTGRESQL16_IMAGE) .

run-postgresql16:
	docker run -d --name $(POSTGRESQL16_CONTAINER) $(POSTGRESQL16_IMAGE)
	@echo "Waiting for PostgreSQL 16 to initialize (15s)..."
	sleep 15

audit-postgresql16:
	docker exec $(POSTGRESQL16_CONTAINER) python3 /datas/$(POSTGRESQL16_SCRIPT)

report-postgresql16:
	docker cp $(POSTGRESQL16_CONTAINER):/datas/$(POSTGRESQL16_REPORT) .
	@echo "Report copied to $(POSTGRESQL16_REPORT)"

clean-postgresql16:
	docker rm -f $(POSTGRESQL16_CONTAINER) || true

test-postgresql16: clean-postgresql16 build-postgresql16 run-postgresql16 audit-postgresql16 report-postgresql16 clean-postgresql16
	@echo "Full test cycle for PostgreSQL 16 completed."
