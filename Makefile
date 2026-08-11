# Makefile for CIS Benchmark Tools

# Variables for Cassandra 4.0
CASSANDRA40_DOCKERFILE = Dockerfile_cassandra40
CASSANDRA40_IMAGE = cassandra40-audit
CASSANDRA40_CONTAINER = cassandra40-test
CASSANDRA40_SCRIPT = audit_cis_cassandra_40.py
CASSANDRA40_REPORT = rapport_cis_cassandra_40.html

.PHONY: help build-cassandra40 run-cassandra40 audit-cassandra40 report-cassandra40 clean-cassandra40 test-cassandra40

help:
	@echo "Available commands for Cassandra 4.0:"
	@echo "  make test-cassandra40    - Complete cycle: build, run, audit, get report, and clean"
	@echo "  make build-cassandra40   - Build the Docker image"
	@echo "  make run-cassandra40     - Start the Docker container"
	@echo "  make audit-cassandra40   - Run the audit script inside the container"
	@echo "  make report-cassandra40  - Copy the report from the container to the host"
	@echo "  make clean-cassandra40   - Remove the Docker container"

build-cassandra40:
	docker build -f $(CASSANDRA40_DOCKERFILE) -t $(CASSANDRA40_IMAGE) .

run-cassandra40:
	docker run -d --name $(CASSANDRA40_CONTAINER) $(CASSANDRA40_IMAGE)
	@echo "Waiting for Cassandra 4.0 to initialize (60s)..."
	sleep 60

audit-cassandra40:
	docker exec $(CASSANDRA40_CONTAINER) python3 /datas/$(CASSANDRA40_SCRIPT)

report-cassandra40:
	docker cp $(CASSANDRA40_CONTAINER):/datas/$(CASSANDRA40_REPORT) .
	@echo "Report copied to $(CASSANDRA40_REPORT)"

clean-cassandra40:
	docker rm -f $(CASSANDRA40_CONTAINER) || true

test-cassandra40: clean-cassandra40 build-cassandra40 run-cassandra40 audit-cassandra40 report-cassandra40 clean-cassandra40
	@echo "Full test cycle for Cassandra 4.0 completed."
