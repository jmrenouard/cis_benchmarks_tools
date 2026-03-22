# Makefile for CIS Benchmark Tools

# Variables
MYSQL80_DOCKERFILE = Dockerfile_mysql80
MYSQL80_IMAGE = mysql80-audit
MYSQL80_CONTAINER = mysql80-test
MYSQL80_SCRIPT = audit_cis_mysql_80.py
MYSQL80_REPORT = rapport_cis_mysql_8.html

.PHONY: help build-mysql80 run-mysql80 audit-mysql80 report-mysql80 clean-mysql80 test-mysql80

help:
	@echo "Available commands:"
	@echo "  make test-mysql80    - Complete cycle: build, run, audit, get report, and clean for MySQL 8.0"
	@echo "  make build-mysql80   - Build the Docker image"
	@echo "  make run-mysql80     - Start the Docker container"
	@echo "  make audit-mysql80   - Run the audit script inside the container"
	@echo "  make report-mysql80  - Copy the report from the container to the host"
	@echo "  make clean-mysql80   - Remove the Docker container"

build-mysql80:
	docker build -f $(MYSQL80_DOCKERFILE) -t $(MYSQL80_IMAGE) .

run-mysql80:
	docker run -d --name $(MYSQL80_CONTAINER) $(MYSQL80_IMAGE)
	@echo "Waiting for MySQL to initialize (15s)..."
	sleep 15

audit-mysql80:
	docker exec $(MYSQL80_CONTAINER) python3 /datas/$(MYSQL80_SCRIPT)

report-mysql80:
	docker cp $(MYSQL80_CONTAINER):/datas/$(MYSQL80_REPORT) .
	@echo "Report copied to $(MYSQL80_REPORT)"

clean-mysql80:
	docker rm -f $(MYSQL80_CONTAINER) || true

test-mysql80: clean-mysql80 build-mysql80 run-mysql80 audit-mysql80 report-mysql80 clean-mysql80
	@echo "Full test cycle for MySQL 8.0 completed."
