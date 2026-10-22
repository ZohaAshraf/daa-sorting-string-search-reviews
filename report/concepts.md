Why heap sort is unstable
Heap sort moves the root to the end by swapping it with the last element. That swap jumps over other elements with the same value, so their original order can change.
Example: take [2a, 2b, 1] (2a and 2b are equal, 2a came first). Sorting ascending with a max-heap:

Build heap: stays [2a, 2b, 1]
Swap root with last: [1, 2b, 2a], then fix the heap: [2b, 1, 2a]
Swap root with position 1: [1, 2b, 2a]

The result is [1, 2b, 2a]. 2b now comes before 2a, so the order of equal keys changed. That proves it is unstable.

Why counting sort’s placement loop runs backwards
After the prefix sums, count[s] points to the last free spot for score s. Going backwards, the last item with that score gets the last spot, the one before it gets the spot before, and so on. So equal items keep their original order. If you run it forwards, the first item with score s takes the last spot, so equal items end up reversed. The sort still works, but it is no longer stable. Stability matters because radix sort uses counting sort inside it.

Why counting sort on Unix timestamps is a terrible idea
Counting sort needs a count array as big as the range of values. The timestamps in this data span about 400 million seconds (1999 to 2012), so the array would have hundreds of millions of cells for only about 300K reviews. That wastes huge memory. The time is O(n + k), and here k is far bigger than n, so it is slower than a normal O(n log n) sort.
Does fewer passes always mean faster? No. Base-256 needs only 4 passes instead of 10, but each pass uses a 256-slot count array and scatters items into 256 different output regions. On a large array, those scattered writes can cause cache and TLB misses, especially if the digit size gets bigger (for example base 65536, where the count array alone no longer fits in L1/L2 cache). So the best base depends on the machine's cache sizes. With 256 buckets the count array is tiny and fits in cache, so it usually still wins here. In pure Python, interpreter overhead also hides much of the cache effect.