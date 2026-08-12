#!/usr/bin/env python3
"""
E2E Audit Reports Analysis Engine (Python PSL ONLY).
Parses all .txt report files in reports/, computes global compliance statistics,
extracts FAIL, ERROR, and MANUAL controls, and generates reports/analyse_tests_e2e.md.
"""

import glob
import os
import re
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")
OUTPUT_MD = os.path.join(REPORTS_DIR, "analyse_tests_e2e.md")


def parse_txt_report(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    filename = os.path.basename(filepath)
    target_name = filename.replace("rapport_cis_", "").replace(".txt", "").upper()

    # Match header info
    target_match = re.search(r"AUDIT REPORT -\s*(.+)", content)
    if target_match:
        target_name = target_match.group(1).strip()

    score_match = re.search(r"Global Score\s*:\s*([\d\.]+)%", content)
    score = float(score_match.group(1)) if score_match else 0.0

    date_match = re.search(r"Report Date\s*:\s*(.+)", content)
    report_date = date_match.group(1).strip() if date_match else "N/A"

    # Parse individual controls
    # Pattern matches lines starting with [PASS], [FAIL], [MANUAL], [ERROR], [N/A]
    controls = []
    blocks = re.split(r"-{50,}", content)

    for block in blocks:
        block = block.strip()
        status_match = re.search(r"^\[(PASS|FAIL|MANUAL|ERROR|N/A)\]\s+([\d\.\-]+)\s+-\s+(.+)", block, re.MULTILINE)
        if not status_match:
            continue

        status = status_match.group(1)
        ctrl_id = status_match.group(2)
        ctrl_name = status_match.group(3)

        cat_match = re.search(r"Category:\s*(.+)", block)
        category = cat_match.group(1).strip() if cat_match else "General"

        out_match = re.search(r"Output:\s*(.*?)(?=\n\s*Remediation:|\Z)", block, re.DOTALL)
        output = out_match.group(1).strip() if out_match else ""

        rem_match = re.search(r"Remediation:\s*(.*)", block, re.DOTALL)
        remediation = rem_match.group(1).strip() if rem_match else "N/A"

        controls.append({
            "status": status,
            "id": ctrl_id,
            "name": ctrl_name,
            "category": category,
            "output": output,
            "remediation": remediation
        })

    pass_cnt = sum(1 for c in controls if c["status"] == "PASS")
    fail_cnt = sum(1 for c in controls if c["status"] == "FAIL")
    manual_cnt = sum(1 for c in controls if c["status"] == "MANUAL")
    error_cnt = sum(1 for c in controls if c["status"] == "ERROR")
    na_cnt = sum(1 for c in controls if c["status"] == "N/A")

    return {
        "filename": filename,
        "target": target_name,
        "date": report_date,
        "score": score,
        "total": len(controls),
        "pass": pass_cnt,
        "fail": fail_cnt,
        "manual": manual_cnt,
        "error": error_cnt,
        "na": na_cnt,
        "controls": controls
    }


def generate_analysis_markdown(targets_data):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_targets = len(targets_data)
    total_checks = sum(t["total"] for t in targets_data)
    total_pass = sum(t["pass"] for t in targets_data)
    total_fail = sum(t["fail"] for t in targets_data)
    total_manual = sum(t["manual"] for t in targets_data)
    total_error = sum(t["error"] for t in targets_data)
    avg_score = (sum(t["score"] for t in targets_data) / total_targets) if total_targets > 0 else 0.0

    lines = []
    lines.append("# 📊 CIS Benchmarks Suite - E2E Execution Audit & Compliance Analysis")
    lines.append("")
    lines.append(f"> **Rapport d'Analyse des Tests E2E généré le** : `{now_str}`  ")
    lines.append(f"> **Moteur d'Audit** : `CIS Benchmarks Tools Suite v2.0.0` (100% Python Standard Library - PSL ONLY)  ")
    lines.append(f"> **Périmètre** : {total_targets} cibles d'audit évaluées (Bases de données & Systèmes Linux RHEL)")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## 📈 Executive Dashboard (Synthèse Globale par Cible)")
    lines.append("")
    lines.append("| Cible / Benchmark | Mode | Date d'Exécution | Score Global | Total | Succès (PASS) | Échecs (FAIL) | Erreurs (ERROR) | Manuels (MANUAL) |")
    lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")

    for t in sorted(targets_data, key=lambda x: x["target"]):
        score_badge = f"`{t['score']:.1f}%`"
        if t["score"] >= 80:
            score_status = f"🟢 {score_badge}"
        elif t["score"] >= 50:
            score_status = f"🟡 {score_badge}"
        else:
            score_status = f"🔴 {score_badge}"

        mode_badge = "`SSH`" if "_SSH" in t["filename"].upper() else "`Local`"
        lines.append(f"| **{t['target']}** | {mode_badge} | {t['date']} | {score_status} | {t['total']} | {t['pass']} | {t['fail']} | {t['error']} | {t['manual']} |")

    lines.append("")
    lines.append("### 📊 Statistiques Consolidées sur l'Ensemble de la Suite")
    lines.append("")
    lines.append(f"- **Nombre total de benchmarks évalués** : `{total_targets}`")
    lines.append(f"- **Nombre total de règles/contrôles vérifiés** : `{total_checks}`")
    lines.append(f"- **Score de conformité moyen** : `{avg_score:.1f}%`")
    lines.append(f"- **Contrôles en succès (`PASS`)** : `{total_pass}` ({ (total_pass/total_checks*100) if total_checks else 0:.1f}%)")
    lines.append(f"- **Contrôles en échec (`FAIL`)** : `{total_fail}` ({ (total_fail/total_checks*100) if total_checks else 0:.1f}%)")
    lines.append(f"- **Contrôles en erreur d'exécution (`ERROR`)** : `{total_error}` ({ (total_error/total_checks*100) if total_checks else 0:.1f}%)")
    lines.append(f"- **Contrôles à vérification manuelle (`MANUAL`)** : `{total_manual}` ({ (total_manual/total_checks*100) if total_checks else 0:.1f}%)")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## ❌ Registre Détaillé des Contrôles en Échec (`FAIL`) & Erreurs (`ERROR`)")
    lines.append("")
    lines.append("Ce registre liste l'ensemble des règles ayant échoué lors de l'exécution automatique, classées par cible d'audit avec leurs explications et procédures de remédiation.")
    lines.append("")

    for t in sorted(targets_data, key=lambda x: x["target"]):
        failing = [c for c in t["controls"] if c["status"] in ["FAIL", "ERROR"]]
        if not failing:
            continue

        lines.append(f"### 🛑 {t['target']} (`{len(failing)}` échecs / erreurs)")
        lines.append("")
        lines.append("| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation Suggérée |")
        lines.append("| :---: | :---: | :--- | :--- | :--- | :--- |")

        for c in failing:
            status_str = "🔴 FAIL" if c["status"] == "FAIL" else "⚠️ ERROR"
            clean_name = c["name"].replace("|", "\\|")
            clean_cat = c["category"].replace("|", "\\|")
            out_snippet = c["output"].split("\n")[0][:80].replace("|", "\\|") if c["output"] else "Aucune sortie"
            rem_snippet = c["remediation"].split("\n")[0][:100].replace("|", "\\|") if c["remediation"] else "N/A"
            lines.append(f"| **{c['id']}** | {status_str} | {clean_name} | {clean_cat} | `{out_snippet}` | {rem_snippet} |")

        lines.append("")

    lines.append("---")
    lines.append("")

    lines.append("## ⚠️ Registre Détaillé des Contrôles Manuels (`MANUAL`)")
    lines.append("")
    lines.append("Ce registre recense les contrôles nécessitant une vérification manuelle par un auditeur de sécurité ou un administrateur système.")
    lines.append("")

    for t in sorted(targets_data, key=lambda x: x["target"]):
        manuals = [c for c in t["controls"] if c["status"] == "MANUAL"]
        if not manuals:
            continue

        lines.append(f"### 📋 {t['target']} (`{len(manuals)}` contrôles manuels)")
        lines.append("")
        lines.append("| ID Règle | Nom du Contrôle | Catégorie | Note de Vérification |")
        lines.append("| :---: | :--- | :--- | :--- |")

        for c in manuals:
            clean_name = c["name"].replace("|", "\\|")
            clean_cat = c["category"].replace("|", "\\|")
            lines.append(f"| **{c['id']}** | {clean_name} | {clean_cat} | Vérification visuelle / politique organisationnelle requise |")

        lines.append("")

    lines.append("---")
    lines.append("")

    lines.append("## 💡 Recommandations et Plan d'Action pour la Conformité")
    lines.append("")
    lines.append("1. **Remédiation Prioritaire des Échecs (`FAIL`)** :")
    lines.append("   - Appliquer en priorité les scripts de remédiation fournis dans les tables d'échecs ci-dessus pour corriger les paramètres système et de base de données non conformes.")
    lines.append("2. **Traiter les Erreurs d'Exécution (`ERROR`)** :")
    lines.append("   - S'assurer que les utilitaires système nécessaires (ex: `systemctl`, sockets de connexion BDD) sont disponibles et accessibles.")
    lines.append("3. **Automatisation Continue (Phase 8)** :")
    lines.append("   - Poursuivre la conversion des règles `MANUAL` vers des règles `Automated` en étendant les procédures de vérification SQL et commandes système.")
    lines.append("")

    return "\n".join(lines)


def main():
    txt_files = sorted(glob.glob(os.path.join(REPORTS_DIR, "*.txt")))
    print(f"Analyzing {len(txt_files)} text audit report files in reports/...")

    targets_data = []
    for fpath in txt_files:
        try:
            data = parse_txt_report(fpath)
            if data["total"] > 0:
                targets_data.append(data)
                print(f"  ✓ Parsed {data['filename']}: {data['target']} (Score: {data['score']}%, Controls: {data['total']})")
        except Exception as e:
            print(f"  ❌ Error parsing {fpath}: {e}")

    md_content = generate_analysis_markdown(targets_data)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"\n🎉 E2E Analysis Report successfully generated at: {OUTPUT_MD}")


if __name__ == "__main__":
    main()
