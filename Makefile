# Makefile for CIS Benchmark Tools

# Variables for MySQL Community 8.4
MYSQL_COMMUNITY84_DOCKERFILE = Dockerfile_mysql_community_84
MYSQL_COMMUNITY84_IMAGE = mysql-community84-audit
MYSQL_COMMUNITY84_CONTAINER = mysql-community84-test
MYSQL_COMMUNITY84_SCRIPT = audit_cis_mysql_community_84.py
MYSQL_COMMUNITY84_REPORT = rapport_cis_mysql_community_84.html

.PHONY: help build-mysql-community84 run-mysql-community84 audit-mysql-community84 report-mysql-community84 clean-mysql-community84 test-mysql-community84

help:
	@echo "Available commands for MySQL Community 8.4:"
	@echo "  make test-mysql-community84    - Complete cycle: build, run, audit, get report, and clean"
	@echo "  make build-mysql-community84   - Build the Docker image"
	@echo "  make run-mysql-community84     - Start the Docker container"
	@echo "  make audit-mysql-community84   - Run the audit script inside the container"
	@echo "  make report-mysql-community84  - Copy the report from the container to the host"
	@echo "  make clean-mysql-community84   - Remove the Docker container"

build-mysql-community84:
	docker build -f $(MYSQL_COMMUNITY84_DOCKERFILE) -t $(MYSQL_COMMUNITY84_IMAGE) .

run-mysql-community84:
	docker run -d --name $(MYSQL_COMMUNITY84_CONTAINER) $(MYSQL_COMMUNITY84_IMAGE)
	@echo "Waiting for MySQL Community 8.4 to initialize (45s)..."
	sleep 45

audit-mysql-community84:
	docker exec $(MYSQL_COMMUNITY84_CONTAINER) python3 /datas/$(MYSQL_COMMUNITY84_SCRIPT)

report-mysql-community84:
	docker cp $(MYSQL_COMMUNITY84_CONTAINER):/datas/$(MYSQL_COMMUNITY84_REPORT) .
	@echo "Report copied to $(MYSQL_COMMUNITY84_REPORT)"

clean-mysql-community84:
	docker rm -f $(MYSQL_COMMUNITY84_CONTAINER) || true

test-mysql-community84: clean-mysql-community84 build-mysql-community84 run-mysql-community84 audit-mysql-community84 report-mysql-community84 clean-mysql-community84
	@echo "Full test cycle for MySQL Community 8.4 completed."
