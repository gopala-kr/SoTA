"""scorecard.py — plan vs outcome after 18 months (Part 3's plan vs the story).

Plan numbers are from earlier parts' scripts; outcomes are the SCENARIO.
A line is green within 10% of plan, amber within 25%, red beyond.
"""
ROWS = [  # name, plan, outcome, unit, higher_is_better
    ("Training compute spent", 8.1, 8.4, "$M", False),
    ("Main run duration", 31.4, 32.5, "days", False),
    ("Months to first partner use", 4, 4.5, "months", False),
    ("Months to Maestro-1 release", 13, 13.5, "months", False),
    ("Release-set improvement over Maestro-0", 4.0, 5.1, "points", True),
    ("Loop updates approved by the gate", 12, 7, "updates", True),
    ("Paying customers at month 18", 12, 9, "customers", True),
    ("Monthly burn", 318, 352, "$k", False),
]

def rag(plan, out, hib):
    d = (out - plan) / plan if hib else (plan - out) / plan
    return "G" if d >= -0.10 else ("A" if d >= -0.25 else "R")

def main():
    counts = {"G": 0, "A": 0, "R": 0}
    for name, plan, out, unit, hib in ROWS:
        r = rag(plan, out, hib); counts[r] += 1
        print(f"[{r}] {name:40s} plan {plan:7.1f} {unit:9s} outcome {out:7.1f}")
    print(f"green {counts['G']}, amber {counts['A']}, red {counts['R']}")

if __name__ == "__main__":
    main()
