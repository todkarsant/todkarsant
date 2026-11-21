#!/usr/bin/env python3
"""Check PR statuses on GitHub and update README.md OSS sections."""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PRS_FILE = REPO_ROOT / "prs.json"
README_FILE = REPO_ROOT / "README.md"

START_MARKER = "<!-- AUTO:OSS:START -->"
END_MARKER = "<!-- AUTO:OSS:END -->"

GITHUB_API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")


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


def build_row(pr):
    owner, repo, number = pr["owner"], pr["repo"], pr["number"]
    url = f"https://github.com/{owner}/{repo}"
    pr_url = f"{url}/pull/{number}"
    return (
        f'| {pr["badge"]} **[{pr["display_name"]}]({url})** '
        f'`{pr["stars"]}` | {pr["description"]} | [{pr["fix"]}]({pr_url}) |'
    )


def build_section(title, prs):
    if not prs:
        return ""
    lines = [
        f"### {title}",
        "",
        "| Project | What it is | Fix |",
        "| :-- | :-- | :-- |",
    ]
    for pr in prs:
        lines.append(build_row(pr))
    return "\n".join(lines)


def main():
    prs = json.loads(PRS_FILE.read_text())

    buckets = {"merged": [], "approved": [], "in_review": []}

    for pr in prs:
        status = get_pr_status(pr)
        print(f"  {pr['owner']}/{pr['repo']}#{pr['number']} -> {status}")
        if status in buckets:
            buckets[status].append(pr)

    sections = []
    for key, title in [("merged", "Merged"), ("approved", "Approved"), ("in_review", "In review")]:
        s = build_section(title, buckets[key])
        if s:
            sections.append(s)

    generated = "\n\n".join(sections)
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
