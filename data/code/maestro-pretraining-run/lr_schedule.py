"""lr_schedule.py — cosine vs warmup-stable-decay (WSD) learning rates.

Cosine decays from the start, so the run length must be fixed in
advance. WSD (used by MiniCPM, 2024) holds the rate flat and decays only
at the end, so a run can be extended, and a decayed checkpoint can be
branched off at any point to check progress. Numbers are our plan.
"""
import math

PEAK, MIN_FRAC, WARM, TOTAL = 3e-4, 0.1, 2_000, 600_000   # steps (16.8M-token batches ~ 10T tokens)
DECAY_FRAC = 0.15

def cosine(s):
    if s < WARM: return PEAK * s / WARM
    p = (s - WARM) / (TOTAL - WARM)
    return PEAK * (MIN_FRAC + (1 - MIN_FRAC) * 0.5 * (1 + math.cos(math.pi * p)))

def wsd(s):
    if s < WARM: return PEAK * s / WARM
    start = TOTAL * (1 - DECAY_FRAC)
    if s < start: return PEAK
    p = (s - start) / (TOTAL - start)
    return PEAK * (MIN_FRAC + (1 - MIN_FRAC) * (1 - p))

def main():
    print(f"tokens per step = {16.8e6:,.0f} -> {TOTAL*16.8e6/1e12:.1f}T tokens")
    print(f"{'step':>8s} {'% run':>6s} {'cosine':>9s} {'WSD':>9s}")
    for s in (0, 1_000, 2_000, 60_000, 150_000, 300_000, 450_000, 510_000, 555_000, 600_000):
        print(f"{s:8,d} {s/TOTAL:6.0%} {cosine(s):9.2e} {wsd(s):9.2e}")
    area = lambda f: sum(f(s) for s in range(0, TOTAL, 1000))
    print(f"average LR: cosine {area(cosine)/(TOTAL/1000):.2e}, WSD {area(wsd)/(TOTAL/1000):.2e}")

if __name__ == "__main__":
    main()
