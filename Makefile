# Makefile for CIS Benchmark Tools

# Variables for PostgreSQL 17
POSTGRESQL17_DOCKERFILE = Dockerfile_postgresql17
POSTGRESQL17_IMAGE = postgresql17-audit
POSTGRESQL17_CONTAINER = postgresql17-test
POSTGRESQL17_SCRIPT = audit_cis_postgresql_17.py
POSTGRESQL17_REPORT = rapport_cis_postgresql_17.html

.PHONY: help build-postgresql17 run-postgresql17 audit-postgresql17 report-postgresql17 clean-postgresql17 test-postgresql17

help:
	@echo "Available commands for PostgreSQL 17:"
	@echo "  make test-postgresql17    - Complete cycle: build, run, audit, get report, and clean"
	@echo "  make build-postgresql17   - Build the Docker image"
	@echo "  make run-postgresql17     - Start the Docker container"
	@echo "  make audit-postgresql17   - Run the audit script inside the container"
	@echo "  make report-postgresql17  - Copy the report from the container to the host"
	@echo "  make clean-postgresql17   - Remove the Docker container"

build-postgresql17:
	docker build -f $(POSTGRESQL17_DOCKERFILE) -t $(POSTGRESQL17_IMAGE) .

run-postgresql17:
	docker run -d --name $(POSTGRESQL17_CONTAINER) $(POSTGRESQL17_IMAGE)
	@echo "Waiting for PostgreSQL 17 to initialize (15s)..."
	sleep 15

audit-postgresql17:
	docker exec $(POSTGRESQL17_CONTAINER) python3 /datas/$(POSTGRESQL17_SCRIPT)

report-postgresql17:
	docker cp $(POSTGRESQL17_CONTAINER):/datas/$(POSTGRESQL17_REPORT) .
	@echo "Report copied to $(POSTGRESQL17_REPORT)"

clean-postgresql17:
	docker rm -f $(POSTGRESQL17_CONTAINER) || true

test-postgresql17: clean-postgresql17 build-postgresql17 run-postgresql17 audit-postgresql17 report-postgresql17 clean-postgresql17
	@echo "Full test cycle for PostgreSQL 17 completed."
