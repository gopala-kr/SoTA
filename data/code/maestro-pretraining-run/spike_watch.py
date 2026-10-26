"""spike_watch.py — catch loss spikes early and decide what to do.

A SIMULATED loss curve (smooth power-law decline plus noise, with two
injected spikes) is streamed through a detector that compares each step
with an exponential moving average and its running spread. Policy:
a short spike that recovers is logged; a spike that persists triggers a
rewind to the last good checkpoint and skipping the offending batches.
"""
import math, random

def loss_stream(n, seed=7):
    rng = random.Random(seed)
    for s in range(1, n + 1):
        base = 1.9 + 9.0 * s ** -0.35
        x = base + rng.gauss(0, 0.012)
        if 4200 <= s < 4206: x += 0.9           # brief spike (bad batch)
        if 7400 <= s < 7700: x += 0.6 * min(1, (s - 7400) / 10)   # persistent divergence
        yield s, x

def main():
    ema, var, alpha = None, 0.0, 0.02
    above, events = 0, []
    for s, x in loss_stream(9000):
        if ema is None: ema = x; continue
        z = (x - ema) / math.sqrt(var + 1e-9) if s > 200 else 0
        if z > 6:
            above += 1
            if above == 1: start = s
            if above == 50:
                events.append((start, "PERSISTENT", f"rewind to checkpoint before step {start}, skip batches {start}-{s}"))
        else:
            if 0 < above < 50:
                events.append((start, "transient", f"{above} steps above threshold, recovered: log and continue"))
            above = 0
            if z < 3:   # only learn from normal steps, so a spike cannot drag the baseline up
                d = x - ema; ema += alpha * d; var = (1 - alpha) * (var + alpha * d * d)
    for s, kind, action in events:
        print(f"step {s:5d}  {kind:10s} {action}")
    print(f"{len(events)} events in 9,000 simulated steps")

if __name__ == "__main__":
    main()
