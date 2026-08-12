#!/usr/bin/env python3
"""
Fetch all Pull Request reviews, comments, and issue details from GitHub via `gh` CLI.
Parse feedback, review notes, resolved issues, and roadmap items, and update ROADMAP.md and POTENTIAL_ISSUES.md.
100% Python Standard Library (PSL ONLY).
"""

import json
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fetch_github_prs():
    """Fetch PR details including reviews and comments using gh CLI."""
    try:
        cmd = ["gh", "pr", "list", "--state", "all", "--limit", "100", "--json", "number,title,state,mergedAt,createdAt,body,reviews,comments"]
        output = subprocess.check_output(cmd, text=True, cwd=REPO_ROOT)
        return json.loads(output)
    except Exception as e:
        print(f"⚠️ Error fetching PRs from GitHub: {e}", file=sys.stderr)
        return []


def analyze_prs(prs):
    """Extract review feedback, resolved backlog, and roadmap items from PRs."""
    resolved_backlog = []
    roadmap_items = []
    reviews_summary = []

    for pr in sorted(prs, key=lambda x: x.get("number", 0)):
        num = pr.get("number")
        title = pr.get("title", "")
        state = pr.get("state", "")
        body = pr.get("body", "") or ""
        reviews = pr.get("reviews", [])
        comments = pr.get("comments", [])

        # Process PR reviews
        for rev in reviews:
            rev_state = rev.get("state", "")
            rev_body = rev.get("body", "").strip()
            rev_author = rev.get("author", {}).get("login", "reviewer")
            if rev_body:
                reviews_summary.append(f"PR #{num} ({title}) - [{rev_state}] by @{rev_author}: {rev_body[:120]}")

        # Process PR comments
        for c in comments:
            c_body = c.get("body", "").strip()
            c_author = c.get("author", {}).get("login", "user")
            if c_body:
                reviews_summary.append(f"PR #{num} Comment by @{c_author}: {c_body[:120]}")

        # Categorize PR title and body into backlog or roadmap
        clean_title = title.replace("feat: ", "").replace("fix: ", "").replace("docs: ", "").strip()
        if state == "MERGED" or state == "CLOSED":
            resolved_backlog.append(f"PR #{num}: {clean_title}")
        else:
            roadmap_items.append(f"PR #{num} (Open): {clean_title}")

    return resolved_backlog, roadmap_items, reviews_summary


def update_roadmap(resolved_backlog, roadmap_items, reviews_summary):
    """Enrich ROADMAP.md with PR review insights and completed milestones."""
    roadmap_path = os.path.join(REPO_ROOT, "ROADMAP.md")
    with open(roadmap_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Append PR Review Feedback Section if not already present
    review_section = "\n\n### 💬 GitHub PR Reviews & Feedback Summary\n"
    for r in reviews_summary[:10]:
        review_section += f"- {r}\n"

    if "### 💬 GitHub PR Reviews & Feedback Summary" not in content:
        content += review_section
    else:
        content = re_replace_section(content, "### 💬 GitHub PR Reviews & Feedback Summary", review_section)

    with open(roadmap_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ ROADMAP.md enriched with PR review insights!")


def update_potential_issues(resolved_backlog, reviews_summary):
    """Enrich POTENTIAL_ISSUES.md with resolved PR debt and technical backlog."""
    issues_path = os.path.join(REPO_ROOT, "POTENTIAL_ISSUES.md")
    with open(issues_path, "r", encoding="utf-8") as f:
        content = f.read()

    resolved_section = "\n\n## 🔄 Resolved Pull Requests & Technical Improvements\n"
    for item in resolved_backlog:
        resolved_section += f"- [x] **{item}**\n"

    if "## 🔄 Resolved Pull Requests & Technical Improvements" not in content:
        content += resolved_section
    else:
        content = re_replace_section(content, "## 🔄 Resolved Pull Requests & Technical Improvements", resolved_section)

    with open(issues_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ POTENTIAL_ISSUES.md enriched with PR resolution history!")


def re_replace_section(content, header, new_section):
    """Utility helper to replace a markdown section."""
    import re
    pattern = re.escape(header) + r".*?(?=\n\n#|\n\n##|\Z)"
    if re.search(pattern, content, flags=re.DOTALL):
        return re.sub(pattern, new_section.strip(), content, flags=re.DOTALL)
    return content + new_section


def main():
    print("🔍 Fetching GitHub Pull Requests and Review comments...")
    prs = fetch_github_prs()
    print(f"📋 Analyzed {len(prs)} Pull Requests.")
    resolved_backlog, roadmap_items, reviews_summary = analyze_prs(prs)
    update_roadmap(resolved_backlog, roadmap_items, reviews_summary)
    update_potential_issues(resolved_backlog, reviews_summary)
    print("🎉 PR reviews and comments successfully synchronized into ROADMAP.md and POTENTIAL_ISSUES.md!")


if __name__ == "__main__":
    main()
