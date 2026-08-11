# Makefile for CIS Benchmark Tools

# Variables for MariaDB 10.11
MARIADB1011_DOCKERFILE = Dockerfile_mariadb1011
MARIADB1011_IMAGE = mariadb1011-audit
MARIADB1011_CONTAINER = mariadb1011-test
MARIADB1011_SCRIPT = audit_cis_mariadb_1011.py
MARIADB1011_REPORT = rapport_cis_mariadb_1011.html

.PHONY: help build-mariadb1011 run-mariadb1011 audit-mariadb1011 report-mariadb1011 clean-mariadb1011 test-mariadb1011

help:
	@echo "Available commands for MariaDB 10.11:"
	@echo "  make test-mariadb1011    - Complete cycle: build, run, audit, get report, and clean"
	@echo "  make build-mariadb1011   - Build the Docker image"
	@echo "  make run-mariadb1011     - Start the Docker container"
	@echo "  make audit-mariadb1011   - Run the audit script inside the container"
	@echo "  make report-mariadb1011  - Copy the report from the container to the host"
	@echo "  make clean-mariadb1011   - Remove the Docker container"

build-mariadb1011:
	docker build -f $(MARIADB1011_DOCKERFILE) -t $(MARIADB1011_IMAGE) .

run-mariadb1011:
	docker run -d --name $(MARIADB1011_CONTAINER) $(MARIADB1011_IMAGE)
	@echo "Waiting for MariaDB 10.11 to initialize (30s)..."
	sleep 30

audit-mariadb1011:
	docker exec $(MARIADB1011_CONTAINER) python3 /datas/$(MARIADB1011_SCRIPT)

report-mariadb1011:
	docker cp $(MARIADB1011_CONTAINER):/datas/$(MARIADB1011_REPORT) .
	@echo "Report copied to $(MARIADB1011_REPORT)"

clean-mariadb1011:
	docker rm -f $(MARIADB1011_CONTAINER) || true

test-mariadb1011: clean-mariadb1011 build-mariadb1011 run-mariadb1011 audit-mariadb1011 report-mariadb1011 clean-mariadb1011
	@echo "Full test cycle for MariaDB 10.11 completed."
