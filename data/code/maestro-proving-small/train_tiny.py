"""train_tiny.py — a minimal GPT trainer for the Maestro's small-scale proofs.

The same file trains a 0.1M-parameter smoke-test model on a laptop CPU and,
unchanged, a 125M–1B model on one rented GPU (multi-GPU comes in Part 9).
Features that matter later: cosine schedule with warmup, bf16 autocast, gradient
clipping, periodic eval, and checkpoint/resume so a crashed run loses minutes.

  python3 train_tiny.py --size xs --steps 400          # CPU smoke test
  python3 train_tiny.py --size 125M --steps 20000 --bs 64 --ctx 1024 --lr 6e-4   # one GPU
"""
import argparse, glob, math, os, time
import torch
import torch.nn as nn
import torch.nn.functional as F

SIZES = {  # name: (layers, heads, d_model) — params grow ~12·L·d²
    "xs": (2, 2, 64), "s": (4, 4, 128), "sm": (4, 4, 192), "m": (6, 8, 256),
    "125M": (12, 12, 768), "350M": (24, 16, 1024), "1B": (24, 16, 2048),
}


class Block(nn.Module):
    def __init__(self, d, h):
        super().__init__()
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.qkv, self.proj, self.h = nn.Linear(d, 3 * d), nn.Linear(d, d), h
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))

    def forward(self, x):
        B, T, C = x.shape
        q, k, v = self.qkv(self.ln1(x)).split(C, dim=2)
        q, k, v = (t.view(B, T, self.h, C // self.h).transpose(1, 2) for t in (q, k, v))
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)   # FlashAttention on GPU
        x = x + self.proj(y.transpose(1, 2).reshape(B, T, C))
        return x + self.mlp(self.ln2(x))


class GPT(nn.Module):
    def __init__(self, vocab, ctx, L, H, D):
        super().__init__()
        self.tok, self.pos = nn.Embedding(vocab, D), nn.Embedding(ctx, D)
        self.blocks = nn.ModuleList(Block(D, H) for _ in range(L))
        self.ln, self.head = nn.LayerNorm(D), nn.Linear(D, vocab, bias=False)
        self.head.weight = self.tok.weight                            # weight tying
        self.apply(self._init)

    @staticmethod
    def _init(m):                                                      # GPT-2 style: small init
        if isinstance(m, (nn.Linear, nn.Embedding)):
            nn.init.normal_(m.weight, std=0.02)
        if isinstance(m, nn.Linear) and m.bias is not None:
            nn.init.zeros_(m.bias)

    def forward(self, idx, targets=None):
        x = self.tok(idx) + self.pos(torch.arange(idx.shape[1], device=idx.device))
        for b in self.blocks:
            x = b(x)
        logits = self.head(self.ln(x))
        loss = None if targets is None else F.cross_entropy(logits.flatten(0, 1), targets.flatten())
        return logits, loss


def load_text():
    """Byte-level data: any local text. Default: the Python standard library source."""
    root = os.path.dirname(os.__file__)
    files = sorted(glob.glob(os.path.join(root, "*.py")))[:120]
    data = b"".join(open(f, "rb").read() for f in files)
    t = torch.tensor(list(data), dtype=torch.long)
    n = int(0.95 * len(t))
    return t[:n], t[n:]


def batch(data, bs, ctx, gen):
    ix = torch.randint(len(data) - ctx - 1, (bs,), generator=gen)
    x = torch.stack([data[i:i + ctx] for i in ix])
    return x, torch.stack([data[i + 1:i + ctx + 1] for i in ix])


def lr_at(step, total, peak, warm):
    if step < warm:
        return peak * (step + 1) / warm
    return peak * 0.5 * (1 + math.cos(math.pi * (step - warm) / max(1, total - warm)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", default="xs"); ap.add_argument("--steps", type=int, default=400)
    ap.add_argument("--bs", type=int, default=16); ap.add_argument("--ctx", type=int, default=128)
    ap.add_argument("--lr", type=float, default=3e-3); ap.add_argument("--ckpt", default="ckpt_tiny.pt")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    torch.manual_seed(a.seed); gen = torch.Generator().manual_seed(a.seed)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    train, val = load_text()
    L, H, D = SIZES[a.size]
    model = GPT(256, a.ctx, L, H, D).to(dev)
    n_params = sum(p.numel() for p in model.parameters()) - model.pos.weight.numel()
    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, betas=(0.9, 0.95), weight_decay=0.1)
    start = 0
    if os.path.exists(a.ckpt):                                        # resume after a crash
        s = torch.load(a.ckpt, map_location=dev)
        model.load_state_dict(s["model"]); opt.load_state_dict(s["opt"]); start = s["step"]
    tokens = a.steps * a.bs * a.ctx
    print(f"size={a.size} params={n_params/1e6:.2f}M tokens={tokens/1e6:.2f}M "
          f"compute≈{6*n_params*tokens:.2e} FLOPs device={dev}")
    t0 = time.time()
    for step in range(start, a.steps):
        for g in opt.param_groups:
            g["lr"] = lr_at(step, a.steps, a.lr, warm=max(1, a.steps // 20))
        x, y = batch(train, a.bs, a.ctx, gen)
        with torch.autocast(dev, dtype=torch.bfloat16, enabled=dev == "cuda"):
            _, loss = model(x.to(dev), y.to(dev))
        opt.zero_grad(set_to_none=True); loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step()
        if step % 100 == 0 or step == a.steps - 1:
            model.eval()
            with torch.no_grad():
                vl = sum(model(*(t.to(dev) for t in batch(val, a.bs, a.ctx, gen)))[1].item() for _ in range(8)) / 8
            model.train()
            print(f"step {step:5d}  train {loss.item():.3f}  val {vl:.3f}  ({time.time()-t0:.0f}s)")
            torch.save({"model": model.state_dict(), "opt": opt.state_dict(), "step": step + 1}, a.ckpt)
    print(f"final_val {vl:.4f} params {n_params}")


if __name__ == "__main__":
    main()
