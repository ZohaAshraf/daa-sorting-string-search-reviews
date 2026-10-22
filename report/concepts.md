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
Why is one bucket so large, and how does it affect O(n)?
People rarely vote "somewhat helpful". Most reviews with votes get either all helpful votes (ratio exactly 1.0) or none (0.0), and many have just 1 or 2 votes, which gives ratios like 1/1, 1/2 and 2/2. So the values pile up at the ends, and the 1.0 spike falls in bucket 9. Bucket sort's O(n) average case assumes values are spread uniformly across buckets so each holds about n/10 items. Here one bucket holds a large fraction of all n items, so insertion sort inside it costs O(n²) and the whole sort degrades toward O(n²) in the worst case. A fix would be to use more buckets, or to sort big buckets with a better algorithm such as merge sort.
Pattern: really really good (18 characters, the spaces count)

i	0	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17
char	r	e	a	l	l	y	␣	r	e	a	l	l	y	␣	g	o	o	d
LPS	0	0	0	0	0	0	0	1	2	3	4	5	6	7	0	0	0	0

LPS = [0,0,0,0,0,0,0,1,2,3,4,5,6,7,0,0,0,0]

Show your working in the report. At index 7, r matches the pattern's first character, so the LPS becomes 1. It then grows by 1 at each step as really␣ repeats, reaching 7 at index 13. At index 14, g doesn't match r, and it falls back all the way to 0. Your program prints the same array, so use it to verify.

Concept draft (reword in your own words)

Why does naive search work well on English text?
Naive search is slow only when the text has long partial matches that fail late, like searching for aaaaab in aaaaaaaa. In natural language, a mismatch almost always happens on the first or second character. For highly recommend, most positions fail immediately because the letter isn't h, so each position costs about 1 comparison, giving roughly O(n) in practice. Long repeated runs are rare in real text, so the O(n·m) worst case almost never shows up, and KMP saves only a small amount. That is why your comparison counts will be close to each other.
Why is summing ASCII values a bad hash?
A plain sum ignores the order of the characters, so any anagram gets the same hash. "listen" and "silent" use the same letters, so both sum to 633 and look identical to the algorithm. Different words with the same letter total also collide. That causes a flood of spurious hits, and every one of them needs a full character-by-character check, so the search can degrade toward O(n·m). A polynomial hash multiplies each character by a different power of the base, so position matters and "listen" and "silent" get different values. Spurious hits are then rare, and they happen only when the modulus is small.

Observation for your report: with q = 101 there are only 101 possible hash values, so unrelated windows collide often. With q = 1,000,000,007 collisions are very unlikely, so hash hits are almost exactly the real matches.