"""moe_params.py — count total and active parameters of Maestro-1's MoE.

A mixture-of-experts layer holds many feed-forward "experts" but each
token uses only a few, so compute follows ACTIVE parameters and memory
follows TOTAL parameters. Configuration is our design for this story.
"""
CFG = dict(layers=40, d=4096, heads=32, kv_heads=8, vocab=128_000,
           experts=64, top_k=8, shared=1, d_ff_expert=2048, dense_first=2, d_ff_dense=14336)

def count(c):
    d, hd = c["d"], c["d"] // c["heads"]
    attn = d * d * 2 + d * hd * c["kv_heads"] * 2           # Q,O full; K,V grouped (GQA)
    expert = 3 * d * c["d_ff_expert"]                        # SwiGLU: gate, up, down
    dense_ffn = 3 * d * c["d_ff_dense"]
    router = d * c["experts"]
    moe_layers = c["layers"] - c["dense_first"]
    emb = c["vocab"] * d * 2                                 # input + output (untied)
    total = (c["layers"] * attn + c["dense_first"] * dense_ffn
             + moe_layers * ((c["experts"] + c["shared"]) * expert + router) + emb)
    active = (c["layers"] * attn + c["dense_first"] * dense_ffn
              + moe_layers * ((c["top_k"] + c["shared"]) * expert + router) + emb)
    return attn, expert, total, active, emb

def main():
    attn, expert, total, active, emb = count(CFG)
    print(f"per layer: attention {attn/1e6:.1f}M, one expert {expert/1e6:.1f}M")
    print(f"total parameters  {total/1e9:6.1f}B   (memory, checkpoints)")
    print(f"active per token  {active/1e9:6.1f}B   (compute: 6 x active x tokens)")
    print(f"  of which embeddings {emb/1e9:.1f}B; active without embeddings {(active-emb)/1e9:.1f}B")
    print(f"sparsity: each token uses {active/total:.0%} of the weights")
    for k in (2, 4, 6, 8):
        c = dict(CFG, top_k=k)
        print(f"  top_k={k}: active {count(c)[3]/1e9:5.1f}B")

if __name__ == "__main__":
    main()
