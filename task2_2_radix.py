import time
import pandas as pd


def radix_sort_indices(keys, base):
    """LSD radix sort. Returns original row positions in sorted order.
    Each pass is a stable counting sort on one digit (in the given base)."""
    n = len(keys)
    order = list(range(n))
    max_key = max(keys)
    div = 1
    passes = 0
    while max_key // div > 0:
        count = [0] * base
        for i in order:
            count[(keys[i] // div) % base] += 1
        for d in range(1, base):                 # prefix sums
            count[d] += count[d - 1]
        out = [0] * n
        for i in reversed(order):                # BACKWARDS = stable
            d = (keys[i] // div) % base
            count[d] -= 1
            out[count[d]] = i
        order = out
        div *= base
        passes += 1
    return order, passes


def check(keys, order):
    sorted_keys = [keys[i] for i in order]
    ok_sorted = sorted_keys == sorted(keys)
    ok_stable = all(order[j] < order[j + 1]
                    for j in range(len(order) - 1)
                    if sorted_keys[j] == sorted_keys[j + 1])
    return ok_sorted, ok_stable


if __name__ == "__main__":
    # --- test on S1000 first ---
    s = pd.read_pickle("data/s1000.pkl")
    small = s["Time"].astype(int).tolist()
    for b in (10, 256):
        o, p = radix_sort_indices(small, b)
        print("S1000 base", b, "-> sorted/stable:", check(small, o))

    # --- full dataset ---
    df = pd.read_pickle("data/clean.pkl")
    times = df["Time"].astype(int).tolist()
    print("Rows:", len(times))

    results = {}
    for b in (10, 256):
        start = time.perf_counter()
        order, passes = radix_sort_indices(times, b)
        elapsed = time.perf_counter() - start
        results[b] = elapsed
        print("Base %d: %d passes, %.2f seconds" % (b, passes, elapsed))
        print("  sorted/stable:", check(times, order))

    print("Base-10 / Base-256 time ratio: %.2fx" % (results[10] / results[256]))
    print(df.iloc[order][["ProductId", "Time"]].head())