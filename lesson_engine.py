import pandas as pd
import os

DATA_PATHS = [
    "data/master.tsv",
    "master.tsv"
]

def load_data():
    for path in DATA_PATHS:
        if os.path.exists(path):
            df = pd.read_csv(path, sep="\t")
            break
    else:
        raise FileNotFoundError("❌ master.tsv not found. Put it inside /data folder.")

    # normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    REQUIRED = ["class", "subject", "chapter", "learning_outcome"]
    for col in REQUIRED:
        if col not in df.columns:
            raise KeyError(f"❌ Required column missing: {col}")

    return df


def get_chapters(df, grade, subject):
    sub = df[(df["class"] == grade) & (df["subject"] == subject)]
    return sorted(sub["chapter"].unique())


def get_learning_outcomes(df, grade, subject, chapter):
    sub = df[
        (df["class"] == grade) &
        (df["subject"] == subject) &
        (df["chapter"] == chapter)
    ]
    return sub["learning_outcome"].dropna().unique().tolist()
