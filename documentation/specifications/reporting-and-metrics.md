---
title: Reporting & Compliance Metrics Specification
date: 2026-11-08
category: specification
---

# Reporting & Compliance Metrics Specification

## 1. 5-State Compliance Taxonomy
Every evaluated security control must resolve to exactly one of the five official compliance states:

1. **`Pass` (`PASS`, `SUCCÈS`)**: Automated check succeeded; target conforms to benchmark recommendation.
2. **`Fail` (`FAIL`, `ÉCHEC`)**: Automated check failed; target exhibits non-compliance. Actionable remediation is required.
3. **`Error` (`ERROR`, `ERREUR`)**: Execution error occurred (syntax error, command not found, permission denied, timeout). Stderr is captured and classified by `CommandFailureClassifier`.
4. **`Manual` (`MANUAL`, `MANUEL`)**: Check requires administrative inspection or context-specific policy evaluation.
5. **`Not Applicable` (`N/A`, `NA`)**: Feature, package, or daemon is not installed, disabled, or not relevant to the target profile.

## 2. Scoring Formulas
- **Attempted Automated Checks**:

$$
\text{Attempted} = \text{Pass} + \text{Fail} + \text{N/A}
$$

- **Overall Compliance Score (%)**:

$$
\text{Score} = \frac{\text{Pass} + \text{N/A}}{\text{Attempted}} \times 100 \quad (\text{or } 0.0\% \text{ if Attempted} = 0)
$$

- **Category Compliance Score (%)**:
  Calculated identically per category across all attempted controls.

## 3. 100% Offline Inline SVG Graphics (`PSL ONLY`)
- In compliance with `IMP-002`, **all chart visualizers are rendered using pure inline SVG generated directly in Python Standard Library**:
  - `build_inline_svg_donut_chart(p, f, e, na, score)`: Renders overall percentage donut chart.
  - `build_inline_svg_category_chart(categories_scores)`: Renders category breakdown bars.
- **Strict Prohibition**: External JavaScript CDNs (e.g., Chart.js, CDN D3) are prohibited. Reports must remain fully functional and visual on isolated air-gapped workstations without internet connectivity.

## 4. Multi-Format Output Support
Reports may be exported in four formats:
- **HTML (`.html`)**: Rich, interactive dashboard with inline SVG, category filters, and dark mode support.
- **JSON (`.json`)**: Machine-readable compliance payload including summary, category metrics, and raw check results.
- **JUnit XML (`.xml`)**: CI/CD integration format allowing test suites to track compliance regressions.
- **Plain Text (`.txt`)**: Terminal summary for headless pipelines.
