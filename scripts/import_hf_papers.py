#!/usr/bin/env python3
"""Refresh data/hf-papers.json from Hugging Face Daily Papers (community-voted).

    python3 scripts/import_hf_papers.py --from 2023-05 --top 50     # needs network access to huggingface.co
    python3 scripts/import_hf_papers.py --dump-dir exports/          # offline: read saved API JSON, see below
    python3 scripts/import_hf_papers.py --relabel                    # re-run the theme rules on the saved file

Network is only needed for the fetch; build.py never touches it. Only ids, titles, upvote and comment counts and
our own theme labels are stored (no abstracts). The API shape was not verified from the build sandbox (huggingface.co
is blocked there), so field access is defensive: unknown fields are skipped, and the script prints how many rows
it could not read. Offline mode expects files named YYYY-MM-DD.json, each the JSON returned by
https://huggingface.co/api/daily_papers?date=YYYY-MM-DD
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date, timedelta
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "hf-papers.json"
API = "https://huggingface.co/api/daily_papers?date={d}"

# code, name, colour, keyword rules (lower-case substrings matched on title + HF keywords). First best score wins.
THEMES = [
    ["reason", "Reasoning & RL post-training", "#7c3aed", ["reasoning", "chain-of-thought", "reinforcement learning", " rl ", "rlvr", "grpo", "reward model", "math", "post-training", "thinking"]],
    ["agent", "Agents & tool use", "#ea580c", ["agent", "tool use", "tool-use", "computer use", "gui", "web navigation", "swe-bench", "coding agent", "mcp"]],
    ["mm", "Multimodal understanding", "#2563eb", ["multimodal", "vision-language", "vlm", "mllm", "visual question", "image understanding", "video understanding", "omni"]],
    ["gen", "Image & video generation", "#db2777", ["diffusion", "text-to-image", "text-to-video", "video generation", "image generation", "image editing", "flow matching", "3d generation", "world model"]],
    ["speech", "Speech & audio", "#0891b2", ["speech", "audio", "tts", "asr", "voice", "music generation", "text-to-speech"]],
    ["eff", "Efficiency & inference", "#16a34a", ["efficient", "quantization", "distillation", "speculative decoding", "kv cache", "sparse attention", "mixture-of-experts", "moe", "inference", "pruning", "compression", "long-context", "long context"]],
    ["data", "Data & synthetic data", "#ca8a04", ["dataset", "synthetic data", "data curation", "data selection", "pretraining data", "corpus", "data mixture"]],
    ["eval", "Evaluation & benchmarks", "#64748b", ["benchmark", "evaluation", "evaluating", "leaderboard", "judge", "survey"]],
    ["safe", "Safety & alignment", "#be123c", ["safety", "alignment", "jailbreak", "hallucination", "trustworthy", "red teaming", "interpretability", "bias"]],
    ["embody", "Robotics & embodied AI", "#0d9488", ["robot", "embodied", "vision-language-action", "vla", "manipulation", "navigation", "autonomous driving"]],
    ["sci", "Science & domain models", "#8b5cf6", ["protein", "biology", "chemistry", "medical", "clinical", "scientific", "physics", "finance", "legal", "code generation", "geospatial"]],
    ["arch", "Architectures & training", "#0ea5e9", ["architecture", "transformer", "state space", "mamba", "attention", "pre-training", "pretraining", "scaling law", "optimizer", "tokenizer", "instruction tuning", "fine-tun", "lora", "model merging", "imitation"]],
    ["vision", "3D & vision tasks", "#d946ef", ["3d", "gaussian splatting", "radiance field", "nerf", "segmentation", "depth estimation", "object detection", "avatar", "novel-view", "tracking", "image restoration"]],
    ["rag", "Retrieval & RAG", "#f43f5e", ["retrieval", "rag", "recommend", "question answering", "document"]],
    ["other", "Other", "#94a3b8", []],
]


def label(title, kws):
    text = " " + (title + " " + " ".join(kws)).lower() + " "
    best, score = "other", 0
    hits = {}
    for code, _, _, rules in THEMES:
        n = sum(1 for r in rules if r in text)
        if n:
            hits[code] = n
    for code, n in sorted(hits.items(), key=lambda kv: (-kv[1], [t[0] for t in THEMES].index(kv[0]))):
        best, score = code, n
        break
    tags = [c for c in hits if c != best][:2]
    return best, tags


def rows_from(payload):
    out, bad = [], 0
    for r in payload if isinstance(payload, list) else []:
        p = r.get("paper") or {}
        pid = p.get("id") or r.get("id")
        title = p.get("title") or r.get("title")
        if not (pid and title and re.fullmatch(r"\d{4}\.\d{4,5}", str(pid))):
            bad += 1
            continue
        kws = [k for k in (p.get("ai_keywords") or []) if isinstance(k, str)]
        up = p.get("upvotes", r.get("upvotes", 0))
        cm = r.get("numComments", p.get("numComments", 0))
        out.append({"id": str(pid), "ti": re.sub(r"\s+", " ", title).strip(), "u": int(up or 0), "c": int(cm or 0), "kw": kws[:8]})
    return out, bad


def month_days(ym):
    y, m = int(ym[:4]), int(ym[5:])
    d = date(y, m, 1)
    while d.month == m and d <= date.today():
        yield d
        d += timedelta(days=1)


def months_between(a, b):
    y, m = int(a[:4]), int(a[5:])
    while f"{y:04d}-{m:02d}" <= b:
        yield f"{y:04d}-{m:02d}"
        m += 1
        if m == 13:
            y, m = y + 1, 1


def fetch_day(d, tries=6):
    """One day of Daily Papers. Retries 429/5xx with backoff (honours Retry-After); raises if it still fails."""
    headers = {"User-Agent": "FrontierAGI-Academy importer"}
    if os.environ.get("HF_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["HF_TOKEN"]
    for n in range(tries):
        try:
            req = urllib.request.Request(API.format(d=d.isoformat()), headers=headers)
            return json.loads(urllib.request.urlopen(req, timeout=60).read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or n == tries - 1:
                raise
            wait = int(e.headers.get("Retry-After") or 0) or 15 * 2 ** n
            print(f"  {d}: HTTP {e.code}, waiting {wait}s (try {n + 1}/{tries})", file=sys.stderr)
            time.sleep(min(wait, 300))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", default="2023-05")
    ap.add_argument("--to", default=(date.today().replace(day=1) - timedelta(days=1)).strftime("%Y-%m"), help="last month to fetch (default: last complete month)")
    ap.add_argument("--top", type=int, default=50)
    ap.add_argument("--dump-dir")
    ap.add_argument("--relabel", action="store_true")
    ap.add_argument("--include-current", action="store_true", help="also fetch the current, incomplete month and flag it as partial (in progress) in the data")
    ap.add_argument("--resume", action="store_true", help="keep months already in the file (except the newest, which may be partial) and fetch only the rest")
    ap.add_argument("--pause", type=float, default=1.2, help="seconds between requests")
    a = ap.parse_args()
    cur = date.today().strftime("%Y-%m")
    if a.include_current and a.to < cur:
        a.to = cur

    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else None
    if a.relabel:
        if not old:
            sys.exit("nothing to relabel: data/hf-papers.json does not exist")
        for ps in old["months"].values():
            for p in ps:
                p["th"], p["tg"] = label(p["ti"], p.get("kw", []))
        months = old["months"]
    else:
        months, bad_total, incomplete = {}, 0, []
        kept = {}
        if a.resume and old:
            stale = set(old.get("partial", []))
            kept = {m: v for m, v in old["months"].items() if m not in stale and a.start <= m <= a.to}
            print(f"resuming: keeping {len(kept)} saved months, refetching the rest" + (f" (including in-progress {', '.join(sorted(stale))})" if stale else ""))
        for ym in months_between(a.start, a.to):
            if ym in kept:
                months[ym] = kept[ym]
                continue
            seen, failed = {}, 0
            for d in month_days(ym):
                try:
                    if a.dump_dir:
                        f = Path(a.dump_dir) / f"{d.isoformat()}.json"
                        if not f.exists():
                            continue
                        payload = json.loads(f.read_text(encoding="utf-8"))
                    else:
                        payload = fetch_day(d)
                        time.sleep(a.pause)
                except Exception as e:
                    print(f"FAILED {d}: {e}", file=sys.stderr)
                    failed += 1
                    continue
                rows, bad = rows_from(payload)
                bad_total += bad
                for r in rows:
                    if r["id"] not in seen or r["u"] > seen[r["id"]]["u"]:
                        seen[r["id"]] = r
            if failed:
                incomplete.append(ym)
                print(f"{ym}: {failed} day(s) failed, month NOT saved (a partial month would skew the charts)", file=sys.stderr)
                continue
            top = sorted(seen.values(), key=lambda r: (-r["u"], r["id"]))[: a.top]
            for r in top:
                r["th"], r["tg"] = label(r["ti"], r["kw"])
            if top:
                months[ym] = top
                print(ym, len(top), "papers")
        if bad_total:
            print(f"warning: {bad_total} rows had an unexpected shape and were skipped", file=sys.stderr)
        if not months:
            sys.exit("no papers read; nothing written (is huggingface.co reachable, or is --dump-dir right?)")

    data = {
        "about": "Generated by scripts/import_hf_papers.py from Hugging Face Daily Papers. Per month: the top papers by upvotes. th = primary theme from keyword rules on title + HF keywords (see THEMES in the script), tg = up to two secondary themes. u = upvotes, c = comments at fetch time.",
        "source": {"name": "Hugging Face Daily Papers", "url": "https://huggingface.co/papers", "retrieved": date.today().isoformat(), "top": a.top},
        "themes": [[t[0], t[1], t[2]] for t in THEMES],
        "months": dict(sorted(months.items())),
    }
    if not a.relabel:
        part = [cur] if (a.include_current and cur in months) else []
    else:
        part = [m for m in (old or {}).get("partial", []) if m in months]
    if part:
        data["partial"] = part
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    n = sum(len(v) for v in months.values())
    other = sum(1 for v in months.values() for p in v if p["th"] == "other")
    print(f"wrote {OUT.name}: {n} papers over {len(months)} months; 'Other' = {other} ({100 * other // max(n, 1)}%)")
    if not a.relabel and incomplete:
        print(f"INCOMPLETE months not saved: {', '.join(incomplete)}. Re-run with --resume (add HF_TOKEN to raise rate limits).", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
