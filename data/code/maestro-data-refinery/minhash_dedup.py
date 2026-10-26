"""minhash_dedup.py — near-duplicate detection with MinHash + LSH bands.

Exact hashing misses pages that differ by a date or a menu; MinHash
estimates Jaccard similarity of word 5-gram sets cheaply, and banding
finds candidate pairs without comparing every pair. Documents are
written for this article. Standard library only; fixed seeds.
"""
import hashlib, itertools, random

DOCS = {
    "a": "the cluster uses three power feeds per rack so that losing one feed leaves four of six supplies running in every node",
    "b": "the cluster uses three power feeds per rack so that losing one feed leaves four of six supplies running in every node updated 2026",
    "c": "posted today: the cluster uses three power feeds per rack so that losing one feed leaves four of six supplies running in every node",
    "d": "gradient checkpointing trades extra compute in the backward pass for a large reduction in activation memory during training",
    "e": "a mixture of experts routes each token to a few experts so that total parameters grow while compute per token stays fixed",
}
K, PERM, BANDS = 5, 128, 32          # 5-word shingles, 128 hashes, 32 bands of 4 rows

def shingles(t):
    w = t.split()
    return {" ".join(w[i:i + K]) for i in range(len(w) - K + 1)}

def h(s, seed):
    return int.from_bytes(hashlib.blake2b(f"{seed}:{s}".encode(), digest_size=8).digest(), "big")

def signature(sh):
    return [min(h(s, i) for s in sh) for i in range(PERM)]

def main():
    sh = {k: shingles(v) for k, v in DOCS.items()}
    sig = {k: signature(v) for k, v in sh.items()}
    rows = PERM // BANDS
    buckets = {}
    for k, s in sig.items():
        for b in range(BANDS):
            buckets.setdefault((b, tuple(s[b * rows:(b + 1) * rows])), set()).add(k)
    cand = {tuple(sorted(p)) for ks in buckets.values() if len(ks) > 1 for p in itertools.combinations(ks, 2)}
    print(f"{'pair':5s} {'true Jaccard':>12s} {'MinHash est':>11s}  candidate?")
    for a, b in itertools.combinations(sorted(DOCS), 2):
        j = len(sh[a] & sh[b]) / len(sh[a] | sh[b])
        est = sum(x == y for x, y in zip(sig[a], sig[b])) / PERM
        print(f"{a}-{b}   {j:12.2f} {est:11.2f}  {'yes' if (a, b) in cand else 'no'}")
    keep, drop = [], set()
    for a, b in sorted(cand):
        if sum(x == y for x, y in zip(sig[a], sig[b])) / PERM >= 0.7:
            drop.add(b)
    print("drop as near-duplicates:", ", ".join(sorted(drop)) or "none")
    # probability a pair with similarity s becomes a candidate: 1-(1-s^r)^b
    for s in (0.5, 0.7, 0.8, 0.9):
        print(f"  P(candidate | similarity {s}) = {1 - (1 - s ** rows) ** BANDS:.3f}")

if __name__ == "__main__":
    random.seed(0); main()
