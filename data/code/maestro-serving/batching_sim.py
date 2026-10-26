"""batching_sim.py — static vs continuous batching on one replica.

Requests arrive at random with random output lengths. Static batching
waits for the whole batch to finish before admitting new requests;
continuous batching (Orca, 2022; used by vLLM and others) admits a new
request as soon as any slot frees. One 'step' = one token for every
active request. SIMULATED workload, fixed seed.
"""
import random

def run(mode, slots=32, n=600, rate=0.9, seed=5):
    rng = random.Random(seed)
    arrivals, t = [], 0.0
    for _ in range(n):
        t += rng.expovariate(rate); arrivals.append((t, rng.choice([40, 80, 200, 600, 1500])))
    queue, active, done, step, i = [], [], [], 0, 0
    while len(done) < n:
        while i < n and arrivals[i][0] <= step:
            queue.append(arrivals[i]); i += 1
        if mode == "continuous" or not active:
            while queue and len(active) < slots:
                a, L = queue.pop(0); active.append([a, L, L])
        for r in active: r[2] -= 1
        for r in [r for r in active if r[2] <= 0]:
            active.remove(r); done.append(step + 1 - r[0])
        step += 1
    done.sort()
    return step, done[len(done) // 2], done[int(len(done) * 0.95)]

def main():
    for mode in ("static", "continuous"):
        steps, p50, p95 = run(mode)
        print(f"{mode:10s} finished 600 requests in {steps:6d} steps; latency p50 {p50:6.0f}, p95 {p95:6.0f} steps")

if __name__ == "__main__":
    main()
