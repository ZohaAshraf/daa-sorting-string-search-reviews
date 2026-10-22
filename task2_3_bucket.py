import time
import pandas as pd


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def bucket_sort(values, num_buckets=10):
    """Values must be in [0.0, 1.0]. Returns (sorted list, bucket sizes)."""
    buckets = [[] for _ in range(num_buckets)]
    for v in values:
        idx = int(v * num_buckets)
        if idx == num_buckets:          # ratio == 1.0 goes in the last bucket
            idx = num_buckets - 1
        buckets[idx].append(v)
    sizes = [len(b) for b in buckets]
    for b in buckets:
        insertion_sort(b)
    result = []
    for b in buckets:
        result.extend(b)
    return result, sizes


def bucket_sizes_only(values, num_buckets=10):
    sizes = [0] * num_buckets
    for v in values:
        idx = int(v * num_buckets)
        if idx == num_buckets:
            idx = num_buckets - 1
        sizes[idx] += 1
    return sizes


if __name__ == "__main__":
    # --- S1000 first ---
    s = pd.read_pickle("data/s1000.pkl")
    small = s["ratio"].astype(float).tolist()
    out, sizes = bucket_sort(small)
    print("S1000 correct:", out == sorted(small))
    print("S1000 bucket sizes:", sizes)

    # --- full dataset: bucket sizes only ---
    df = pd.read_pickle("data/clean.pkl")
    ratios = df["ratio"].astype(float).tolist()
    print("\nRows:", len(ratios))
    sizes = bucket_sizes_only(ratios)
    for i, c in enumerate(sizes):
        print("Bucket %d [%.1f, %.1f%s: %d (%.1f%%)" % (
            i, i / 10, (i + 1) / 10, "]" if i == 9 else ")",
            c, 100 * c / len(ratios)))

    # --- full bucket sort + insertion sort on a 20,000-row sample ---
    sample = ratios[:20000]
    start = time.perf_counter()
    out, sample_sizes = bucket_sort(sample)
    print("\n20,000-row sample: sorted in %.2f s, correct: %s"
          % (time.perf_counter() - start, out == sorted(sample)))
    print("Sample bucket sizes:", sample_sizes)
    print("Note: insertion sort on the full largest bucket (%d items) "
          "is O(n^2), impractical in pure Python." % max(sizes))