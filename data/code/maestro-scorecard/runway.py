"""runway.py — cash after 18 months and the path to the next raise.

Starts from the $20M seed (Part 3). Spend by phase from the story's
Mission Control; revenue from SCENARIO customers growing per month.
"""
RAISE = 20.0
SPENT_18M = 12.6                 # $M, scenario total through month 18
BURN = 0.352                     # $M per month after month 18 (scenario)
REV_M18 = 0.11                   # $M monthly revenue at month 18 (scenario)
GROWTH = 0.12                    # monthly revenue growth (assumption)

def main():
    cash = RAISE - SPENT_18M
    print(f"cash at month 18: ${cash:.1f}M of ${RAISE:.0f}M")
    rev, m = REV_M18, 18
    while cash > 0 and m < 60:
        m += 1; rev *= 1 + GROWTH; cash -= max(0, BURN - rev)
        if rev >= BURN:
            print(f"break-even on monthly burn at month {m} with ${cash:.1f}M left"); break
    else:
        print(f"cash runs out at month {m}")
    for g in (0.06, 0.09, 0.12, 0.15):
        cash, rev, m = RAISE - SPENT_18M, REV_M18, 18
        while cash > 0 and rev < BURN and m < 80:
            m += 1; rev *= 1 + g; cash -= BURN - rev
        print(f"  growth {g:.0%}/month: {'break-even' if rev >= BURN else 'out of cash'} at month {m}")

if __name__ == "__main__":
    main()
