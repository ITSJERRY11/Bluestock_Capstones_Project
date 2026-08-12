import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw"
PROCESSED = BASE / "data" / "processed"
DB_PATH = BASE / "db" / "bluestock_mf.db"
SCHEMA_PATH = BASE / "sql" / "schema.sql"

engine = create_engine(f"sqlite:///{DB_PATH}")

def build_schema():
    with engine.begin() as conn:
        with open(SCHEMA_PATH, "r") as f:
            schema_sql = f.read()
        for statement in schema_sql.split(";"):
            statement = statement.strip()
            if statement:
                conn.exec_driver_sql(statement)
    print("Schema created.")

def build_dim_date():
    nav = pd.read_csv(PROCESSED / "nav_history_clean.csv", parse_dates=["date"])
    txn = pd.read_csv(PROCESSED / "investor_transactions_clean.csv", parse_dates=["transaction_date"])
    all_dates = pd.concat([nav["date"], txn["transaction_date"]]).drop_duplicates().sort_values()

    dim_date = pd.DataFrame({"date": all_dates})
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["quarter"] = dim_date["date"].dt.quarter
    dim_date["day_of_week"] = dim_date["date"].dt.day_name()
    dim_date["is_weekday"] = dim_date["date"].dt.dayofweek.lt(5).astype(int)
    dim_date["date"] = dim_date["date"].dt.strftime("%Y-%m-%d")

    dim_date.to_sql("dim_date", engine, if_exists="append", index=False)
    print(f"Loaded dim_date: {len(dim_date)} rows")

    return pd.read_sql("SELECT date_id, date FROM dim_date", engine)

def load_dim_fund():
    df = pd.read_csv(RAW / "01_fund_master.csv")
    df.to_sql("dim_fund", engine, if_exists="append", index=False)
    print(f"Loaded dim_fund: {len(df)} rows")

def load_fact_nav(date_map):
    df = pd.read_csv(PROCESSED / "nav_history_clean.csv")
    df = df.merge(date_map, on="date", how="left")
    df = df[["amfi_code", "date_id", "nav"]]
    df.to_sql("fact_nav", engine, if_exists="append", index=False)
    print(f"Loaded fact_nav: {len(df)} rows")

def load_fact_transactions(date_map):
    df = pd.read_csv(PROCESSED / "investor_transactions_clean.csv")
    df = df.rename(columns={"transaction_date": "date"})
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    df = df.merge(date_map, on="date", how="left")
    df = df.drop(columns=["date"])
    df.to_sql("fact_transactions", engine, if_exists="append", index=False)
    print(f"Loaded fact_transactions: {len(df)} rows")

def load_fact_performance():
    df = pd.read_csv(PROCESSED / "scheme_performance_clean.csv")
    keep_cols = [
        "amfi_code", "return_1yr_pct", "return_3yr_pct", "return_5yr_pct",
        "benchmark_3yr_pct", "alpha", "beta", "sharpe_ratio", "sortino_ratio",
        "std_dev_ann_pct", "max_drawdown_pct", "aum_crore", "expense_ratio_pct",
        "morningstar_rating", "risk_grade"
    ]
    df = df[keep_cols]
    df.to_sql("fact_performance", engine, if_exists="append", index=False)
    print(f"Loaded fact_performance: {len(df)} rows")

def load_fact_portfolio():
    df = pd.read_csv(RAW / "09_portfolio_holdings.csv")
    df.to_sql("fact_portfolio", engine, if_exists="append", index=False)
    print(f"Loaded fact_portfolio: {len(df)} rows")

def load_fact_aum():
    df = pd.read_csv(RAW / "03_aum_by_fund_house.csv")
    df.to_sql("fact_aum", engine, if_exists="append", index=False)
    print(f"Loaded fact_aum: {len(df)} rows")

def load_fact_sip_industry():
    df = pd.read_csv(RAW / "04_monthly_sip_inflows.csv")
    df.to_sql("fact_sip_industry", engine, if_exists="append", index=False)
    print(f"Loaded fact_sip_industry: {len(df)} rows")

if __name__ == "__main__":
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()  # fresh DB each run

    build_schema()
    load_dim_fund()
    date_map = build_dim_date()
    load_fact_nav(date_map)
    load_fact_transactions(date_map)
    load_fact_performance()
    load_fact_portfolio()
    load_fact_aum()
    load_fact_sip_industry()
    print("\nAll tables loaded successfully.")