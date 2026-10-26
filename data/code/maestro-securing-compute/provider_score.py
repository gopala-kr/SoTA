"""provider_score.py — compare GPU cloud offers on cost per USEFUL GPU-hour.

The list price is not the price. What matters is how many hours of real
training you get per dollar, after the cluster's own failures, slow
hand-offs and the support you will need at 3 a.m.
Providers P1-P4 are illustrative offers, not real quotes.
"""
GPUS = 1024            # Maestro-1 main run (Part 3)
MONTHS = 12            # reservation length

# name, $/GPU-hr, availability (fraction of hours the reserved nodes are up),
# goodput (fraction of up-hours doing useful training: restarts, slow nodes),
# hours to replace a failed node, network rating 1-5, support rating 1-5,
# security rating 1-5, upfront payment fraction
OFFERS = [
    ("P1 neocloud, top-rated",   2.65, 0.990, 0.93, 4,  5, 5, 4, 0.25),
    ("P2 neocloud, cheap",       2.10, 0.960, 0.85, 48, 3, 2, 3, 0.50),
    ("P3 hyperscaler",           3.40, 0.995, 0.92, 2,  4, 4, 5, 0.00),
    ("P4 broker, mixed sites",   1.95, 0.940, 0.80, 72, 2, 2, 2, 1.00),
]
WEIGHTS = {"cost": 0.40, "network": 0.20, "support": 0.20, "security": 0.20}

def useful_cost(price, avail, goodput):
    # you pay for every reserved hour; you only get avail*goodput of it
    return price / (avail * goodput)

def main():
    hours = MONTHS * 730
    rows = []
    for n, p, a, g, rep, net, sup, sec, up in OFFERS:
        u = useful_cost(p, a, g)
        rows.append((n, p, u, rep, net, sup, sec, up, p * GPUS * hours))
    best = min(r[2] for r in rows)
    print(f"{'offer':26s} {'list':>6s} {'useful':>7s} {'repl h':>6s} {'contract':>9s} {'upfront':>8s} {'score':>6s}")
    scored = []
    for n, p, u, rep, net, sup, sec, up, total in rows:
        s = (WEIGHTS["cost"] * 5 * best / u + WEIGHTS["network"] * net
             + WEIGHTS["support"] * sup + WEIGHTS["security"] * sec)
        scored.append((s, n))
        print(f"{n:26s} ${p:5.2f} ${u:6.2f} {rep:6d} ${total/1e6:7.1f}M ${total*up/1e6:6.1f}M {s:6.2f}")
    scored.sort(reverse=True)
    print("ranking:", " > ".join(n.split()[0] for _, n in scored))
    # what a 10-point goodput gap costs on the 31-day main run
    run_h = 31 * 24 * GPUS
    print(f"main run = {run_h:,} GPU-hours of useful work; at P2 that needs "
          f"{run_h/(0.96*0.85):,.0f} paid hours vs {run_h/(0.99*0.93):,.0f} at P1")

if __name__ == "__main__":
    main()
