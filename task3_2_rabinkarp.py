import pandas as pd


def rabin_karp(text, pat, q, d=256):
    """Rolling polynomial hash. Returns (hash_hits, verified, spurious)."""
    n, m = len(text), len(pat)
    h = pow(d, m - 1, q)              # d^(m-1) mod q, used to drop the leading char
    p = t = 0
    for i in range(m):                # hash of pattern and first window
        p = (d * p + ord(pat[i])) % q
        t = (d * t + ord(text[i])) % q

    hash_hits = verified = spurious = 0
    for i in range(n - m + 1):
        if p == t:
            hash_hits += 1
            if text[i:i + m] == pat:  # verify character by character
                verified += 1
            else:
                spurious += 1
        if i < n - m:                 # roll the hash to the next window
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
    return hash_hits, verified, spurious


if __name__ == "__main__":
    pattern = "gluten free"

    # --- S1000 check first ---
    s = pd.read_pickle("data/s1000.pkl")
    small = "\n".join(s["Text"].tolist())
    print("S1000 expected:", small.count(pattern),
          "| RK (q=101):", rabin_karp(small, pattern, 101),
          "| RK (q=1e9+7):", rabin_karp(small, pattern, 1_000_000_007))

    # --- first 100,000 characters of the dataset ---
    df = pd.read_pickle("data/clean.pkl")
    text = "\n".join(df["Text"].tolist()[:2000])[:100000]
    print("\nText length:", len(text))
    print("Expected matches (str.count):", text.count(pattern))

    for q in (101, 1_000_000_007):
        hh, vm, sp = rabin_karp(text, pattern, q)
        print("\nq = %d" % q)
        print("  Hash hits:       ", hh)
        print("  Verified matches:", vm)
        print("  Spurious hits:   ", sp)

    # --- concept demo: ASCII-sum hash ---
    print("\nASCII sum of 'listen':", sum(ord(c) for c in "listen"))
    print("ASCII sum of 'silent':", sum(ord(c) for c in "silent"))