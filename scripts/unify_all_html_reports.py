#!/usr/bin/env python3
"""
Unify HTML report templates and generators across ALL 18 audit scripts (PSL ONLY).
Upgrades RHEL 8, RHEL 9, and RHEL 10 to use the exact same modern Tailwind CSS + Inline PSL SVG engine
with Dark Mode, Status Filter Buttons, Executive Summary Cards, and detailed Remediation / Test Command blocks.
"""

import glob
import os
import re

rhel_files = ["audit_cis_rhel_8.py", "audit_cis_rhel_9.py", "audit_cis_rhel_10.py"]
print(f"Unifying HTML report rendering for RHEL scripts: {rhel_files}...")

rhel_template_loader = '''
def load_html_template():
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "report_template.html")
    if os.path.exists(template_path):
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return """<!DOCTYPE html>
<html lang="{lang}" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CIS Benchmark Audit Report - {benchmark_title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body { font-family: 'Inter', sans-serif; transition: background-color 0.3s, color 0.3s; }
        .status-pass { background-color: #DEF7EC; color: #03543F; }
        .status-fail { background-color: #FDE8E8; color: #9B1C1C; }
        .status-manual { background-color: #FEF3C7; color: #92400E; }
        .status-error { background-color: #F3F4F6; color: #1F2937; }
        .status-na { background-color: #E5E7EB; color: #4B5563; }
        pre { white-space: pre-wrap; word-wrap: break-word; font-size: 0.75rem; }
        body.dark-mode { background-color: #0f172a; color: #f8fafc; }
        body.dark-mode aside, body.dark-mode header, body.dark-mode footer, body.dark-mode .bg-white { background-color: #1e293b !important; color: #f8fafc !important; border-color: #334155 !important; }
        body.dark-mode .text-gray-900, body.dark-mode .text-gray-800 { color: #f8fafc !important; }
        body.dark-mode .text-gray-700, body.dark-mode .text-gray-600 { color: #cbd5e1 !important; }
        body.dark-mode .text-gray-500, body.dark-mode .text-gray-400 { color: #94a3b8 !important; }
        body.dark-mode .bg-gray-50, body.dark-mode .bg-gray-100 { background-color: #0f172a !important; }
    </style>
</head>
<body class="bg-gray-50 flex">
    <aside class="w-64 h-screen bg-white border-r border-gray-200 sticky top-0 overflow-y-auto hidden lg:block">
        <div class="p-6">
            <h2 class="text-xl font-bold text-blue-600 flex items-center gap-2"><i class="fas fa-shield-halved"></i>{benchmark_title}</h2>
            <p class="text-xs text-gray-500 mt-1">Audit Security Report v2.1.0</p>
        </div>
        <nav class="px-4 pb-6">
            <a href="#summary" class="flex items-center p-3 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors mb-1 font-medium">
                <i class="fas fa-chart-pie w-5 mr-3 text-blue-500"></i> Synthèse & Métriques
            </a>
            <div class="mt-4 mb-2 text-xs font-semibold text-gray-400 uppercase px-3">Catégories</div>
            {sidebar_links}
        </nav>
    </aside>
    <main class="flex-1 min-w-0">
        <header class="bg-white border-b border-gray-200 p-6 flex justify-between items-center">
            <div>
                <h1 class="text-2xl font-bold text-gray-900">Benchmark CIS {benchmark_title}</h1>
                <p class="text-sm text-gray-500">Date du rapport: {report_date}</p>
            </div>
            <div class="flex items-center space-x-3">
                <button id="themeToggle" onclick="toggleDarkMode()" class="px-3 py-1.5 bg-gray-100 border border-gray-300 text-gray-700 rounded-lg text-xs font-semibold hover:bg-gray-200 transition-colors flex items-center gap-1.5">
                    <i class="fas fa-moon"></i> Mode Sombre
                </button>
                <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">{target_version}</span>
                <span class="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-xs font-medium border border-gray-200">v{suite_version}</span>
            </div>
        </header>
        <div class="p-8 max-w-7xl mx-auto">
            <section id="summary" class="mb-12">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col items-center">
                        <span class="text-sm font-medium text-gray-500 uppercase tracking-wider mb-2">Score Global</span>
                        <div class="relative flex items-center justify-center">
                            <span class="text-3xl font-black text-gray-900">{overall_score:.1f}%</span>
                        </div>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 border-l-4 border-l-green-500">
                        <span class="text-xs font-bold text-green-600 uppercase tracking-widest">Succès</span>
                        <div class="text-3xl font-bold text-gray-900 mt-1">{passed_automated_count}</div>
                        <p class="text-xs text-gray-500 mt-1">Vérifications conformes</p>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 border-l-4 border-l-red-500">
                        <span class="text-xs font-bold text-red-600 uppercase tracking-widest">Échecs</span>
                        <div class="text-3xl font-bold text-gray-900 mt-1">{failed_automated_count}</div>
                        <p class="text-xs text-gray-500 mt-1">Non-conformités détectées</p>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 border-l-4 border-l-amber-500">
                        <span class="text-xs font-bold text-amber-600 uppercase tracking-widest">Manuels</span>
                        <div class="text-3xl font-bold text-gray-900 mt-1">{manual_checks}</div>
                        <p class="text-xs text-gray-500 mt-1">À vérifier manuellement</p>
                    </div>
                </div>
                {donut_svg}
                {bar_svg}
            </section>
            <section id="details">
                <div class="flex items-center justify-between mb-6">
                    <h2 class="text-xl font-bold text-gray-900">Détails des Contrôles d'Audit</h2>
                    <div class="flex gap-2">
                        <button onclick="filterStatus('all')" class="px-3 py-1.5 bg-blue-600 text-white rounded-lg text-xs font-semibold hover:bg-blue-700 transition-colors">Tous</button>
                        <button onclick="filterStatus('PASS')" class="px-3 py-1.5 bg-green-100 text-green-800 rounded-lg text-xs font-semibold hover:bg-green-200 transition-colors">Succès</button>
                        <button onclick="filterStatus('FAIL')" class="px-3 py-1.5 bg-red-100 text-red-800 rounded-lg text-xs font-semibold hover:bg-red-200 transition-colors">Échecs</button>
                        <button onclick="filterStatus('MANUAL')" class="px-3 py-1.5 bg-amber-100 text-amber-800 rounded-lg text-xs font-semibold hover:bg-amber-200 transition-colors">Manuels</button>
                        <button onclick="filterStatus('ERROR')" class="px-3 py-1.5 bg-gray-100 text-gray-800 rounded-lg text-xs font-semibold hover:bg-gray-200 transition-colors">Erreurs</button>
                    </div>
                </div>
                {categories_reports}
            </section>
        </div>
    </main>
    <script>
        function toggleDarkMode() { document.body.classList.toggle('dark-mode'); }
        function filterStatus(status) {
            document.querySelectorAll('tr[data-status]').forEach(row => {
                if (status === 'all' || row.getAttribute('data-status') === status) { row.style.display = ''; }
                else { row.style.display = 'none'; }
            });
        }
    </script>
</body>
</html>"""
'''

