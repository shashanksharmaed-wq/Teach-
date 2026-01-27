import pandas as pd
import os
from math import floor
from openai import OpenAI

DATA_PATH = "data/master.tsv"

# ================= OPENAI CONFIG =================
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


# ================= LOAD DATA =================
def load_data():
    df = pd.read_csv(DATA_PATH, sep="\t")
    df.columns = [c.strip().lower() for c in df.columns]
    df.rename(columns={
        "chapter name": "chapter",
        "learning outcomes": "learning_outcomes"
    }, inplace=True)
    return df


# ================= PERIOD STRUCTURE (CBSE) =================
PERIOD_STRUCTURE = [
    ("Engage", 5),
    ("Concept Build", 12),
    ("Guided Interaction", 10),
    ("Integration Slot", 12),
    ("Closure & Assessment", 6)
]


# ================= INTEGRATION ASSIGNMENT =================
def assign_integrations(total_days):
    """
    Returns a list of integrations per day index (0-based).
    Rules:
    - Every chapter must have ART, SUBJECT_LANGUAGE, PLAY at least once
    - Not forced daily
    """
    integrations = [None] * total_days

    if total_days == 1:
        integrations[0] = "SUBJECT_LANGUAGE"

    elif total_days == 2:
        integrations[1] = "PLAY"

    elif total_days == 3:
        integrations[1] = "ART"
        integrations[2] = "PLAY"

    else:
        integrations[1] = "SUBJECT_LANGUAGE"
        integrations[2] = "ART"
        integrations[-1] = "PLAY"

    return integrations


# ================= PEDAGOGY FLOW =================
def pedagogy_flow(pedagogy):
    if pedagogy == "LEARN360":
        return [
            "Launch",
            "Explore",
            "Anchor",
            "Relate",
            "Nurture",
            "Apply & Reflect"
        ]
    if pedagogy == "BLOOMS":
        return [
            "Remember",
            "Understand",
            "Apply",
            "Analyze",
            "Evaluate",
            "Create"
        ]
    if pedagogy == "5E":
        return [
            "Engage",
            "Explore",
            "Explain",
            "Elaborate",
            "Evaluate"
        ]
    return []


# ================= AI SCRIPT GENERATION =================
def generate_ai_script(
    grade, subject, chapter, day_no,
    pedagogy, learning_outcomes, integration
):
    if not client:
        return (
            "Detailed teaching script can be generated when AI is available.\n"
            "Use the structure above for classroom execution."
        )

    prompt = f"""
You are a senior Indian CBSE school teacher.

Create a VERY DETAILED, execution-level teaching script for ONE PERIOD.

Class: {grade}
Subject: {subject}
Chapter: {chapter}
Day: {day_no}
Pedagogy: {pedagogy}

Learning Outcomes:
{learning_outcomes}

Period Structure (40–45 min):
{PERIOD_STRUCTURE}

Pedagogy Flow:
{pedagogy_flow(pedagogy)}

Integration for this day:
{integration}

STRICT REQUIREMENTS:
- Minute-wise teacher narration (what teacher says)
- Exact questions teacher asks
- Expected student responses
- Likely misconceptions & correction
- If integration exists, fully execute it (art / language / play)
- No advice, no instructions — only classroom execution text
- Plain text only
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI temporarily unavailable: {str(e)}"


# ================= CHAPTER PLAN GENERATION =================
def generate_chapter_plan(
    df, grade, subject, chapter, total_days, pedagogy
):
    outcomes = df[
        (df["grade"] == grade) &
        (df["subject"] == subject) &
        (df["chapter"] == chapter)
    ]["learning_outcomes"].tolist()

    integrations = assign_integrations(total_days)

    chapter_plan = {
        "grade": grade,
        "subject": subject,
        "chapter": chapter,
        "pedagogy": pedagogy,
        "total_days": total_days,
        "days": []
    }

    for i in range(total_days):
        day_no = i + 1
        day_plan = {
            "day_no": day_no,
            "status": "unlocked" if i == 0 else "locked",
            "integration": integrations[i],
            "period_structure": PERIOD_STRUCTURE,
            "learning_outcomes": outcomes,
            "pedagogy_flow": pedagogy_flow(pedagogy),
            "teaching_script": generate_ai_script(
                grade, subject, chapter,
                day_no, pedagogy, outcomes,
                integrations[i]
            )
        }

        chapter_plan["days"].append(day_plan)

    return chapter_plan
