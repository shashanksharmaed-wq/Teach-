import pandas as pd
import os

DATA_PATH = "data/Teachshank_Master_Database_FINAL_v2.tsv"

# --------------------------------------------------
# DATA LOADER (SCHEMA-SAFE)
# --------------------------------------------------
def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"❌ Data file not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH, sep="\t")

    # Normalize headers
    df.columns = [c.strip().lower() for c in df.columns]

    # Column mapping (HUMAN → SYSTEM)
    column_map = {
        "grade": "class",
        "class": "class",
        "subject": "subject",
        "chapter name": "chapter",
        "chapter": "chapter",
        "learning outcomes": "learning_outcome",
        "learning outcome": "learning_outcome",
        "lo": "learning_outcome"
    }

    df = df.rename(columns=column_map)

    required = ["class", "subject", "chapter", "learning_outcome"]
    for col in required:
        if col not in df.columns:
            raise KeyError(f"❌ Required column missing after mapping: {col}")

    # Clean values
    df["class"] = df["class"].astype(str).str.strip()
    df["subject"] = df["subject"].str.strip()
    df["chapter"] = df["chapter"].str.strip()
    df["learning_outcome"] = df["learning_outcome"].str.strip()

    return df


# --------------------------------------------------
# UTIL HELPERS
# --------------------------------------------------
def get_classes(df):
    return sorted(df["class"].unique())


def get_subjects(df, grade):
    return sorted(df[df["class"] == grade]["subject"].unique())


def get_chapters(df, grade, subject):
    return sorted(
        df[
            (df["class"] == grade) &
            (df["subject"] == subject)
        ]["chapter"].unique()
    )
