import random

def generate_questions(df, filters, count):
    filtered = df[
        (df["board"] == filters["board"]) &
        (df["grade"] == filters["grade"]) &
        (df["subject"] == filters["subject"]) &
        (df["chapter"].isin(filters["chapters"]))
    ]

    if filtered.empty:
        return []

    return filtered.sample(min(count, len(filtered))).to_dict("records")
