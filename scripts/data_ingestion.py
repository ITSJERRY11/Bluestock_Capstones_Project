import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

def load_all_csvs():
    csv_files = sorted(RAW_DIR.glob("*.csv"))
    print(f"Found {len(csv_files)} CSV files in {RAW_DIR}\n")

    dataframes = {}
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            print(f"=== {file.name} ===")
            print("Shape:", df.shape)
            print("Dtypes:\n", df.dtypes)
            print("Head:\n", df.head())
            print("-" * 60, "\n")
            dataframes[file.stem] = df
        except Exception as e:
            print(f"FAILED to load {file.name}: {e}\n")

    return dataframes

if __name__ == "__main__":
    load_all_csvs()