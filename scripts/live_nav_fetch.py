import requests
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

SCHEMES = {
    "125497": "HDFC Top 100",
    "119551": "SBI Bluechip",
    "120503": "ICICI Bluechip",
    "118632": "Nippon Large Cap",
    "119092": "Axis Bluechip",
    "120841": "Kotak Bluechip",
}

def fetch_nav(scheme_code: str, name: str):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    payload = resp.json()

    nav_df = pd.DataFrame(payload["data"])
    nav_df["scheme_code"] = scheme_code
    nav_df["scheme_name"] = name

    out_path = RAW_DIR / f"nav_{scheme_code}.csv"
    nav_df.to_csv(out_path, index=False)
    print(f"Saved {out_path.name} — {nav_df.shape[0]} rows")

if __name__ == "__main__":
    for code, name in SCHEMES.items():
        try:
            fetch_nav(code, name)
        except Exception as e:
            print(f"FAILED for {name} ({code}): {e}")