rhel_generate_html = '''
def generate_html_report(results, overall_score, categories_scores, filename=None, lang="en"):
    """Generate modern unified responsive HTML audit report for RHEL."""
    target_name = "RHEL"
    if filename:
        if "rhel_8" in filename: target_name = "RHEL 8"
        elif "rhel_9" in filename: target_name = "RHEL 9"
        elif "rhel_10" in filename: target_name = "RHEL 10"

    if not filename:
        filename = "reports/rapport_cis_rhel.html"

    if os.path.dirname(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    report_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    flat_results = []
    if isinstance(results, dict):
        for cat, checks in results.items():
            for c in checks: flat_results.append(c)
    else:
        flat_results = list(results)

    passed_count = sum(1 for c in flat_results if c.get("status") in ["PASS", "Pass"])
    failed_count = sum(1 for c in flat_results if c.get("status") in ["FAIL", "Fail"])
    manual_count = sum(1 for c in flat_results if c.get("status") in ["MANUAL", "Manual"])
    error_count = sum(1 for c in flat_results if c.get("status") in ["ERROR", "Error"])
    na_count = sum(1 for c in flat_results if c.get("status") in ["N/A", "NA"])

    donut_svg = build_inline_svg_donut_chart(passed_count, failed_count, error_count, na_count, overall_score)

    # Categories Breakdown & Sidebar Links
    cat_names = []
    cat_pass = []
    cat_fail = []
    cat_err = []
    cat_na = []

    sidebar_links_html = ""
    categories_reports_html = ""

    # Group by category if flat list
    cat_groups = {}
    for item in flat_results:
        c_name = item.get("category", "General")
        cat_groups.setdefault(c_name, []).append(item)

    for cat_idx, (cat_name, items) in enumerate(cat_groups.items(), 1):
        cat_anchor = f"category-{cat_idx}"
        sidebar_links_html += f"""
        <a href="#{cat_anchor}" class="flex items-center px-3 py-2 text-xs text-gray-600 hover:bg-gray-100 rounded-lg transition-colors truncate">
            <span class="truncate">{html.escape(cat_name)}</span>
        </a>"""

        p_c = sum(1 for c in items if c.get("status") in ["PASS", "Pass"])
        f_c = sum(1 for c in items if c.get("status") in ["FAIL", "Fail"])
        e_c = sum(1 for c in items if c.get("status") in ["ERROR", "Error"])
        n_c = sum(1 for c in items if c.get("status") in ["N/A", "NA"])

        cat_names.append(cat_name)
        cat_pass.append(p_c)
        cat_fail.append(f_c)
        cat_err.append(e_c)
        cat_na.append(n_c)

        rows_html = ""
        for item in items:
            st = item.get("status", "FAIL").upper()
            st_class = "status-pass" if st == "PASS" else ("status-fail" if st == "FAIL" else ("status-manual" if st == "MANUAL" else "status-error"))
            st_badge = f'<span class="px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wider {st_class}">{st}</span>'

            ctrl_id = html.escape(str(item.get("id", item.get("number", ""))))
            ctrl_title = html.escape(str(item.get("title", item.get("name", ""))))
            test_proc = html.escape(str(item.get("test_procedure", item.get("audit", ""))))
            out_txt = html.escape(str(item.get("output", item.get("stdout", ""))))
            rem_txt = html.escape(str(item.get("remediation", "")))

            rows_html += f"""
            <tr data-status="{st}" class="hover:bg-gray-50 transition-colors border-b border-gray-100">
                <td class="py-4 px-4 text-sm font-bold text-gray-500 align-top">{ctrl_id}</td>
                <td class="py-4 px-4 align-top">
                    <div class="text-sm font-bold text-gray-900 mb-1">{ctrl_title}</div>
                    {f'<div class="text-xs text-gray-500 font-mono bg-gray-100 p-1.5 rounded mt-1 truncate max-w-md"><code>{test_proc}</code></div>' if test_proc else ''}
                </td>
                <td class="py-4 px-4 align-top text-center">{st_badge}</td>
                <td class="py-4 px-4 text-sm align-top">
                    <div class="mb-3">
                        <div class="text-[10px] font-bold text-gray-400 uppercase mb-1">Résultat de l'audit / Output:</div>
                        <div class="bg-gray-900 text-gray-100 p-3 rounded-lg border border-gray-700">
                            <pre class="overflow-x-auto">{out_txt}</pre>
                        </div>
                    </div>
                    {f'<div class="p-3 bg-blue-50 border-l-4 border-blue-400 rounded-r-lg"><div class="text-[10px] font-bold text-blue-600 uppercase mb-1"><i class="fas fa-wrench mr-1"></i> Procédure de remédiation:</div><div class="text-xs text-blue-800 leading-relaxed font-medium">{rem_txt}</div></div>' if rem_txt else ''}
                </td>
            </tr>"""

        categories_reports_html += f"""
        <div id="{cat_anchor}" class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8 overflow-hidden">
            <div class="bg-gray-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
                <h3 class="font-bold text-gray-800 text-lg flex items-center gap-2"><i class="fas fa-folder text-blue-500"></i> {html.escape(cat_name)}</h3>
                <span class="text-xs font-semibold text-gray-500">{len(items)} contrôles</span>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-gray-50/50 text-xs font-bold text-gray-500 uppercase border-b border-gray-200">
                            <th class="py-3 px-4 w-16">#</th>
                            <th class="py-3 px-4">Contrôle / Nom & Commande</th>
                            <th class="py-3 px-4 text-center w-28">Statut</th>
                            <th class="py-3 px-4">Détails (Résultat & Remédiation)</th>
                        </tr>
                    </thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>
        </div>"""

    bar_svg = build_inline_svg_category_chart(cat_names, cat_pass, cat_fail, cat_err, cat_na)

    html_template = load_html_template()
    html_content = html_template.format(
        benchmark_title=target_name,
        lang=lang,
        report_date=report_date,
        suite_version="2.1.0",
        target_version="1.4.0",
        overall_score=overall_score,
        passed_automated_count=passed_count,
        failed_automated_count=failed_count,
        manual_checks=manual_count,
        sidebar_links=sidebar_links_html,
        donut_svg=donut_svg,
        bar_svg=bar_svg,
        categories_reports=categories_reports_html
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"📄 Unified HTML Report successfully generated: {filename}")
'''

for fpath in rhel_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Re-inject template loader & generate_html_report
    content = re.sub(r'def load_html_template\(.*?\):\n.*?(?=\n\ndef generate_html_report|\ndef run_command)', '', content, flags=re.DOTALL)
    content = re.sub(r'def generate_html_report\(.*?\):\n.*?(?=\n\nif __name__|\nRECOMMENDATIONS_DATA)', '', content, flags=re.DOTALL)

    content = content.replace("def run_command(", rhel_template_loader + "\n\n\ndef run_command(")
    content = content.replace("if __name__ ==", rhel_generate_html + "\n\n\nif __name__ ==")

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Unified HTML report generators across RHEL 8, 9, 10!")
