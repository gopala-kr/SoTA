"""task_cost.py — what one agent task costs, and why context caching matters.

An agent loop re-sends its growing context every step: system prompt,
repository files read so far, tool outputs. Without caching, input tokens
grow roughly quadratically with steps. Prices are Maestro's own serving
costs from Part 15 plus our assumptions for input and cached tokens.
"""
OUT_PRICE = 1.17 / 1e6        # $/output token (serving_capacity.py, FP8 on 2 GPUs)
IN_PRICE = OUT_PRICE / 5      # prefill is cheaper per token than decode (assumption)
CACHED = IN_PRICE / 10        # reusing a cached prefix (assumption)
SYSTEM, PER_STEP_IN, PER_STEP_OUT = 6_000, 2_500, 400   # tokens

def task(steps, cache):
    ctx, cost, tin = SYSTEM, 0.0, 0
    for _ in range(steps):
        new = PER_STEP_IN
        if cache:
            cost += ctx * CACHED + new * IN_PRICE
        else:
            cost += (ctx + new) * IN_PRICE
        tin += ctx + new
        cost += PER_STEP_OUT * OUT_PRICE
        ctx += new + PER_STEP_OUT
    return tin, cost

def main():
    print(f"{'steps':>5s} {'input tokens':>13s} {'no cache':>9s} {'cached':>8s}")
    for s in (5, 15, 30, 60):
        tin, c0 = task(s, False); _, c1 = task(s, True)
        print(f"{s:5d} {tin:13,d} ${c0:8.3f} ${c1:7.3f}")
    _, c = task(30, True)
    print(f"a typical 30-step task costs ~${c:.3f} to serve; at 60% success, ${c/0.6:.3f} per solved task")

if __name__ == "__main__":
    main()
