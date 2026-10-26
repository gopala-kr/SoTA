"""nccl_check.py — read nccl-tests all_reduce_perf output and flag bad nodes.

Usage: python3 nccl_check.py [log ...]. With no file it parses SAMPLE,
a log written for this article in the nccl-tests format (not from a real
cluster) so the parser and the maths can be checked.
"""
import re, sys

# Pairwise 2-node runs (16 GPUs): node pair -> busbw at 8 GB messages.
SAMPLE = """\
# pair node001,node002
  8589934592    2147483648     float     sum      -1  45210  190.00  356.25      0
# pair node003,node004
  8589934592    2147483648     float     sum      -1  45480  188.87  354.13      0
# pair node005,node006
  8589934592    2147483648     float     sum      -1  98120   87.54  164.14      0
# pair node007,node008
  8589934592    2147483648     float     sum      -1  45390  189.24  354.83      0
"""
ROW = re.compile(r"^\s*(\d+)\s+(\d+)\s+\w+\s+\w+\s+-?\d+\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+(\d+)")

def busbw_factor(n):
    # all-reduce moves 2(n-1)/n of the data per rank (nccl-tests PERFORMANCE.md)
    return 2 * (n - 1) / n

def parse(text):
    out, pair = [], None
    for line in text.splitlines():
        if line.startswith("# pair"):
            pair = line.split()[2]
        m = ROW.match(line)
        if m and pair:
            size, t_us, alg, bus, wrong = int(m[1]), float(m[3]), float(m[4]), float(m[5]), int(m[6])
            out.append((pair, size, t_us, alg, bus, wrong))
    return out

def main():
    text = "".join(open(f).read() for f in sys.argv[1:]) if sys.argv[1:] else SAMPLE
    rows = parse(text)
    n = 16
    f = busbw_factor(n)
    print(f"ranks={n}: busbw = algbw x {f:.4f}")
    best = max(r[4] for r in rows)
    for pair, size, t, alg, bus, wrong in rows:
        alg_calc = size / (t * 1e-6) / 1e9
        flag = "OK" if bus >= 0.9 * best and wrong == 0 else "SUSPECT"
        print(f"{pair:18s} algbw {alg:6.2f} (recalc {alg_calc:6.2f}) busbw {bus:6.2f} GB/s "
              f"x{f:.4f}={alg*f:6.2f}  {flag}")
    bad = [r[0] for r in rows if r[4] < 0.9 * best]
    print("drain and re-test individually:", ", ".join(bad) if bad else "none")

if __name__ == "__main__":
    main()
