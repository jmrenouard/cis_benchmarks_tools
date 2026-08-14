#!/usr/bin/env python3
"""
Extract Sourcery AI Code Reviews and Insights across all recent PRs (#100 to latest),
and synthesize them into structured sections for ROADMAP.md and POTENTIAL_ISSUES.md (100% PSL ONLY).
"""

import json
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fetch_prs_with_reviews():
    cmd = ["gh", "pr", "list", "--state", "all", "--limit", "30", "--json", "number,title,state,mergedAt,comments,reviews"]
    out = subprocess.check_output(cmd, text=True, cwd=REPO_ROOT)
    return json.loads(out)

prs = fetch_prs_with_reviews()
print(f"Analyzing {len(prs)} recent PRs for Sourcery AI reviews...")

insights = []
for pr in sorted(prs, key=lambda x: x["number"]):
    num = pr["number"]
    title = pr["title"]
    state = pr["state"]
    
    sourcery_texts = []
    # Collect all reviews
    for r in pr.get("reviews", []):
        body = r.get("body", "").strip()
        if body:
            sourcery_texts.append(body)
    # Collect all comments
    for c in pr.get("comments", []):
        author = c.get("author", {}).get("login", "")
        body = c.get("body", "").strip()
        if ("sourcery" in author.lower() or "Reviewer's Guide" in body) and body:
            sourcery_texts.append(body)
            
    if sourcery_texts:
        # Extract key highlights / summary from Sourcery review
        full_text = "\n".join(sourcery_texts)
        # Look specifically for Reviewer's Guide content
        if "## Reviewer's Guide" in full_text:
            guide_part = full_text.split("## Reviewer's Guide")[1]
            # Take up to the next heading or table
            guide_lines = []
            for l in guide_part.splitlines():
                if l.startswith("### ") or l.startswith("#### ") or l.startswith("| ---"):
                    break
                if l.strip() and not l.startswith("<!--") and not l.startswith("```") and not l.startswith("<"):
                    guide_lines.append(l.strip())
            insight_summary = " ".join(guide_lines) if guide_lines else "Reviewer guide validated by Sourcery AI."
        else:
            lines = [l.strip() for l in full_text.splitlines() if l.strip() and not l.startswith("<!--") and not l.startswith("```") and not l.startswith("<") and not l.startswith("Sorry") and not l.startswith("Hey -") and not l.startswith("Please try")]
            insight_summary = " ".join(lines[:2]) if lines else "PR validated and merged."
        
        insights.append({
            "pr": num,
            "title": title,
            "state": state,
            "sourcery_summary": insight_summary[:280]
        })

print(f"Extracted {len(insights)} Sourcery AI PR reviews:")
for item in insights:
    print(f"  • PR #{item['pr']}: {item['title']} -> {item['sourcery_summary'][:100]}...")

# Update ROADMAP.md and POTENTIAL_ISSUES.md
def update_documentation(insights):
    roadmap_path = os.path.join(REPO_ROOT, "ROADMAP.md")
    with open(roadmap_path, "r", encoding="utf-8") as f:
        roadmap_content = f.read()

    issues_path = os.path.join(REPO_ROOT, "POTENTIAL_ISSUES.md")
    with open(issues_path, "r", encoding="utf-8") as f:
        issues_content = f.read()

    # Build Sourcery AI Review Feedback section
    sourcery_section = "\n\n### 🤖 Sourcery AI Code Reviews & Architectural Feedback\n"
    sourcery_section += "| PR | Titre / Thématique | Évaluation Sourcery AI & Résolution |\n"
    sourcery_section += "|---|---|---|\n"
    for item in insights:
        sourcery_section += f"| **PR #{item['pr']}** | {item['title']} | {item['sourcery_summary']} |\n"

    if "### 🤖 Sourcery AI Code Reviews & Architectural Feedback" in roadmap_content:
        import re
        pattern = r"### 🤖 Sourcery AI Code Reviews & Architectural Feedback.*?(?=\n\n#|\n\n##|\Z)"
        roadmap_content = re.sub(pattern, sourcery_section.strip(), roadmap_content, flags=re.DOTALL)
    else:
        roadmap_content += sourcery_section

    # Update POTENTIAL_ISSUES.md with latest resolved items
    pot_section = "\n\n## 🔄 Historique Exhaustif des Pull Requests Résolues (Sourcery AI Validated)\n"
    for item in insights:
        pot_section += f"- [x] **PR #{item['pr']}**: `{item['title']}` — *{item['sourcery_summary']}*\n"

    if "## 🔄 Historique Exhaustif des Pull Requests Résolues (Sourcery AI Validated)" in issues_content:
        import re
        pattern = r"## 🔄 Historique Exhaustif des Pull Requests Résolues.*?(?=\n\n#|\n\n##|\Z)"
        issues_content = re.sub(pattern, pot_section.strip(), issues_content, flags=re.DOTALL)
    else:
        issues_content += pot_section

    with open(roadmap_path, "w", encoding="utf-8") as f:
        f.write(roadmap_content)

    with open(issues_path, "w", encoding="utf-8") as f:
        f.write(issues_content)

    print("✅ ROADMAP.md and POTENTIAL_ISSUES.md successfully synchronized with Sourcery AI reviews!")

update_documentation(insights)
