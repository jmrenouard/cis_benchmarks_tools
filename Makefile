# Makefile for CIS Benchmark Tools

# Variables for MariaDB 10.6
MARIADB106_DOCKERFILE = Dockerfile_mariadb106
MARIADB106_IMAGE = mariadb106-audit
MARIADB106_CONTAINER = mariadb106-test
MARIADB106_SCRIPT = audit_cis_mariadb_106.py
MARIADB106_REPORT = rapport_cis_mariadb_106.html

.PHONY: help build-mariadb106 run-mariadb106 audit-mariadb106 report-mariadb106 clean-mariadb106 test-mariadb106

help:
	@echo "Available commands for MariaDB 10.6:"
	@echo "  make test-mariadb106    - Complete cycle: build, run, audit, get report, and clean"
	@echo "  make build-mariadb106   - Build the Docker image"
	@echo "  make run-mariadb106     - Start the Docker container"
	@echo "  make audit-mariadb106   - Run the audit script inside the container"
	@echo "  make report-mariadb106  - Copy the report from the container to the host"
	@echo "  make clean-mariadb106   - Remove the Docker container"

build-mariadb106:
	docker build -f $(MARIADB106_DOCKERFILE) -t $(MARIADB106_IMAGE) .

run-mariadb106:
	docker run -d --name $(MARIADB106_CONTAINER) $(MARIADB106_IMAGE)
	@echo "Waiting for MariaDB 10.6 to initialize (30s)..."
	sleep 30

audit-mariadb106:
	docker exec $(MARIADB106_CONTAINER) python3 /datas/$(MARIADB106_SCRIPT)

report-mariadb106:
	docker cp $(MARIADB106_CONTAINER):/datas/$(MARIADB106_REPORT) .
	@echo "Report copied to $(MARIADB106_REPORT)"

clean-mariadb106:
	docker rm -f $(MARIADB106_CONTAINER) || true

test-mariadb106: clean-mariadb106 build-mariadb106 run-mariadb106 audit-mariadb106 report-mariadb106 clean-mariadb106
	@echo "Full test cycle for MariaDB 10.6 completed."
