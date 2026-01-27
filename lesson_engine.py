import pandas as pd
import os
import google.generativeai as genai
from math import floor

DATA_PATH = "data/master.tsv"

# ================= AI CONFIG (AUTO-DETECT) =================
API_KEY = os.environ.get("GEMINI_API_KEY")
model = None

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                model = genai.GenerativeModel(m.name)
                break
    except:
        model = None


# ================= LOAD DATA =================
def load_data():
    df = pd.read_csv(DATA_PATH, sep="\t")
    df.columns = [c.strip().lower() for c in df.columns]
    df.rename(columns={
        "chapter name": "chapter",
        "learning outcomes": "learning_outcomes"
    }, inplace=True)
    return df


# ================= ANNUAL PLAN ENGINE =================
def generate_annual_plan(df, grade, subject, total_days):
    filtered = df[(df["grade"] == grade) & (df["subject"] == subject)]

    chapter_weights = (
        filtered.groupby("chapter")["learning_outcomes"]
        .count()
        .to_dict()
    )

    total_weight = sum(chapter_weights.values())

    # Initial allocation
    allocation = {
        ch: max(1, floor((w / total_weight) * total_days))
        for ch, w in chapter_weights.items()
    }

    # Adjust to fix rounding drift
    current_total = sum(allocation.values())
    diff = total_days - current_total

    chapters = list(allocation.keys())
    i = 0
    while diff != 0:
        allocation[chapters[i % len(chapters)]] += 1 if diff > 0 else -1
        diff = total_days - sum(allocation.values())
        i += 1

    return allocation


# ================= PEDAGOGY STRUCTURES =================
def pedagogy_learn360():
    return [
        "Launch – connect with life and emotions",
        "Explore – guided discovery through story or activity",
        "Anchor – clear concept explanation",
        "Relate – personal and real-life linkage",
        "Nurture – practice and support",
        "Apply & Reflect – consolidation"
    ]


def pedagogy_blooms():
    return [
        "Remember",
        "Understand",
        "Apply",
        "Analyze",
        "Evaluate",
        "Create"
    ]


def pedagogy_5e():
    return [
        "Engage",
        "Explore",
        "Explain",
        "Elaborate",
        "Evaluate"
    ]


PEDAGOGY_MAP = {
    "LEARN360": pedagogy_learn360,
    "BLOOMS": pedagogy_blooms,
    "5E": pedagogy_5e
}


# ================= DAILY PLAN GENERATOR =================
def generate_daily_plans(
    df, grade, subject, chapter, days, pedagogy
):
    outcomes = df[
        (df["grade"] == grade) &
        (df["subject"] == subject) &
        (df["chapter"] == chapter)
    ]["learning_outcomes"].tolist()

    structure = PEDAGOGY_MAP[pedagogy]()
    plans = []

    for day in range(1, days + 1):
        plans.append({
            "day": f"Day {day}",
            "pedagogy": pedagogy,
            "structure": structure,
            "learning_outcomes": outcomes,
            "teacher_guidance": (
                f"This day focuses on progressing learners through "
                f"the {pedagogy} framework while reinforcing core ideas."
            ),
            "assessment": (
                "Observation, questioning, participation, concept clarity."
            )
        })

    return plans


# ================= AI ENRICHMENT =================
def enrich_with_ai(plan, grade, subject, chapter):
    if not model:
        plan["ai_script"] = "AI not available. Pedagogical structure remains valid."
        return plan

    prompt = f"""
Create a FULL teacher script.

Class: {grade}
Subject: {subject}
Chapter: {chapter}
Pedagogy: {plan['pedagogy']}
Day: {plan['day']}

Learning Outcomes:
{plan['learning_outcomes']}

Pedagogy Structure:
{plan['structure']}

Requirements:
- Minute-wise teacher narration
- Exact questions
- Expected student responses
- Full stories or examples
- Plain text only
"""

    try:
        plan["ai_script"] = model.generate_content(prompt).text
    except Exception as e:
        plan["ai_script"] = f"AI unavailable: {str(e)}"

    return plan
