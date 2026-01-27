import pandas as pd
import os
import google.generativeai as genai

DATA_PATH = "data/master.tsv"

# ---------- AI SETUP ----------
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-pro")
else:
    model = None


# ---------- LOAD DATA ----------
def load_data():
    df = pd.read_csv(DATA_PATH, sep="\t")
    df.columns = [c.strip().lower() for c in df.columns]
    df.rename(columns={
        "chapter name": "chapter",
        "learning outcomes": "learning_outcomes"
    }, inplace=True)
    return df


# ---------- ANNUAL PLAN ----------
def calculate_annual_plan(df, grade, subject):
    filtered = df[(df["grade"] == grade) & (df["subject"] == subject)]
    plan = {}
    for chapter in filtered["chapter"].unique():
        lo_count = len(
            filtered[filtered["chapter"] == chapter]["learning_outcomes"]
        )
        plan[chapter] = max(1, lo_count)  # 1 day per outcome (safe default)
    return plan


# ---------- DAY-WISE PLAN ----------
def generate_daywise_plan(df, grade, subject, chapter, days, period_minutes):
    chapter_df = df[
        (df["grade"] == grade) &
        (df["subject"] == subject) &
        (df["chapter"] == chapter)
    ]

    learning_outcomes = chapter_df["learning_outcomes"].tolist()

    plans = []

    for day in range(1, days + 1):
        plans.append({
            "day": f"Day {day}",
            "learning_outcomes": learning_outcomes,
            "time_flow": [
                {"Time": "5 min", "Activity": "Warm-up & conversation", "Pedagogy": "Oral interaction"},
                {"Time": f"{period_minutes - 15} min", "Activity": "Concept exploration", "Pedagogy": "Play-based learning"},
                {"Time": "5 min", "Activity": "Activity / rhyme / story", "Pedagogy": "Experiential"},
                {"Time": "5 min", "Activity": "Reflection & closure", "Pedagogy": "Observation"},
            ],
            "tlm": [
                "Picture cards",
                "Rhymes / charts",
                "Real-life objects",
                "Notebook"
            ],
            "assessment": [
                "Observation",
                "Oral response",
                "Participation"
            ]
        })

    return plans


# ---------- AI ENRICHMENT ----------
def enrich_lesson_content(day_plan, grade, subject, chapter):
    if not model:
        day_plan["enriched_content"] = "AI enrichment disabled."
        return day_plan

    prompt = f"""
You are an expert Indian early-years teacher.

Create COMPLETE teaching content (not instructions) for:
Class: {grade}
Subject: {subject}
Chapter: {chapter}

Learning Outcomes:
{day_plan["learning_outcomes"]}

Rules:
- Include FULL rhymes / stories / activities
- Age-appropriate language
- No HTML
- No teacher directives
- Plain text
"""

    try:
        day_plan["enriched_content"] = model.generate_content(prompt).text
    except:
        day_plan["enriched_content"] = "AI content could not be generated."

    return day_plan
