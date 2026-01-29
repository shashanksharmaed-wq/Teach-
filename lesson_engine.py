import pandas as pd
import os

# ==================================================
# SAFE DATA LOADING
# ==================================================

DATA_PATHS = [
    "data/master.tsv",
    "master.tsv"
]

COLUMN_MAP = {
    "class": ["class", "grade"],
    "subject": ["subject"],
    "chapter": ["chapter", "lesson"],
    "learning_outcome": ["learning_outcome", "learning outcomes", "lo"]
}

def load_data():
    # locate file
    for path in DATA_PATHS:
        if os.path.exists(path):
            df = pd.read_csv(path, sep="\t")
            break
    else:
        raise FileNotFoundError("❌ data/master.tsv not found")

    # normalize columns
    df.columns = [c.strip().lower() for c in df.columns]

    # resolve column aliases
    resolved = {}
    for standard, variants in COLUMN_MAP.items():
        for v in variants:
            if v in df.columns:
                resolved[standard] = v
                break
        if standard not in resolved:
            raise KeyError(f"❌ Required column missing: {standard}")

    df = df.rename(columns={v: k for k, v in resolved.items()})
    return df


# ==================================================
# BASIC SYLLABUS HELPERS
# ==================================================

def get_classes(df):
    return sorted(df["class"].unique())

def get_subjects(df, grade):
    return sorted(df[df["class"] == grade]["subject"].unique())

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


# ==================================================
# DEEP DAILY LESSON PLAN ENGINE
# ==================================================

def generate_daily_plan(chapter, day, total_days, subject, grade):
    """
    Generates a deeply detailed daily lesson plan.
    ALWAYS returns a dictionary with 'steps'.
    """

    steps = [
        {
            "title": "CONNECT",
            "duration": "5 minutes",
            "teacher_says": (
                f"Teacher begins by connecting the topic '{chapter}' with students’ daily life. "
                f"Teacher asks age-appropriate questions related to home, surroundings, or experiences."
            ),
            "student_does": (
                "Students share their experiences and respond orally."
            ),
            "learning_intent": (
                "Activate prior knowledge and emotional engagement."
            )
        },
        {
            "title": "UNPACK",
            "duration": "10 minutes",
            "teacher_says": (
                "Teacher introduces important words and ideas from the lesson. "
                "Each word is clearly explained with meaning, usage, and examples."
            ),
            "student_does": (
                "Students listen, repeat key terms, and ask clarification questions."
            ),
            "learning_intent": (
                "Build strong conceptual and language clarity."
            )
        },
        {
            "title": "ILLUSTRATE",
            "duration": "10 minutes",
            "teacher_says": (
                "Teacher explains the concept using a full story or example.\n\n"
                "Example:\n"
                "Lencho was a poor farmer who depended entirely on rain for his crops. "
                "When a storm destroyed his fields, he wrote a letter to God asking for help...\n\n"
                "Teacher narrates the complete story, explaining emotions and events."
            ),
            "student_does": (
                "Students listen attentively and answer short oral questions."
            ),
            "learning_intent": (
                "Develop deep understanding through narrative and examples."
            )
        },
        {
            "title": "PRACTISE",
            "duration": "10 minutes",
            "teacher_says": (
                "Teacher asks guided questions and solves one example step-by-step on the board."
            ),
            "student_does": (
                "Students answer questions orally or write short responses."
            ),
            "learning_intent": (
                "Reinforce learning through guided practice."
            )
        },
        {
            "title": "INTEGRATE",
            "duration": "10 minutes",
            "teacher_says": (
                "Teacher conducts an integration activity such as drawing, role-play, or a simple game "
                "connected to the chapter."
            ),
            "student_does": (
                "Students participate in creative or play-based activities."
            ),
            "learning_intent": (
                "Deepen understanding through experiential learning."
            )
        },
        {
            "title": "CHECKPOINT",
            "duration": "5 minutes",
            "teacher_says": (
                "Teacher asks short assessment questions to check understanding."
            ),
            "student_does": (
                "Students respond and clarify doubts."
            ),
            "learning_intent": (
                "Assess learning informally."
            )
        },
        {
            "title": "CONSOLIDATE",
            "duration": "5 minutes",
            "teacher_says": (
                "Teacher summarizes the lesson and links it to the next day’s topic."
            ),
            "student_does": (
                "Students reflect and share one key takeaway."
            ),
            "learning_intent": (
                "Ensure retention and closure."
            )
        }
    ]

    return {
        "chapter": chapter,
        "subject": subject,
        "grade": grade,
        "day": day,
        "total_days": total_days,
        "title": f"{chapter} – Day {day} of {total_days}",
        "steps": steps
    }
