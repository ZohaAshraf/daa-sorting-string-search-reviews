import time
import pandas as pd


# ---------- MAX-HEAP (0-based) ----------
def max_heapify(arr, n, i):
    while True:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest == i:
            break
        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest


def build_max_heap(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        max_heapify(arr, n, i)


# ---------- MIN-HEAP (used for the descending sort) ----------
def min_heapify(arr, n, i):
    while True:
        smallest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] < arr[smallest]:
            smallest = left
        if right < n and arr[right] < arr[smallest]:
            smallest = right
        if smallest == i:
            break
        arr[i], arr[smallest] = arr[smallest], arr[i]
        i = smallest


def build_min_heap(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        min_heapify(arr, n, i)


def heap_sort_descending(arr):
    """Build a MIN-heap, then move the smallest to the end each time.
    The array ends up in descending order."""
    build_min_heap(arr)
    for end in range(len(arr) - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        min_heapify(arr, end, 0)


if __name__ == "__main__":
    # --- test on S1000 first ---
    s = pd.read_pickle("data/s1000.pkl")
    small = s["HelpfulnessDenominator"].astype(int).tolist()
    expected = sorted(small, reverse=True)
    heap_sort_descending(small)
    print("S1000 correct:", small == expected)

    # --- max-heap check ---
    test = [4, 10, 3, 5, 1]
    build_max_heap(test)
    print("Max-heap of [4,10,3,5,1]:", test, "(root should be 10)")

    # --- full dataset ---
    df = pd.read_pickle("data/clean.pkl")
    data = df["HelpfulnessDenominator"].astype(int).tolist()
    expected = sorted(data, reverse=True)   # only to verify

    start = time.time()
    heap_sort_descending(data)
    print("Full data sorted in %.2f seconds" % (time.time() - start))
    print("Full data correct:", data == expected)

    print("Top 10 largest HelpfulnessDenominator:", data[:10])