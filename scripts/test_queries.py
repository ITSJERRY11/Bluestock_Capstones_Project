from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///db/bluestock_mf.db')

with open('sql/queries.sql') as f:
    content = f.read()

raw_blocks = [b.strip() for b in content.split(';') if b.strip()]

queries = []
for block in raw_blocks:
    lines = [line for line in block.split('\n') if not line.strip().startswith('--')]
    cleaned = '\n'.join(lines).strip()
    if cleaned:
        queries.append(cleaned)

print(f"Found {len(queries)} queries to test.\n")

for i, q in enumerate(queries, 1):
    try:
        df = pd.read_sql(q, engine)
        print(f'Query {i}: OK ({len(df)} rows)')
    except Exception as e:
        print(f'Query {i}: FAILED - {e}')
