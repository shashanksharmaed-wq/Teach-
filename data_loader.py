import pandas as pd
import os

DATA_PATH = "data/master.tsv"

REQUIRED_COLUMNS = [
    "grade",
    "subject",
    "chapter name",
    "learning outcomes"
]

def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"❌ Data file not found at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH, sep="\t")

    # normalize columns
    df.columns = [c.strip().lower() for c in df.columns]

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise KeyError(f"❌ Required column missing: {col}")

    return df
