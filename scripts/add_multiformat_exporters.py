#!/usr/bin/env python3
import glob
import re

audit_files = sorted(glob.glob("audit_cis_*.py"))
print(f"Injecting Multi-Format Exporters into {len(audit_files)} audit scripts...")

exporter_func = r'''def export_results(results, overall_score, categories_scores, target_name, filename, fmt="html", lang="en"):
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

    if fmt == "json":
        data = {
            "benchmark": target_name,
            "report_date": datetime.now().isoformat(),
            "overall_score": overall_score,
            "total_checks": len(results),
            "results": results
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"📄 JSON Report successfully generated: {filename}")

    elif fmt == "xml":
        root = ET.Element("testsuite", name=target_name, tests=str(len(results)), failures=str(sum(1 for r in results if r.get("status") == "FAIL")), timestamp=datetime.now().isoformat())
        for r in results:
            tc = ET.SubElement(root, "testcase", id=str(r.get("number", r.get("id", ""))), name=str(r.get("name", r.get("title", ""))), classname=str(r.get("category", "")))
            if r.get("status") == "FAIL":
                failure = ET.SubElement(tc, "failure", message="Control failed")
                failure.text = str(r.get("output", r.get("stdout", "")))
            elif r.get("status") == "ERROR":
                err = ET.SubElement(tc, "error", message="Control execution error")
                err.text = str(r.get("output", r.get("stderr", "")))
        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        print(f"📄 XML Report successfully generated: {filename}")

    elif fmt == "txt":
        lines = [
            "=" * 70,
            f"🛡️  {target_name} - CIS Benchmark Audit Report",
            f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Global Score: {overall_score:.1f}%",
            "=" * 70,
            ""
        ]
        for r in results:
            status = r.get("status", "")
            status_icon = "[PASS]" if status == "PASS" else ("[FAIL]" if status == "FAIL" else "[MANUAL]")
            rec_id = r.get("number", r.get("id", ""))
            rec_name = r.get("name", r.get("title", ""))
            lines.append(f"{status_icon} {rec_id} - {rec_name}")
            lines.append(f"  Category: {r.get('category')}")
            out = r.get('output', r.get('stdout', ''))
            if out:
                lines.append(f"  Output: {str(out).strip()}")
            rem = r.get('remediation', '')
            if rem and status == "FAIL":
                lines.append(f"  Remediation: {str(rem).strip()}")
            lines.append("-" * 70)
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"📄 TXT Report successfully generated: {filename}")

    else:
        try:
            generate_html_report(results, overall_score, categories_scores, filename=filename, lang=lang)
        except TypeError:
            generate_html_report(results, overall_score, categories_scores, filename=filename)
'''

for fpath in audit_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Clean previous export_results
    content = re.sub(r'def export_results\(.*?\):\n.*?(?=\n\ndef generate_html_report|\ndef main|\nRECOMMENDATIONS_DATA)', '', content, flags=re.DOTALL)

    if "def export_results(" not in content:
        content = content.replace("def generate_html_report(", exporter_func + "\n\n\ndef generate_html_report(")

    # Ensure -f / --format in main parser
    if 'add_argument("-f", "--format"' not in content:
        content = content.replace(
            'parser.add_argument("-o", "--output"',
            'parser.add_argument("-f", "--format", choices=["html", "json", "xml", "txt"], default="html", help="Report output format (html/json/xml/txt)")\n    parser.add_argument("-l", "--lang", choices=["en", "fr"], default="en", help="Language for report and CLI output (en/fr)")\n    parser.add_argument("-o", "--output"'
        )

    # In main(), replace call to generate_html_report with export_results
    main_split = content.split("def main():")
    if len(main_split) == 2:
        pre_main = main_split[0]
        main_body = main_split[1]
        main_body = re.sub(
            r'generate_html_report\([^)]+\)',
            'export_results(results, overall_score, {}, target_name=BENCHMARK_NAME if "BENCHMARK_NAME" in globals() else "CIS Audit", filename=args.output, fmt=getattr(args, "format", "html"), lang=getattr(args, "lang", "en"))',
            main_body
        )
        content = pre_main + "def main():" + main_body

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Updated Multi-Format Exporters across all 18 audit scripts!")
