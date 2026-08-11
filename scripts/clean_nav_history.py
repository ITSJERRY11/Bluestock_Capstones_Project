import pandas as pd
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "data" / "raw" / "02_nav_history.csv"
OUT = Path(__file__).resolve().parent.parent / "data" / "processed" / "nav_history_clean.csv"
OUT.parent.mkdir(parents=True, exist_ok=True)

def clean_nav_history():
    df = pd.read_csv(RAW)
    print("Initial shape:", df.shape)

    # 1. Parse dates
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    bad_dates = df["date"].isna().sum()
    if bad_dates:
        print(f"Dropping {bad_dates} rows with unparseable dates")
        df = df.dropna(subset=["date"])

    # 2. Sort by amfi_code + date
    df = df.sort_values(["amfi_code", "date"]).reset_index(drop=True)

    # 3. Drop exact duplicates
    before = len(df)
    df = df.drop_duplicates(subset=["amfi_code", "date"], keep="first")
    print(f"Dropped {before - len(df)} duplicate rows")

    # 4. Forward-fill NAV on weekends/holidays: build full daily calendar per fund
    filled_frames = []
    for code, grp in df.groupby("amfi_code"):
        grp = grp.set_index("date").sort_index()
        full_range = pd.date_range(grp.index.min(), grp.index.max(), freq="D")
        grp = grp.reindex(full_range)
        grp["amfi_code"] = code
        grp["nav"] = grp["nav"].ffill()
        grp.index.name = "date"
        filled_frames.append(grp.reset_index())

    df = pd.concat(filled_frames, ignore_index=True)

    # 5. Assert nav > 0
    invalid = df[df["nav"] <= 0]
    if len(invalid):
        print(f"WARNING: {len(invalid)} rows with nav <= 0 — dropping them")
        df = df[df["nav"] > 0]

    assert (df["nav"] > 0).all(), "Found non-positive NAV after cleaning!"

    df = df[["amfi_code", "date", "nav"]]
    df.to_csv(OUT, index=False)
    print("Final shape:", df.shape)
    print(f"Saved to {OUT}")
    return df

if __name__ == "__main__":
    clean_nav_history()