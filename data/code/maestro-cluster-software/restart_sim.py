"""restart_sim.py — replay a 31-day run through the failure and restart logic.

Monte Carlo: failures arrive at random (exponential gaps) at a given
cluster MTTF. Each failure loses the work since the last checkpoint and
costs a recovery time that depends on whether a hot spare is free;
failed nodes come back after a repair time. Compares two failure rates:
the one scaled from Llama 3 (Part 7, ~49 h) and the much worse 7.9 h
reported for 1,024-GPU jobs in Meta's research clusters (A100s).
All timings are our assumptions. Fixed seed, so the output is reproducible.
"""
import random

DAYS, CKPT_H, SAVE_H = 31, 1.0, 30 / 3600
RECOVER_SPARE_H, RECOVER_WAIT_H, REPAIR_H = 10 / 60, 4.0, 48.0

def run(mttf_h, spares, seed):
    rng = random.Random(seed)
    t, lost, fails, waits, back = 0.0, 0.0, 0, 0, []
    end = DAYS * 24
    while True:
        gap = rng.expovariate(1 / mttf_h)
        if t + gap >= end:
            break
        t += gap; fails += 1
        back = [b for b in back if b > t]            # repaired nodes rejoin the spare pool
        lost += (t % CKPT_H)                           # work since last checkpoint
        if len(back) < spares:
            rec = RECOVER_SPARE_H
        else:
            rec = RECOVER_WAIT_H; waits += 1           # wait for the provider to swap a node
        back.append(t + REPAIR_H)
        lost += rec; t += rec
    saves = end / CKPT_H * SAVE_H
    return fails, waits, 1 - (lost + saves) / end

def main():
    print(f"{'cluster MTTF':>12s} {'spares':>6s} {'failures':>8s} {'no spare':>8s} {'goodput':>8s}")
    for mttf in (49.0, 7.9):
        for spares in (0, 4, 8):
            res = [run(mttf, spares, s) for s in range(200)]
            f = sum(r[0] for r in res) / len(res); w = sum(r[1] for r in res) / len(res)
            g = sum(r[2] for r in res) / len(res)
            print(f"{mttf:10.1f} h {spares:6d} {f:8.1f} {w:8.1f} {g:8.1%}")

if __name__ == "__main__":
    main()
