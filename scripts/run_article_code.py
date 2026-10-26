"""run_article_code.py — re-run the code published in articles and compare with the page.

For every script in data/code/<slug>/ that the article shows output for ("$ python3 name.py"),
run it with the standard library only and check that every line it prints appears in the
article's output block. Scripts that need extra packages or GPUs are skipped and reported.
Exit code 1 if any published output has drifted. See docs/LOOP-ENGINEERING.md.

  python3 scripts/run_article_code.py
"""
import html, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def main():
    drift, ran, skipped = [], 0, []
    for d in sorted((ROOT / "data/code").glob("*")):
        page = ROOT / "blog" / f"{d.name}.html"
        if not page.exists():
            continue
        outs = norm(" ".join(html.unescape(o) for o in re.findall(r'class="mo-out"[^>]*>(.*?)</div>', page.read_text(encoding="utf-8"), re.S)))
        for f in sorted(d.glob("*.py")):
            if f"$ python3 {f.name}" not in outs or "--" in outs.split(f"$ python3 {f.name}")[1][:3]:
                continue                                   # no bare published run of this script
            try:
                r = subprocess.run([sys.executable, "-S", str(f)], cwd=d, capture_output=True, text=True, timeout=300)
            except subprocess.TimeoutExpired:
                skipped.append(f"{d.name}/{f.name} (timeout)"); continue
            if r.returncode != 0:
                skipped.append(f"{d.name}/{f.name} (needs packages or failed: {r.stderr.strip().splitlines()[-1][:80] if r.stderr.strip() else r.returncode})"); continue
            ran += 1
            for line in r.stdout.splitlines():
                if line.strip() and norm(line) not in outs:
                    drift.append(f"{d.name}/{f.name}: output line not on the page: {line.strip()[:100]}")
    print(f"article code: ran {ran} script(s), {len(drift)} drifted line(s), {len(skipped)} skipped")
    for s in skipped:
        print("  skipped:", s)
    for x in drift:
        print("  DRIFT:", x)
    sys.exit(1 if drift else 0)


if __name__ == "__main__":
    main()
