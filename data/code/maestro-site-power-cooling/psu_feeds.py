"""psu_feeds.py — does a node survive losing one power feed?

A DGX H100 has six power supplies and needs at least four energised.
NVIDIA's SuperPOD design guide therefore asks for THREE independent
sources per rack, each feeding two of the six supplies. This checks
every possible wiring with two and with three feeds.
"""
from itertools import product

NEED = 4

def survives(wiring, lost):
    return sum(1 for f in wiring if f != lost) >= NEED

def ok_all(w, feeds):
    return all(survives(w, f) for f in feeds)

def main():
    for feeds in ("AB", "ABC"):
        ways = list(product(feeds, repeat=6))
        good = [w for w in ways if ok_all(w, feeds)]
        print(f"{len(feeds)} feeds: {len(good)} of {len(ways)} wirings survive any one feed failing")
    cases = {"A/B, 3+3 (enterprise habit)": ("AAABBB", "AB"),
             "A/B/C, 2+2+2 (NVIDIA design)": ("AABBCC", "ABC"),
             "A/B/C, one cord on wrong strip": ("AAABCC", "ABC"),
             "A/B/C, C strip never cabled": ("AAABBB", "ABC")}
    for name, (w, feeds) in cases.items():
        res = "  ".join(f"lose {f}: {'runs' if survives(w, f) else 'STOPS'}" for f in feeds)
        print(f"  {name:32s} {res}")
    print("lesson: with a 4-of-6 minimum, two feeds can never protect the node;")
    print("        three feeds work only if every node is cabled 2+2+2 - check it rack by rack")

if __name__ == "__main__":
    main()
