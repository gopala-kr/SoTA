"""skill_eval.py — H1 with a real model: does retrieving verified skills help?

Runs the same coding tasks twice against any OpenAI-compatible endpoint (for
example an open 7–8B model served by vLLM on one rented GPU):
  arm "base":   task prompt only
  arm "skills": task prompt + the k most similar verified skills from the library
Each answer is executed against the task's hidden tests in a subprocess with a
timeout. Same model, same sampling settings, same number of attempts per task.

  vllm serve <open-model> --port 8000           # on the rented GPU
  python3 skill_eval.py tasks.jsonl skills.jsonl --base-url http://localhost:8000/v1

tasks.jsonl  : {"id", "prompt", "tests"}           (tests = Python asserts)
skills.jsonl : {"name", "code", "doc", "tests"}    (only skills that passed the gate)
NOTE: this script needs a running model server; it was not executed for this article.
"""
import argparse, json, re, subprocess, sys, tempfile
from collections import Counter
from openai import OpenAI          # pip install openai


def tokens(s):
    return Counter(re.findall(r"[a-z_]{3,}", s.lower()))


def top_k(task, skills, k=3):
    """Cheap lexical retrieval; swap in embeddings once the library is large."""
    q = tokens(task["prompt"])
    score = lambda s: sum((q & tokens(s["doc"] + " " + s["name"])).values())
    return [s for s in sorted(skills, key=score, reverse=True)[:k] if score(s) > 0]


def extract_code(text):
    m = re.search(r"```(?:python)?\n(.*?)```", text, re.S)
    return m.group(1) if m else text


def run_tests(code, tests, timeout=10):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code + "\n\n" + tests + "\n")
    try:
        r = subprocess.run([sys.executable, f.name], capture_output=True, timeout=timeout)
        return r.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def ask(client, model, prompt, n):
    out = client.chat.completions.create(model=model, n=n, temperature=0.6, max_tokens=1024,
                                         messages=[{"role": "user", "content": prompt}])
    return [extract_code(c.message.content) for c in out.choices]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tasks"); ap.add_argument("skills")
    ap.add_argument("--base-url", default="http://localhost:8000/v1"); ap.add_argument("--model", default="default")
    ap.add_argument("--attempts", type=int, default=4)
    a = ap.parse_args()
    client = OpenAI(base_url=a.base_url, api_key="local")
    tasks = [json.loads(l) for l in open(a.tasks)]
    skills = [json.loads(l) for l in open(a.skills)]
    wins = {"base": 0, "skills": 0}
    for t in tasks:
        arms = {"base": t["prompt"]}
        found = top_k(t, skills)
        ctx = "\n\n".join(f"# Verified skill: {s['name']}\n# {s['doc']}\n{s['code']}" for s in found)
        arms["skills"] = (f"These verified helper functions may be useful:\n```python\n{ctx}\n```\n\n" if found else "") + t["prompt"]
        for arm, prompt in arms.items():
            ok = any(run_tests(c, t["tests"]) for c in ask(client, a.model, prompt, a.attempts))
            wins[arm] += ok
    n = len(tasks)
    print(f"pass@{a.attempts}: base {wins['base']}/{n}  skills {wins['skills']}/{n}")


if __name__ == "__main__":
    main()
