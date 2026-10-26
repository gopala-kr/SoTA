"""serving_capacity.py — how many users can 64 H100s serve, and at what cost?

Memory per replica = weights + KV cache for active conversations.
Decode speed is limited by reading weights and KV cache from HBM each
step. Architecture from Part 9; bandwidth and efficiency are our
assumptions (H100 SXM HBM3 ~3.35 TB/s is NVIDIA's figure).
"""
TOTAL, ACTIVE = 65.2e9, 11.7e9
KV_PER_TOKEN = 2 * 40 * 8 * 128 * 2          # bytes, BF16 KV, GQA (Part 9) = 160 KB
HBM, BW, EFF = 80e9, 3.35e12, 0.5             # per GPU; EFF = achieved share of bandwidth (assumption)
GPUS, PRICE = 64, 2.35
CTX = 16_000                                   # average live context per conversation (assumption)

def replica(bytes_per_w, gpus):
    weights = TOTAL * bytes_per_w
    free = gpus * HBM * 0.9 - weights
    seqs = int(free // (KV_PER_TOKEN * CTX))
    # per decode step: read active expert weights (all tokens in batch share them) + every sequence's KV
    step_bytes = ACTIVE * bytes_per_w + seqs * KV_PER_TOKEN * CTX
    step_s = step_bytes / (gpus * BW * EFF)
    return weights, seqs, seqs / step_s

def main():
    print(f"KV cache per token: {KV_PER_TOKEN/1024:.0f} KB; per {CTX:,}-token conversation: {KV_PER_TOKEN*CTX/1e9:.2f} GB")
    for name, b, g in [("BF16 weights, 2 GPUs/replica", 2, 2), ("FP8 weights, 1 GPU/replica", 1, 1), ("FP8 weights, 2 GPUs/replica", 1, 2)]:
        w, seqs, tps = replica(b, g)
        if seqs <= 0:
            print(f"{name:30s} weights {w/1e9:.0f} GB -> does not fit"); continue
        reps = GPUS // g
        total_tps = tps * reps
        cost = GPUS * PRICE / (total_tps * 3600) * 1e6
        print(f"{name:30s} {reps:2d} replicas x {seqs:3d} live chats = {reps*seqs:4d}; "
              f"{total_tps:8,.0f} tokens/s; ${cost:.2f} per million output tokens")

if __name__ == "__main__":
    main()
