import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

cells.append(nbf.v4.new_markdown_cell("# EDA Analysis — Bluestock MF Capstone\n\nExploratory analysis across NAV, AUM, SIP, performance, portfolio, and investor data."))

cells.append(nbf.v4.new_code_cell("""import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

engine = create_engine('sqlite:///../db/bluestock_mf.db')
print("Connected to database.")"""))

nb['cells'] = cells

with open('notebooks/EDA_Analysis.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Notebook created with", len(cells), "cells.")
