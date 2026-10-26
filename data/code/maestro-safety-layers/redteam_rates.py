"""redteam_rates.py — attack success rates with honest uncertainty.

Red-team results are small counts; a 95% Wilson interval shows how little
"2 of 40" proves. Counts are SCENARIO numbers for this article.
"""
from math import sqrt

RESULTS = {  # category: (successful attacks, attempts) for Maestro-1 candidate
    "prompt injection via repository files": (6, 80),
    "destructive command without confirmation": (1, 60),
    "secret exfiltration through tool calls": (2, 50),
    "harmful-content requests (general)": (3, 120),
    "gaming the tests (reward hacking probes)": (4, 40),
}

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

def main():
    for cat, (k, n) in RESULTS.items():
        lo, hi = wilson(k, n)
        print(f"{cat:42s} {k:2d}/{n:3d} = {k/n:5.1%}  95% CI [{lo:5.1%}, {hi:5.1%}]")
    k = sum(v[0] for v in RESULTS.values()); n = sum(v[1] for v in RESULTS.values())
    lo, hi = wilson(k, n)
    print(f"{'all categories':42s} {k:2d}/{n:3d} = {k/n:5.1%}  95% CI [{lo:5.1%}, {hi:5.1%}]")
    print("zero successes in 60 tries still allows a true rate up to "
          f"{wilson(0, 60)[1]:.1%}")

if __name__ == "__main__":
    main()
