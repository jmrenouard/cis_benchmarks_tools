#!/usr/bin/env python3
"""
E2E Audit Reports Analysis Engine (Python PSL ONLY).
Parses all .txt report files in reports/ (both Local & SSH Remote Mode),
computes global compliance statistics, extracts FAIL, ERROR, and MANUAL controls,
and generates separate analysis reports for Local Mode and SSH Remote Mode:
  - reports/analyse_tests_e2e_local.md
  - reports/analyse_tests_e2e_ssh.md
  - reports/analyse_tests_e2e.md (Unified Comparison Dashboard)
"""

import glob
import os
import re
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")

def get_current_version():
    vfile = os.path.join(REPO_ROOT, "VERSION")
    if os.path.exists(vfile):
        with open(vfile, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "v2.6.0"


def parse_txt_report(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    filename = os.path.basename(filepath)
    is_ssh = "_SSH" in filename.upper()
    target_name = filename.replace("rapport_cis_", "").replace("_ssh", "").replace(".txt", "").upper()

    target_match = re.search(r"AUDIT REPORT -\s*(.+)", content)
    if target_match:
        target_name = target_match.group(1).strip()

    score_match = re.search(r"Global Score\s*:\s*([\d\.]+)%", content)
    score = float(score_match.group(1)) if score_match else 0.0

    date_match = re.search(r"Report Date\s*:\s*(.+)", content)
    report_date = date_match.group(1).strip() if date_match else "N/A"

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
        "is_ssh": is_ssh,
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


def generate_single_mode_markdown(mode_title, mode_badge_str, targets_data):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_targets = len(targets_data)
    total_checks = sum(t["total"] for t in targets_data)
    total_pass = sum(t["pass"] for t in targets_data)
    total_fail = sum(t["fail"] for t in targets_data)
    total_manual = sum(t["manual"] for t in targets_data)
    total_error = sum(t["error"] for t in targets_data)
    avg_score = (sum(t["score"] for t in targets_data) / total_targets) if total_targets > 0 else 0.0

    lines = []
    lines.append(f"# 📊 CIS Benchmarks Suite - Analyse Spécifique {mode_title}")
    lines.append("")
    lines.append(f"> **Rapport d'Analyse E2E ({mode_title}) généré le** : `{now_str}`  ")
    lines.append(f"> **Moteur d'Audit** : `CIS Benchmarks Tools Suite v{get_current_version().lstrip('v')}` (100% Python Standard Library - PSL ONLY)  ")
    lines.append(f"> **Mode d'Exécution** : {mode_badge_str}  ")
    lines.append(f"> **Périmètre** : {total_targets} cibles d'audit évaluées dans ce mode")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append(f"## 📈 Executive Dashboard ({mode_title})")
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

        lines.append(f"| **{t['target']}** | {mode_badge_str} | {t['date']} | {score_status} | {t['total']} | {t['pass']} | {t['fail']} | {t['error']} | {t['manual']} |")

    lines.append("")
    lines.append("### 📊 Statistiques Consolidées pour ce Mode")
    lines.append("")
    lines.append(f"- **Nombre total de benchmarks évalués** : `{total_targets}`")
    lines.append(f"- **Nombre total de règles/contrôles vérifiés** : `{total_checks}`")
    lines.append(f"- **Score de conformité moyen** : `{avg_score:.1f}%`")
    lines.append(f"- **Contrôles en succès (`PASS`)** : `{total_pass}` ({ (total_pass/total_checks*100) if total_checks else 0:.1f}%)")
    lines.append(f"- **Contrôles en échec (`FAIL`)** : `{total_fail}` ({ (total_fail/total_checks*100) if total_checks else 0:.1f}%)")
    lines.append(f"- **Contrôles en erreur (`ERROR`)** : `{total_error}` ({ (total_error/total_checks*100) if total_checks else 0:.1f}%)")
    lines.append(f"- **Contrôles manuels (`MANUAL`)** : `{total_manual}` ({ (total_manual/total_checks*100) if total_checks else 0:.1f}%)")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append(f"## ❌ Registre Détaillé des Contrôles en Échec (`FAIL`) & Erreurs (`ERROR`) - {mode_title}")
    lines.append("")

    for t in sorted(targets_data, key=lambda x: x["target"]):
        failing = [c for c in t["controls"] if c["status"] in ["FAIL", "ERROR"]]
        if not failing:
            continue

        lines.append(f"### 🛑 {t['target']} (`{len(failing)}` échecs / erreurs)")
        lines.append("")
        lines.append("| ID Règle | Statut | Nom du Contrôle | Catégorie | Extrait Résultat / Message d'Erreur | Procédure de Remédiation |")
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

    lines.append(f"## ⚠️ Registre Détaillé des Contrôles Manuels (`MANUAL`) - {mode_title}")
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

    return "\n".join(lines)


def generate_unified_comparison_markdown(local_targets, ssh_targets):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append("# 📊 CIS Benchmarks Suite - Tableau Comparatif (Mode Local vs SSH Remote)")
    lines.append("")
    lines.append(f"> **Dernière mise à jour** : `{now_str}`  ")
    lines.append(f"> **Moteur d'Audit** : `CIS Benchmarks Tools Suite v{get_current_version().lstrip('v')}` (100% Python Standard Library - PSL ONLY)  ")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## 🔄 Matrice de Comparaison des Scores (Mode Local vs Mode SSH Remote)")
    lines.append("")
    lines.append("| Cible / Benchmark | Score Mode Local | Score Mode SSH | Écart de Score | Statut Parité | Rapport Local | Rapport SSH |")
    lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")

    ssh_map = {t["target"]: t for t in ssh_targets}
    local_map = {t["target"]: t for t in local_targets}

    all_target_names = sorted(list(set(local_map.keys()).union(set(ssh_map.keys()))))

    for name in all_target_names:
        loc = local_map.get(name)
        ssh = ssh_map.get(name)

        loc_score_str = f"`{loc['score']:.1f}%`" if loc else "N/A"
        ssh_score_str = f"`{ssh['score']:.1f}%`" if ssh else "N/A"

        if loc and ssh:
            diff = abs(loc["score"] - ssh["score"])
            diff_str = f"`{diff:.1f}%`"
            parity_str = "🟢 `Parité Parfaite`" if diff < 0.01 else "⚠️ `Écart Détecté`"
        else:
            diff_str = "N/A"
            parity_str = "⚪ `Mode Incomplet`"

        loc_link = f"[rapport_cis_{name.lower()}.txt](file://{loc['filename']})" if loc else "N/A"
        ssh_link = f"[rapport_cis_{name.lower()}_ssh.txt](file://{ssh['filename']})" if ssh else "N/A"

        lines.append(f"| **{name}** | {loc_score_str} | {ssh_score_str} | {diff_str} | {parity_str} | [Local MD](file:///home/jmren/GIT_REPOS/cis_benchmarks_tools/reports/analyse_tests_e2e_local.md) | [SSH MD](file:///home/jmren/GIT_REPOS/cis_benchmarks_tools/reports/analyse_tests_e2e_ssh.md) |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📂 Rapports d'Analyse Séparés")
    lines.append("")
    lines.append("- 💻 **Analyse Complète Mode Local** : [reports/analyse_tests_e2e_local.md](file:///home/jmren/GIT_REPOS/cis_benchmarks_tools/reports/analyse_tests_e2e_local.md)")
    lines.append("- 🌐 **Analyse Complète Mode SSH Remote** : [reports/analyse_tests_e2e_ssh.md](file:///home/jmren/GIT_REPOS/cis_benchmarks_tools/reports/analyse_tests_e2e_ssh.md)")
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
        except Exception as e:
            print(f"  ❌ Error parsing {fpath}: {e}")

    local_targets = [t for t in targets_data if not t["is_ssh"]]
    ssh_targets = [t for t in targets_data if t["is_ssh"]]

    # 1. Generate Local Analysis Report
    local_md = generate_single_mode_markdown("Mode Local (-m local)", "💻 `Local`", local_targets)
    local_path = os.path.join(REPORTS_DIR, "analyse_tests_e2e_local.md")
    with open(local_path, "w", encoding="utf-8") as f:
        f.write(local_md)
    print(f"  ✓ Local Mode Analysis Report generated: {local_path}")

    # 2. Generate SSH Remote Analysis Report
    ssh_md = generate_single_mode_markdown("Mode SSH Remote (-m ssh)", "🌐 `SSH Remote`", ssh_targets)
    ssh_path = os.path.join(REPORTS_DIR, "analyse_tests_e2e_ssh.md")
    with open(ssh_path, "w", encoding="utf-8") as f:
        f.write(ssh_md)
    print(f"  ✓ SSH Remote Mode Analysis Report generated: {ssh_path}")

    # 3. Generate Unified Comparison Dashboard
    unified_md = generate_unified_comparison_markdown(local_targets, ssh_targets)
    unified_path = os.path.join(REPORTS_DIR, "analyse_tests_e2e.md")
    with open(unified_path, "w", encoding="utf-8") as f:
        f.write(unified_md)
    print(f"  ✓ Unified Comparison Dashboard generated: {unified_path}")

    print("\n🎉 All 3 E2E Analysis Reports successfully generated!")


if __name__ == "__main__":
    main()
