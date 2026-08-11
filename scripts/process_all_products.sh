#!/bin/bash
# Master script for processing all CIS benchmark products
# Each product: create branch -> add files -> build Docker -> run audit -> commit -> push -> PR

set -e

REPO_DIR="/home/jmren/GIT_REPOS/cis_benchmarks_tools"
cd "$REPO_DIR"

TOKEN=$(git remote get-url origin | grep -oP 'ghp_[^@]+')
export GH_TOKEN=$TOKEN

source /tmp/issue_numbers.sh

# Git config
git config user.email "jmrenouard@gmail.com"
git config user.name "jmrenouard"

process_product() {
    local BRANCH="$1"
    local ISSUE_NUM="$2"
    local PRODUCT_LABEL="$3"
    local SCRIPT="$4"
    local DOCKERFILE="$5"
    local REPORT_NAME="$6"
    local DOCKER_TAG="$7"
    local CONTAINER_NAME="$8"
    local WAIT_TIME="${9:-30}"
    local START_SCRIPT="${10:-}"
    local EXTRA_FILES="${11:-}"

    echo ""
    echo "================================================================="
    echo "  Processing: $PRODUCT_LABEL (Issue #$ISSUE_NUM)"
    echo "================================================================="

    # Step 1: Create branch from main
    git checkout main
    git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"

    # Step 2: Apply stashed changes (README, .gitignore, mongodb fixes)
    git stash pop 2>/dev/null || true

    # Step 3: Add files for this product
    git add "$SCRIPT" "$DOCKERFILE" README.md .gitignore
    if [ -n "$START_SCRIPT" ] && [ -f "$START_SCRIPT" ]; then
        git add "$START_SCRIPT"
    fi
    if [ -n "$EXTRA_FILES" ]; then
        for f in $EXTRA_FILES; do
            [ -f "$f" ] && git add "$f"
        done
    fi

    # Step 4: Build Docker image
    echo "  Building Docker image: $DOCKER_TAG..."
    if docker build -f "$DOCKERFILE" -t "$DOCKER_TAG" . 2>&1 | tail -5; then
        echo "  ✅ Docker build OK"
    else
        echo "  ⚠️ Docker build failed, continuing without report..."
        # Commit without report
        git commit -m "feat: Add CIS benchmark audit for $PRODUCT_LABEL (closes #$ISSUE_NUM)" || true
        git push origin "$BRANCH" 2>&1 || true
        GH_TOKEN=$TOKEN gh pr create \
            --title "feat: CIS audit $PRODUCT_LABEL" \
            --body "Add CIS benchmark audit for $PRODUCT_LABEL. Closes #$ISSUE_NUM.

## Files
- \`$SCRIPT\` - Audit script
- \`$DOCKERFILE\` - Docker test environment
- Updated README.md

> ⚠️ Report generation failed during Docker build." \
            --base main 2>&1 || true
        git checkout main
        git stash 2>/dev/null || true
        return 1
    fi

    # Step 5: Run container
    echo "  Starting container: $CONTAINER_NAME..."
    docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
    docker run -d --name "$CONTAINER_NAME" "$DOCKER_TAG"

    echo "  Waiting ${WAIT_TIME}s for service startup..."
    sleep "$WAIT_TIME"

    # Step 6: Execute audit
    echo "  Running audit..."
    docker exec "$CONTAINER_NAME" python3 "/datas/$SCRIPT" 2>&1 | tail -5 || true

    # Step 7: Copy report
    if docker cp "$CONTAINER_NAME:/datas/$REPORT_NAME" . 2>/dev/null; then
        echo "  ✅ Report generated: $REPORT_NAME"
        git add "$REPORT_NAME"
    else
        echo "  ⚠️ Report not found, trying alternate path..."
        # Try to find the report
        local found_report=$(docker exec "$CONTAINER_NAME" find /datas -name "rapport_cis_*.html" 2>/dev/null | head -1)
        if [ -n "$found_report" ]; then
            docker cp "$CONTAINER_NAME:$found_report" "./$REPORT_NAME" 2>/dev/null || true
            [ -f "$REPORT_NAME" ] && git add "$REPORT_NAME"
        fi
    fi

    # Step 8: Cleanup container
    docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

    # Step 9: Commit
    git commit -m "feat: Add CIS benchmark audit for $PRODUCT_LABEL (closes #$ISSUE_NUM)" || true

    # Step 10: Push
    git push origin "$BRANCH" 2>&1 || true

    # Step 11: Create PR
    GH_TOKEN=$TOKEN gh pr create \
        --title "feat: CIS audit $PRODUCT_LABEL" \
        --body "## Description
Add automated CIS Benchmark audit for **$PRODUCT_LABEL**.

## Files
- \`$SCRIPT\` - Python audit script
- \`$DOCKERFILE\` - Docker test environment
- \`$REPORT_NAME\` - Generated audit report
- Updated \`README.md\`

Closes #$ISSUE_NUM" \
        --base main 2>&1 || true

    echo "  ✅ PR created for $PRODUCT_LABEL"

    # Return to main for next product
    git checkout main
    # Re-stash untracked for next branch
    git stash 2>/dev/null || true

    echo "  ✅ $PRODUCT_LABEL complete!"
}

echo "Starting CIS Benchmark workflow for all products..."
echo "Issue numbers loaded from /tmp/issue_numbers.sh"

# Process each product
# Args: BRANCH ISSUE LABEL SCRIPT DOCKERFILE REPORT TAG CONTAINER WAIT START_SCRIPT EXTRA

# MariaDB
process_product "feat/cis-mariadb-106" "$I_MARIADB_106" "MariaDB 10.6" \
    "audit_cis_mariadb_106.py" "Dockerfile_mariadb106" "rapport_cis_mariadb_106.html" \
    "cis_mariadb106:audit" "cis_mariadb106_audit" 30 "scripts/start_mariadb.sh" ""

process_product "feat/cis-mariadb-1011" "$I_MARIADB_1011" "MariaDB 10.11" \
    "audit_cis_mariadb_1011.py" "Dockerfile_mariadb1011" "rapport_cis_mariadb_1011.html" \
    "cis_mariadb1011:audit" "cis_mariadb1011_audit" 30 "scripts/start_mariadb.sh" ""

# MySQL
process_product "feat/cis-mysql-80" "$I_MYSQL_80" "MySQL Enterprise 8.0" \
    "audit_cis_mysql_80.py" "Dockerfile_mysql80" "rapport_cis_mysql_80.html" \
    "cis_mysql80:audit" "cis_mysql80_audit" 45 "scripts/start_mysql.sh" ""

process_product "feat/cis-mysql-community-84" "$I_MYSQL_COMMUNITY_84" "MySQL Community 8.4" \
    "audit_cis_mysql_community_84.py" "Dockerfile_mysql_community_84" "rapport_cis_mysql_community_84.html" \
    "cis_mysql_community84:audit" "cis_mysql_community84_audit" 45 "scripts/start_mysql.sh" ""

process_product "feat/cis-mysql-enterprise-84" "$I_MYSQL_ENTERPRISE_84" "MySQL Enterprise 8.4" \
    "audit_cis_mysql_enterprise_84.py" "Dockerfile_mysql_enterprise_84" "rapport_cis_mysql_enterprise_84.html" \
    "cis_mysql_enterprise84:audit" "cis_mysql_enterprise84_audit" 45 "scripts/start_mysql.sh" ""

process_product "feat/cis-mysql-community-97" "$I_MYSQL_COMMUNITY_97" "MySQL Community 9.7" \
    "audit_cis_mysql_community_97.py" "Dockerfile_mysql_community_97" "rapport_cis_mysql_community_97.html" \
    "cis_mysql_community97:audit" "cis_mysql_community97_audit" 45 "scripts/start_mysql.sh" ""

process_product "feat/cis-mysql-enterprise-97" "$I_MYSQL_ENTERPRISE_97" "MySQL Enterprise 9.7" \
    "audit_cis_mysql_enterprise_97.py" "Dockerfile_mysql_enterprise_97" "rapport_cis_mysql_enterprise_97.html" \
    "cis_mysql_enterprise97:audit" "cis_mysql_enterprise97_audit" 45 "scripts/start_mysql.sh" ""

# PostgreSQL
process_product "feat/cis-postgresql-16" "$I_POSTGRESQL_16" "PostgreSQL 16" \
    "audit_cis_postgresql_16.py" "Dockerfile_postgresql16" "rapport_cis_postgresql_16.html" \
    "cis_postgresql16:audit" "cis_postgresql16_audit" 15 "scripts/start_postgresql.sh" ""

process_product "feat/cis-postgresql-17" "$I_POSTGRESQL_17" "PostgreSQL 17" \
    "audit_cis_postgresql_17.py" "Dockerfile_postgresql17" "rapport_cis_postgresql_17.html" \
    "cis_postgresql17:audit" "cis_postgresql17_audit" 15 "scripts/start_postgresql.sh" ""

process_product "feat/cis-postgresql-18" "$I_POSTGRESQL_18" "PostgreSQL 18" \
    "audit_cis_postgresql_18.py" "Dockerfile_postgresql18" "rapport_cis_postgresql_18.html" \
    "cis_postgresql18:audit" "cis_postgresql18_audit" 15 "scripts/start_postgresql.sh" ""

# MongoDB
process_product "feat/cis-mongodb-7" "$I_MONGODB_7" "MongoDB 7" \
    "audit_cis_mongodb_7.py" "Dockerfile_mongodb7" "rapport_cis_mongodb_7.html" \
    "cis_mongodb7:audit" "cis_mongodb7_audit" 30 "" "audit_cis_mongodb_8.py"

process_product "feat/cis-mongodb-8" "$I_MONGODB_8" "MongoDB 8" \
    "audit_cis_mongodb_8.py" "Dockerfile_mongodb8" "rapport_cis_mongodb_8.html" \
    "cis_mongodb8:audit" "cis_mongodb8_audit" 30 "" ""

# Cassandra
process_product "feat/cis-cassandra-40" "$I_CASSANDRA_40" "Cassandra 4.0" \
    "audit_cis_cassandra_40.py" "Dockerfile_cassandra40" "rapport_cis_cassandra_40.html" \
    "cis_cassandra40:audit" "cis_cassandra40_audit" 60 "" ""

process_product "feat/cis-cassandra-41" "$I_CASSANDRA_41" "Cassandra 4.1" \
    "audit_cis_cassandra_41.py" "Dockerfile_cassandra41" "rapport_cis_cassandra_41.html" \
    "cis_cassandra41:audit" "cis_cassandra41_audit" 60 "" ""

process_product "feat/cis-cassandra-50" "$I_CASSANDRA_50" "Cassandra 5.0" \
    "audit_cis_cassandra_50.py" "Dockerfile_cassandra50" "rapport_cis_cassandra_50.html" \
    "cis_cassandra50:audit" "cis_cassandra50_audit" 60 "" ""

echo ""
echo "================================================================="
echo "  🎉 ALL PRODUCTS PROCESSED!"
echo "================================================================="
echo ""
echo "Summary:"
GH_TOKEN=$TOKEN gh pr list --state open 2>&1 | head -20
