---
trigger: explicit_call
description: Workflow for building the docker image, running the container, and executing the audit script.
category: workflow
---
# Test Benchmark Workflow

## 🧠 Rationale
Provide a repeatable, isolated environment for testing audit scripts to ensure they work on clean installations of the target database.

## 🛠️ Implementation
To test `audit_cis_<db_name>_<version>.py`:

1. **Build Image**: 
   ```bash
   docker build -f Dockerfile_<db_name><version> -t <db_name><version>-audit .
   ```
2. **Run Container**:
   ```bash
   docker run -d --name <db_name><version>-test <db_name><version>-audit
   ```
3. **Wait for DB**: Ensure the database service has started inside the container.
4. **Execute Audit**:
   ```bash
   docker exec -it <db_name><version>-test python3 /datas/audit_cis_<db_name>_<version>.py
   ```
5. **Review Output**: Check the console output and the generated `rapport_cis_<db_name>_<version>.html` (can be extracted via `docker cp`).
6. **Cleanup**:
   ```bash
   docker rm -f <db_name><version>-test
   ```

## ✅ Verification
- No unexpected Python exceptions during execution.
- HTML report is generated.
- The proportion of "Error" status checks is minimized.