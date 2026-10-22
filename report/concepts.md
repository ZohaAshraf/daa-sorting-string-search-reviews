# Conceptual Answers

## Task 1.1: Why heap sort is unstable
Heap sort swaps the root with the last element of the heap. That one swap carries an element past all the others in between, including ones with the same key, so equal keys can end up in a different order.

Example: [2a, 2b, 1], where 2a and 2b are equal and 2a came first. Sorting ascending with a max-heap:

- The array is already a max-heap: [2a, 2b, 1]
- Swap root with last, then fix the heap: [1, 2b, 2a] becomes [2b, 1, 2a]
- Swap root with position 1: [1, 2b, 2a]

In the result, 2b comes before 2a, so the original order of equal keys was lost.

## Task 2.1: Why the placement loop runs backwards
After the prefix sums, count[s] points just past the last slot for score s. Going backwards, the last item with that score takes the last slot, the one before it takes the slot before, and so on, so equal items keep their order. Going forwards, the first item takes the last slot and equal items come out reversed. The data is still sorted but the sort is no longer stable, which breaks radix sort because it needs a stable sort in every pass.

## Task 2.1: Why counting sort on timestamps is a bad idea
Counting sort needs one counter for every possible value. Unix timestamps in this data span about 400 million seconds, so we would need hundreds of millions of counters for only a few hundred thousand reviews. The time is O(n + k) and k is far bigger than n, so it wastes memory and is slower than a normal O(n log n) sort.

## Task 2.2: Is base-256 always faster?
Not always. Base-256 needs 4 passes instead of 10, but each pass writes items into 256 different places in memory. On a large array this can cause cache misses, and with a much bigger base the count array would no longer fit in the CPU cache. So the best base depends on the machine. Base-256 is small enough to fit in cache, so it usually wins.
My times: Base-10 = [  ] s, Base-256 = [  ] s.

## Task 2.3: Why one bucket is so large
Most people either vote that a review was helpful or not, and many reviews have only 1 or 2 votes. That gives ratios of exactly 1.0 or 0.0, so the values pile up at the ends, and the 1.0 values all land in bucket 9.
My bucket sizes: [  ].
Bucket sort is O(n) only when items spread evenly, about n/10 per bucket. With one huge bucket, most of the work happens inside it, so the speed moves toward O(n squared). It is not always that bad, because a pile of identical values is cheap for insertion sort, but the mixed values in the same bucket still cost extra. More buckets, or merge sort inside big buckets, would fix this.

## Task 3.1: LPS array for "really really good"
The pattern has 18 characters (spaces count, shown here as _).

```
index: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17
char:  r e a l l y _ r e a l  l  y  _  g  o  o  d
LPS:   0 0 0 0 0 0 0 1 2 3 4  5  6  7  0  0  0  0
```

Working: indexes 0 to 6 are 0 because nothing has repeated yet. At index 7, "r" matches the first character of the pattern, so the value is 1. It grows by 1 each step while "really_" repeats, reaching 7 at index 13. At index 14, "g" does not match "r", so it falls back to 0, and "o", "o", "d" stay 0.
My comparison counts for "highly recommend": Naive = [  ], KMP = [  ].

## Task 3.1: Why naive search works well on English
Naive search is slow only when long partial matches fail late, like searching for aaaaab in aaaaaaaa. In normal English a mismatch usually happens on the first or second character. For "highly recommend", most positions fail right away because the letter is not "h", so each position costs about one comparison. The O(n*m) worst case almost never appears, so KMP saves very little.

## Task 3.2: Why summing ASCII values is a bad hash
A plain sum ignores the order of letters, so every anagram gets the same hash. "listen" and "silent" both sum to 655, so they look identical. Other words with the same letter total also collide. This creates many spurious hits, and each one needs a full check, so the search can slow toward O(n*m). A polynomial hash multiplies each letter by a different power of the base, so position matters and the two words get different hashes.

With q = 101 there are only 101 possible hash values, so unrelated windows collide often. With q = 1,000,000,007 collisions are very rare, so hash hits are almost the same as real matches.
My results: q = 101: hash hits [  ], verified [  ], spurious [  ]. q = 1,000,000,007: hash hits [  ], verified [  ], spurious [  ].

## Task 4.1: Notes on the pipeline
The search matches the exact phrase "gluten free", so reviews that write "gluten-free" with a hyphen are not counted. Percentages use the cleaned dataset, so review counts per product are lower than in the raw file. KMP flags the reviews, radix sort groups them by ProductId, and one pass over the groups computes each percentage. Only the final Top 10 selection uses a built-in sort.