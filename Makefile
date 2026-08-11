# Makefile for CIS Benchmark Tools

# Variables for MySQL Enterprise 8.4
MYSQL_ENTERPRISE84_DOCKERFILE = Dockerfile_mysql_enterprise_84
MYSQL_ENTERPRISE84_IMAGE = mysql-enterprise84-audit
MYSQL_ENTERPRISE84_CONTAINER = mysql-enterprise84-test
MYSQL_ENTERPRISE84_SCRIPT = audit_cis_mysql_enterprise_84.py
MYSQL_ENTERPRISE84_REPORT = rapport_cis_mysql_enterprise_84.html

.PHONY: help build-mysql-enterprise84 run-mysql-enterprise84 audit-mysql-enterprise84 report-mysql-enterprise84 clean-mysql-enterprise84 test-mysql-enterprise84

help:
	@echo "Available commands for MySQL Enterprise 8.4:"
	@echo "  make test-mysql-enterprise84    - Complete cycle: build, run, audit, get report, and clean"
	@echo "  make build-mysql-enterprise84   - Build the Docker image"
	@echo "  make run-mysql-enterprise84     - Start the Docker container"
	@echo "  make audit-mysql-enterprise84   - Run the audit script inside the container"
	@echo "  make report-mysql-enterprise84  - Copy the report from the container to the host"
	@echo "  make clean-mysql-enterprise84   - Remove the Docker container"

build-mysql-enterprise84:
	docker build -f $(MYSQL_ENTERPRISE84_DOCKERFILE) -t $(MYSQL_ENTERPRISE84_IMAGE) .

run-mysql-enterprise84:
	docker run -d --name $(MYSQL_ENTERPRISE84_CONTAINER) $(MYSQL_ENTERPRISE84_IMAGE)
	@echo "Waiting for MySQL Enterprise 8.4 to initialize (45s)..."
	sleep 45

audit-mysql-enterprise84:
	docker exec $(MYSQL_ENTERPRISE84_CONTAINER) python3 /datas/$(MYSQL_ENTERPRISE84_SCRIPT)

report-mysql-enterprise84:
	docker cp $(MYSQL_ENTERPRISE84_CONTAINER):/datas/$(MYSQL_ENTERPRISE84_REPORT) .
	@echo "Report copied to $(MYSQL_ENTERPRISE84_REPORT)"

clean-mysql-enterprise84:
	docker rm -f $(MYSQL_ENTERPRISE84_CONTAINER) || true

test-mysql-enterprise84: clean-mysql-enterprise84 build-mysql-enterprise84 run-mysql-enterprise84 audit-mysql-enterprise84 report-mysql-enterprise84 clean-mysql-enterprise84
	@echo "Full test cycle for MySQL Enterprise 8.4 completed."
