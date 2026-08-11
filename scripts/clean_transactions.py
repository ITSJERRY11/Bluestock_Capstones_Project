import pandas as pd
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "data" / "raw" / "08_investor_transactions.csv"
OUT = Path(__file__).resolve().parent.parent / "data" / "processed" / "investor_transactions_clean.csv"
OUT.parent.mkdir(parents=True, exist_ok=True)

VALID_TXN_TYPES = {"SIP", "Lumpsum", "Redemption"}
VALID_KYC = {"Verified", "Pending"}

def clean_transactions():
    df = pd.read_csv(RAW)
    print("Initial shape:", df.shape)

    # 1. Standardize transaction_type (strip/title-case just in case, then validate)
    df["transaction_type"] = df["transaction_type"].astype(str).str.strip().str.title()
    df["transaction_type"] = df["transaction_type"].replace({"Sip": "SIP"})
    bad_types = df[~df["transaction_type"].isin(VALID_TXN_TYPES)]
    if len(bad_types):
        print(f"WARNING: {len(bad_types)} rows with invalid transaction_type — dropping")
        df = df[df["transaction_type"].isin(VALID_TXN_TYPES)]

    # 2. Validate amount > 0
    before = len(df)
    df = df[df["amount_inr"] > 0]
    print(f"Dropped {before - len(df)} rows with amount_inr <= 0")

    # 3. Check KYC status values
    bad_kyc = df[~df["kyc_status"].isin(VALID_KYC)]
    if len(bad_kyc):
        print(f"WARNING: {len(bad_kyc)} rows with unexpected kyc_status — dropping")
        df = df[df["kyc_status"].isin(VALID_KYC)]

    # 4. Fix date formats
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    bad_dates = df["transaction_date"].isna().sum()
    if bad_dates:
        print(f"Dropping {bad_dates} rows with unparseable transaction_date")
        df = df.dropna(subset=["transaction_date"])

    # 5. Drop exact duplicates
    before = len(df)
    df = df.drop_duplicates()
    print(f"Dropped {before - len(df)} duplicate rows")

    df.to_csv(OUT, index=False)
    print("Final shape:", df.shape)
    print(f"Saved to {OUT}")
    return df

if __name__ == "__main__":
    clean_transactions()