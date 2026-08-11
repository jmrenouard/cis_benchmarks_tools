# Makefile for CIS Benchmark Tools

# Variables for Cassandra 4.1
CASSANDRA41_DOCKERFILE = Dockerfile_cassandra41
CASSANDRA41_IMAGE = cassandra41-audit
CASSANDRA41_CONTAINER = cassandra41-test
CASSANDRA41_SCRIPT = audit_cis_cassandra_41.py
CASSANDRA41_REPORT = rapport_cis_cassandra_41.html

.PHONY: help build-cassandra41 run-cassandra41 audit-cassandra41 report-cassandra41 clean-cassandra41 test-cassandra41

help:
	@echo "Available commands for Cassandra 4.1:"
	@echo "  make test-cassandra41    - Complete cycle: build, run, audit, get report, and clean"
	@echo "  make build-cassandra41   - Build the Docker image"
	@echo "  make run-cassandra41     - Start the Docker container"
	@echo "  make audit-cassandra41   - Run the audit script inside the container"
	@echo "  make report-cassandra41  - Copy the report from the container to the host"
	@echo "  make clean-cassandra41   - Remove the Docker container"

build-cassandra41:
	docker build -f $(CASSANDRA41_DOCKERFILE) -t $(CASSANDRA41_IMAGE) .

run-cassandra41:
	docker run -d --name $(CASSANDRA41_CONTAINER) $(CASSANDRA41_IMAGE)
	@echo "Waiting for Cassandra 4.1 to initialize (60s)..."
	sleep 60

audit-cassandra41:
	docker exec $(CASSANDRA41_CONTAINER) python3 /datas/$(CASSANDRA41_SCRIPT)

report-cassandra41:
	docker cp $(CASSANDRA41_CONTAINER):/datas/$(CASSANDRA41_REPORT) .
	@echo "Report copied to $(CASSANDRA41_REPORT)"

clean-cassandra41:
	docker rm -f $(CASSANDRA41_CONTAINER) || true

test-cassandra41: clean-cassandra41 build-cassandra41 run-cassandra41 audit-cassandra41 report-cassandra41 clean-cassandra41
	@echo "Full test cycle for Cassandra 4.1 completed."
