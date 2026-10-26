#!/usr/bin/env python3
"""Find recursive-self-improvement style papers on arXiv that neither the Awesome-RSI catalog nor
data/rsi-supplement.json covers yet, and write them to data/rsi-candidates.json for human review.

    python3 scripts/discover_rsi_candidates.py --since 2026-06-01
    python3 scripts/discover_rsi_candidates.py --selftest          # offline parser check, no network

This only DISCOVERS. It never assigns a level (L1-L5) or family: that takes reading the paper, so candidates
are reviewed by a person (or a reviewing session) and moved into data/rsi-supplement.json with a rationale.
Needs network access to export.arxiv.org (not reachable from the authoring sandbox; runs in GitHub Actions).
arXiv asks API clients for at most one request every three seconds; this script waits 3.5 s.
arXiv metadata is CC0, so titles and abstract snippets may be stored.
"""

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "rsi-candidates.json"
API = "https://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom"}

# (term, weight). Matched case-insensitively on title + abstract.
TERMS = [
    ("recursive self-improvement", 4), ("recursively self-improving", 4), ("recursive self improvement", 4),
    ("self-improving agent", 3), ("self-improving ai", 3), ("self-improving system", 3), ("self-improvement of agent", 3),
    ("self-evolving agent", 3), ("self-evolving", 2), ("self-evolution", 2), ("self evolving", 2),
    ("evolving agent harness", 3), ("harness self-improvement", 3), ("agent harness", 1),
    ("automated ai research", 3), ("automating ai research", 3), ("autonomous research agent", 2), ("ai scientist", 2),
    ("self-referential", 2), ("godel machine", 3), ("gödel machine", 3), ("self-rewriting", 2), ("self-modifying", 2),
    ("improve itself", 2), ("improves itself", 2), ("meta-optimi", 2), ("self-play", 1), ("self-distillation", 1),
    ("bootstrapp", 1), ("experience-driven", 1), ("continual self", 2),
]
QUERIES = [
    'abs:"recursive self-improvement" OR ti:"recursive self-improvement"',
    'ti:"self-improving" OR ti:"self-evolving" OR ti:"self-evolution"',
    'abs:"self-improving agent" OR abs:"self-evolving agent" OR abs:"self-improving agents" OR abs:"self-evolving agents"',
    'abs:"agent harness" AND (abs:"self-improv" OR abs:"evolv")',
    'abs:"automating AI research" OR abs:"automated AI research" OR abs:"autonomous research agent"',
]


def ids_in_catalog():
    have = set()
    for f in ("data/rsi-papers.json", "data/rsi-supplement.json"):
        p = ROOT / f
        if p.exists():
            have |= {x["id"] for x in json.loads(p.read_text(encoding="utf-8"))["papers"]}
    return have


def parse_feed(xml_text):
    """Parse an arXiv Atom feed into dicts. Tolerant: skips entries missing an id or title."""
    out = []
    root = ET.fromstring(xml_text)
    for e in root.findall("a:entry", NS):
        raw = (e.findtext("a:id", default="", namespaces=NS) or "").strip()
        m = re.search(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", raw)
        title = re.sub(r"\s+", " ", (e.findtext("a:title", default="", namespaces=NS) or "")).strip()
        if not m or not title:
            continue
        summ = re.sub(r"\s+", " ", (e.findtext("a:summary", default="", namespaces=NS) or "")).strip()
        pub = (e.findtext("a:published", default="", namespaces=NS) or "")[:10]
        cats = [c.get("term") for c in e.findall("a:category", NS) if c.get("term")]
        out.append({"id": m.group(1), "title": title, "published": pub, "abstract": summ, "cats": cats})
    return out


def score(p):
    text = (p["title"] + " " + p["abstract"]).lower()
    hits = [(t, w) for t, w in TERMS if t in text]
    return sum(w for _, w in hits), [t for t, _ in hits]


def fetch(query, since, until, start=0, size=100):
    q = f"({query}) AND submittedDate:[{since.replace('-', '')}0000 TO {until.replace('-', '')}2359]"
    url = API + "?" + urllib.parse.urlencode({"search_query": q, "start": start, "max_results": size, "sortBy": "submittedDate", "sortOrder": "descending"})
    for n in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "FrontierAGI-Academy candidate finder"})
            return urllib.request.urlopen(req, timeout=90).read().decode("utf-8")
        except Exception as e:
            if n == 3:
                raise
            time.sleep(10 * 2 ** n)
            print(f"  retry after {e}", file=sys.stderr)


def selftest():
    xml = """<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom">
    <entry><id>http://arxiv.org/abs/2609.24972v2</id><published>2026-09-28T10:00:00Z</published><title>RRSI:  Regularized Recursive Self-Improvement
    of Agent Harnesses</title><summary>We study recursive self-improvement of agent harnesses.</summary><category term="cs.AI"/></entry>
    <entry><id>http://arxiv.org/abs/2609.00001v1</id><title>Unrelated vision paper</title><summary>Segmentation.</summary></entry>
    <entry><title>No id</title></entry></feed>"""
    rows = parse_feed(xml)
    assert [r["id"] for r in rows] == ["2609.24972", "2609.00001"], rows
    assert rows[0]["title"] == "RRSI: Regularized Recursive Self-Improvement of Agent Harnesses"
    s, hits = score(rows[0]); assert s >= 7 and "recursive self-improvement" in hits, (s, hits)
    assert score(rows[1])[0] == 0
    print("selftest ok")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2026-06-01")
    ap.add_argument("--until", default=date.today().isoformat())
    ap.add_argument("--min-score", type=int, default=3)
    ap.add_argument("--max", type=int, default=250)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    have, found, errors = ids_in_catalog(), {}, 0
    for q in QUERIES:
        try:
            rows = parse_feed(fetch(q, a.since, a.until))
        except Exception as e:
            errors += 1
            print(f"query failed: {q[:60]}: {e}", file=sys.stderr)
            continue
        print(f"{len(rows):3d} results for {q[:70]}")
        for r in rows:
            found.setdefault(r["id"], r)
        time.sleep(3.5)
    if not found:
        sys.exit("no arXiv results at all; nothing written (is export.arxiv.org reachable?)")
    hf = {}
    hp = ROOT / "data" / "hf-papers.json"
    if hp.exists():
        for ps in json.loads(hp.read_text(encoding="utf-8"))["months"].values():
            for p in ps:
                hf[p["id"]] = p["u"]
    cands = []
    for r in found.values():
        sc, hits = score(r)
        if r["id"] in have or sc < a.min_score:
            continue
        cands.append({"id": r["id"], "title": r["title"], "published": r["published"], "score": sc, "hits": hits,
                      "cats": r["cats"][:4], "abstract": r["abstract"][:900], "hf_upvotes": hf.get(r["id"])})
    cands.sort(key=lambda c: c["published"], reverse=True)
    cands.sort(key=lambda c: -c["score"])
    cands = cands[: a.max]
    data = {"about": "Papers found on arXiv by keyword search that neither the Awesome-RSI catalog nor data/rsi-supplement.json covers. Candidates only: no level or family is assigned. Review each, then move accepted ones to data/rsi-supplement.json with a rationale.",
            "generated": datetime.utcnow().strftime("%Y-%m-%d"), "since": a.since, "until": a.until,
            "source": "arXiv API (metadata is CC0)", "papers": cands}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT.name}: {len(cands)} candidates from {len(found)} arXiv results ({errors} query errors)")
    if errors == len(QUERIES):
        sys.exit(2)


if __name__ == "__main__":
    main()
