#!/bin/bash
# Pre-Commit Routine Wrapper Script
# Delegates all code concatenation, syntax compilation, and PSL compliance checks to Python Standard Library.

set -e

exec python3 "$(dirname "$0")/pre_commit_checks.py" "$@"
