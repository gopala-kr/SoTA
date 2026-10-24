#!/usr/bin/env python3
"""
Regenerates the Blog Posts table in README.md from blog/index.json.
Run manually or via GitHub Actions on every push.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
MANIFEST = ROOT / "blog" / "index.json"
README = ROOT / "README.md"
BASE_URL = "https://gopalakrbiec-ui.github.io/FrontierAGI-Academy"

MARKER_START = "<!-- BLOG_POSTS_START -->"
MARKER_END   = "<!-- BLOG_POSTS_END -->"

def _escape_cell(text):
    # Keep markdown table rows intact: escape pipes and collapse newlines.
    return text.replace("|", "\\|").replace("\n", " ").strip()

def _one_line_summary(excerpt, max_len=140):
    # Excerpts run multiple sentences; keep just the first sentence (or a
    # clean truncation) so the table stays scannable in one line per row.
    text = _escape_cell(excerpt)
    first_sentence_end = text.find(". ")
    candidate = text[:first_sentence_end + 1] if first_sentence_end != -1 else text
    if len(candidate) > max_len:
        candidate = candidate[:max_len].rsplit(" ", 1)[0] + "…"
    return candidate

def build_table(posts):
    # Newest first, consistent with the manifest's own top-to-bottom order.
    header = "| Article | Summary | Date |\n|---|---|---|"
    lines = [header]
    for p in posts:
        emoji    = p.get("emoji", "📝")
        title    = _escape_cell(p.get("title", "Untitled"))
        slug     = p.get("slug", "")
        summary  = _one_line_summary(p.get("excerpt", ""))
        date     = p.get("date", "")
        featured = " ⭐" if p.get("featured") else ""
        url      = f"{BASE_URL}/blog/{slug}.html"
        lines.append(f"| {emoji} [{title}]({url}){featured} | {summary} | {date} |")
    return "\n".join(lines)

def update_readme(check=False):
    with open(MANIFEST, encoding="utf-8") as f:
        data = json.load(f)
    posts = data.get("posts", [])

    with open(README, encoding="utf-8") as f:
        content = f.read()

    table = build_table(posts)
    new_block = f"{MARKER_START}\n{table}\n{MARKER_END}"

    pattern = re.compile(
        re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
        re.DOTALL
    )
    if not pattern.search(content):
        print("ERROR: markers not found in README.md")
        return 1

    updated = pattern.sub(lambda _: new_block, content)
    if check:
        return 0 if updated == content else 1
    with open(README, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"README updated — {len(posts)} post(s) written.")
    return 0

if __name__ == "__main__":
    import sys
    raise SystemExit(update_readme(check="--check" in sys.argv))
