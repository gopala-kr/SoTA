"""quality_filter.py — heuristic document filters in the style of the
Gopher rules (Rae et al., 2021), the first gate of the data refinery.

Each rule is cheap and explainable; together they remove most junk before
any model-based classifier runs. SAMPLE documents are written for this
article. Thresholds follow the published Gopher rules where they exist.
"""
import re

SAMPLE = {
    "tutorial": "To install the package, open a terminal and run the installer. "
                "Then create a configuration file in your home directory and set the "
                "path to your data. The tool reads the file on start-up and reports "
                "any missing values, so check the log after the first run. " * 3,
    "spam":     "BUY NOW!!! $$$ best price best price best price click here click here "
                "#### $$$ !!! ### deal deal deal $$$ ### !!! click click",
    "boilerplate": "Home | About | Contact | Login\nHome | About | Contact | Login\n"
                   "Home | About | Contact | Login\nCopyright 2026. All rights reserved.",
    "code_doc": "def area(r):\n    return 3.14159 * r * r\n# compute the area of a circle "
                "given its radius r; returns a float. Use it in geometry exercises "
                "and check results against a calculator before submitting work. " * 2,
    "short":    "Click to continue.",
}
STOP = {"the", "be", "to", "of", "and", "that", "have", "with"}

def rules(doc):
    words = re.findall(r"\S+", doc)
    n = len(words)
    alpha = [w for w in words if re.search(r"[A-Za-z]", w)]
    lines = [l for l in doc.splitlines() if l.strip()]
    return {
        "50 <= words <= 100k": 50 <= n <= 100_000,
        "mean word length 3-10": n > 0 and 3 <= sum(map(len, words)) / n <= 10,
        "symbol/word ratio < 0.1": n > 0 and (doc.count("#") + doc.count("...")) / n < 0.1,
        ">= 80% words have a letter": n > 0 and len(alpha) / n >= 0.8,
        ">= 2 stop words": len({w.lower() for w in words} & STOP) >= 2,
        "duplicate lines < 30%": not lines or 1 - len(set(lines)) / len(lines) < 0.30,
    }

def main():
    kept = 0
    for name, doc in SAMPLE.items():
        r = rules(doc)
        failed = [k for k, ok in r.items() if not ok]
        kept += not failed
        print(f"{name:12s} {'KEEP' if not failed else 'DROP'}  " + ("; ".join(failed) if failed else "passes all 6 rules"))
    print(f"kept {kept} of {len(SAMPLE)}")

if __name__ == "__main__":
    main()
