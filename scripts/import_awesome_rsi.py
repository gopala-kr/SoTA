#!/usr/bin/env python3
"""Refresh data/rsi-papers.json from the Awesome-RSI catalog (CC0-1.0).

    python3 scripts/import_awesome_rsi.py            # fetch README from GitHub raw
    python3 scripts/import_awesome_rsi.py --file README.md

Source: https://github.com/theseus-labs-rsi/awesome-rsi (companion to arXiv:2609.11873).
Needs network access only for the fetch; build.py itself never touches the network.
"""

import argparse
import html
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

RAW = "https://raw.githubusercontent.com/theseus-labs-rsi/awesome-rsi/main/README.md"
OUT = Path(__file__).resolve().parent.parent / "data" / "rsi-papers.json"

LEVELS = [
    [1, "L1", "Improvement execution", "Executes a human-defined improvement procedure; accepted results persist.", "#2563eb"],
    [2, "L2", "Improvement strategy", "Chooses how to improve a target; the objective and acceptance rule stay external.", "#7c3aed"],
    [3, "L3", "Future learning experience", "The learner's state shapes which experience, tasks or curriculum it gets next.", "#ea580c"],
    [4, "L4", "Deployment adaptation", "Keeps memory, skills or agent components that change later behaviour, inside a fixed improvement process.", "#16a34a"],
    [5, "L5", "Meta-improvement", "Improves the mechanism that produces future improvements: search, evaluation, research control.", "#be123c"],
]
FAMILIES = [
    ["1", "Prompt & Context", "#0ea5e9"], ["2", "Memory & Knowledge", "#8b5cf6"], ["3", "Harness / Workflow", "#14b8a6"],
    ["4", "Tools & Skills", "#f59e0b"], ["5", "Model", "#ef4444"], ["6", "Trainer / Optimization", "#ec4899"],
    ["7", "Evaluator & Feedback", "#84cc16"], ["8", "Data & Environment", "#64748b"], ["9", "External Artifact", "#f97316"],
    ["10", "Full-system / Co-evolution", "#0f172a"],
]
FAM_BY_NAME = {"prompt & context": "1", "memory & knowledge": "2", "harness / workflow": "3", "tools & skills": "4", "model": "5",
               "trainer / optimization": "6", "evaluator & feedback": "7", "data & environment": "8", "external artifact": "9",
               "full-system / co-evolution": "10"}


def short_name(title):
    m = re.search(r"\(([^()]{2,14})\)\s*$", title)
    if m and not m.group(1).lower().startswith(("part", "and ")):
        return m.group(1)
    head = title.split(":")[0].strip()
    return head if len(head) <= 44 else head[:43].rsplit(" ", 1)[0] + "…"


def clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"\*\*|\\", "", s))).strip()


def parse(text):
    first = re.search(r"^## 1\. L1", text, re.M).start()
    end = re.search(r"^## Contributing", text, re.M).start()
    body = text[first:end]
    secs = [(m.start(), int(m.group(1))) for m in re.finditer(r"^## (\d)\. L\d ", body, re.M)]
    lvl_at = lambda p: [l for s, l in secs if s <= p][-1]

    feat = {}
    for m in re.finditer(r"^### Featured representative papers\n\n\| Paper \| Representative mechanism \|\n\| --- \| --- \|\n((?:\|[^\n]*\n)+)", body, re.M):
        for r in m.group(1).strip().split("\n"):
            mm = re.match(r"\| \[(.+?)\]\(https://arxiv.org/abs/(\d{4}\.\d{4,5})\) \| (.+) \|$", r)
            if mm:
                feat[mm.group(2)] = (clean(mm.group(1)), clean(mm.group(3)))

    starts = list(re.finditer(r"^1\. \*\*(.+?)\*\*(?:<br>)?[ ]*$", body, re.M))
    papers, seen = [], set()
    for i, m in enumerate(starts):
        seg = body[m.end():(starts[i + 1].start() if i + 1 < len(starts) else len(body))]
        seg = re.split(r"\n</details>|\n### |\n## ", seg)[0]
        aid = re.search(r"arXiv:(\d{4}\.\d{4,5})", seg)
        if not aid or aid.group(1) in seen:
            continue
        aid = aid.group(1)
        seen.add(aid)
        lv = re.search(r"Level--L(\d)", seg)
        tg = re.search(r"Target--(.+?)-[0-9a-f]{6}\)", seg)
        fam_name = clean(tg.group(1).replace("_", " ").replace("%2F", "/").replace("--", "-")).lower() if tg else ""
        upd = re.search(r"\*Updated object\(s\):\*\s*([^\n]+)", seg)
        upd = clean(upd.group(1)).rstrip(".") if upd else ""
        codes = sorted(set(re.findall(r"(?:^|;\s*)(\d+)\.\d+ ", upd)), key=int)
        primary = FAM_BY_NAME.get(fam_name) or (codes[0] if codes else "5")
        fams = [primary] + [c for c in codes if c != primary]
        rat = re.search(r"\*(?:Survey-table|Editorial) rationale:\*\s*(.*?)\s*\*Updated object", seg, re.S)
        title = clean(m.group(1))
        p = {"id": aid, "d": "20" + aid[:2] + "-" + aid[2:4], "t": title, "s": short_name(title),
             "l": int(lv.group(1)) if lv else lvl_at(m.start()), "f": primary, "o": fams, "u": upd}
        if rat:
            p["r"] = clean(rat.group(1))
        if aid in feat:
            p["star"] = 1
            p["s"] = feat[aid][0]
            p["m"] = feat[aid][1]
        papers.append(p)
    papers.sort(key=lambda p: (p["d"], p["id"]), reverse=True)

    a = text.index("## Public Industry Practices")
    b = text.index("## Table of Contents")
    industry = []
    for row in [r for r in text[a:b].split("\n") if r.startswith("| 20")]:
        c = [x.strip() for x in re.split(r"(?<!\\)\|", row)[1:-1]]
        mm = re.match(r"\[(.+?)\]\((https?://[^)]+)\)", c[1])
        org, _, ttl = clean(mm.group(1)).partition(" — ")
        industry.append({"date": c[0], "org": org.strip(), "title": ttl.strip("* ").strip(), "url": mm.group(2),
                         "practice": clean(c[2]), "result": clean(c[3])})
    return papers, industry


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file")
    args = ap.parse_args()
    text = Path(args.file).read_text(encoding="utf-8") if args.file else urllib.request.urlopen(RAW, timeout=60).read().decode("utf-8")
    papers, industry = parse(text)
    data = {
        "about": "Generated by scripts/import_awesome_rsi.py from the Awesome-RSI catalog. Papers keep their arXiv id, autonomy level (l), primary family (f), all touched families (o) and updated objects (u). star=1 marks the catalog's featured papers (m = its mechanism note); r = written rationale where the catalog has one.",
        "source": {"name": "Awesome Recursive Self-Improvement (theseus-labs-rsi/awesome-rsi)", "repo": "https://github.com/theseus-labs-rsi/awesome-rsi",
                   "survey": "https://arxiv.org/abs/2609.11873", "surveyTitle": "The Last AI Built by Humans: Toward Genuine Recursive Self-Improvement",
                   "license": "CC0-1.0", "retrieved": date.today().isoformat()},
        "levels": LEVELS, "families": FAMILIES, "papers": papers, "industry": industry,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(OUT.parent.parent)}: {len(papers)} papers ({sum(1 for p in papers if p.get('star'))} featured), {len(industry)} industry cases")


if __name__ == "__main__":
    sys.exit(main())
