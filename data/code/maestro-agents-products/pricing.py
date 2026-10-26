"""pricing.py — per-seat vs per-solved-task pricing for the agent product.

Gross margin = (revenue - serving cost) / revenue. Usage per engineer
varies a lot, so seat pricing can lose money on heavy users. All prices,
usage levels and success rates are our assumptions for the story.
"""
COST_PER_TASK = 0.065         # task_cost.py: 30-step task with caching
SUCCESS = 0.6
SEAT = 40.0                   # $ per engineer per month
PER_SOLVED = 1.50             # $ per merged/accepted task

def main():
    print(f"{'tasks/eng/month':>15s} {'seat margin':>12s} {'per-task margin':>16s}")
    for tasks in (20, 100, 300, 600):
        cost = tasks * COST_PER_TASK
        seat_m = (SEAT - cost) / SEAT
        rev = tasks * SUCCESS * PER_SOLVED
        task_m = (rev - cost) / rev
        print(f"{tasks:15d} {seat_m:12.0%} {task_m:16.0%}")
    print("hybrid: seat fee with an included allowance, then per solved task above it")

if __name__ == "__main__":
    main()
