import pandas as pd
import os
from openai import OpenAI

DATA_PATH = "data/Teachshank_Master_Database_FINAL.tsv"

# ---------------- LOAD DATA ----------------
def load_data():
    df = pd.read_csv(DATA_PATH, sep="\t")
    df.columns = [c.strip().lower() for c in df.columns]
    df.rename(columns={
        "grade": "grade",
        "subject": "subject",
        "chapter name": "chapter",
        "learning outcomes": "learning_outcome"
    }, inplace=True)
    return df

# ---------------- PERIOD STRUCTURE ----------------
PERIOD_STRUCTURE = [
    ("Engage", 5),
    ("Concept Build", 15),
    ("Guided Practice", 10),
    ("Integration / Activity", 10),
    ("Closure & Assessment", 5)
]

# ---------------- INTEGRATION LOGIC ----------------
def assign_integrations(total_days):
    integrations = [None] * total_days
    if total_days >= 1:
        integrations[0] = "Language Integration"
    if total_days >= 2:
        integrations[1] = "Art Integration"
    if total_days >= 3:
        integrations[-1] = "Play-Based Activity"
    return integrations

# ---------------- AI CLIENT ----------------
def get_ai_client():
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return None
    return OpenAI(api_key=key)

# ---------------- TEACHING SCRIPT ----------------
def generate_teaching_script(
    grade, subject, chapter, day_no,
    pedagogy, learning_outcomes, integration, language
):
    client = get_ai_client()
    if not client:
        return "AI unavailable. Follow the structured lesson table and outcomes."

    prompt = f"""
You are an expert CBSE teacher.

Create a VERY DETAILED, minute-wise teaching script.

Class: {grade}
Subject: {subject}
Chapter: {chapter}
Day: {day_no}
Pedagogy: {pedagogy}
Language: {language}

Learning Outcomes:
{learning_outcomes}

Period Structure:
{PERIOD_STRUCTURE}

Integration Today:
{integration}

Rules:
- Exact teacher dialogue
- Questions to ask
- Expected student responses
- Misconceptions & correction
- No advice, only classroom execution
- Plain text only
"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"AI error: {e}"

# ---------------- CHAPTER PLAN ----------------
def generate_chapter_plan(df, grade, subject, chapter, total_days, pedagogy, language):
    lo_list = df[
        (df["grade"] == grade) &
        (df["subject"] == subject) &
        (df["chapter"] == chapter)
    ]["learning_outcome"].dropna().tolist()

    integrations = assign_integrations(total_days)

    plan = {
        "grade": grade,
        "subject": subject,
        "chapter": chapter,
        "total_days": total_days,
        "pedagogy": pedagogy,
        "days": []
    }

    for i in range(total_days):
        plan["days"].append({
            "day_no": i + 1,
            "status": "unlocked" if i == 0 else "locked",
            "integration": integrations[i],
            "learning_outcomes": lo_list,
            "period_structure": PERIOD_STRUCTURE,
            "script": generate_teaching_script(
                grade, subject, chapter, i + 1,
                pedagogy, lo_list, integrations[i], language
            )
        })

    return plan
