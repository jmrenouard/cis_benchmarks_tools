# Makefile for CIS Benchmark Tools

# Variables for all targets
MARIADB106_DOCKERFILE = Dockerfile_mariadb106
MARIADB106_IMAGE = mariadb106-audit
MARIADB106_CONTAINER = mariadb106-test
MARIADB106_SCRIPT = audit_cis_mariadb_106.py
MARIADB106_REPORT = rapport_cis_mariadb_106.html

MARIADB1011_DOCKERFILE = Dockerfile_mariadb1011
MARIADB1011_IMAGE = mariadb1011-audit
MARIADB1011_CONTAINER = mariadb1011-test
MARIADB1011_SCRIPT = audit_cis_mariadb_1011.py
MARIADB1011_REPORT = rapport_cis_mariadb_1011.html

MYSQL80_DOCKERFILE = Dockerfile_mysql80
MYSQL80_IMAGE = mysql80-audit
MYSQL80_CONTAINER = mysql80-test
MYSQL80_SCRIPT = audit_cis_mysql_80.py
MYSQL80_REPORT = rapport_cis_mysql_8.html

MYSQL_COMMUNITY84_DOCKERFILE = Dockerfile_mysql_community_84
MYSQL_COMMUNITY84_IMAGE = mysql-community84-audit
MYSQL_COMMUNITY84_CONTAINER = mysql-community84-test
MYSQL_COMMUNITY84_SCRIPT = audit_cis_mysql_community_84.py
MYSQL_COMMUNITY84_REPORT = rapport_cis_mysql_community_84.html

MYSQL_ENTERPRISE84_DOCKERFILE = Dockerfile_mysql_enterprise_84
MYSQL_ENTERPRISE84_IMAGE = mysql-enterprise84-audit
MYSQL_ENTERPRISE84_CONTAINER = mysql-enterprise84-test
MYSQL_ENTERPRISE84_SCRIPT = audit_cis_mysql_enterprise_84.py
MYSQL_ENTERPRISE84_REPORT = rapport_cis_mysql_enterprise_84.html

MYSQL_COMMUNITY97_DOCKERFILE = Dockerfile_mysql_community_97
MYSQL_COMMUNITY97_IMAGE = mysql-community97-audit
MYSQL_COMMUNITY97_CONTAINER = mysql-community97-test
MYSQL_COMMUNITY97_SCRIPT = audit_cis_mysql_community_97.py
MYSQL_COMMUNITY97_REPORT = rapport_cis_mysql_community_97.html

MYSQL_ENTERPRISE97_DOCKERFILE = Dockerfile_mysql_enterprise_97
MYSQL_ENTERPRISE97_IMAGE = mysql-enterprise97-audit
MYSQL_ENTERPRISE97_CONTAINER = mysql-enterprise97-test
MYSQL_ENTERPRISE97_SCRIPT = audit_cis_mysql_enterprise_97.py
MYSQL_ENTERPRISE97_REPORT = rapport_cis_mysql_enterprise_97.html

POSTGRESQL16_DOCKERFILE = Dockerfile_postgresql16
POSTGRESQL16_IMAGE = postgresql16-audit
POSTGRESQL16_CONTAINER = postgresql16-test
POSTGRESQL16_SCRIPT = audit_cis_postgresql_16.py
POSTGRESQL16_REPORT = rapport_cis_postgresql_16.html

POSTGRESQL17_DOCKERFILE = Dockerfile_postgresql17
POSTGRESQL17_IMAGE = postgresql17-audit
POSTGRESQL17_CONTAINER = postgresql17-test
POSTGRESQL17_SCRIPT = audit_cis_postgresql_17.py
POSTGRESQL17_REPORT = rapport_cis_postgresql_17.html

POSTGRESQL18_DOCKERFILE = Dockerfile_postgresql18
POSTGRESQL18_IMAGE = postgresql18-audit
POSTGRESQL18_CONTAINER = postgresql18-test
POSTGRESQL18_SCRIPT = audit_cis_postgresql_18.py
POSTGRESQL18_REPORT = rapport_cis_postgresql_18.html

MONGODB7_DOCKERFILE = Dockerfile_mongodb7
MONGODB7_IMAGE = mongodb7-audit
MONGODB7_CONTAINER = mongodb7-test
MONGODB7_SCRIPT = audit_cis_mongodb_7.py
MONGODB7_REPORT = rapport_cis_mongodb_7.html

