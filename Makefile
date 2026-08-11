# Makefile for CIS Benchmark Tools

# Variables for MySQL Community 9.7
MYSQL_COMMUNITY97_DOCKERFILE = Dockerfile_mysql_community_97
MYSQL_COMMUNITY97_IMAGE = mysql-community97-audit
MYSQL_COMMUNITY97_CONTAINER = mysql-community97-test
MYSQL_COMMUNITY97_SCRIPT = audit_cis_mysql_community_97.py
MYSQL_COMMUNITY97_REPORT = rapport_cis_mysql_community_97.html

.PHONY: help build-mysql-community97 run-mysql-community97 audit-mysql-community97 report-mysql-community97 clean-mysql-community97 test-mysql-community97

help:
	@echo "Available commands for MySQL Community 9.7:"
	@echo "  make test-mysql-community97    - Complete cycle: build, run, audit, get report, and clean"
	@echo "  make build-mysql-community97   - Build the Docker image"
	@echo "  make run-mysql-community97     - Start the Docker container"
	@echo "  make audit-mysql-community97   - Run the audit script inside the container"
	@echo "  make report-mysql-community97  - Copy the report from the container to the host"
	@echo "  make clean-mysql-community97   - Remove the Docker container"

build-mysql-community97:
	docker build -f $(MYSQL_COMMUNITY97_DOCKERFILE) -t $(MYSQL_COMMUNITY97_IMAGE) .

run-mysql-community97:
	docker run -d --name $(MYSQL_COMMUNITY97_CONTAINER) $(MYSQL_COMMUNITY97_IMAGE)
	@echo "Waiting for MySQL Community 9.7 to initialize (45s)..."
	sleep 45

audit-mysql-community97:
	docker exec $(MYSQL_COMMUNITY97_CONTAINER) python3 /datas/$(MYSQL_COMMUNITY97_SCRIPT)

report-mysql-community97:
	docker cp $(MYSQL_COMMUNITY97_CONTAINER):/datas/$(MYSQL_COMMUNITY97_REPORT) .
	@echo "Report copied to $(MYSQL_COMMUNITY97_REPORT)"

clean-mysql-community97:
	docker rm -f $(MYSQL_COMMUNITY97_CONTAINER) || true

test-mysql-community97: clean-mysql-community97 build-mysql-community97 run-mysql-community97 audit-mysql-community97 report-mysql-community97 clean-mysql-community97
	@echo "Full test cycle for MySQL Community 9.7 completed."
