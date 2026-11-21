#!/usr/bin/env python3
"""Check PR statuses on GitHub and update README.md OSS sections.

Groups PRs by domain (not status) with per-row status badges.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from collections import OrderedDict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PRS_FILE = REPO_ROOT / "prs.json"
README_FILE = REPO_ROOT / "README.md"

START_MARKER = "<!-- AUTO:OSS:START -->"
END_MARKER = "<!-- AUTO:OSS:END -->"

GITHUB_API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

NARRATIVE = (
    "*Production bugs in AI infrastructure — LLM gateways, observability pipelines, "
    "model serving, and GPU compute — across codebases I ramp on in days, not weeks.*"
)

# Display order for domains
DOMAIN_ORDER = [
    "LLM Gateway & Runtime",
    "AI Observability & Cost",
    "Model Serving & Document Intelligence",
    "AI Security & Agents",
]

STATUS_BADGES = {
    "merged": "![merged](https://img.shields.io/badge/merged-2ea44f?style=flat-square)",
    "approved": "![approved](https://img.shields.io/badge/approved-0969da?style=flat-square)",
    "in_review": "![in review](https://img.shields.io/badge/in_review-e3b341?style=flat-square)",
}

# Minimal colored dot + lowercase heading per domain
DOMAIN_DOTS = {
    "LLM Gateway & Runtime": ("FF6B35", "LLM gateway & runtime"),
    "AI Observability & Cost": ("0969DA", "AI observability & cost"),
    "Model Serving & Document Intelligence": ("8B5CF6", "Model serving & document intelligence"),
    "AI Security & Agents": ("16A34A", "AI security & agents"),
}


def gh_get(path):
    url = f"{GITHUB_API}{path}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  Warning: {e.code} for {path}", file=sys.stderr)
        return None


def get_pr_status(pr):
    """Return: merged, approved, in_review, closed, or inaccessible."""
    owner, repo, number = pr["owner"], pr["repo"], pr["number"]

    data = gh_get(f"/repos/{owner}/{repo}/pulls/{number}")
    if data is None:
        return "inaccessible"

    if data.get("merged"):
        return "merged"
    if data.get("state") == "closed":
        return "closed"

    reviews = gh_get(f"/repos/{owner}/{repo}/pulls/{number}/reviews")
    if reviews:
        latest_by_user = {}
        for review in reviews:
            user = review.get("user", {}).get("login", "")
            if user.endswith("[bot]"):
                continue
            state = review.get("state")
            if state in ("APPROVED", "CHANGES_REQUESTED"):
                latest_by_user[user] = state

        states = set(latest_by_user.values())
        if "CHANGES_REQUESTED" in states and "APPROVED" not in states:
            return "in_review"
        if "APPROVED" in states:
            return "approved"

    return "in_review"


def build_row(pr, status):
    owner, repo, number = pr["owner"], pr["repo"], pr["number"]
    url = f"https://github.com/{owner}/{repo}"
    pr_url = f"{url}/pull/{number}"
    badge = STATUS_BADGES.get(status, STATUS_BADGES["in_review"])
    fix_type = pr.get("fix_type", "")
    return (
        f'| {pr["badge"]} **[{pr["display_name"]}]({url})** '
        f'`{pr["stars"]}` | [{pr["fix"]}]({pr_url}) | '
        f'`{fix_type}` | {badge} |'
    )


def build_domain_section(domain, prs_with_status):
    if not prs_with_status:
        return ""
    # Sort: merged first, then approved, then in_review
    order = {"merged": 0, "approved": 1, "in_review": 2}
    prs_with_status.sort(key=lambda x: order.get(x[1], 2))

    dot_info = DOMAIN_DOTS.get(domain)
    if dot_info:
        color, label = dot_info
        header = f'<img src="https://img.shields.io/badge/-{color}?style=flat-square" height="11" alt="" /> &nbsp;**{label}**'
    else:
        header = f"**{domain}**"
    lines = [
        header,
        "",
        "| Project | Fix | Type | Status |",
        "| :-- | :-- | :--: | :--: |",
    ]
    for pr, status in prs_with_status:
        lines.append(build_row(pr, status))
    return "\n".join(lines)


def main():
    prs = json.loads(PRS_FILE.read_text())

    # Group by domain, attach status
    domains = OrderedDict((d, []) for d in DOMAIN_ORDER)

    for pr in prs:
        status = get_pr_status(pr)
        print(f"  {pr['owner']}/{pr['repo']}#{pr['number']} -> {status}")
        if status in ("closed", "inaccessible"):
            continue
        domain = pr.get("domain", "Other")
        if domain not in domains:
            domains[domain] = []
        domains[domain].append((pr, status))

    # Count stats
    total = sum(len(v) for v in domains.values())
    merged = sum(1 for v in domains.values() for _, s in v if s == "merged")
    approved = sum(1 for v in domains.values() for _, s in v if s == "approved")
    repos = len(set(f'{pr["owner"]}/{pr["repo"]}' for v in domains.values() for pr, _ in v))

    stats = f"**{total} contributions** across **{repos} repos**"
    if merged:
        stats += f" · **{merged} merged**"
    if approved:
        stats += f" · **{approved} approved**"

    sections = [NARRATIVE, "", stats]

    for domain in DOMAIN_ORDER:
        s = build_domain_section(domain, domains.get(domain, []))
        if s:
            sections.append("")
            sections.append(s)

    # Handle any domains not in DOMAIN_ORDER
    for domain, prs_with_status in domains.items():
        if domain not in DOMAIN_ORDER and prs_with_status:
            sections.append("")
            sections.append(build_domain_section(domain, prs_with_status))

    generated = "\n".join(sections)
    content = f"{START_MARKER}\n\n{generated}\n\n{END_MARKER}"

    readme = README_FILE.read_text(encoding="utf-8")

    start = readme.find(START_MARKER)
    end = readme.find(END_MARKER)
    if start == -1 or end == -1:
        print("ERROR: markers not found in README.md", file=sys.stderr)
        sys.exit(1)

    new_readme = readme[:start] + content + readme[end + len(END_MARKER):]

    if new_readme == readme:
        print("No changes needed.")
        return

    README_FILE.write_text(new_readme, encoding="utf-8")
    print("README.md updated.")


if __name__ == "__main__":
    main()
