"""run_ledger.py — is the main run on schedule?

Daily check of tokens trained against plan: the plan (Part 3) is 10T
tokens in ~31.4 days on 1,024 GPUs. The DAILY numbers below are
SCENARIO values written for this story, not measurements.
"""
PLAN_TOKENS, PLAN_DAYS = 10e12, 31.4
DAILY = [0.31, 0.33, 0.33, 0.30, 0.33, 0.33, 0.24, 0.33, 0.33, 0.32,   # trillions of tokens per day
         0.33, 0.33, 0.33, 0.29, 0.33, 0.33, 0.33, 0.33, 0.26, 0.33]

def main():
    rate = PLAN_TOKENS / PLAN_DAYS / 1e12
    done = 0
    print(f"plan: {rate:.3f}T tokens/day")
    for d, t in enumerate(DAILY, 1):
        done += t
        if d % 5 == 0:
            ahead = done - rate * d
            eta = d + (PLAN_TOKENS / 1e12 - done) / (done / d)
            print(f"day {d:2d}: {done:5.2f}T done ({done/(PLAN_TOKENS/1e12):4.0%}), "
                  f"{'ahead' if ahead >= 0 else 'behind'} by {abs(ahead):.2f}T, finish ~day {eta:.1f}")
    low = [d for d, t in enumerate(DAILY, 1) if t < 0.9 * rate]
    print("days below 90% of plan (investigate):", ", ".join(map(str, low)))

if __name__ == "__main__":
    main()
