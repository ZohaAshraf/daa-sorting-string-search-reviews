import pandas as pd


def load_and_clean(path="data/Reviews.csv"):
    df = pd.read_csv(path)
    print("Rows in raw file:", len(df))

    # 1. Drop rows with missing values in the important columns
    must_have = ["ProductId", "Score", "Time",
                 "HelpfulnessNumerator", "HelpfulnessDenominator", "Text"]
    df = df.dropna(subset=must_have)

    # 2. Keep a raw copy of Text, then clean it
    df["Text_raw"] = df["Text"]
    df["Text"] = (df["Text"]
                  .str.replace(r"<[^>]+>", " ", regex=True)  # html tags -> space
                  .str.lower())

    # 3. Drop denominator 0 FIRST, then make ratio, then drop ratio > 1
    df = df[df["HelpfulnessDenominator"] != 0]
    df["ratio"] = df["HelpfulnessNumerator"] / df["HelpfulnessDenominator"]
    df = df[df["ratio"] <= 1]

    df = df.reset_index(drop=True)
    return df


if __name__ == "__main__":
    df = load_and_clean()
    print("Rows after cleaning:", len(df))

    # 4. S1000 = first 1000 rows of the cleaned data
    S1000 = df.head(1000).copy()
    print("S1000 rows:", len(S1000))

    # Save for fast loading in later tasks (ignored by git)
    df.to_pickle("data/clean.pkl")
    S1000.to_pickle("data/s1000.pkl")

    print(df[["ProductId", "Score", "Time", "ratio"]].head())
    print(df["Text"].iloc[0][:150])