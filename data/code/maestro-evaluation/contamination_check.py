"""contamination_check.py — did benchmark items leak into training data?

Long word n-gram overlap (13-grams, as in the GPT-3 paper's check)
between each benchmark item and a training shard. Texts are written for
this article. Real runs index the 10T-token blend with hashed n-grams.
"""
N = 13
BENCH = {
    "task-017": "write a function that returns the longest strictly increasing contiguous subsequence of a list of integers and its starting index",
    "task-042": "given a log file with timestamps in mixed time zones convert every entry to utc and report the gaps longer than five minutes",
    "task-108": "implement a rate limiter that allows at most n requests per rolling window of t seconds for each api key",
}
SHARD = ("forum post: homework help please. write a function that returns the longest strictly increasing contiguous "
         "subsequence of a list of integers and its starting index, my code fails on empty lists. "
         "another thread discusses how to implement a rate limiter for an api using a token bucket.")

def grams(t):
    w = t.lower().replace(",", "").replace(".", "").split()
    return {" ".join(w[i:i + N]) for i in range(len(w) - N + 1)}

def main():
    sg = grams(SHARD)
    for k, v in BENCH.items():
        g = grams(v)
        hit = len(g & sg)
        print(f"{k}: {hit}/{len(g)} 13-grams found in training shard -> {'CONTAMINATED: remove from eval or from data' if hit else 'clean'}")

if __name__ == "__main__":
    main()
