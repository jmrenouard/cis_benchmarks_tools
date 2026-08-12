# -*- coding: utf-8 -*-
import argparse
import subprocess
import json
import os
from datetime import datetime
import re # Pour les expressions régulières
import html # Pour échapper les caractères spéciaux HTML

# --- Configuration ---
# Command pour se connecter au CQL Shell Cassandra
# Pour une utilisation en production, ajustez avec -u <user> -p <password>
CQLSH_CMD = "cqlsh -e"
# Chemin par défaut pour le fichier de configuration Cassandra sur Linux.
CASSANDRA_CONFIG_PATH = "/etc/cassandra/cassandra.yaml"
CASSANDRA_ENV_PATH = "/etc/cassandra/cassandra-env.sh"

# --- Structure des Recommandations (Adaptée pour Apache Cassandra 5.0) ---
# Basée sur le document "CIS Apache Cassandra 5.0 Benchmark v1.1.0"
RECOMMENDATIONS_DATA = [
    # Category 1: Installation et Mises à jour
    {"category": "1 Installation et Mises à jour", "number": "1.1", "name": "S'assurer qu'un utilisateur et un groupe dédiés existent pour Cassandra", "type": "Manual",
     "test_procedure": "getent group cassandra && getent passwd cassandra",
     "expected_output": None,
     "remediation": "Créer un groupe et un utilisateur dédiés : groupadd cassandra && useradd -g cassandra -s /sbin/nologin cassandra.",
     "manual_steps": ["Vérifier que le groupe 'cassandra' existe.", "Vérifier que l'utilisateur 'cassandra' existe.", "Vérifier que l'utilisateur appartient au bon groupe."]},
    {"category": "1 Installation et Mises à jour", "number": "1.2", "name": "S'assurer que la dernière version de Java est installée", "type": "Automated",
     "test_procedure": "java -version 2>&1 | head -1",
     "expected_output": {"type": "stdout_regex_match", "pattern": r"(11|17|21)\.\d+"},
     "remediation": "Mettre à jour Java vers la dernière version LTS supportée (Java 11, 17 ou 21)."},
    {"category": "1 Installation et Mises à jour", "number": "1.3", "name": "S'assurer que la dernière version de Python est installée", "type": "Automated",
     "test_procedure": "python3 --version 2>&1",
     "expected_output": {"type": "stdout_regex_match", "pattern": r"Python 3\.\d+"},
     "remediation": "Mettre à jour Python vers la dernière version 3.x."},
    {"category": "1 Installation et Mises à jour", "number": "1.4", "name": "S'assurer que la dernière version de Cassandra est installée", "type": "Automated",
     "test_procedure": "cassandra -v 2>/dev/null || nodetool version 2>/dev/null",
     "expected_output": {"type": "stdout_regex_match", "pattern": r"4\.0\.\d+"},
     "remediation": "Mettre à jour Cassandra vers la dernière version 5.0.x."},
    {"category": "1 Installation et Mises à jour", "number": "1.5", "name": "S'assurer que le service Cassandra est exécuté en tant qu'utilisateur non-root", "type": "Automated",
     "test_procedure": "ps -ef | grep -E '[c]assandra' | awk '{print $1}' | head -n 1",
     "expected_output": {"type": "stdout_not_equals", "value": "root"},
     "remediation": "Configurer le service Cassandra pour qu'il s'exécute sous un utilisateur dédié (ex: 'cassandra')."},
    {"category": "1 Installation et Mises à jour", "number": "1.6", "name": "S'assurer que les horloges sont synchronisées sur tous les nœuds", "type": "Manual",
     "test_procedure": "timedatectl status 2>/dev/null | grep 'synchronized' || ntpstat 2>/dev/null || chronyc tracking 2>/dev/null",
     "expected_output": None,
     "remediation": "Configurer NTP ou chronyd pour synchroniser les horloges sur tous les nœuds du cluster.",
     "manual_steps": ["Vérifier que NTP/chrony est installé.", "Vérifier que la synchronisation est active.", "S'assurer que tous les nœuds utilisent la même source."]},

    # Category 2: Authentification et Autorisation
    {"category": "2 Authentification et Autorisation", "number": "2.1", "name": "S'assurer que l'authentification est activée pour les bases de données Cassandra", "type": "Automated",
     "test_procedure": f"grep -E '^authenticator:' {CASSANDRA_CONFIG_PATH}",
     "expected_output": {"type": "stdout_contains", "value": "PasswordAuthenticator"},
     "remediation": "Modifier cassandra.yaml pour définir 'authenticator: PasswordAuthenticator' et redémarrer Cassandra."},
    {"category": "2 Authentification et Autorisation", "number": "2.2", "name": "S'assurer que l'autorisation est activée pour les bases de données Cassandra", "type": "Automated",
     "test_procedure": f"grep -E '^authorizer:' {CASSANDRA_CONFIG_PATH}",
     "expected_output": {"type": "stdout_contains", "value": "CassandraAuthorizer"},
     "remediation": "Modifier cassandra.yaml pour définir 'authorizer: CassandraAuthorizer' et redémarrer Cassandra."},

    # Category 3: Contrôle d'accès / Politiques de mots de passe
    {"category": "3 Contrôle d'accès", "number": "3.1", "name": "S'assurer que les rôles cassandra et superuser sont séparés", "type": "Automated",
     "test_procedure": f"{CQLSH_CMD} \"LIST ROLES;\" 2>/dev/null | grep -v 'cassandra' | grep -c 'True'",
     "expected_output": {"type": "stdout_regex_match", "pattern": r"[1-9]\d*"},
     "remediation": "Créer un nouveau rôle superuser, se connecter avec ce rôle, puis exécuter ALTER ROLE cassandra WITH SUPERUSER = false;"},
    {"category": "3 Contrôle d'accès", "number": "3.2", "name": "S'assurer que le mot de passe par défaut du rôle cassandra est changé", "type": "Automated",
     "test_procedure": f"{CQLSH_CMD} \"SELECT * FROM system_auth.roles WHERE role='cassandra';\" -u cassandra -p cassandra 2>&1 | grep -c 'AuthenticationFailed\\|Unauthorized\\|Bad credentials'",
     "expected_output": {"type": "stdout_regex_match", "pattern": r"[1-9]"},
     "remediation": "Se connecter et exécuter ALTER ROLE cassandra WITH PASSWORD = '<nouveau_mot_de_passe>';"},
    {"category": "3 Contrôle d'accès", "number": "3.3", "name": "S'assurer qu'il n'y a pas de rôles ou privilèges excessifs", "type": "Manual",
     "test_procedure": f"{CQLSH_CMD} \"LIST ROLES;\" 2>/dev/null",
     "expected_output": None,
     "remediation": "Révoquer les rôles et privilèges inutiles. Utiliser REVOKE et DROP ROLE.",
     "manual_steps": ["Lister tous les rôles (LIST ROLES;).", "Identifier les rôles avec des privilèges excessifs.", "Révoquer les privilèges non nécessaires."]},
    {"category": "3 Contrôle d'accès", "number": "3.4", "name": "S'assurer que Cassandra est exécuté sous un compte de service dédié", "type": "Automated",
     "test_procedure": "ps -ef | grep -E '[c]assandra' | awk '{print $1}' | head -n 1",
     "expected_output": {"type": "stdout_equals", "value": "cassandra"},
     "remediation": "Configurer le service Cassandra pour qu'il s'exécute sous l'utilisateur 'cassandra'."},
    {"category": "3 Contrôle d'accès", "number": "3.5", "name": "S'assurer que Cassandra n'écoute que sur les interfaces autorisées", "type": "Manual",
     "test_procedure": f"grep -E '^listen_address:|^rpc_address:' {CASSANDRA_CONFIG_PATH}",
     "expected_output": None,
     "remediation": "Modifier cassandra.yaml pour définir 'listen_address' et 'rpc_address' sur des interfaces spécifiques.",
     "manual_steps": ["Vérifier listen_address dans cassandra.yaml.", "Vérifier rpc_address dans cassandra.yaml.", "S'assurer que les adresses ne sont pas 0.0.0.0 sauf si justifié."]},
    {"category": "3 Contrôle d'accès", "number": "3.6", "name": "S'assurer que les autorisations Data Center sont activées", "type": "Manual",
     "test_procedure": f"grep -E '^authorizer:' {CASSANDRA_CONFIG_PATH}",
     "expected_output": None,
     "remediation": "Configurer l'autorisation par Data Center si nécessaire.",
     "manual_steps": ["Vérifier la configuration de l'authorizer.", "Vérifier les permissions par DC."]},
    {"category": "3 Contrôle d'accès", "number": "3.7", "name": "Réviser les rôles définis par l'utilisateur", "type": "Manual",
     "test_procedure": f"{CQLSH_CMD} \"LIST ROLES;\" 2>/dev/null",
     "expected_output": None,
     "remediation": "Supprimer les rôles inutiles et révoquer les privilèges excessifs.",
     "manual_steps": ["Lister les rôles avec LIST ROLES;.", "Identifier les rôles personnalisés.", "Vérifier les privilèges de chaque rôle."]},
    {"category": "3 Contrôle d'accès", "number": "3.8", "name": "Réviser les rôles superuser/administrateur", "type": "Manual",
     "test_procedure": f"{CQLSH_CMD} \"LIST ROLES;\" 2>/dev/null | grep 'True'",
     "expected_output": None,
     "remediation": "Limiter le nombre de rôles superuser au strict nécessaire.",
     "manual_steps": ["Lister les rôles superuser.", "Vérifier que chaque rôle superuser est justifié.", "Révoquer le privilège superuser si non nécessaire."]},

    # Category 4: Audit et Journalisation
    {"category": "4 Audit et Journalisation", "number": "4.1", "name": "S'assurer que la journalisation est activée", "type": "Automated",
     "test_procedure": "ls -la /var/log/cassandra/system.log 2>/dev/null || ls -la /opt/cassandra/logs/system.log 2>/dev/null",
     "expected_output": {"type": "stdout_not_empty"},
     "remediation": "Vérifier que la journalisation est configurée dans logback.xml et que les fichiers de log existent."},
    {"category": "4 Audit et Journalisation", "number": "4.2", "name": "S'assurer que l'audit est activé", "type": "Manual",
     "test_procedure": f"grep -E '^audit_logging_options:' {CASSANDRA_CONFIG_PATH} || grep -A5 'audit_logging_options' {CASSANDRA_CONFIG_PATH}",
     "expected_output": None,
     "remediation": "Activer l'audit en configurant 'audit_logging_options' dans cassandra.yaml (Cassandra 5.0+).",
     "manual_steps": ["Vérifier la configuration audit_logging_options dans cassandra.yaml.", "S'assurer que enabled: true est défini.", "Configurer les filtres d'audit appropriés."]},

    # Category 5: Chiffrement
    {"category": "5 Chiffrement", "number": "5.1", "name": "Chiffrement inter-nœuds", "type": "Automated",
     "test_procedure": f"grep -A20 'server_encryption_options:' {CASSANDRA_CONFIG_PATH} | grep 'internode_encryption'",
     "expected_output": {"type": "stdout_regex_match", "pattern": r"internode_encryption:\s*(all|dc|rack)"},
     "remediation": "Configurer server_encryption_options dans cassandra.yaml : internode_encryption: all, et fournir les certificats SSL/TLS."},
    {"category": "5 Chiffrement", "number": "5.2", "name": "Chiffrement client", "type": "Automated",
     "test_procedure": f"grep -A20 'client_encryption_options:' {CASSANDRA_CONFIG_PATH} | grep 'enabled'",
     "expected_output": {"type": "stdout_contains", "value": "true"},
     "remediation": "Configurer client_encryption_options dans cassandra.yaml : enabled: true, et fournir les certificats SSL/TLS."},
]
# --- Modèle HTML pour le rapport ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CIS Benchmark Audit Report Apache Cassandra 5.0.0 Benchmark</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    
    <style>
        /* Styles personnalisés pour le rapport */
        .status-pass {{ color: #10B981; }} /* green-500 */
        .status-fail {{ color: #EF4444; }} /* red-500 */
        .status-manual {{ color: #F59E0B; }} /* yellow-500 */
        .status-error {{ color: #6B7280; }} /* gray-500 */
        .status-na {{ color: #9CA3AF; }} /* gray-400 */
        pre {{ white-space: pre-wrap; word-wrap: break-word; background-color: #f3f4f6; padding: 0.5rem; border-radius: 0.25rem; font-size: 0.875rem;}}
        table {{ table-layout: fixed; width: 100%; }} /* Ajouté pour un meilleur contrôle de la largeur des colonnes */
        td, th {{ word-break: break-word; }} /* Permettre la coupure des mots longs */
        .chart-container {{ width: 300px; height: 300px; margin: 20px auto; }} /* Style pour le conteneur du graphique */
        .category-chart-container {{ width: 80%; margin: 20px auto; }} /* Style pour le conteneur du graphique par catégorie */
        code {{ background-color: #e5e7eb; padding: 0.1rem 0.3rem; border-radius: 0.25rem; font-family: monospace;}}
    </style>
</head>
<body class="font-sans bg-gray-100 text-gray-800 p-6">
    <div class="container mx-auto bg-white p-8 rounded-lg shadow-lg">
        <h1 class="text-3xl font-bold mb-6 text-gray-900">CIS Benchmark Audit Report Apache Cassandra 5.0.0 Benchmark</h1>
        <p class="text-gray-600 mb-4">Report Date: {report_date}</p>
        <p class="text-gray-600 mb-8">Généré par un script basé sur le document CIS Apache Cassandra 5.0.0 Benchmark (Version 1.3.0).</p>

        <div class="mb-8 p-4 bg-gray-50 rounded-md border border-gray-200">
            <h2 class="text-2xl font-semibold mb-3 text-gray-800">Score Global</h2>
            <p class="text-xl font-bold {overall_score_class}">{overall_score:.2f}%</p>
            <p class="text-gray-700">des contrôles automatisés réussis ({passed_automated}/{total_automated} vérifiés).</p>
            <p class="text-gray-700">{manual_checks} contrôles nécessitent une vérification manuelle.</p>
            <p class="text-gray-700">{error_checks} controls encountered an execution error.</p>
            <p class="text-gray-700">{na_checks} contrôles ne sont pas applicables (ex: plugin non installé, commande introuvable).</p>

            {svg_global_chart_html}
        </div>

        {categories_reports}

    </div>

    
</body>
</html>
"""

# Modèle pour le rapport par catégorie
def load_html_template():
    """Load common HTML report template from templates/ or fallback."""
    tmpl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "report_template.html")
    if os.path.exists(tmpl_path):
        try:
            with open(tmpl_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return HTML_TEMPLATE


def load_category_template():
    """Load common category report template from templates/ or fallback."""
    tmpl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "category_report_template.html")
    if os.path.exists(tmpl_path):
        try:
            with open(tmpl_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return CATEGORY_REPORT_TEMPLATE

CATEGORY_REPORT_TEMPLATE = """
        <div class="mb-10 p-4 bg-gray-50 rounded-md border border-gray-200">
            <h2 class="text-2xl font-semibold mb-3 text-gray-800">{category_name}</h2>
            <p class="text-lg font-bold {category_score_class}">{category_score:.2f}%</p>
            <p class="text-gray-700">des contrôles automatisés réussis dans cette catégorie ({passed_automated}/{total_automated} vérifiés).</p>
            <p class="text-gray-700">{manual_checks} contrôles nécessitent une vérification manuelle.</p>
            <p class="text-gray-700">{error_checks} controls encountered an execution error.</p>
            <p class="text-gray-700">{na_checks} contrôles ne sont pas applicables.</p>

            <table class="min-w-full border border-gray-300 divide-y divide-gray-300 mt-6">
                <thead>
                    <tr class="bg-gray-200 text-gray-700 uppercase text-sm leading-normal">
                        <th class="py-3 px-4 text-left w-1/12">Numéro</th>
                        <th class="py-3 px-4 text-left w-3/12">Recommandation</th>
                        <th class="py-3 px-4 text-left w-1/12">Type</th>
                        <th class="py-3 px-4 text-left w-2/12">Test Exécuté</th>
                        <th class="py-3 px-4 text-left w-1/12">Résultat</th>
                        <th class="py-3 px-4 text-left w-2/12">Output / Error / Notes</th>
                        <th class="py-3 px-4 text-left w-2/12">Procédure de Remediation</th>
                    </tr>
                </thead>
                <tbody class="text-gray-600 text-sm font-light divide-y divide-gray-200">
                    {checks_rows}
                </tbody>
            </table>
        </div>
"""

# Nouveau modèle pour le canvas du graphique par catégorie
CATEGORY_CHART_CANVAS_TEMPLATE = ""


# Modèle pour une ligne de vérification individuelle
CHECK_ROW_TEMPLATE = """
                    <tr class="border-b border-gray-200 hover:bg-gray-100">
                        <td class="py-3 px-4 text-left align-top">{number}</td>
                        <td class="py-3 px-4 text-left align-top">{name}</td>
                        <td class="py-3 px-4 text-left align-top">{type}</td>
                        <td class="py-3 px-4 text-left align-top"><code>{test_procedure}</code></td>
                        <td class="py-3 px-4 text-left align-top"><span class="{status_class} font-semibold">{status_icon} {status_text}</span></td>
                        <td class="py-3 px-4 text-left align-top"><pre>{output}</pre></td>
                        <td class="py-3 px-4 text-left align-top">{remediation}</td>
                    </tr>
"""

# --- Execution and evaluation functions ---


def build_inline_svg_donut_chart(passed, failed, errors, na, score):
    """Generate 100% self-contained Inline SVG Donut Chart (PSL ONLY, Zero JS)."""
    total = passed + failed + errors + na
    p_pass = (passed / total * 100) if total > 0 else 0
    p_fail = (failed / total * 100) if total > 0 else 0
    p_err = (errors / total * 100) if total > 0 else 0
    p_na = (na / total * 100) if total > 0 else 0

    offset_pass = 25
    offset_fail = 25 - p_pass
    offset_err = offset_fail - p_fail
    offset_na = offset_err - p_err

    return f"""
    <div style="display: flex; align-items: center; justify-content: center; gap: 40px; margin: 20px 0; flex-wrap: wrap;">
      <div style="position: relative; width: 170px; height: 170px;">
        <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg);">
          <path stroke-dasharray="100 100" stroke="#e5e7eb" stroke-width="3.8" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          <path stroke-dasharray="{p_na:.1f} 100" stroke-dashoffset="{offset_na:.1f}" stroke="#9ca3af" stroke-width="3.8" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          <path stroke-dasharray="{p_err:.1f} 100" stroke-dashoffset="{offset_err:.1f}" stroke="#6b7280" stroke-width="3.8" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          <path stroke-dasharray="{p_fail:.1f} 100" stroke-dashoffset="{offset_fail:.1f}" stroke="#ef4444" stroke-width="3.8" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          <path stroke-dasharray="{p_pass:.1f} 100" stroke-dashoffset="{offset_pass:.1f}" stroke="#10b981" stroke-width="3.8" stroke-linecap="round" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
        </svg>
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
          <span style="font-size: 24px; font-weight: 800; color: #111827;">{score:.1f}%</span>
          <span style="font-size: 11px; color: #6b7280; font-weight: 600;">Score Global</span>
        </div>
      </div>
      <div style="display: flex; flex-direction: column; gap: 8px; font-size: 13px;">
        <div style="display: flex; align-items: center; gap: 8px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #10b981; display: inline-block;"></span> <strong>Réussi (PASS) :</strong> {passed}</div>
        <div style="display: flex; align-items: center; gap: 8px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #ef4444; display: inline-block;"></span> <strong>Échoué (FAIL) :</strong> {failed}</div>
        <div style="display: flex; align-items: center; gap: 8px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #6b7280; display: inline-block;"></span> <strong>Erreur (Error) :</strong> {errors}</div>
        <div style="display: flex; align-items: center; gap: 8px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #9ca3af; display: inline-block;"></span> <strong>Non Applicable (N/A) :</strong> {na}</div>
      </div>
    </div>
    """


def build_inline_svg_category_chart(categories_scores):
    """Generate 100% self-contained Inline SVG/HTML5 Horizontal Stacked Bar Charts per category (PSL ONLY, Zero JS)."""
    if not categories_scores or not isinstance(categories_scores, dict):
        return ""
    items_html = []
    for label, cat in categories_scores.items():
        p = cat.get("passed_automated", cat.get("passed", 0))
        f = cat.get("failed_automated", cat.get("failed", 0))
        e = cat.get("error_checks", cat.get("errors", 0))
        n = cat.get("na_checks", cat.get("na", 0))
        cat_total = p + f + e + n
        cat_score = cat.get("score", (p / cat_total * 100) if cat_total > 0 else 0)

        p_pass = (p / cat_total * 100) if cat_total > 0 else 0
        p_fail = (f / cat_total * 100) if cat_total > 0 else 0
        p_err = (e / cat_total * 100) if cat_total > 0 else 0
        p_na = (n / cat_total * 100) if cat_total > 0 else 0

        badge_color = "#10b981" if cat_score >= 80 else ("#f59e0b" if cat_score >= 50 else "#ef4444")

        bar_segments = []
        if p > 0: bar_segments.append(f'<div style="width: {p_pass:.1f}%; background: #10b981;" title="Réussi: {p}"></div>')
        if f > 0: bar_segments.append(f'<div style="width: {p_fail:.1f}%; background: #ef4444;" title="Échoué: {f}"></div>')
        if e > 0: bar_segments.append(f'<div style="width: {p_err:.1f}%; background: #6b7280;" title="Error: {e}"></div>')
        if n > 0: bar_segments.append(f'<div style="width: {p_na:.1f}%; background: #9ca3af;" title="N/A: {n}"></div>')
        if not bar_segments:
            bar_segments.append('<div style="width: 100%; background: #e5e7eb;" title="Aucun contrôle"></div>')

        items_html.append(f"""
        <div style="margin-bottom: 16px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-weight: 600; font-size: 14px; color: #374151;">{label}</span>
            <span style="font-weight: 700; font-size: 13px; color: {badge_color};">{cat_score:.1f}% ({p}/{cat_total})</span>
          </div>
          <div style="display: flex; height: 16px; width: 100%; border-radius: 8px; overflow: hidden; background: #f3f4f6; border: 1px solid #e5e7eb;">
            {''.join(bar_segments)}
          </div>
        </div>
        """)

    legend_html = """
    <div style="display: flex; gap: 20px; justify-content: center; margin-bottom: 20px; font-size: 13px;">
      <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #10b981; display: inline-block;"></span> Réussi</div>
      <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #ef4444; display: inline-block;"></span> Échoué</div>
      <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #6b7280; display: inline-block;"></span> Erreur</div>
      <div style="display: flex; align-items: center; gap: 6px;"><span style="width: 12px; height: 12px; border-radius: 3px; background: #9ca3af; display: inline-block;"></span> N/A</div>
    </div>
    """

    return f"""
    <div style="background: #ffffff; padding: 24px; border-radius: 12px; border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-top: 24px;">
      <h3 style="font-size: 18px; font-weight: 700; color: #111827; margin-bottom: 16px; text-align: center;">Répartition des contrôles automatisés par catégorie</h3>
      {legend_html}
      {''.join(items_html)}
    </div>
    """


def load_recommendations(target_key):
    """Load audit control specifications from rules/<target_key>.json with inline fallback (PSL ONLY)."""
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rules", f"{target_key}.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Warning: Could not load rule spec '{json_path}': {e}", file=sys.stderr)
    return RECOMMENDATIONS_DATA



def detect_docker_container(remote_host=None, docker_name=None):
    """Detect active Cassandra Docker container name."""
    if docker_name:
        return docker_name
    stdout, stderr, ret = run_command("docker ps --format '{{.Names}}' 2>/dev/null | grep -iE 'cassandra' | head -n 1", remote_host=remote_host)
    if ret == 0 and stdout:
        return stdout.strip()
    return None


def run_command(command, remote_host=None, docker_container=None):
    """Execute command safely locally, over SSH, or inside Docker container (PSL ONLY)."""
    try:
        if isinstance(command, str):
            if docker_container and not command.startswith("docker exec"):
                command = f"docker exec -i {docker_container} /bin/bash -c {json.dumps(command)}"
            elif "systemctl" in command and (os.path.exists("/.dockerenv") or not os.path.exists("/run/systemd/system")):
                if "cassandra" in command:
                    command = "nodetool status 2>/dev/null || ps aux | grep -v grep | grep cassandra"
            cmd_args = ["/bin/bash", "-c", command]
        else:
            cmd_args = list(command)

        if remote_host:
            cmd_args = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", "-i", "/root/.ssh/id_rsa", remote_host] + cmd_args

        process = subprocess.run(cmd_args, check=False, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10)
        stdout_text = process.stdout.strip()
        stderr_text = process.stderr.strip()

        if stderr_text:
            filtered_lines = [
                line for line in stderr_text.splitlines()
                if not line.startswith("Warning: Permanently added")
                and "pseudo-terminal" not in line
            ]
            stderr_text = chr(10).join(filtered_lines).strip()

        return stdout_text, stderr_text, process.returncode
    except subprocess.TimeoutExpired:
        return "", "Command execution timed out after 10 seconds", -1
    except Exception as e:
        return "", str(e), -1



def evaluate_condition(condition, stdout, stderr, returncode):
    """
    Évalue si le résultat de la commande correspond à la condition attendue.
    """
    if not condition:
        return False # Aucune condition définie

    condition_type = condition.get("type")
    expected_value = condition.get("value")
    expected_values = condition.get("values")
    regex_pattern = condition.get("pattern")
    regex_patterns = condition.get("patterns") # Nouveau pour all_lines_match_regex

    if condition_type == "returncode_zero":
        return returncode == 0
    elif condition_type == "returncode_equals":
        return returncode == expected_value
    elif condition_type == "stdout_not_equals":
        return stdout != expected_value
    elif condition_type == "stdout_not_contains":
        return expected_value not in stdout
    elif condition_type == "stdout_equals":
        # L'output peut contenir des espaces/retours à la ligne supplémentaires, on le nettoie.
        return stdout.strip() == str(expected_value) # Convertir l'attendu en chaîne pour comparaison
    elif condition_type == "stdout_contains":
        return str(expected_value) in stdout
    elif condition_type == "stdout_not_contains":
        return str(expected_value) not in stdout
    elif condition_type == "stdout_not_empty":
        return stdout != "" and stdout is not None
    elif condition_type == "stdout_is_empty":
        return stdout == "" or stdout is None
    elif condition_type == "stdout_contains_any":
        if expected_values is None: return False
        return any(str(value) in stdout for value in expected_values)
    elif condition_type == "stdout_not_contains_any":
        if expected_values is None: return True
        return not any(str(value) in stdout for value in expected_values)
    elif condition_type == "stdout_regex_match":
        if regex_pattern is None: return False
        return re.search(regex_pattern, stdout) is not None
    elif condition_type == "all_lines_match_regex": # Nouveau type de condition
        if regex_patterns is None: return False
        lines = stdout.splitlines()
        # Pour que cela réussisse, tous les motifs donnés doivent trouver une correspondance quelque part dans la sortie.
        # C'est un ET logique pour tous les motifs.
        for pattern in regex_patterns:
            found_match_for_pattern = False
            for line in lines:
                if re.search(pattern, line):
                    found_match_for_pattern = True
                    break
            if not found_match_for_pattern:
                return False # Si un motif n'est trouvé dans aucune ligne, cela échoue
        return True # Tous les motifs ont été trouvés
    elif condition_type == "stdout_is_numeric_greater_than":
        try:
            numeric_value_match = re.match(r'^(\d+)', stdout)
            if numeric_value_match:
                numeric_value = int(numeric_value_match.group(1))
                return numeric_value > expected_value
            return False
        except (ValueError, TypeError):
            return False
    elif condition_type == "stdout_is_numeric_less_equal":
        try:
            numeric_value_match = re.match(r'^(\d+)', stdout)
            if numeric_value_match:
                numeric_value = int(numeric_value_match.group(1))
                # Gérer le cas où '0' signifie une durée de vie infinie, qui est considérée > 365
                if numeric_value == 0:
                    return False # 0 (infini) n'est pas <= 365
                return numeric_value <= expected_value
            return False
        except (ValueError, TypeError):
            return False

    # Cas par défaut : type de condition inconnu
    print(f"ATTENTION : Type de condition inconnu '{condition_type}'")
    return False

def perform_checks(recommendations, remote_host=None, docker_container=None):
    """
    Exécute tous les contrôles définis dans les recommandations et stocke les résultats.
    """
    results = {}
    # Initialise les résultats par catégorie en respectant l'ordre de définition
    category_order = list(dict.fromkeys(rec["category"] for rec in RECOMMENDATIONS_DATA))
    for category in category_order:
        results[category] = []

    for rec in recommendations:
        category = rec["category"]
        check_number = rec.get("number", "N/A")

        check_result = {
            "number": check_number,
            "name": rec["name"],
            "type": rec["type"],
            "test_procedure": rec.get("test_procedure", ""),
            "remediation": rec.get("remediation", ""),
            "status": "Not Applicable", # Status par défaut (sera modifié pour les automatisés)
            "output": "",
            "error": ""
        }

        if rec["type"] == "Manual":
            check_result["status"] = "Manual"
            check_result["output"] = "This control requires manual verification."
            # Ajoute la description de la procédure de test manuelle pour l'affichage
            check_result["output"] += f"\n\nProcédure suggérée:\n{rec.get('test_procedure', 'N/A')}"
        elif rec["type"] == "Automated":
            cmd_to_run = None
            command_executed_display = "N/A"
            stdout, stderr, returncode = "", "", -1 # Initialise les résultats d'exécution

            try:
                # Gérer les contrôles qui nécessitent d'obtenir d'abord un chemin dynamique (non utilisé pour Apache Cassandra ici, mais conservé)
                if "path_command" in rec:
                    path_cmd = rec["path_command"]
                    path_stdout, path_stderr, path_returncode = run_command(path_cmd, remote_host=remote_host)

                    if path_returncode != 0 or not path_stdout:
                        check_result["status"] = "Error"
                        check_result["output"] = f"Error lors de l'obtention du chemin via:\n`{path_cmd}`\nStdout:\n{path_stdout}\nStderr:\n{path_stderr}"
                        check_result["error"] = path_stderr
                        results[category].append(check_result)
                        continue # Passer à la recommandation suivante

                    dynamic_path = path_stdout.strip()

                    if "test_procedure_template" in rec:
                        cmd_to_run = rec["test_procedure_template"].format(path=dynamic_path)
                        command_executed_display = cmd_to_run # Stocke la commande formatée
                    else:
                        # Si seul path_command est défini sans template, c'est une erreur de configuration du test.
                        check_result["status"] = "Error"
                        check_result["output"] = f"Configuration d'audit invalid: 'path_command' défini mais pas 'test_procedure_template' pour {check_number}."
                        results[category].append(check_result)
                        continue
                elif "test_procedure" in rec:
                    cmd_to_run = rec["test_procedure"]
                    command_executed_display = cmd_to_run
                else:
                    # Ni 'test_procedure' ni 'path_command' définis, erreur de configuration.
                    check_result["status"] = "Error"
                    check_result["output"] = f"Configuration d'audit invalid: Ni 'test_procedure' ni 'path_command' définis pour {check_number}."
                    results[category].append(check_result)
                    continue

                # Exécuter la commande
                stdout, stderr, returncode = run_command(cmd_to_run, remote_host=remote_host)
                check_result["output"] = f"Stdout:\n{stdout}\nStderr:\n{stderr}\nReturn Code: {returncode}"
                check_result["error"] = stderr
                check_result["test_procedure"] = command_executed_display # Met à jour avec la commande réellement exécutée

                # --- Évaluation ---
                condition = rec.get("expected_output")

                # Gérer les conditions d'erreur spécifiques avant d'évaluer le succès
                if returncode == 127: # Command not found
                    check_result["status"] = "Error"
                    check_result["output"] = f"Error: Command not found.\n{check_result['output']}"
                elif returncode == 124: # Timeout
                    check_result["status"] = "Error"
                    check_result["output"] = f"Error: Timeout.\n{check_result['output']}"
                elif "command not found" in stderr.lower(): # Une autre façon de détecter une commande introuvable
                    check_result["status"] = "Error"
                    check_result["output"] = f"Error: Command not found (détecté dans stderr).\n{check_result['output']}"
                elif "Error: command failed" in stderr or "Failed to connect to" in stderr: # Errors Apache Cassandra (connexion/commande)
                     check_result["status"] = "Error"
                     check_result["output"] = f"Execution error de la commande Apache Cassandra. Vérifiez la disponibilité/configuration du serveur/client.\n{check_result['output']}"
                elif returncode != 0 and stderr and not condition:
                    # Si la commande a échoué avec stderr, et aucune condition spécifique à vérifier, marquer comme Error
                    check_result["status"] = "Error"
                    check_result["output"] = f"Execution error (code {returncode}).\n{check_result['output']}"
                elif condition:
                    # Évaluer la condition seulement si aucune erreur critique n'est survenue ci-dessus
                    if evaluate_condition(condition, stdout, stderr, returncode):
                        check_result["status"] = "Pass"
                    else:
                        # La condition n'est pas remplie, mais la commande a été exécutée (potentiellement avec des erreurs non fatales)
                        check_result["status"] = "Fail"
                        check_result["output"] += "\n\nCondition de succès non remplie."
                elif returncode == 0 and not condition:
                    # La commande a réussi mais aucune condition à vérifier ? Marquer comme Succès (par exemple, commandes informatives)
                    check_result["status"] = "Pass"
                    check_result["output"] += "\n\nNote : Command exécutée avec succès, mais aucune condition de succès n'était définie pour ce test automatisé."
                # else: Le statut reste 'Not Applicable' ou 'Error' si défini précédemment


            except Exception as e:
                check_result["status"] = "Error"
                check_result["output"] = f"Error interne du script lors de l'exécution du contrôle {check_number}: {e}\nCommand tentée: {command_executed_display}"
                check_result["error"] = str(e)


        # Ajouter le résultat final de cette vérification
        results[category].append(check_result)

    return results

def calculate_scores(results):
    """
    Calcule les scores globaux et par catégorie.
    """
    overall = {"total_automated": 0, "passed_automated": 0, "failed_automated": 0, "manual": 0, "error": 0, "na": 0}
    categories_scores = {}
    # Initialiser les compteurs par catégorie en respectant l'ordre de RECOMMENDATIONS_DATA
    category_order = list(dict.fromkeys(rec["category"] for rec in RECOMMENDATIONS_DATA))
    for category in category_order:
        categories_scores[category] = {
            "score": 0,
            "total_automated": 0, # Total tenté (Pass + Fail)
            "passed_automated": 0,
            "failed_automated": 0,
            "manual_checks": 0,
            "error_checks": 0,
            "na_checks": 0,
            "pass_count": 0, # Compteurs pour les graphiques
            "fail_count": 0,
            "error_count": 0,
            "na_count": 0
        }


    for category, checks in results.items():
        if category not in categories_scores:
            print(f"ATTENTION : Category '{category}' trouvée dans les résultats mais non pré-initialisée. Ignorée.")
            continue
        for check in checks:
            cat_stats = categories_scores[category]
            if check["type"] == "Automated":
                if check["status"] == "Pass":
                    overall["passed_automated"] += 1
                    cat_stats["passed_automated"] += 1
                    cat_stats["pass_count"] += 1
                elif check["status"] == "Fail":
                    overall["failed_automated"] += 1
                    cat_stats["failed_automated"] += 1
                    cat_stats["fail_count"] += 1
                elif check["status"] == "Error":
                    overall["error"] += 1
                    cat_stats["error_checks"] += 1
                    cat_stats["error_count"] += 1
                elif check["status"] == "Not Applicable": # Ce cas est peu probable pour les automatisés avec la logique actuelle
                    overall["na"] += 1
                    cat_stats["na_checks"] += 1
                    cat_stats["na_count"] += 1
            elif check["type"] == "Manual":
                overall["manual"] += 1
                cat_stats["manual_checks"] += 1

    # Calculer les scores
    overall_attempted_automated = overall["passed_automated"] + overall["failed_automated"]
    overall_score = (overall["passed_automated"] / overall_attempted_automated * 100) if overall_attempted_automated > 0 else 0

    for category in category_order:
        cat_stats = categories_scores[category]
        cat_attempted_automated = cat_stats["passed_automated"] + cat_stats["failed_automated"]
        cat_stats["total_automated"] = cat_attempted_automated # Stocker le nombre de tentatives
        cat_stats["score"] = (cat_stats["passed_automated"] / cat_attempted_automated * 100) if cat_attempted_automated > 0 else 0

    # Préparer les données pour le graphique à barres par catégorie (en utilisant l'ordre original)
    category_labels = json.dumps(category_order)
    category_pass_counts = json.dumps([categories_scores[cat]["pass_count"] for cat in category_order])
    category_fail_counts = json.dumps([categories_scores[cat]["fail_count"] for cat in category_order])
    category_error_counts = json.dumps([categories_scores[cat]["error_count"] for cat in category_order])
    category_na_counts = json.dumps([categories_scores[cat]["na_count"] for cat in category_order])


    # Retourner le score global, les détails par catégorie, les totaux globaux et les données des graphiques
    return (overall_score, categories_scores,
            overall["manual"], overall["error"], overall["na"],
            overall["passed_automated"], overall["failed_automated"], overall["error"], overall["na"], # Compteurs pour le graphique global
            category_labels, category_pass_counts, category_fail_counts, category_error_counts, category_na_counts) # Données pour le graphique par catégorie

def get_score_class(score):
    """Retourne la classe CSS pour la couleur du score."""
    if score >= 80:
        return "text-green-600"
    elif score >= 50:
        return "text-yellow-600"
    else:
        return "text-red-600"

def get_status_info(status):
    """Retourne l'icône, le texte et la classe CSS pour un statut."""
    if status == "Pass":
        return "✅", "Réussi", "status-pass"
    elif status == "Fail":
        return "❌", "Échoué", "status-fail"
    elif status == "Manual":
        return "⚠️", "Manuel", "status-manual"
    elif status == "Error":
        return "❓", "Error", "status-error"
    elif status == "Not Applicable":
        return "➖", "N/A", "status-na"
    else:
        return "❓", status, "status-error" # Fallback







def export_results(results, overall_score, categories_scores, target_name, filename, fmt="html", lang="en"):
    """Export audit results into HTML, JSON, XML, or TXT formats using PSL ONLY."""
    import json
    import os
    import xml.etree.ElementTree as ET
    from datetime import datetime

    if not filename:
        ext = "html" if fmt == "html" else fmt
        target_slug = target_name.lower().replace(" ", "_").replace(".", "")
        filename = f"reports/rapport_cis_{target_slug}.{ext}"

    if os.path.dirname(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Flatten results if dictionary categorized
    flat_results = []
    if isinstance(results, dict):
        for cat, checks in results.items():
            for c in checks:
                c_copy = dict(c)
                c_copy["category"] = cat
                flat_results.append(c_copy)
    else:
        flat_results = results

    if fmt == "json":
        data = {
            "benchmark": target_name,
            "report_date": datetime.now().isoformat(),
            "overall_score": overall_score,
            "total_checks": len(flat_results),
            "results": flat_results
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"📄 JSON Report successfully generated: {filename}")

    elif fmt == "xml":
        root = ET.Element("testsuite", name=target_name, tests=str(len(flat_results)), failures=str(sum(1 for r in flat_results if r.get("status") in ["FAIL", "Fail"])), timestamp=datetime.now().isoformat())
        for r in flat_results:
            tc = ET.SubElement(root, "testcase", id=str(r.get("number", r.get("id", ""))), name=str(r.get("name", r.get("title", ""))), classname=str(r.get("category", "")))
            test_proc = r.get("test_procedure", r.get("audit", ""))
            if test_proc:
                cmd_elem = ET.SubElement(tc, "system-out")
                cmd_elem.text = f"Test Command: {str(test_proc).strip()}"
            rem = r.get("remediation", "")
            if rem:
                rem_elem = ET.SubElement(tc, "remediation")
                rem_elem.text = str(rem).strip()
            if r.get("status") in ["FAIL", "Fail"]:
                failure = ET.SubElement(tc, "failure", message="Control failed")
                failure.text = str(r.get("output", r.get("stdout", "")))
            elif r.get("status") in ["ERROR", "Error"]:
                err = ET.SubElement(tc, "error", message="Control execution error")
                err.text = str(r.get("output", r.get("stderr", "")))
        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        print(f"📄 XML Report successfully generated: {filename}")

    elif fmt == "txt":
        lines = [
            "=" * 90,
            f"               CIS BENCHMARK AUDIT REPORT - {target_name.upper()}",
            "=" * 90,
            f"Report Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Global Score  : {overall_score:.1f}%",
            f"Total Controls: {len(flat_results)}",
            "-" * 90,
            " CATEGORY BREAKDOWN & COMPLIANCE SUMMARY TABLE",
            "-" * 90,
            f"  {'ID':<6} {'Category Name':<45} {'Pass':<6} {'Fail':<6} {'Manual':<8} {'Score':<8}",
            f"  {'-'*6} {'-'*45} {'-'*6} {'-'*6} {'-'*8} {'-'*8}",
        ]
        if isinstance(categories_scores, dict):
            for cat_id, data in categories_scores.items():
                name = str(data.get('name', cat_id))[:44]
                p = data.get('passed_automated', 0)
                f = data.get('failed_automated', 0)
                m = data.get('manual_checks', 0)
                sc = data.get('score', 0.0)
                lines.append(f"  {str(cat_id):<6} {name:<45} {p:<6} {f:<6} {m:<8} {sc:>6.1f}%")
        lines.extend([
            "=" * 90,
            " DETAILED CONTROL RESULTS",
            "=" * 90,
            ""
        ])
        for r in flat_results:
            status = r.get("status", "")
            status_icon = "[PASS]" if status in ["PASS", "Pass"] else ("[FAIL]" if status in ["FAIL", "Fail"] else "[MANUAL]")
            rec_id = r.get("number", r.get("id", ""))
            rec_name = r.get("name", r.get("title", ""))
            lines.append(f"{status_icon} {rec_id} - {rec_name}")
            lines.append(f"  Category: {r.get('category')}")
            test_proc = r.get("test_procedure", r.get("audit", ""))
            if test_proc:
                lines.append(f"  Commande de test: {str(test_proc).strip()}")
            out = r.get('output', r.get('stdout', ''))
            if out:
                lines.append(f"  Output: {str(out).strip()}")
            rem = r.get('remediation', '')
            if rem:
                lines.append(f"  Procédure de remédiation: {str(rem).strip()}")
            lines.append("-" * 90)
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"📄 TXT Report successfully generated: {filename}")

    else:
        try:
            generate_html_report(results, overall_score, categories_scores, filename=filename, lang=lang)
        except TypeError:
            try:
                generate_html_report(results, overall_score, categories_scores, filename=filename)
            except TypeError:
                # Legacy positional args fallback
                generate_html_report(results, overall_score, categories_scores, 0, 0, 0, 0, 0, 0, 0, [], [], [], [], [], filename)



def generate_html_report(results, overall_score, categories_scores, filename=None, lang="en"):
    if not filename:
        filename = "reports/rapport_cis_cassandra_50.html"

    report_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    overall_score_class = get_score_class(overall_score)
    categories_html = ""
    sidebar_links_html = ""

    flat_results = []
    if isinstance(results, dict):
        for cat, checks in results.items():
            for c in checks:
                flat_results.append(c)
    else:
        flat_results = results

    passed_auto_count = sum(1 for c in flat_results if c.get("status") in ["PASS", "Pass"])
    failed_auto_count = sum(1 for c in flat_results if c.get("status") in ["FAIL", "Fail"])
    error_auto_count = sum(1 for c in flat_results if c.get("status") in ["ERROR", "Error"])
    na_auto_count = sum(1 for c in flat_results if c.get("status") in ["N/A", "NA"])
    total_manual = sum(1 for c in flat_results if c.get("status") in ["MANUAL", "Manual"])
    total_errors = error_auto_count
    total_na = na_auto_count

    svg_global_chart_html = build_inline_svg_donut_chart(passed_auto_count, failed_auto_count, error_auto_count, na_auto_count, overall_score)

    category_order = list(dict.fromkeys(rec["category"] for rec in RECOMMENDATIONS_DATA)) # Obtenir l'ordre des données

    for category in category_order:
        checks = results.get(category, [])
        cat_info = categories_scores.get(category, {})
        category_score = cat_info.get("score", 0)
        cat_score_class = get_score_class(category_score)
        cat_total_automated = cat_info.get("total_automated", 0) # Tenté
        cat_passed_automated = cat_info.get("passed_automated", 0)
        cat_manual_checks = cat_info.get("manual_checks", 0)
        cat_error_checks = cat_info.get("error_checks", 0)
        cat_na_checks = cat_info.get("na_checks", 0)

        checks_rows_html = ""
        # Trier les vérifications au sein de la catégorie par numéro (gérer les parties non numériques potentielles)
        def sort_key(check):
            parts = re.split(r'[._-]', check['number'])
            return [int(p) if p.isdigit() else p for p in parts]

        try:
            sorted_checks = sorted(checks, key=sort_key)
        except Exception as e:
            print(f"ATTENTION : Impossible de trier les vérifications pour la catégorie '{category}'. Error: {e}")
            sorted_checks = checks # Garder l'ordre original si le tri échoue

        for check in sorted_checks:
            status_icon, status_text, status_class = get_status_info(check["status"])

            # Échapper les caractères spéciaux HTML
            escaped_name = html.escape(check["name"])
            # Note: Pour les procédures de test contenant des guillemets (ex: dans les commandes mongosh),
            # l'échappement HTML peut les remplacer par &quot;. L'affichage dans <code> devrait être correct.
            escaped_test_procedure = html.escape(check["test_procedure"]) 
            # L'output et la remédiation sont déjà échappés par `perform_checks`
            output_display = html.escape(check["output"]) # Assurer l'échappement même si déjà fait.
            remediation_display = html.escape(check["remediation"]) if check["remediation"] else "N/A"

            checks_rows_html += CHECK_ROW_TEMPLATE.format(
                number=check["number"],
                name=escaped_name,
                type=check["type"],
                test_procedure=escaped_test_procedure,
                status_icon=status_icon,
                status_text=status_text,
                status_class=status_class,
                output=output_display,
                remediation=remediation_display
            )

        categories_html += CATEGORY_REPORT_TEMPLATE.format(
            category_name=html.escape(category),
            category_score=category_score,
            category_score_class=cat_score_class,
            passed_automated=cat_passed_automated,
            total_automated=cat_total_automated, # Afficher le nombre de tentatives
            manual_checks=cat_manual_checks,
            error_checks=cat_error_checks,
            na_checks=cat_na_checks,
            checks_rows=checks_rows_html
        )

    # Ajouter le canvas du graphique par catégorie après tous les rapports de catégorie
    categories_html += CATEGORY_CHART_CANVAS_TEMPLATE
    class SafeDict(dict):
        def __missing__(self, key):
            return f"{{{key}}}"

    html_output = load_html_template().format_map(SafeDict(
        benchmark_title=target_name if 'target_name' in locals() else "CIS Benchmark",
        lang=lang if 'lang' in locals() else "en",
        report_date=report_date,
        suite_version="2.0.0",
        target_version="2.0.0",
        overall_score=overall_score,
        overall_score_class=overall_score_class,
        passed_automated_count=passed_auto_count if 'passed_auto_count' in locals() else 0,
        failed_automated_count=failed_auto_count if 'failed_auto_count' in locals() else 0,
        passed_automated=passed_auto_count if 'passed_auto_count' in locals() else 0,
        total_automated=(passed_auto_count + failed_auto_count) if 'passed_auto_count' in locals() else 0,
        manual_checks=total_manual if 'total_manual' in locals() else 0,
        error_checks=total_errors if 'total_errors' in locals() else 0,
        na_checks=total_na if 'total_na' in locals() else 0,
        sidebar_links=sidebar_links_html if 'sidebar_links_html' in locals() else "",
        categories_reports=categories_html,
        donut_svg=svg_global_chart_html if 'svg_global_chart_html' in locals() else "",
        bar_svg=build_inline_svg_category_chart(categories_scores) if 'categories_scores' in locals() else "",
        svg_global_chart_html=svg_global_chart_html if 'svg_global_chart_html' in locals() else ""
    ))

    try:
        if os.path.dirname(filename):
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_output)
        print(f"Report successfully generated: {filename}")
    except IOError as e:
        print(f"Error writing report file '{filename}': {e}")


# --- Main Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CIS Audit Benchmark (Local & SSH Remote Modes)")
    parser.add_argument("--docker", "--container", dest="docker_container", default=None, help="Target Docker container name or ID")
    parser.add_argument("-m", "--mode", choices=["local", "ssh"], default="local", help="Audit execution mode (local or ssh)")
    parser.add_argument("-r", "--remote", "--ssh", dest="remote_host", default=None, help="Remote SSH server target (e.g. user@hostname)")
    parser.add_argument("--ssh-port", type=int, default=22, help="SSH port for remote execution (default: 22)")
    parser.add_argument("--ssh-key", default=None, help="Path to SSH private key file")
    parser.add_argument("--sudo", action="store_true", help="Execute remote/local commands with sudo privileges")
    parser.add_argument("--db-host", "--host", dest="db_host", default="localhost", help="Database host address (default: localhost)")
    parser.add_argument("--db-port", "--port", dest="db_port", type=int, default=None, help="Database port number")
    parser.add_argument("--db-user", "--user", dest="db_user", default=None, help="Database username")
    parser.add_argument("--db-password", "--password", dest="db_password", default=None, help="Database password")
    parser.add_argument("--local", action="store_true", help="Force local audit execution mode")
    parser.add_argument("-f", "--format", choices=["html", "json", "xml", "txt"], default="html", help="Report output format")
    parser.add_argument("-l", "--lang", choices=["en", "fr"], default="en", help="Report language choice (en/fr)")
    parser.add_argument("-o", "--output", default=None, help="Custom output report file path")
    args = parser.parse_args()

    remote_target = None
    if args.mode == "ssh" or args.remote_host:
        remote_target = args.remote_host
        if not remote_target:
            print("❌ SSH mode requires a remote host target via --remote user@hostname or --ssh user@hostname", file=sys.stderr)
            sys.exit(1)
        print(f"🌐 Running Audit in SSH Remote Mode on host: '{remote_target}'...")
    else:
        print("🖥️  Running Audit in Local Mode on local machine...")

    rules_data = load_recommendations("cassandra_50")
    docker_target = detect_docker_container(remote_host=remote_target, docker_name=args.docker_container)
    check_results = perform_checks(rules_data, remote_host=remote_target, docker_container=docker_target)
    (overall_score, categories_scores, *rest) = calculate_scores(check_results)
    export_results(check_results, overall_score, categories_scores, target_name="cassandra_50", filename=args.output, fmt=args.format, lang=args.lang)