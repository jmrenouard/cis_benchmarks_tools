# 🛠️ CIS Benchmarks Tools - Resolved Debt & Technical Backlog (v1.7.0)

This document tracks technical debt, security considerations, and resolved architectural backlog items.

---

## 🔒 Resolved Architectural Backlog

### 1. Externalization of Audit Rules into `rules/` Directory (Resolved in v1.7.0 ✅)
- **Problem**: Audit rule control specifications (`RECOMMENDATIONS_DATA`) were hardcoded inside Python script source files, mixing code logic with data specs.
- **Resolution**: Created top-level `rules/` directory containing 18 clean JSON specification files (`rules/mariadb_106.json`, `rules/cassandra_40.json`, `rules/rhel_8.json`, etc.). Created dynamic rule loader `load_recommendations()` in `audit_cis_*.py` and `audit_cis.py` with inline fallback.

### 2. Chart.js CDN Dependency & Missing Offline Charts (Resolved in v1.7.0 ✅)
- **Problem**: HTML audit reports depended on CDN-hosted Chart.js (`https://cdn.jsdelivr.net/npm/chart.js`), causing blank chart canvases when opened offline or behind firewalls.
- **Resolution**: Designed a 100% self-contained Inline SVG & HTML5 Donut and Stacked Bar Chart engine built in Python PSL (`build_inline_svg_donut_chart()` and `build_inline_svg_category_chart()`). Zero external JavaScript required. Works 100% offline.

### 3. Local & SSH Remote Execution Modes (Resolved in v1.6.0 ✅)
- **Problem**: Inability to select Local vs SSH execution mode explicitly across all benchmarks.
- **Resolution**: Standardized `-m / --mode {local,ssh}`, `-r / --remote / --ssh user@host`, and `--local` CLI options across all 18 audit scripts and `audit_cis.py`.

---

## 📝 Active Quality Controls
- **PSL Compliance**: AST pre-commit checks block non-PSL imports.
- **Unit Tests**: 100% passing PSL `unittest` suite (`tests/test_evaluate_condition.py`).
- **Pre-Commit Checks**: 8-step quality checker (`make pre-commit`).
