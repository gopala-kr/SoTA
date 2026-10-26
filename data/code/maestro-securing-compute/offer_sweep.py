"""offer_sweep.py — when does the cheap offer really win?

Two questions the list price hides:
1. How good must the cheap offer's goodput be to match the premium one?
2. What does the whole contract cost once upfront cash, storage, egress
   and the cost of delay are counted?
All inputs are our assumptions; change them to your quotes.
"""
GPUS, MONTHS, H = 1024, 12, 730
P1 = dict(price=2.65, avail=0.990, good=0.93, upfront=0.25, storage=45_000, egress=0)
P2 = dict(price=2.10, avail=0.960, good=0.85, upfront=0.50, storage=60_000, egress=90_000)
CASH_RATE = 0.12        # yearly cost of cash tied up upfront (what else it could fund)
DELAY_WEEKS = {"P1": 0, "P2": 3}   # later delivery in the scenario
BURN_WEEK = 318_000 * 12 / 52      # Part 3 burn

def useful(o):
    return o["price"] / (o["avail"] * o["good"])

def contract(name, o):
    compute = o["price"] * GPUS * H * MONTHS
    cash = compute * o["upfront"] * CASH_RATE * (MONTHS / 12) / 2
    other = o["storage"] * MONTHS + o["egress"]
    delay = DELAY_WEEKS[name] * BURN_WEEK
    useful_h = GPUS * H * MONTHS * o["avail"] * o["good"]
    total = compute + cash + other + delay
    print(f"{name}: compute ${compute/1e6:5.2f}M + cash ${cash/1e6:4.2f}M + storage/egress "
          f"${other/1e6:4.2f}M + delay ${delay/1e6:4.2f}M = ${total/1e6:5.2f}M "
          f"-> ${total/useful_h:4.2f} per useful GPU-hour")
    return total / useful_h

def main():
    print(f"useful price: P1 ${useful(P1):.2f}  P2 ${useful(P2):.2f}")
    # break-even goodput for P2 against P1
    be = P2["price"] / (P2["avail"] * useful(P1))
    print(f"P2 matches P1 on useful price at goodput {be:.1%} (P1 needs {P1['good']:.0%})")
    print("goodput of P2 -> useful price")
    for g in (0.70, 0.75, 0.80, 0.85, 0.90, 0.95):
        u = P2["price"] / (P2["avail"] * g)
        bar = "#" * int((u - 2.0) * 20)
        print(f"  {g:.0%}  ${u:4.2f} {bar}{'  <- cheaper than P1' if u < useful(P1) else ''}")
    a, b = contract("P1", P1), contract("P2", P2)
    print(f"whole-contract winner: {'P1' if a < b else 'P2'} by ${abs(a-b):.2f} per useful GPU-hour")

if __name__ == "__main__":
    main()
