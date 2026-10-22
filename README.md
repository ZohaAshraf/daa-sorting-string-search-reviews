# DAA Assignment 3: Sorting and String Searching on Real Data

**Course:** CS2009 Design and Analysis of Algorithms, Fall 2026
**University:** National University of Computer and Emerging Sciences
**Dataset:** Amazon Fine Food Reviews (Kaggle)

## About
This project implements sorting and string-searching algorithms from scratch and runs them on over 500,000 real product reviews. The goal is to see how these algorithms behave on real data, not just on textbook examples. Pandas is used only for data cleaning (Part 0) and to double-check my own results. Every sorting and searching algorithm is written by hand.

## What is implemented

| Part | Task | Algorithm | File |
|------|------|-----------|------|
| 0 | Data preparation | Cleaning and the S1000 sample | `part0_prepare.py` |
| 1 | 1.1 | Max-Heap, Min-Heap, Heap Sort, Top 10 | `task1_1_heap.py` |
| 2 | 2.1 | Stable Counting Sort on Score | `task2_1_counting.py` |
| 2 | 2.2 | LSD Radix Sort on Time (base 10 vs base 256) | `task2_2_radix.py` |
| 2 | 2.3 | Bucket Sort on helpfulness ratio | `task2_3_bucket.py` |
| 3 | 3.1 | Naive search vs KMP | `task3_1_search.py` |
| 3 | 3.2 | Rabin-Karp with two moduli | `task3_2_rabinkarp.py` |
| 4 | 4.1 | "Gluten free" mini-pipeline | `task4_1_pipeline.py` |

## Project structure
```
daa-sorting-string-search-reviews/
|-- data/                    (Reviews.csv and generated files, not tracked by git)
|-- report/                  (output screenshots, concepts.md, final PDF)
|-- part0_prepare.py
|-- task1_1_heap.py
|-- task2_1_counting.py
|-- task2_2_radix.py
|-- task2_3_bucket.py
|-- task3_1_search.py
|-- task3_2_rabinkarp.py
|-- task4_1_pipeline.py
|-- build_report.py
`-- README.md
```

## Requirements
- Python 3.9 or newer
- pandas (data cleaning and verification only)
- fpdf2 and pillow (only for building the PDF report)

```
pip install pandas fpdf2 pillow
```

## How to run
1. Download `Reviews.csv` from [Kaggle](https://www.kaggle.com/snap/amazon-fine-food-reviews) and place it in the `data/` folder.
2. Run Part 0 first. It cleans the data and saves `clean.pkl` and `s1000.pkl` in `data/`:
```
   python part0_prepare.py
```
3. Run any task from the project folder:
```
   python task1_1_heap.py
   python task2_1_counting.py
   python task2_2_radix.py      # takes 1 to 3 minutes
   python task2_3_bucket.py
   python task3_1_search.py
   python task3_2_rabinkarp.py
   python task4_1_pipeline.py   # takes 1 to 3 minutes
```
4. Build the final report:
```
   python build_report.py
```
   This creates `report/DAA_Assignment3_Report.pdf`.

## Data cleaning (Part 0)
- Dropped rows with missing ProductId, Score, Time, HelpfulnessNumerator, HelpfulnessDenominator or Text.
- Removed HTML tags from the review text and converted it to lowercase. The original text is kept in `Text_raw`.
- Added `ratio = HelpfulnessNumerator / HelpfulnessDenominator`, and dropped rows where the denominator is 0 or the ratio is above 1.
- `S1000` is the first 1,000 rows of the cleaned data. It was used to test and debug before running on the full dataset.

## Notes
- Every algorithm was checked against Python's built-in result, and the scripts print the outcome of that check.
- Task 4.1 searches for the exact phrase "gluten free", so reviews written as "gluten-free" are not counted.
- Percentages in Task 4.1 use the cleaned dataset, so review counts per product are lower than in the raw file.

## Author
Zoha Ashraf