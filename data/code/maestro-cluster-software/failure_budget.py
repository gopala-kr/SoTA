"""failure_budget.py — how often will Maestro-1's run be interrupted?

Scales Meta's published Llama 3 405B failure record (419 unexpected
interruptions in 54 days on 16,384 H100s) to Gopala's cluster, then
asks how checkpoint interval and recovery time change goodput.
Assumes failures scale linearly with GPU count (our assumption).
"""
META = {"gpus": 16384, "days": 54, "unexpected": 419}
GPUS, DAYS = 1024, 31

def main():
    rate = META["unexpected"] / META["gpus"] / META["days"]   # per GPU-day
    n = rate * GPUS * DAYS
    print(f"rate {rate*1e3:.3f} interruptions per 1,000 GPU-days")
    print(f"Maestro-1: {GPUS} GPUs x {DAYS} days -> {n:.1f} expected interruptions "
          f"(one every {DAYS*24/n:.0f} h)")
    print(f"{'ckpt every':>10s} {'recover':>8s} {'lost h':>7s} {'goodput':>8s}")
    for ckpt_min in (15, 30, 60, 180):
        for rec_min in (10, 45):
            # lose half a checkpoint interval of work plus the recovery time
            lost = n * (ckpt_min / 2 + rec_min) / 60
            save = DAYS * 24 * 60 / ckpt_min * 0.5 / 60    # 30 s blocking save, our assumption
            good = 1 - (lost + save) / (DAYS * 24)
            print(f"{ckpt_min:7d} min {rec_min:5d} min {lost+save:7.1f} {good:8.1%}")

if __name__ == "__main__":
    main()
