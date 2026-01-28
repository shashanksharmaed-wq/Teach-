"""
ERPACAD – Annual Academic Planning Engine
PERIOD-BASED (CBSE ALIGNED)

Authoritative rules:
- Principal sets ONLY total working days per class
- Everything else is system controlled
- Chapters are planned in TEACHING PERIODS
"""

# =====================================================
# CONFIGURATION (ACADEMIC ASSUMPTIONS)
# =====================================================

PERIODS_PER_DAY = 8

CBSE_BLOCKS = {
    "teaching": 0.65,
    "revision": 0.10,
    "assessment": 0.10,
    "exams": 0.10,
    "buffer": 0.05
}

# Weekly subject frequency (CBSE realistic)
WEEKLY_PERIODS = {
    "Science": 5,
    "Mathematics": 5,
    "English": 5,
    "Social Science": 4,
    "Hindi": 4,
    "Language": 4,
    "Computer": 2,
    "GK": 2,
    "EVS": 5
}

# Base chapter period requirements by class band
BASE_CHAPTER_PERIODS = {
    "primary": 6,     # Class 1–5
    "middle": 10,     # Class 6–8
    "secondary": 14   # Class 9–10
}

# Additional load for complexity & integrations
INTEGRATION_PERIODS = 3   # art / subject / play integration (mandatory)


# =====================================================
# HELPERS
# =====================================================

def get_class_band(grade: int) -> str:
    if grade <= 5:
        return "primary"
    elif grade <= 8:
        return "middle"
    return "secondary"


def subject_key(subject: str) -> str:
    for key in WEEKLY_PERIODS:
        if key.lower() in subject.lower():
            return key
    return "Language"


def calculate_chapter_periods(grade, subject, lo_count):
    """
    Determines minimum teaching periods required for a chapter.
    Prevents unrealistically short chapters.
    """
    band = get_class_band(grade)
    base = BASE_CHAPTER_PERIODS[band]

    # Learning outcome influence (soft, capped)
    lo_factor = min(max(lo_count, 1), 5)

    total_periods = base + lo_factor + INTEGRATION_PERIODS

    # Absolute minimum safety
    if band == "middle" and total_periods < 10:
        total_periods = 10
    if band == "secondary" and total_periods < 14:
        total_periods = 14

    return total_periods


# =====================================================
# MAIN ENGINE
# =====================================================

def generate_annual_plan(df, grade, subject, total_working_days):
    """
    Returns a CBSE-aligned annual plan for ONE class + subject
    Planned strictly in TEACHING PERIODS.
    """

    # -----------------------------
    # STEP 1: TOTAL PERIODS
    # -----------------------------
    total_periods = total_working_days * PERIODS_PER_DAY

    teaching_periods = int(total_periods * CBSE_BLOCKS["teaching"])

    # -----------------------------
    # STEP 2: WEEKLY FREQUENCY
    # -----------------------------
    subject_type = subject_key(subject)
    weekly_periods = WEEKLY_PERIODS.get(subject_type, 4)

    # -----------------------------
    # STEP 3: FILTER CHAPTERS
    # -----------------------------
    chapters_df = df[
        (df["grade"] == grade) &
        (df["subject"] == subject)
    ]

    chapters = []

    total_required_periods = 0

    for chapter, group in chapters_df.groupby("chapter"):
        lo_count = group["learning_outcome"].nunique()

        required_periods = calculate_chapter_periods(
            grade=grade,
            subject=subject,
            lo_count=lo_count
        )

        total_required_periods += required_periods

        chapters.append({
            "chapter": chapter,
            "required_periods": required_periods
        })

    # -----------------------------
    # STEP 4: NORMALIZE IF OVERFLOW
    # -----------------------------
    if total_required_periods > teaching_periods:
        scale = teaching_periods / total_required_periods
        for ch in chapters:
            ch["required_periods"] = max(
                int(ch["required_periods"] * scale),
                BASE_CHAPTER_PERIODS[get_class_band(grade)]
            )

    # -----------------------------
    # STEP 5: CALCULATE APPROX WEEKS
    # -----------------------------
    for ch in chapters:
        ch["approx_weeks"] = round(
            ch["required_periods"] / weekly_periods,
            1
        )
        ch["status"] = "Planned"

    return {
        "grade": grade,
        "subject": subject,
        "total_working_days": total_working_days,
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