MONGODB8_DOCKERFILE = Dockerfile_mongodb8
MONGODB8_IMAGE = mongodb8-audit
MONGODB8_CONTAINER = mongodb8-test
MONGODB8_SCRIPT = audit_cis_mongodb_8.py
MONGODB8_REPORT = rapport_cis_mongodb_8.html

CASSANDRA40_DOCKERFILE = Dockerfile_cassandra40
CASSANDRA40_IMAGE = cassandra40-audit
CASSANDRA40_CONTAINER = cassandra40-test
CASSANDRA40_SCRIPT = audit_cis_cassandra_40.py
CASSANDRA40_REPORT = rapport_cis_cassandra_40.html

CASSANDRA41_DOCKERFILE = Dockerfile_cassandra41
CASSANDRA41_IMAGE = cassandra41-audit
CASSANDRA41_CONTAINER = cassandra41-test
CASSANDRA41_SCRIPT = audit_cis_cassandra_41.py
CASSANDRA41_REPORT = rapport_cis_cassandra_41.html

CASSANDRA50_DOCKERFILE = Dockerfile_cassandra50
CASSANDRA50_IMAGE = cassandra50-audit
CASSANDRA50_CONTAINER = cassandra50-test
CASSANDRA50_SCRIPT = audit_cis_cassandra_50.py
CASSANDRA50_REPORT = rapport_cis_cassandra_50.html

.PHONY: help test-all build-mariadb106 run-mariadb106 audit-mariadb106 report-mariadb106 clean-mariadb106 test-mariadb106 build-mariadb1011 run-mariadb1011 audit-mariadb1011 report-mariadb1011 clean-mariadb1011 test-mariadb1011 build-mysql80 run-mysql80 audit-mysql80 report-mysql80 clean-mysql80 test-mysql80 build-mysql-community84 run-mysql-community84 audit-mysql-community84 report-mysql-community84 clean-mysql-community84 test-mysql-community84 build-mysql-enterprise84 run-mysql-enterprise84 audit-mysql-enterprise84 report-mysql-enterprise84 clean-mysql-enterprise84 test-mysql-enterprise84 build-mysql-community97 run-mysql-community97 audit-mysql-community97 report-mysql-community97 clean-mysql-community97 test-mysql-community97 build-mysql-enterprise97 run-mysql-enterprise97 audit-mysql-enterprise97 report-mysql-enterprise97 clean-mysql-enterprise97 test-mysql-enterprise97 build-postgresql16 run-postgresql16 audit-postgresql16 report-postgresql16 clean-postgresql16 test-postgresql16 build-postgresql17 run-postgresql17 audit-postgresql17 report-postgresql17 clean-postgresql17 test-postgresql17 build-postgresql18 run-postgresql18 audit-postgresql18 report-postgresql18 clean-postgresql18 test-postgresql18 build-mongodb7 run-mongodb7 audit-mongodb7 report-mongodb7 clean-mongodb7 test-mongodb7 build-mongodb8 run-mongodb8 audit-mongodb8 report-mongodb8 clean-mongodb8 test-mongodb8 build-cassandra40 run-cassandra40 audit-cassandra40 report-cassandra40 clean-cassandra40 test-cassandra40 build-cassandra41 run-cassandra41 audit-cassandra41 report-cassandra41 clean-cassandra41 test-cassandra41 build-cassandra50 run-cassandra50 audit-cassandra50 report-cassandra50 clean-cassandra50 test-cassandra50

