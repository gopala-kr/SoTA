"""mixture.py — plan Maestro-1's 10T-token mixture and check repetition.

A target share per source, the unique tokens available after filtering,
and how many times each source must be repeated (epochs). Repeating a
source a few times is mostly fine; many more starts to waste compute
(Muennighoff et al., 2023, "Scaling Data-Constrained Language Models").
Available-token figures are our planning assumptions, not measurements.
"""
TOTAL = 10e12
# source: (target share, unique tokens available after filtering)
SRC = {
    "web (filtered, deduplicated)": (0.55, 9.0e12),
    "code (permissive licences)":   (0.20, 1.2e12),
    "maths and science":            (0.08, 0.35e12),
    "books and long documents":     (0.05, 0.25e12),
    "multilingual web":             (0.07, 1.5e12),
    "verified skills (partners)":   (0.02, 0.02e12),
    "synthetic (from verified)":    (0.03, 0.15e12),
}

def main():
    assert abs(sum(s for s, _ in SRC.values()) - 1) < 1e-9
    print(f"{'source':30s} {'share':>6s} {'tokens':>8s} {'unique':>8s} {'epochs':>7s}")
    for name, (share, avail) in SRC.items():
        t = share * TOTAL
        ep = t / avail
        flag = "  <- heavy repetition" if ep > 4 else ("  <- repeated" if ep > 1 else "")
        print(f"{name:30s} {share:6.0%} {t/1e12:7.2f}T {avail/1e12:7.2f}T {ep:7.1f}{flag}")
    uniq = sum(min(s * TOTAL, a) for s, a in SRC.values())
    print(f"unique tokens seen: {uniq/1e12:.2f}T of {TOTAL/1e12:.0f}T ({uniq/TOTAL:.0%})")

if __name__ == "__main__":
    main()
