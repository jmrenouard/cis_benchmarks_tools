---
trigger: explicit_call
description: Workflow for adding a new CIS benchmark for a new database or version.
category: workflow
---
# Add Benchmark Workflow

## 🧠 Rationale
Standardize the process of integrating a new CIS Benchmark into the toolset to ensure consistency in data structure and testing.

## 🛠️ Implementation
When a user requests to add a new benchmark (e.g., "Add CIS for Redis 6"):

1. **Extract Data**: Obtain the CIS recommendations for the target database/version.
2. **Create Python Script**: 
   - Copy an existing template (e.g., `audit_cis_mysql_80.py`).
   - Rename to `audit_cis_<db_name>_<version>.py`.
   - Update the `RECOMMENDATIONS_DATA` array with the new benchmark checks.
3. **Write Test Procedures**: Define the `test_procedure` (bash commands) for each automated check.
4. **Create Dockerfile**: Create `Dockerfile_<db_name><version>` that sets up the database environment.
5. **Run Tests**: Execute the `.agent/workflows/test-benchmark.md` workflow to validate the new script against the Docker container.

## ✅ Verification
- Script parses without syntax errors.
- `RECOMMENDATIONS_DATA` covers the desired scope.
- Docker image builds successfully.