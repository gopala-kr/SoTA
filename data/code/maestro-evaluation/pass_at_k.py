"""pass_at_k.py — the unbiased pass@k estimator (Chen et al., 2021, Codex paper).

Generate n samples per task, count c that pass the tests; the chance that
at least one of k random samples passes is 1 - C(n-c, k) / C(n, k).
Naively computing 1-(1-c/n)^k is biased. Counts below are made up.
"""
from math import comb

def pass_at_k(n, c, k):
    if n - c < k:
        return 1.0
    return 1 - comb(n - c, k) / comb(n, k)

TASKS = [(20, 0), (20, 1), (20, 5), (20, 12), (20, 20)]   # (samples, correct) per task

def main():
    print(f"{'n':>3s} {'c':>3s} {'pass@1':>7s} {'pass@5':>7s} {'pass@10':>8s} {'naive@10':>9s}")
    for n, c in TASKS:
        naive = 1 - (1 - c / n) ** 10
        print(f"{n:3d} {c:3d} {pass_at_k(n,c,1):7.3f} {pass_at_k(n,c,5):7.3f} {pass_at_k(n,c,10):8.3f} {naive:9.3f}")
    for k in (1, 5, 10):
        print(f"benchmark pass@{k}: {sum(pass_at_k(n, c, k) for n, c in TASKS) / len(TASKS):.3f}")

if __name__ == "__main__":
    main()
