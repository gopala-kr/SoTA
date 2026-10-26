"""paired_bootstrap.py — is Maestro-1 really better than Maestro-0?

Both models attempt the SAME tasks; a paired bootstrap resamples tasks
(not answers) to get a confidence interval for the difference. Then:
how many tasks are needed to detect a given improvement? Per-task results
are SIMULATED with a fixed seed, not real model results.
"""
import random

def simulate(n, p0, gain, rho_seed=11):
    rng = random.Random(rho_seed)
    out = []
    for _ in range(n):
        hard = rng.random()                     # shared task difficulty makes results correlated
        a = 1 if rng.random() < p0 * (1.6 - hard) else 0
        b = 1 if rng.random() < (p0 + gain) * (1.6 - hard) else 0
        out.append((a, b))
    return out

def paired_ci(pairs, reps=4000, seed=3):
    rng = random.Random(seed)
    n = len(pairs)
    diffs = []
    for _ in range(reps):
        s = [pairs[rng.randrange(n)] for _ in range(n)]
        diffs.append(sum(b - a for a, b in s) / n)
    diffs.sort()
    return diffs[int(0.025 * reps)], diffs[int(0.975 * reps)]

def main():
    pairs = simulate(500, 0.40, 0.04)
    a = sum(p[0] for p in pairs) / 500; b = sum(p[1] for p in pairs) / 500
    lo, hi = paired_ci(pairs)
    print(f"500 tasks: Maestro-0 {a:.1%}, Maestro-1 {b:.1%}, difference {b-a:+.1%}, 95% CI [{lo:+.1%}, {hi:+.1%}]")
    print("tasks needed so the 95% CI of a +4-point gain excludes zero (simulated):")
    for n in (100, 250, 500, 1000, 2000):
        lo, hi = paired_ci(simulate(n, 0.40, 0.04, rho_seed=n), reps=1500)
        print(f"  {n:5d} tasks: CI [{lo:+.1%}, {hi:+.1%}] -> {'detected' if lo > 0 else 'not detected'}")

if __name__ == "__main__":
    main()
