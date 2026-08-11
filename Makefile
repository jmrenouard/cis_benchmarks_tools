# Makefile for CIS Benchmark Tools

# Variables for PostgreSQL 18
POSTGRESQL18_DOCKERFILE = Dockerfile_postgresql18
POSTGRESQL18_IMAGE = postgresql18-audit
POSTGRESQL18_CONTAINER = postgresql18-test
POSTGRESQL18_SCRIPT = audit_cis_postgresql_18.py
POSTGRESQL18_REPORT = rapport_cis_postgresql_18.html

.PHONY: help build-postgresql18 run-postgresql18 audit-postgresql18 report-postgresql18 clean-postgresql18 test-postgresql18

help:
	@echo "Available commands for PostgreSQL 18:"
	@echo "  make test-postgresql18    - Complete cycle: build, run, audit, get report, and clean"
	@echo "  make build-postgresql18   - Build the Docker image"
	@echo "  make run-postgresql18     - Start the Docker container"
	@echo "  make audit-postgresql18   - Run the audit script inside the container"
	@echo "  make report-postgresql18  - Copy the report from the container to the host"
	@echo "  make clean-postgresql18   - Remove the Docker container"

build-postgresql18:
	docker build -f $(POSTGRESQL18_DOCKERFILE) -t $(POSTGRESQL18_IMAGE) .

run-postgresql18:
	docker run -d --name $(POSTGRESQL18_CONTAINER) $(POSTGRESQL18_IMAGE)
	@echo "Waiting for PostgreSQL 18 to initialize (15s)..."
	sleep 15

audit-postgresql18:
	docker exec $(POSTGRESQL18_CONTAINER) python3 /datas/$(POSTGRESQL18_SCRIPT)

report-postgresql18:
	docker cp $(POSTGRESQL18_CONTAINER):/datas/$(POSTGRESQL18_REPORT) .
	@echo "Report copied to $(POSTGRESQL18_REPORT)"

clean-postgresql18:
	docker rm -f $(POSTGRESQL18_CONTAINER) || true

test-postgresql18: clean-postgresql18 build-postgresql18 run-postgresql18 audit-postgresql18 report-postgresql18 clean-postgresql18
	@echo "Full test cycle for PostgreSQL 18 completed."
