# Makefile for CIS Benchmark Tools

# Variables for MySQL Enterprise 9.7
MYSQL_ENTERPRISE97_DOCKERFILE = Dockerfile_mysql_enterprise_97
MYSQL_ENTERPRISE97_IMAGE = mysql-enterprise97-audit
MYSQL_ENTERPRISE97_CONTAINER = mysql-enterprise97-test
MYSQL_ENTERPRISE97_SCRIPT = audit_cis_mysql_enterprise_97.py
MYSQL_ENTERPRISE97_REPORT = rapport_cis_mysql_enterprise_97.html

.PHONY: help build-mysql-enterprise97 run-mysql-enterprise97 audit-mysql-enterprise97 report-mysql-enterprise97 clean-mysql-enterprise97 test-mysql-enterprise97

help:
	@echo "Available commands for MySQL Enterprise 9.7:"
	@echo "  make test-mysql-enterprise97    - Complete cycle: build, run, audit, get report, and clean"
	@echo "  make build-mysql-enterprise97   - Build the Docker image"
	@echo "  make run-mysql-enterprise97     - Start the Docker container"
	@echo "  make audit-mysql-enterprise97   - Run the audit script inside the container"
	@echo "  make report-mysql-enterprise97  - Copy the report from the container to the host"
	@echo "  make clean-mysql-enterprise97   - Remove the Docker container"

build-mysql-enterprise97:
	docker build -f $(MYSQL_ENTERPRISE97_DOCKERFILE) -t $(MYSQL_ENTERPRISE97_IMAGE) .

run-mysql-enterprise97:
	docker run -d --name $(MYSQL_ENTERPRISE97_CONTAINER) $(MYSQL_ENTERPRISE97_IMAGE)
	@echo "Waiting for MySQL Enterprise 9.7 to initialize (45s)..."
	sleep 45

audit-mysql-enterprise97:
	docker exec $(MYSQL_ENTERPRISE97_CONTAINER) python3 /datas/$(MYSQL_ENTERPRISE97_SCRIPT)

report-mysql-enterprise97:
	docker cp $(MYSQL_ENTERPRISE97_CONTAINER):/datas/$(MYSQL_ENTERPRISE97_REPORT) .
	@echo "Report copied to $(MYSQL_ENTERPRISE97_REPORT)"

clean-mysql-enterprise97:
	docker rm -f $(MYSQL_ENTERPRISE97_CONTAINER) || true

test-mysql-enterprise97: clean-mysql-enterprise97 build-mysql-enterprise97 run-mysql-enterprise97 audit-mysql-enterprise97 report-mysql-enterprise97 clean-mysql-enterprise97
	@echo "Full test cycle for MySQL Enterprise 9.7 completed."
