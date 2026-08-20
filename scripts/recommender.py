import sqlite3
import pandas as pd

DB_PATH = "../db/bluestock_mf.db"

def load_fund_performance():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("""
        SELECT p.amfi_code, f.scheme_name, p.sharpe_ratio, p.risk_grade
        FROM fact_performance p
        JOIN dim_fund f ON p.amfi_code = f.amfi_code
    """, conn)
    conn.close()
    return df

def recommend_funds(risk_appetite: str, fund_df: pd.DataFrame = None, top_n: int = 3):
    if fund_df is None:
        fund_df = load_fund_performance()
    matched = fund_df[fund_df["risk_grade"].str.lower() == risk_appetite.lower()]
    return matched.sort_values("sharpe_ratio", ascending=False).head(top_n)

if __name__ == "__main__":
    for level in ["Low", "Moderate", "High"]:
        print(f"\nTop funds for {level} risk appetite:")
        print(recommend_funds(level))