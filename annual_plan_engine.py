"""
ERPACAD – Annual Academic Planning Engine
PERIOD-BASED | CBSE-ALIGNED | STABLE

Design principles:
- Principal sets ONLY total working days per class
- Planning is done in PERIODS (not days)
- CBSE blocks (revision, exams, assessment, remediation) are mandatory
- Chapters cannot be rushed
- Output is structured (UI decides what to display)
"""

# =====================================================
# CONFIGURATION (CBSE REALITY)
# =====================================================

PERIODS_PER_DAY = 8

CBSE_BLOCKS = {
    "teaching": 0.65,
    "revision": 0.10,
    "assessment": 0.10,
    "exams": 0.10,
    "buffer": 0.05
}

# Weekly subject frequency (typical CBSE timetable)
WEEKLY_PERIODS = {
    "science": 5,
    "mathematics": 5,
    "english": 5,
    "social science": 4,
    "hindi": 4,
    "language": 4,
    "computer": 2,
    "gk": 2,
    "evs": 5
}

# Base minimum teaching load per chapter
BASE_CHAPTER_PERIODS = {
    "primary": 6,     # Class 1–5
    "middle": 10,     # Class 6–8
    "secondary": 14  # Class 9–10
}

# Mandatory integrations (play, art/subject, language)
INTEGRATION_PERIODS = 3


# =====================================================
# HELPERS (TYPE SAFE)
# =====================================================

def normalize_grade(grade):
    try:
        return int(grade)
    except Exception:
        raise ValueError(f"Invalid grade value: {grade}")


def get_class_band(grade):
    grade = normalize_grade(grade)
    if grade <= 5:
        return "primary"
    elif grade <= 8:
        return "middle"
    return "secondary"


def get_weekly_periods(subject):
    subject_lower = subject.lower()
    for key, value in WEEKLY_PERIODS.items():
        if key in subject_lower:
            return value
    return 4  # safe default


def calculate_chapter_periods(grade, lo_count):
    """
    Calculates minimum teaching periods required for a chapter.
    Ensures no unrealistic compression.
    """
    band = get_class_band(grade)
    base = BASE_CHAPTER_PERIODS[band]

    # LO influence (soft, capped)
    lo_factor = min(max(lo_count, 1), 5)

    periods = base + lo_factor + INTEGRATION_PERIODS

    # Absolute academic safety
    if band == "middle":
        periods = max(periods, 10)
    elif band == "secondary":
        periods = max(periods, 14)

    return periods


# =====================================================
# MAIN ENGINE
# =====================================================

def generate_annual_plan(df, grade, subject, total_working_days):
    """
    Generates an annual academic plan for ONE class + ONE subject.

    Returns a STRUCTURED DICT.
    UI must display only `plan["chapters"]` as table.
    """

    # -----------------------------
    # Normalize inputs
    # -----------------------------
    grade = normalize_grade(grade)
    total_working_days = int(total_working_days)

    # -----------------------------
    # Total periods
    # -----------------------------
    total_periods = total_working_days * PERIODS_PER_DAY
    teaching_periods = int(total_periods * CBSE_BLOCKS["teaching"])

    # -----------------------------
    # Weekly subject frequency
    # -----------------------------
    weekly_periods = get_weekly_periods(subject)

    # -----------------------------
    # Filter subject data
    # -----------------------------
    subject_df = df[
        (df["grade"] == grade) &
        (df["subject"] == subject)
    ]

    chapters = []
    total_required_periods = 0

    for chapter, group in subject_df.groupby("chapter"):
        lo_count = group["learning_outcome"].nunique()

        required_periods = calculate_chapter_periods(
            grade=grade,
            lo_count=lo_count
        )

        total_required_periods += required_periods

        chapters.append({
            "chapter": chapter,
            "required_periods": required_periods
        })

    # -----------------------------
    # Scale down if overflow
    # -----------------------------
    if total_required_periods > teaching_periods and total_required_periods > 0:
        scale = teaching_periods / total_required_periods
        min_floor = BASE_CHAPTER_PERIODS[get_class_band(grade)]

        for ch in chapters:
            ch["required_periods"] = max(
                int(ch["required_periods"] * scale),
                min_floor
            )

    # -----------------------------
    # Final chapter metadata
    # -----------------------------
    for ch in chapters:
        ch["approx_weeks"] = round(
            ch["required_periods"] / weekly_periods,
            1
        )
        ch["status"] = "Planned"

    # -----------------------------
    # Return structured plan
    # -----------------------------
    return {
        "grade": grade,
        "subject": subject,
        "total_working_days": total_working_days,
        "periods_per_day": PERIODS_PER_DAY,
        "total_periods": total_periods,
        "teaching_periods": teaching_periods,
        "weekly_periods": weekly_periods,
        "chapters": chapters,
        "cbse_blocks": {
            "revision_periods": int(total_periods * CBSE_BLOCKS["revision"]),
            "assessment_periods": int(total_periods * CBSE_BLOCKS["assessment"]),
            "exam_periods": int(total_periods * CBSE_BLOCKS["exams"]),
            "buffer_periods": int(total_periods * CBSE_BLOCKS["buffer"])
        }
    }
