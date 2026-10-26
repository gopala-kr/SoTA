"""scaling_fit.py — fit L(N) = E + A·N^(-alpha) to a ladder of small runs.

Input: one line per run, "params final_val_loss" (the last line printed by
train_tiny.py). Output: the fitted law and a prediction for bigger models.
Uses only numpy: a grid over (E, alpha) with least squares for A.

  python3 scaling_fit.py ladder.txt
"""
import sys
import numpy as np

rows = [tuple(map(float, l.split())) for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
N, Lv = np.array([r[0] for r in rows]), np.array([r[1] for r in rows])

best = None
for E in np.linspace(0, Lv.min() * 0.98, 200):          # irreducible loss below the best run
    for alpha in np.linspace(0.05, 1.0, 200):
        x = N ** -alpha
        A = np.dot(x, Lv - E) / np.dot(x, x)              # least squares for A given E, alpha
        err = np.mean((E + A * x - Lv) ** 2)
        if A > 0 and (best is None or err < best[0]):
            best = (err, E, A, alpha)

err, E, A, alpha = best
print(f"fit: L(N) = {E:.3f} + {A:.2f} * N^-{alpha:.3f}   (rmse {err**0.5:.4f} on {len(N)} runs)")
for n in N:
    print(f"  N={n:>10,.0f}  measured {Lv[list(N).index(n)]:.3f}  fitted {E + A * n ** -alpha:.3f}")
for n in (1e7, 1e8, 1e9):
    print(f"  predicted at N={n:.0e}: {E + A * n ** -alpha:.3f}  (extrapolation: treat with care)")
