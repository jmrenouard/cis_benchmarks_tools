---
trigger: always_on
description: Core execution rules and constraints for the CIS Benchmark Tools project.
category: governance
---
# 03_execution_rules.md

## 🧠 Rationale
To ensure consistency, reliability, security, and smooth code review across all database auditing scripts. Strict adherence to these rules prevents broken tests, inconsistent naming, environment dependencies, and rejected Pull Requests.

## 🛠️ Implementation

### 1. Mandatory Testing
- Any new or modified `audit_cis_*.py` script MUST have a corresponding `Dockerfile_<db_name><version>` for local verification.
- Code must not be committed until the script has been successfully run inside its corresponding Docker container.

### 2. Naming Conventions
- Audit scripts: `audit_cis_<db_name>_<version>.py` (e.g., `audit_cis_mysql_80.py`).
- Dockerfiles: `Dockerfile_<db_name><version>` (e.g., `Dockerfile_mysql80`).
- Generated Reports: `rapport_cis_<db_name>_<version>.html`.

### 3. Self-Containment
- Each audit script MUST remain a single, standalone Python file. 
- Do not import custom local modules. It must be easy for a user to copy a single `.py` file to their target server and run it.
- Depend only on Python standard libraries.

### 4. Pull Request Size & Atomic Splitting
- Maximum PR diff size is strictly **15,000 characters** (`git diff main...HEAD | wc -c` < 15000).
- Large benchmark additions must be split into atomic, sub-15K-character Pull Requests to pass review bots (Sourcery AI limit) and human review.

## ✅ Verification
- Verify that `Dockerfile` exists for the modified script.
- Verify file names match the `<db_name>_<version>` pattern.
- Run `git diff main...HEAD | wc -c` to confirm PR diff size < 15,000 characters before submitting PR.