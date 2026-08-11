import pandas as pd
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "data" / "raw" / "07_scheme_performance.csv"
OUT = Path(__file__).resolve().parent.parent / "data" / "processed" / "scheme_performance_clean.csv"
OUT.parent.mkdir(parents=True, exist_ok=True)

NUMERIC_COLS = [
    "return_1yr_pct", "return_3yr_pct", "return_5yr_pct", "benchmark_3yr_pct",
    "alpha", "beta", "sharpe_ratio", "sortino_ratio", "std_dev_ann_pct",
    "max_drawdown_pct", "aum_crore", "expense_ratio_pct"
]

def clean_performance():
    df = pd.read_csv(RAW)
    print("Initial shape:", df.shape)

    # 1. Validate returns/numeric columns are actually numeric
    for col in NUMERIC_COLS:
        before_na = df[col].isna().sum()
        df[col] = pd.to_numeric(df[col], errors="coerce")
        after_na = df[col].isna().sum()
        newly_bad = after_na - before_na
        if newly_bad > 0:
            print(f"  {col}: {newly_bad} non-numeric values coerced to NaN")

    # Drop rows where core return columns failed to parse
    before = len(df)
    df = df.dropna(subset=["return_1yr_pct", "return_3yr_pct", "return_5yr_pct"])
    print(f"Dropped {before - len(df)} rows with unparseable return values")

    # 2. Flag negative Sharpe ratios (don't drop — just flag, since negative Sharpe is valid data, not an error)
    df["flag_negative_sharpe"] = df["sharpe_ratio"] < 0
    print(f"Flagged {df['flag_negative_sharpe'].sum()} funds with negative Sharpe ratio")

    # 3. Check expense_ratio falls in 0.1%-2.5%
    out_of_range = df[(df["expense_ratio_pct"] < 0.1) | (df["expense_ratio_pct"] > 2.5)]
    print(f"Found {len(out_of_range)} funds with expense_ratio_pct outside 0.1%-2.5% range")
    df["flag_expense_ratio_out_of_range"] = (
        (df["expense_ratio_pct"] < 0.1) | (df["expense_ratio_pct"] > 2.5)
    )

    # 4. Drop exact duplicates
    before = len(df)
    df = df.drop_duplicates()
    print(f"Dropped {before - len(df)} duplicate rows")

    df.to_csv(OUT, index=False)
    print("Final shape:", df.shape)
    print(f"Saved to {OUT}")
    return df

if __name__ == "__main__":
    clean_performance()