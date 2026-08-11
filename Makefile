# Makefile for CIS Benchmark Tools

# Variables for MongoDB 7
MONGODB7_DOCKERFILE = Dockerfile_mongodb7
MONGODB7_IMAGE = mongodb7-audit
MONGODB7_CONTAINER = mongodb7-test
MONGODB7_SCRIPT = audit_cis_mongodb_7.py
MONGODB7_REPORT = rapport_cis_mongodb_7.html

.PHONY: help build-mongodb7 run-mongodb7 audit-mongodb7 report-mongodb7 clean-mongodb7 test-mongodb7

help:
	@echo "Available commands for MongoDB 7:"
	@echo "  make test-mongodb7    - Complete cycle: build, run, audit, get report, and clean"
	@echo "  make build-mongodb7   - Build the Docker image"
	@echo "  make run-mongodb7     - Start the Docker container"
	@echo "  make audit-mongodb7   - Run the audit script inside the container"
	@echo "  make report-mongodb7  - Copy the report from the container to the host"
	@echo "  make clean-mongodb7   - Remove the Docker container"

build-mongodb7:
	docker build -f $(MONGODB7_DOCKERFILE) -t $(MONGODB7_IMAGE) .

run-mongodb7:
	docker run -d --name $(MONGODB7_CONTAINER) $(MONGODB7_IMAGE)
	@echo "Waiting for MongoDB 7 to initialize (30s)..."
	sleep 30

audit-mongodb7:
	docker exec $(MONGODB7_CONTAINER) python3 /datas/$(MONGODB7_SCRIPT)

report-mongodb7:
	docker cp $(MONGODB7_CONTAINER):/datas/$(MONGODB7_REPORT) .
	@echo "Report copied to $(MONGODB7_REPORT)"

clean-mongodb7:
	docker rm -f $(MONGODB7_CONTAINER) || true

test-mongodb7: clean-mongodb7 build-mongodb7 run-mongodb7 audit-mongodb7 report-mongodb7 clean-mongodb7
	@echo "Full test cycle for MongoDB 7 completed."
