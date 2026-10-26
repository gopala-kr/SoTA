"""budget.py — the Maestro's compute and cash plan, from first principles.

Training compute  ≈ 6 · N_active · D        (dense or MoE active params, tokens)
Generation (RL)   ≈ 2 · N_active · D_gen    (rollouts are inference)
GPU-seconds       = FLOPs / (peak FLOP/s · MFU)
All prices and efficiencies are ASSUMPTIONS you should replace with real quotes.

  python3 budget.py
"""

H100_BF16 = 989e12          # NVIDIA H100 SXM dense BF16 peak, FLOP/s (spec sheet)
PRICE = 2.35                # $/GPU-hour, 1-year reserved H100 (secondary report, Mar 2026) — assumption
GPUS = 1024                 # cluster size for the main run

SCENARIOS = [
    # name, active params, train tokens, MFU, RL rollout tokens, experiment multiplier
    ("A  post-train open 32B",          32e9, 0.1e12, 0.40, 1.0e12, 2.0),
    ("B  from scratch 8B dense",         8e9, 15e12,  0.40, 0.5e12, 3.0),
    ("C  from scratch 32B dense",       32e9,  6e12,  0.40, 1.0e12, 3.0),
    ("D  from scratch MoE 12B active",  12e9, 10e12,  0.30, 0.8e12, 3.0),
]
FAILURE_OVERHEAD = 0.10     # restarts, lost steps, bad nodes (Llama 3 saw 466 interruptions in 54 days)
RL_MFU = 0.20               # generation runs at lower utilisation than training


def plan(name, n, d, mfu, d_gen, exp_mult):
    train_flops = 6 * n * d
    gen_flops = 2 * n * d_gen
    gpu_h = (train_flops / (H100_BF16 * mfu) + gen_flops / (H100_BF16 * RL_MFU)) / 3600
    gpu_h *= 1 + FAILURE_OVERHEAD
    days = gpu_h / GPUS / 24
    final = gpu_h * PRICE
    total = final * (1 + exp_mult)          # experiments, ablations, evals cost a multiple of the final run
    return train_flops, gpu_h, days, final, total


print(f"{'scenario':34s} {'train FLOPs':>11s} {'GPU-hours':>10s} {'days@'+str(GPUS):>9s} {'final run':>10s} {'with R&D':>10s}")
for s in SCENARIOS:
    f, h, dys, fin, tot = plan(*s)
    print(f"{s[0]:34s} {f:11.2e} {h:10,.0f} {dys:9.1f} ${fin/1e6:8.2f}M ${tot/1e6:8.2f}M")

# Runway: compute is the biggest line, but not the only one
monthly_people = 150_000     # Gopala, contractors (DC technicians, security, legal), agent API bills (assumption)
monthly_serving = 64 * PRICE * 24 * 30   # a 64-GPU serving cluster for design partners
monthly_other = 60_000       # storage, egress, data licences, tools, insurance (assumption)
raise_usd = 20e6
compute_total = plan(*SCENARIOS[0])[4] + plan(*SCENARIOS[3])[4]     # the hybrid plan: A now, D later
burn = monthly_people + monthly_serving + monthly_other
months = (raise_usd - compute_total) / burn
print(f"\nhybrid plan (A then D): training compute ${compute_total/1e6:.1f}M of a ${raise_usd/1e6:.0f}M raise")
print(f"monthly burn besides training: ${burn/1e3:,.0f}k (people ${monthly_people/1e3:,.0f}k, "
      f"serving ${monthly_serving/1e3:,.0f}k, other ${monthly_other/1e3:,.0f}k) → ~{months:.0f} months of runway")
