"""l4_toy.py — a toy L4 (deployment-adaptation) loop you can run on a laptop.

A solver searches for small programs that match a task's examples. Verified
solutions become reusable skills, kept only if a fixed, human-written gate
approves them. Two versions are compared at the SAME search budget per task:
  v1 "hoard":  every verified solution is added to the search vocabulary
  v2 "curate": abstract the reusable core, retrieve the top skills, try them first
Pure Python 3, no dependencies. Run:  python3 l4_toy.py
"""
import random

PRIMS = {
    "add1": lambda x: x + 1, "add3": lambda x: x + 3, "sub2": lambda x: x - 2,
    "dbl": lambda x: 2 * x, "tri": lambda x: 3 * x, "sq": lambda x: x * x,
    "neg": lambda x: -x, "half": lambda x: x // 2, "mod7": lambda x: x % 7,
}
CORES = [["dbl", "add3"], ["sq", "sub2"], ["tri", "mod7"], ["neg", "half"], ["add1", "sq", "dbl"]]
PROBE = list(range(-9, 10))


def run(prog, x):
    for op in prog:
        x = PRIMS[op](x)
        if abs(x) > 10**9:
            raise OverflowError
    return x


def passes(prog, pairs):
    try:
        return all(run(prog, x) == y for x, y in pairs)
    except OverflowError:
        return False


def make_task(rng):
    """Tasks share hidden sub-routines: a random op, a shared core, a random op."""
    core = rng.choice(CORES)
    pre, post = rng.sample(list(PRIMS), 2)
    target = [pre] + core + [post]
    xs = rng.sample(PROBE, 8)
    pairs = [(x, run(target, x)) for x in xs]
    return {"visible": pairs[:4], "hidden": pairs[4:]}


class Agent:
    def __init__(self, mode, seed):
        self.mode, self.rng, self.skills, self.uses = mode, random.Random(seed), [], {}

    # ── the solver: a fixed budget of candidate programs per task ────────────
    def solve(self, task, budget=3000):
        tried = 0
        if self.mode == "curate" and self.skills:          # retrieval: best skills first
            top = sorted(self.skills, key=lambda s: -self.uses.get(tuple(s), 0))[:8]
            wraps = [[]] + [[p] for p in PRIMS]
            for sk in top:
                for pre in wraps:
                    for post in wraps:
                        prog = pre + sk + post
                        tried += 1
                        if passes(prog, task["visible"]):
                            self.uses[tuple(sk)] = self.uses.get(tuple(sk), 0) + 1
                            return prog
                        if tried >= budget:
                            return None
        vocab = [[p] for p in PRIMS] + (self.skills if self.mode == "hoard" else [])
        while tried < budget:                               # blind search for the rest
            prog = [op for _ in range(self.rng.randint(1, 5)) for op in self.rng.choice(vocab)]
            tried += 1
            if passes(prog, task["visible"]):
                return prog
        return None

    # ── the gate: a fixed improvement process that never rewrites itself ─────
    def gate(self, prog, task, validation):
        if not passes(prog, task["hidden"]):
            return False                                    # overfit to visible examples
        cand = prog[1:-1] if (self.mode == "curate" and len(prog) >= 4) else prog
        sig = tuple(run(cand, x) for x in PROBE) if len(cand) >= 2 else None
        if sig is None or any(tuple(run(s, x) for x in PROBE) == sig for s in self.skills):
            return False                                    # trivial or a duplicate
        before = self.score(validation)
        self.skills.append(cand)
        if self.score(validation) < before:                 # must not make things worse
            self.skills.pop()
            return False
        return True

    def score(self, validation):
        state = self.rng.getstate()
        n = sum(self.solve(v, budget=800) is not None for v in validation)
        self.rng.setstate(state)
        return n


def experiment(mode, rounds=6, per_round=40, seed=1):
    data = random.Random(seed)
    validation = [make_task(data) for _ in range(12)]
    agent, rows = Agent(mode, seed), []
    for r in range(rounds):
        tasks = [make_task(data) for _ in range(per_round)]
        solved = 0
        for t in tasks:
            prog = agent.solve(t)
            if prog and passes(prog, t["hidden"]):
                solved += 1
            if prog and mode != "off":
                agent.gate(prog, t, validation)
        rows.append((r, solved, len(agent.skills)))
    return rows


if __name__ == "__main__":
    for mode in ("off", "hoard", "curate"):
        rows = experiment(mode)
        print(f"{mode:7s}", " ".join(f"r{r}:{s:2d}/40({k:2d})" for r, s, k in rows))
    print("format: round:solved-on-hidden-tests(skills in library)")
