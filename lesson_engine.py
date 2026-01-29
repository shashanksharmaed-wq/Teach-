import pandas as pd
import os

# -------------------------------------------------
# DATA LOADING (SINGLE SOURCE OF TRUTH)
# -------------------------------------------------
DATA_PATHS = [
    "data/master.tsv",
    "master.tsv"
]

def load_data():
    """
    Loads the master TSV file safely.
    Tries multiple paths so Streamlit Cloud never crashes.
    """
    for path in DATA_PATHS:
        if os.path.exists(path):
            df = pd.read_csv(path, sep="\t")
            break
    else:
        raise FileNotFoundError(
            "❌ master.tsv not found. Create data/master.tsv in the repo."
        )

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # Mandatory columns check
    required = ["class", "subject", "chapter", "learning_outcome"]
    for col in required:
        if col not in df.columns:
            raise KeyError(f"❌ Required column missing in TSV: {col}")

    return df


# -------------------------------------------------
# SYLLABUS HELPERS
# -------------------------------------------------
def get_chapters(df, grade, subject):
    sub_df = df[
        (df["class"] == grade) &
        (df["subject"] == subject)
    ]
    return sorted(sub_df["chapter"].dropna().unique().tolist())


def get_learning_outcomes(df, grade, subject, chapter):
    sub_df = df[
        (df["class"] == grade) &
        (df["subject"] == subject) &
        (df["chapter"] == chapter)
    ]
    return sub_df["learning_outcome"].dropna().unique().tolist()
