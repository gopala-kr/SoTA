"""paired_ci.py — is the difference between two arms real, or luck?

Both arms run the SAME tasks, so compare them task by task (a paired test) and
bootstrap a confidence interval for the difference in success rate. Gopala's
rule: proceed only if the 95% interval for (skills − base) is entirely above 0.

  python3 paired_ci.py            # runs a self-check on simulated outcomes
"""
import random


def paired_bootstrap(a, b, iters=10_000, seed=0):
    """a, b: lists of 0/1 outcomes per task for arm A and arm B (same order)."""
    rng, n = random.Random(seed), len(a)
    diffs = []
    for _ in range(iters):
        idx = [rng.randrange(n) for _ in range(n)]
        diffs.append(sum(b[i] - a[i] for i in idx) / n)
    diffs.sort()
    return sum(y - x for x, y in zip(a, b)) / n, diffs[int(0.025 * iters)], diffs[int(0.975 * iters)]


if __name__ == "__main__":
    # Self-check with SIMULATED outcomes (not results): 300 tasks, true rates 40% vs 47%.
    rng = random.Random(1)
    base = [int(rng.random() < 0.40) for _ in range(300)]
    skills = [max(x, int(rng.random() < 0.12)) for x in base]     # skills help some tasks, rarely hurt
    d, lo, hi = paired_bootstrap(base, skills)
    print(f"simulated: base {sum(base)}/300, skills {sum(skills)}/300, diff {d:+.3f}, 95% CI [{lo:+.3f}, {hi:+.3f}]")
    print("decision:", "proceed" if lo > 0 else "not proven")
