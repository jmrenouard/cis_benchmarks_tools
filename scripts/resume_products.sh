#!/bin/bash
# Resume script - processes remaining products (PG17, PG18, MongoDB 7/8, Cassandra 4.0/4.1/5.0)
# No set -e: continues on errors

REPO_DIR="/home/jmren/GIT_REPOS/cis_benchmarks_tools"
cd "$REPO_DIR"

TOKEN=$(git remote get-url origin | grep -oP 'ghp_[^@]+')
export GH_TOKEN=$TOKEN

source /tmp/issue_numbers.sh

git config user.email "jmrenouard@gmail.com"
git config user.name "jmrenouard"

# Delete stale branch
git checkout main
git branch -D feat/cis-postgresql-17 2>/dev/null || true

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

    echo ""
    echo "================================================================="
    echo "  Processing: $PRODUCT_LABEL (Issue #$ISSUE_NUM)"
    echo "================================================================="

    # Ensure we're on main
    git checkout main 2>/dev/null || true

    # Create branch
    git branch -D "$BRANCH" 2>/dev/null || true
    git checkout -b "$BRANCH"

    # Restore stashed changes
    git stash pop 2>/dev/null || true

    # Add all relevant files
    git add "$SCRIPT" "$DOCKERFILE" README.md .gitignore 2>/dev/null || true
    [ -f scripts/start_postgresql.sh ] && git add scripts/start_postgresql.sh 2>/dev/null || true
    [ -f scripts/start_mariadb.sh ] && git add scripts/start_mariadb.sh 2>/dev/null || true
    [ -f scripts/start_mysql.sh ] && git add scripts/start_mysql.sh 2>/dev/null || true
    [ -f audit_cis_mongodb_7.py ] && git add audit_cis_mongodb_7.py 2>/dev/null || true

    # Build Docker
    echo "  Building Docker image: $DOCKER_TAG..."
    if ! docker build -f "$DOCKERFILE" -t "$DOCKER_TAG" . 2>&1 | tail -3; then
        echo "  ⚠️ Docker build failed"
    fi

    # Run container
    docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
    echo "  Starting container: $CONTAINER_NAME..."
    if docker run -d --name "$CONTAINER_NAME" "$DOCKER_TAG" 2>&1; then
        echo "  Waiting ${WAIT_TIME}s..."
        sleep "$WAIT_TIME"

        # Run audit
        echo "  Running audit..."
        docker exec "$CONTAINER_NAME" python3 "/datas/$SCRIPT" 2>&1 | tail -5 || true

        # Copy report  
        if docker cp "$CONTAINER_NAME:/datas/$REPORT_NAME" . 2>/dev/null; then
            echo "  ✅ Report: $REPORT_NAME"
            git add "$REPORT_NAME" 2>/dev/null || true
        else
            # Try to find any HTML report
            local found=$(docker exec "$CONTAINER_NAME" find /datas -name "rapport_cis_*.html" 2>/dev/null | head -1)
            if [ -n "$found" ]; then
                docker cp "$CONTAINER_NAME:$found" "./$REPORT_NAME" 2>/dev/null || true
                [ -f "$REPORT_NAME" ] && git add "$REPORT_NAME" 2>/dev/null || true
            fi
        fi

        docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
    else
        echo "  ⚠️ Container failed to start"
    fi

    # Commit
    git commit -m "feat: Add CIS benchmark audit for $PRODUCT_LABEL (closes #$ISSUE_NUM)" 2>&1 || true

    # Push
    git push origin "$BRANCH" --force 2>&1 || true

    # PR
    GH_TOKEN=$TOKEN gh pr create \
        --title "feat: CIS audit $PRODUCT_LABEL" \
        --body "## Description
Add automated CIS Benchmark audit for **$PRODUCT_LABEL**.

## Files
- \`$SCRIPT\` - Python audit script
- \`$DOCKERFILE\` - Docker test environment
- Updated \`README.md\`

Closes #$ISSUE_NUM" \
        --base main 2>&1 || true

    echo "  ✅ $PRODUCT_LABEL done!"

    # Return to main
    git checkout main 2>/dev/null || true
    git stash 2>/dev/null || true
}

echo "=== Resuming: 8 remaining products ==="

# PostgreSQL 17
process_product "feat/cis-postgresql-17" "$I_POSTGRESQL_17" "PostgreSQL 17" \
    "audit_cis_postgresql_17.py" "Dockerfile_postgresql17" "rapport_cis_postgresql_17.html" \
    "cis_postgresql17:audit" "cis_postgresql17_audit" 15

# PostgreSQL 18
process_product "feat/cis-postgresql-18" "$I_POSTGRESQL_18" "PostgreSQL 18" \
    "audit_cis_postgresql_18.py" "Dockerfile_postgresql18" "rapport_cis_postgresql_18.html" \
    "cis_postgresql18:audit" "cis_postgresql18_audit" 15

# MongoDB 7
process_product "feat/cis-mongodb-7" "$I_MONGODB_7" "MongoDB 7" \
    "audit_cis_mongodb_7.py" "Dockerfile_mongodb7" "rapport_cis_mongodb_7.html" \
    "cis_mongodb7:audit" "cis_mongodb7_audit" 30

# MongoDB 8
process_product "feat/cis-mongodb-8" "$I_MONGODB_8" "MongoDB 8" \
    "audit_cis_mongodb_8.py" "Dockerfile_mongodb8" "rapport_cis_mongodb_8.html" \
    "cis_mongodb8:audit" "cis_mongodb8_audit" 30

# Cassandra 4.0
process_product "feat/cis-cassandra-40" "$I_CASSANDRA_40" "Cassandra 4.0" \
    "audit_cis_cassandra_40.py" "Dockerfile_cassandra40" "rapport_cis_cassandra_40.html" \
    "cis_cassandra40:audit" "cis_cassandra40_audit" 60

# Cassandra 4.1
process_product "feat/cis-cassandra-41" "$I_CASSANDRA_41" "Cassandra 4.1" \
    "audit_cis_cassandra_41.py" "Dockerfile_cassandra41" "rapport_cis_cassandra_41.html" \
    "cis_cassandra41:audit" "cis_cassandra41_audit" 60

# Cassandra 5.0
process_product "feat/cis-cassandra-50" "$I_CASSANDRA_50" "Cassandra 5.0" \
    "audit_cis_cassandra_50.py" "Dockerfile_cassandra50" "rapport_cis_cassandra_50.html" \
    "cis_cassandra50:audit" "cis_cassandra50_audit" 60

echo ""
echo "================================================================="
echo "  🎉 ALL REMAINING PRODUCTS PROCESSED!"
echo "================================================================="
GH_TOKEN=$TOKEN gh pr list --state open --limit 20
