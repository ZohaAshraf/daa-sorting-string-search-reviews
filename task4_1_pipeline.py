import time
import pandas as pd


# ---------- KMP (existence check) ----------
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
            i += 1
    return lps


def kmp_contains(text, pat, lps):
    """True as soon as the pattern is found."""
    n, m = len(text), len(pat)
    i = j = 0
    while i < n:
        if text[i] == pat[j]:
            i += 1
            j += 1
            if j == m:
                return True
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
    return False


# ---------- LSD radix sort on strings (base 256) ----------
def radix_sort_strings(keys):
    """Returns original row positions sorted by key."""
    n = len(keys)
    width = max(len(k) for k in keys)
    padded = [k.ljust(width, "\0") for k in keys]
    order = list(range(n))
    for pos in range(width - 1, -1, -1):          # last char first
        count = [0] * 256
        for i in order:
            count[ord(padded[i][pos])] += 1
        for d in range(1, 256):
            count[d] += count[d - 1]
        out = [0] * n
        for i in reversed(order):                  # backwards = stable
            d = ord(padded[i][pos])
            count[d] -= 1
            out[count[d]] = i
        order = out
    return order


if __name__ == "__main__":
    pattern = "gluten free"
    lps = compute_lps(pattern)

    df = pd.read_pickle("data/clean.pkl")
    ids = df["ProductId"].astype(str).tolist()
    texts = df["Text"].tolist()
    print("Rows:", len(ids))

    # Step 1: flag reviews with KMP
    start = time.perf_counter()
    flags = [kmp_contains(t, pattern, lps) for t in texts]
    print("Step 1 (KMP flagging): %.1f s, flagged: %d"
          % (time.perf_counter() - start, sum(flags)))

    # Step 2: radix sort ProductId to group products
    start = time.perf_counter()
    order = radix_sort_strings(ids)
    print("Step 2 (radix sort): %.1f s" % (time.perf_counter() - start))
    sorted_ids = [ids[i] for i in order]
    print("ProductId sorted correctly:", sorted_ids == sorted(ids))

    # Step 3: scan groups, compute percentages
    results = []
    i = 0
    n = len(order)
    while i < n:
        pid = ids[order[i]]
        total = flagged = 0
        while i < n and ids[order[i]] == pid:
            total += 1
            if flags[order[i]]:
                flagged += 1
            i += 1
        if total >= 50:
            results.append((pid, total, flagged, 100.0 * flagged / total))
    print("Products with >= 50 reviews:", len(results))

    top10 = sorted(results, key=lambda r: (-r[3], -r[1], r[0]))[:10]
    print("\nTop 10 products by %% of reviews containing '%s':" % pattern)
    print("%-4s %-12s %-8s %-8s %s" % ("#", "ProductId", "Reviews", "Matches", "Percent"))
    for rank, (pid, total, flagged, pct) in enumerate(top10, 1):
        print("%-4d %-12s %-8d %-8d %.2f%%" % (rank, pid, total, flagged, pct))

    # Verification with pandas (allowed for checking only)
    check = pd.DataFrame({"pid": ids, "f": df["Text"].str.contains(pattern).tolist()})
    g = check.groupby("pid")["f"].agg(["size", "sum"])
    g = g[g["size"] >= 50]
    print("\nVerification: flagged matches pandas:",
          sum(flags) == int(check["f"].sum()),
          "| valid products match:", len(g) == len(results))