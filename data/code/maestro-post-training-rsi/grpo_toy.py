"""grpo_toy.py — group-relative policy optimisation on a toy task, and
why the verifier decides what the model learns.

A 'policy' picks one of four strategies for a coding task. Each attempt
is checked by a verifier that returns 1 or 0. GRPO (DeepSeekMath, 2024)
samples a GROUP of attempts, scores each against the group's mean and
spread, and pushes probability towards above-average attempts; no value
model is needed. Two verifiers are compared:
  weak   = visible unit tests only (a hack that special-cases the tests passes)
  strong = visible + hidden tests (the hack fails)
Success probabilities are made up for the toy; fixed seed.
"""
import math, random

STRATS = ["careful solution", "quick solution", "special-case the tests (hack)", "give up"]
P_VISIBLE = [0.70, 0.45, 0.98, 0.00]     # chance of passing visible tests
P_HIDDEN  = [0.65, 0.30, 0.02, 0.00]     # chance of passing hidden tests too

def run(verifier, iters=60, group=16, lr=0.5, seed=1):
    rng = random.Random(seed)
    logits = [0.0] * 4
    for _ in range(iters):
        z = max(logits); p = [math.exp(l - z) for l in logits]; s = sum(p); p = [x / s for x in p]
        picks = [rng.choices(range(4), p)[0] for _ in range(group)]
        if verifier == "weak":
            r = [1.0 if rng.random() < P_VISIBLE[a] else 0.0 for a in picks]
        else:
            r = [1.0 if rng.random() < P_HIDDEN[a] else 0.0 for a in picks]
        mu = sum(r) / group; sd = (sum((x - mu) ** 2 for x in r) / group) ** 0.5 or 1.0
        adv = [(x - mu) / sd for x in r]
        for a, A in zip(picks, adv):           # policy gradient on softmax logits
            for j in range(4):
                logits[j] += lr / group * A * ((1 if j == a else 0) - p[j])
    z = max(logits); p = [math.exp(l - z) for l in logits]; s = sum(p)
    return [x / s for x in p]

def main():
    for v in ("weak", "strong"):
        p = run(v)
        real = sum(pi * h for pi, h in zip(p, P_HIDDEN))
        print(f"verifier={v:6s} policy: " + ", ".join(f"{n.split(' (')[0]} {pi:.0%}" for n, pi in zip(STRATS, p)))
        print(f"{'':16s} true success on hidden tests: {real:.0%}")

if __name__ == "__main__":
    main()
