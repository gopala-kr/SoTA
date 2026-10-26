"""flywheel.py — does the verified-skill flywheel compound or stall?

Each two-week cycle: tasks attempted -> verified skills -> (some) gate
approvals -> success rate rises a little, which brings more tasks.
Diminishing returns: each new skill helps less as the library grows.
All parameters are SCENARIO assumptions; the point is the shape.
"""
import math

def run(cycles=12, tasks=400, success=0.48, approve=0.5, gain_per_k=0.012, overlap=0.0004):
    lib = 0
    print(f"{'cycle':>5s} {'tasks':>6s} {'success':>8s} {'new skills':>10s} {'library':>8s}")
    for c in range(1, cycles + 1):
        solved = tasks * success
        new = solved * math.exp(-overlap * lib)          # more overlap with existing skills later
        lib += new
        if c % 2 == 0:                                    # gate approves an update every other cycle on average
            success = min(0.85, success + approve * gain_per_k * (new / 100))
        tasks = int(tasks * (1.04 + (success - 0.48)))   # better product -> more usage
        if c in (1, 3, 6, 9, 12):
            print(f"{c:5d} {tasks:6d} {success:8.1%} {new:10.0f} {lib:8.0f}")

if __name__ == "__main__":
    run()
