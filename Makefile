# Makefile for CIS Benchmark Tools

# Variables for Cassandra 5.0
CASSANDRA50_DOCKERFILE = Dockerfile_cassandra50
CASSANDRA50_IMAGE = cassandra50-audit
CASSANDRA50_CONTAINER = cassandra50-test
CASSANDRA50_SCRIPT = audit_cis_cassandra_50.py
CASSANDRA50_REPORT = rapport_cis_cassandra_50.html

.PHONY: help build-cassandra50 run-cassandra50 audit-cassandra50 report-cassandra50 clean-cassandra50 test-cassandra50

help:
	@echo "Available commands for Cassandra 5.0:"
	@echo "  make test-cassandra50    - Complete cycle: build, run, audit, get report, and clean"
	@echo "  make build-cassandra50   - Build the Docker image"
	@echo "  make run-cassandra50     - Start the Docker container"
	@echo "  make audit-cassandra50   - Run the audit script inside the container"
	@echo "  make report-cassandra50  - Copy the report from the container to the host"
	@echo "  make clean-cassandra50   - Remove the Docker container"

build-cassandra50:
	docker build -f $(CASSANDRA50_DOCKERFILE) -t $(CASSANDRA50_IMAGE) .

run-cassandra50:
	docker run -d --name $(CASSANDRA50_CONTAINER) $(CASSANDRA50_IMAGE)
	@echo "Waiting for Cassandra 5.0 to initialize (60s)..."
	sleep 60

audit-cassandra50:
	docker exec $(CASSANDRA50_CONTAINER) python3 /datas/$(CASSANDRA50_SCRIPT)

report-cassandra50:
	docker cp $(CASSANDRA50_CONTAINER):/datas/$(CASSANDRA50_REPORT) .
	@echo "Report copied to $(CASSANDRA50_REPORT)"

clean-cassandra50:
	docker rm -f $(CASSANDRA50_CONTAINER) || true

test-cassandra50: clean-cassandra50 build-cassandra50 run-cassandra50 audit-cassandra50 report-cassandra50 clean-cassandra50
	@echo "Full test cycle for Cassandra 5.0 completed."
