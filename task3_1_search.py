import time
import pandas as pd


def naive_search(text, pat):
    """Returns (matches, character comparisons)."""
    n, m = len(text), len(pat)
    matches = 0
    comps = 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comps += 1
            if text[i + j] != pat[j]:
                break
            j += 1
        if j == m:
            matches += 1
    return matches, comps


def compute_lps(pat):
    lps = [0] * len(pat)
    length = 0
    i = 1
    while i < len(pat):
        if pat[i] == pat[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


def kmp_search(text, pat, lps):
    """Returns (matches, character comparisons)."""
    n, m = len(text), len(pat)
    i = j = 0
    matches = 0
    comps = 0
    while i < n:
        comps += 1
        if text[i] == pat[j]:
            i += 1
            j += 1
            if j == m:
                matches += 1
                j = lps[j - 1]
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
    return matches, comps


def search_all(texts, pat, use_kmp):
    lps = compute_lps(pat) if use_kmp else None
    total_matches = 0
    total_comps = 0
    for t in texts:
        if use_kmp:
            mt, c = kmp_search(t, pat, lps)
        else:
            mt, c = naive_search(t, pat)
        total_matches += mt
        total_comps += c
    return total_matches, total_comps


if __name__ == "__main__":
    pattern = "highly recommend"

    # --- LPS check for the concept question ---
    print("LPS of 'really really good':", compute_lps("really really good"))

    # --- S1000 first ---
    s = pd.read_pickle("data/s1000.pkl")
    small = s["Text"].tolist()
    expected = sum(t.count(pattern) for t in small)
    print("S1000 expected:", expected,
          "| naive:", search_all(small, pattern, False)[0],
          "| kmp:", search_all(small, pattern, True)[0])

    # --- first 10,000 reviews ---
    df = pd.read_pickle("data/clean.pkl")
    texts = df["Text"].iloc[:10000].tolist()
    expected = sum(t.count(pattern) for t in texts)
    print("\nPhrase:", repr(pattern), "| reviews:", len(texts))
    print("Expected matches (str.count):", expected)

    start = time.perf_counter()
    nm, nc = search_all(texts, pattern, False)
    nt = time.perf_counter() - start

    start = time.perf_counter()
    km, kc = search_all(texts, pattern, True)
    kt = time.perf_counter() - start

    print("Naive: %d matches, %d comparisons, %.2f s" % (nm, nc, nt))
    print("KMP:   %d matches, %d comparisons, %.2f s" % (km, kc, kt))
    print("Naive / KMP comparison ratio: %.3f" % (nc / kc))