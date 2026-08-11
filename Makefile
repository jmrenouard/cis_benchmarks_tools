# Makefile for CIS Benchmark Tools

# Variables for MongoDB 8
MONGODB8_DOCKERFILE = Dockerfile_mongodb8
MONGODB8_IMAGE = mongodb8-audit
MONGODB8_CONTAINER = mongodb8-test
MONGODB8_SCRIPT = audit_cis_mongodb_8.py
MONGODB8_REPORT = rapport_cis_mongodb_8.html

.PHONY: help build-mongodb8 run-mongodb8 audit-mongodb8 report-mongodb8 clean-mongodb8 test-mongodb8

help:
	@echo "Available commands for MongoDB 8:"
	@echo "  make test-mongodb8    - Complete cycle: build, run, audit, get report, and clean"
	@echo "  make build-mongodb8   - Build the Docker image"
	@echo "  make run-mongodb8     - Start the Docker container"
	@echo "  make audit-mongodb8   - Run the audit script inside the container"
	@echo "  make report-mongodb8  - Copy the report from the container to the host"
	@echo "  make clean-mongodb8   - Remove the Docker container"

build-mongodb8:
	docker build -f $(MONGODB8_DOCKERFILE) -t $(MONGODB8_IMAGE) .

run-mongodb8:
	docker run -d --name $(MONGODB8_CONTAINER) $(MONGODB8_IMAGE)
	@echo "Waiting for MongoDB 8 to initialize (30s)..."
	sleep 30

audit-mongodb8:
	docker exec $(MONGODB8_CONTAINER) python3 /datas/$(MONGODB8_SCRIPT)

report-mongodb8:
	docker cp $(MONGODB8_CONTAINER):/datas/$(MONGODB8_REPORT) .
	@echo "Report copied to $(MONGODB8_REPORT)"

clean-mongodb8:
	docker rm -f $(MONGODB8_CONTAINER) || true

test-mongodb8: clean-mongodb8 build-mongodb8 run-mongodb8 audit-mongodb8 report-mongodb8 clean-mongodb8
	@echo "Full test cycle for MongoDB 8 completed."
