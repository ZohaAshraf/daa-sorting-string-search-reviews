import pandas as pd


def counting_sort_indices(scores, k=5):
    """Stable counting sort. Returns the original row positions
    in sorted order, plus the count of each score."""
    count = [0] * (k + 1)
    for s in scores:
        count[s] += 1
    score_counts = count[1:]            # counts for scores 1..5

    for i in range(1, k + 1):           # prefix sums
        count[i] += count[i - 1]

    n = len(scores)
    order = [0] * n
    for i in range(n - 1, -1, -1):      # BACKWARDS loop = stable
        s = scores[i]
        count[s] -= 1
        order[count[s]] = i
    return order, score_counts


if __name__ == "__main__":
    df = pd.read_pickle("data/clean.pkl")
    scores = df["Score"].astype(int).tolist()

    order, score_counts = counting_sort_indices(scores)

    for sc, c in zip(range(1, 6), score_counts):
        print("Score", sc, "count:", c)
    print("Total:", sum(score_counts), "of", len(scores))

    # check: sorted, and stable (same score keeps original order)
    sorted_scores = [scores[i] for i in order]
    print("Sorted correctly:", sorted_scores == sorted(scores))
    stable = all(order[j] < order[j + 1]
                 for j in range(len(order) - 1)
                 if sorted_scores[j] == sorted_scores[j + 1])
    print("Stable:", stable)

    print(df.iloc[order][["ProductId", "Score"]].head())