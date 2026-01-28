# annual_plan_engine.py

def get_weekly_periods(subject: str) -> int:
    """
    CBSE-aligned weekly periods per subject
    Defensive against None / invalid input
    """
    if not subject or not isinstance(subject, str):
        return 5  # safe CBSE default

    s = subject.lower()

    mapping = {
        "math": 6,
        "mathematics": 6,
        "science": 6,
        "physics": 6,
        "chemistry": 6,
        "biology": 6,
        "english": 7,
        "language": 7,
        "evs": 5,
        "social": 5,
        "history": 4,
        "geography": 4,
        "civics": 3,
        "economics": 3,
        "computer": 3,
    }

    for key, val in mapping.items():
        if key in s:
            return val

    return 5


def generate_annual_plan(df, grade, subject, academic_days):
    """
    Period-based annual planning
    CBSE-safe, no rushing chapters
    """

    if subject is None:
        return {"chapters": []}

    weekly_periods = get_weekly_periods(subject)
    total_weeks = academic_days // 5
    total_periods = total_weeks * weekly_periods

    # Reserve CBSE mandatory blocks
    cbse_reserved = {
        "revision": int(total_periods * 0.15),
        "assessment": int(total_periods * 0.10),
        "exams": int(total_periods * 0.10),
        "remediation": int(total_periods * 0.05),
    }

    usable_periods = total_periods - sum(cbse_reserved.values())

    subject_df = df[
        (df["grade"] == grade) &
        (df["subject"] == subject)
    ]

    if subject_df.empty:
        return {"chapters": []}

    chapters = []
    chapter_groups = subject_df.groupby("chapter")

    total_los = chapter_groups["learning_outcome"].nunique().sum()

    for chapter, grp in chapter_groups:
        lo_count = grp["learning_outcome"].nunique()

        # Weight by learning outcomes
        required_periods = max(
            2,
            round((lo_count / total_los) * usable_periods)
        )

        chapters.append({
            "chapter": chapter,
            "learning_outcomes": lo_count,
            "required_periods": required_periods,
            "completed_periods": 0
        })

    return {
        "grade": grade,
        "subject": subject,
        "academic_days": academic_days,
        "weekly_periods": weekly_periods,
        "total_periods": total_periods,
        "cbse_blocks": cbse_reserved,
        "chapters": chapters
    }