help:
	@echo "Available commands:"
	@echo "  make test-all                  - Run test cycle for ALL database benchmarks"
	@echo "  make test-mariadb106           - Full cycle (build, run, audit, report, clean) for MariaDB 10.6"
	@echo "  make test-mariadb1011          - Full cycle (build, run, audit, report, clean) for MariaDB 10.11"
	@echo "  make test-mysql80              - Full cycle (build, run, audit, report, clean) for MySQL Enterprise 8.0"
	@echo "  make test-mysql-community84    - Full cycle (build, run, audit, report, clean) for MySQL Community 8.4"
	@echo "  make test-mysql-enterprise84   - Full cycle (build, run, audit, report, clean) for MySQL Enterprise 8.4"
	@echo "  make test-mysql-community97    - Full cycle (build, run, audit, report, clean) for MySQL Community 9.7"
	@echo "  make test-mysql-enterprise97   - Full cycle (build, run, audit, report, clean) for MySQL Enterprise 9.7"
	@echo "  make test-postgresql16         - Full cycle (build, run, audit, report, clean) for PostgreSQL 16"
	@echo "  make test-postgresql17         - Full cycle (build, run, audit, report, clean) for PostgreSQL 17"
	@echo "  make test-postgresql18         - Full cycle (build, run, audit, report, clean) for PostgreSQL 18"
	@echo "  make test-mongodb7             - Full cycle (build, run, audit, report, clean) for MongoDB 7"
	@echo "  make test-mongodb8             - Full cycle (build, run, audit, report, clean) for MongoDB 8"
	@echo "  make test-cassandra40          - Full cycle (build, run, audit, report, clean) for Cassandra 4.0"
	@echo "  make test-cassandra41          - Full cycle (build, run, audit, report, clean) for Cassandra 4.1"
	@echo "  make test-cassandra50          - Full cycle (build, run, audit, report, clean) for Cassandra 5.0"

test-all: test-mariadb106 test-mariadb1011 test-mysql80 test-mysql-community84 test-mysql-enterprise84 test-mysql-community97 test-mysql-enterprise97 test-postgresql16 test-postgresql17 test-postgresql18 test-mongodb7 test-mongodb8 test-cassandra40 test-cassandra41 test-cassandra50
	@echo "🎉 All database CIS benchmark tests completed!"

# --- MariaDB 10.6 ---
build-mariadb106:
	docker build -f $(MARIADB106_DOCKERFILE) -t $(MARIADB106_IMAGE) .

run-mariadb106:
	docker run -d --name $(MARIADB106_CONTAINER) $(MARIADB106_IMAGE)
	@echo "Waiting for MariaDB 10.6 to initialize (30s)..."
	sleep 30

audit-mariadb106:
	docker exec $(MARIADB106_CONTAINER) python3 /datas/$(MARIADB106_SCRIPT)

report-mariadb106:
	docker cp $(MARIADB106_CONTAINER):/datas/$(MARIADB106_REPORT) .
	@echo "Report copied to $(MARIADB106_REPORT)"

clean-mariadb106:
	docker rm -f $(MARIADB106_CONTAINER) || true

test-mariadb106: clean-mariadb106 build-mariadb106 run-mariadb106 audit-mariadb106 report-mariadb106 clean-mariadb106
	@echo "Full test cycle for MariaDB 10.6 completed."

# --- MariaDB 10.11 ---
build-mariadb1011:
	docker build -f $(MARIADB1011_DOCKERFILE) -t $(MARIADB1011_IMAGE) .

run-mariadb1011:
	docker run -d --name $(MARIADB1011_CONTAINER) $(MARIADB1011_IMAGE)
	@echo "Waiting for MariaDB 10.11 to initialize (30s)..."
	sleep 30

audit-mariadb1011:
	docker exec $(MARIADB1011_CONTAINER) python3 /datas/$(MARIADB1011_SCRIPT)

report-mariadb1011:
	docker cp $(MARIADB1011_CONTAINER):/datas/$(MARIADB1011_REPORT) .
	@echo "Report copied to $(MARIADB1011_REPORT)"

clean-mariadb1011:
	docker rm -f $(MARIADB1011_CONTAINER) || true

test-mariadb1011: clean-mariadb1011 build-mariadb1011 run-mariadb1011 audit-mariadb1011 report-mariadb1011 clean-mariadb1011
	@echo "Full test cycle for MariaDB 10.11 completed."

# --- MySQL Enterprise 8.0 ---
build-mysql80:
	docker build -f $(MYSQL80_DOCKERFILE) -t $(MYSQL80_IMAGE) .

run-mysql80:
	docker run -d --name $(MYSQL80_CONTAINER) $(MYSQL80_IMAGE)
	@echo "Waiting for MySQL Enterprise 8.0 to initialize (15s)..."
	sleep 15

audit-mysql80:
	docker exec $(MYSQL80_CONTAINER) python3 /datas/$(MYSQL80_SCRIPT)

