#!/usr/bin/env python3
"""Add real citation counts from OpenAlex (open data, no key needed) to data/paper-impact.json.

    python3 scripts/enrich_citations.py                # every paper in the RSI catalog and supplement
    python3 scripts/enrich_citations.py --selftest      # offline parser check, no network

Papers are matched by their arXiv DOI (10.48550/arXiv.<id>). Missing papers are simply left out; a count of 0 is
real (brand-new papers have few citations), so the page only treats counts as meaningful for papers that are old
enough. Needs network access to api.openalex.org (not reachable from the authoring sandbox; runs in GitHub Actions).
"""

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "paper-impact.json"
API = "https://api.openalex.org/works"


def arxiv_from_doi(doi):
    m = re.search(r"10\.48550/arxiv\.(\d{4}\.\d{4,5})", (doi or "").lower())
    return m.group(1) if m else None


def parse_works(payload):
    """OpenAlex works response -> {arxiv_id: citation_count}. Tolerant of missing fields."""
    out = {}
    for w in payload.get("results", []) if isinstance(payload, dict) else []:
        aid = arxiv_from_doi(w.get("doi"))
        c = w.get("cited_by_count")
        if aid and isinstance(c, int) and c >= 0:
            out[aid] = max(c, out.get(aid, 0))
    return out


def fetch_batch(ids):
    flt = "doi:" + "|".join("https://doi.org/10.48550/arxiv." + i for i in ids)
    url = API + "?" + urllib.parse.urlencode({"filter": flt, "per-page": 50, "select": "doi,cited_by_count"})
    for n in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "FrontierAGI-Academy citation enrichment"})
            return json.loads(urllib.request.urlopen(req, timeout=60).read().decode("utf-8"))
        except Exception as e:
            if n == 3:
                raise
            time.sleep(5 * 2 ** n)
            print(f"  retry after {e}", file=sys.stderr)


def selftest():
    payload = {"results": [{"doi": "https://doi.org/10.48550/arxiv.2609.24972", "cited_by_count": 3},
                           {"doi": "https://doi.org/10.1234/other", "cited_by_count": 9},
                           {"doi": "https://doi.org/10.48550/arXiv.2203.14465", "cited_by_count": 700}, {"cited_by_count": 1}]}
    assert parse_works(payload) == {"2609.24972": 3, "2203.14465": 700}, parse_works(payload)
    assert arxiv_from_doi(None) is None
    print("selftest ok")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    ids = []
    for f in ("data/rsi-papers.json", "data/rsi-supplement.json"):
        p = ROOT / f
        if p.exists():
            ids += [x["id"] for x in json.loads(p.read_text(encoding="utf-8"))["papers"]]
    ids = sorted(set(ids))
    counts, failed = {}, 0
    for k in range(0, len(ids), 40):
        batch = ids[k:k + 40]
        try:
            counts.update(parse_works(fetch_batch(batch)))
        except Exception as e:
            failed += 1
            print(f"batch {k // 40} failed: {e}", file=sys.stderr)
        time.sleep(0.5)
    if not counts:
        sys.exit("no citation data returned; nothing written (is api.openalex.org reachable?)")
    old = {}
    if OUT.exists():
        old = json.loads(OUT.read_text(encoding="utf-8")).get("papers", {})
    merged = {**old, **{i: c for i, c in counts.items()}}
    data = {"about": "Citation counts from OpenAlex (cited_by_count), matched by arXiv DOI. Not every paper is indexed, and counts for papers under a few months old are not meaningful.",
            "source": "OpenAlex", "url": "https://openalex.org", "license": "CC0", "asof": date.today().isoformat(),
            "papers": dict(sorted(merged.items()))}
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"wrote {OUT.name}: {len(counts)} of {len(ids)} papers matched ({failed} failed batches)")
    if failed:
        sys.exit(2)


if __name__ == "__main__":
    main()
