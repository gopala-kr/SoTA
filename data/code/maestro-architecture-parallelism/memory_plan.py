"""memory_plan.py — which parallel layout fits Maestro-1 on 1,024 H100s?

Memory per GPU = weights + gradients + optimizer state (sharded) +
activations. Mixed-precision Adam keeps ~16 bytes per parameter in total
(bf16 weights and grads, fp32 master weights, two fp32 moments);
ZeRO-1-style sharding spreads the 12 optimizer bytes across data-parallel
ranks. Activation memory is a rough per-token estimate (our assumption).
"""
TOTAL, NON_EXPERT = 65.2e9, 4.1e9   # from moe_params.py: all params; params not split by EP (attention, dense, shared expert, embeddings)
GPUS, HBM = 1024, 80e9
SEQ, MICRO = 8192, 1
ACT_BYTES_PER_TOKEN_LAYER = 34 * 4096 * 2 / 8    # rough, with selective recompute (assumption)
LAYERS = 40

def per_gpu(tp, pp, ep):
    dp = GPUS // (tp * pp)
    expert_params = TOTAL - NON_EXPERT
    params = NON_EXPERT / (tp * pp) + expert_params / (tp * pp * ep)
    w_g = params * 4                                   # bf16 weights + bf16 grads
    opt = params * 12 / dp                             # fp32 master + 2 moments, sharded over DP
    act = SEQ * MICRO * ACT_BYTES_PER_TOKEN_LAYER * (LAYERS / pp) / tp * pp  # 1F1B keeps ~pp micro-batches
    return dp, (w_g + opt + act) / 1e9

def main():
    print(f"{'TP':>3s} {'PP':>3s} {'EP':>3s} {'DP':>4s} {'GB/GPU':>7s}  fits 80 GB with 10% headroom?")
    for tp, pp, ep in [(1, 1, 1), (1, 1, 8), (2, 1, 8), (1, 2, 8), (4, 1, 8), (1, 4, 16), (2, 2, 8), (8, 1, 8)]:
        dp, gb = per_gpu(tp, pp, ep)
        if dp % ep:
            continue
        print(f"{tp:3d} {pp:3d} {ep:3d} {dp:4d} {gb:7.1f}  {'yes' if gb < 0.9 * HBM / 1e9 else 'no'}")
    print("rule: keep TP inside one 8-GPU node (NVLink); EP across nodes costs all-to-all traffic")

if __name__ == "__main__":
    main()