report-mysql80:
	docker cp $(MYSQL80_CONTAINER):/datas/$(MYSQL80_REPORT) .
	@echo "Report copied to $(MYSQL80_REPORT)"

clean-mysql80:
	docker rm -f $(MYSQL80_CONTAINER) || true

test-mysql80: clean-mysql80 build-mysql80 run-mysql80 audit-mysql80 report-mysql80 clean-mysql80
	@echo "Full test cycle for MySQL Enterprise 8.0 completed."

# --- MySQL Community 8.4 ---
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

# --- MySQL Enterprise 8.4 ---
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

# --- MySQL Community 9.7 ---
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

# --- MySQL Enterprise 9.7 ---
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

# --- PostgreSQL 16 ---
build-postgresql16:
	docker build -f $(POSTGRESQL16_DOCKERFILE) -t $(POSTGRESQL16_IMAGE) .

run-postgresql16:
	docker run -d -e POSTGRES_PASSWORD=rootpass --name $(POSTGRESQL16_CONTAINER) $(POSTGRESQL16_IMAGE)
	@echo "Waiting for PostgreSQL 16 to initialize (15s)..."
	sleep 15

audit-postgresql16:
	docker exec $(POSTGRESQL16_CONTAINER) python3 /datas/$(POSTGRESQL16_SCRIPT)

report-postgresql16:
	docker cp $(POSTGRESQL16_CONTAINER):/datas/$(POSTGRESQL16_REPORT) .
	@echo "Report copied to $(POSTGRESQL16_REPORT)"

clean-postgresql16:
	docker rm -f $(POSTGRESQL16_CONTAINER) || true

test-postgresql16: clean-postgresql16 build-postgresql16 run-postgresql16 audit-postgresql16 report-postgresql16 clean-postgresql16
	@echo "Full test cycle for PostgreSQL 16 completed."

# --- PostgreSQL 17 ---
build-postgresql17:
	docker build -f $(POSTGRESQL17_DOCKERFILE) -t $(POSTGRESQL17_IMAGE) .

run-postgresql17:
	docker run -d -e POSTGRES_PASSWORD=rootpass --name $(POSTGRESQL17_CONTAINER) $(POSTGRESQL17_IMAGE)
	@echo "Waiting for PostgreSQL 17 to initialize (15s)..."
	sleep 15

audit-postgresql17:
	docker exec $(POSTGRESQL17_CONTAINER) python3 /datas/$(POSTGRESQL17_SCRIPT)

report-postgresql17:
	docker cp $(POSTGRESQL17_CONTAINER):/datas/$(POSTGRESQL17_REPORT) .
	@echo "Report copied to $(POSTGRESQL17_REPORT)"

clean-postgresql17:
	docker rm -f $(POSTGRESQL17_CONTAINER) || true

test-postgresql17: clean-postgresql17 build-postgresql17 run-postgresql17 audit-postgresql17 report-postgresql17 clean-postgresql17
	@echo "Full test cycle for PostgreSQL 17 completed."

# --- PostgreSQL 18 ---
build-postgresql18:
	docker build -f $(POSTGRESQL18_DOCKERFILE) -t $(POSTGRESQL18_IMAGE) .

run-postgresql18:
	docker run -d -e POSTGRES_PASSWORD=rootpass --name $(POSTGRESQL18_CONTAINER) $(POSTGRESQL18_IMAGE)
	@echo "Waiting for PostgreSQL 18 to initialize (15s)..."
	sleep 15

audit-postgresql18:
	docker exec $(POSTGRESQL18_CONTAINER) python3 /datas/$(POSTGRESQL18_SCRIPT)

report-postgresql18:
	docker cp $(POSTGRESQL18_CONTAINER):/datas/$(POSTGRESQL18_REPORT) .
	@echo "Report copied to $(POSTGRESQL18_REPORT)"

clean-postgresql18:
	docker rm -f $(POSTGRESQL18_CONTAINER) || true

test-postgresql18: clean-postgresql18 build-postgresql18 run-postgresql18 audit-postgresql18 report-postgresql18 clean-postgresql18
	@echo "Full test cycle for PostgreSQL 18 completed."

# --- MongoDB 7 ---
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

# --- MongoDB 8 ---
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

# --- Cassandra 4.0 ---
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

# --- Cassandra 4.1 ---
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

# --- Cassandra 5.0 ---
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
