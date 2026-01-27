import pandas as pd
import os
import google.generativeai as genai

DATA_PATH = "data/master.tsv"

# ================= AI CONFIG =================
API_KEY = os.environ.get("AIzaSyC-EsDH1Xdiwc5qOiB4ba_T94aOhc1w-AA")
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")

model = None
if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(MODEL_NAME)
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


# ================= ANNUAL PLAN =================
def calculate_annual_plan(df, grade, subject):
    filtered = df[(df["grade"] == grade) & (df["subject"] == subject)]
    plan = {}
    for ch in filtered["chapter"].unique():
        lo_count = len(filtered[filtered["chapter"] == ch])
        plan[ch] = max(3, lo_count)
    return plan


# =====================================================
# =============== PEDAGOGY ENGINES ====================
# =====================================================

def generate_learn360(outcomes, period_minutes):
    return {
        "Launch (Engage)": (
            "Begin with an open-ended question connected to students’ life. "
            "Allow free responses without correction to build confidence."
        ),
        "Explore": (
            "Narrate a short story or situation related to the concept. "
            "Ask students what they notice and what they think might happen next."
        ),
        "Anchor": (
            "Clearly explain the core concept using simple language and examples. "
            "Repeat key words aloud with students."
        ),
        "Relate": (
            "Invite students to connect the idea to their own life or surroundings."
        ),
        "Nurture": (
            "Guide a short activity (drawing, speaking, acting) to practice learning."
        ),
        "Apply & Reflect": (
            "Ask reflective questions: What did you learn? Why is it important?"
        )
    }


def generate_blooms(outcomes, period_minutes):
    return {
        "Remember": (
            "Recall facts or ideas using simple questions. Students answer orally."
        ),
        "Understand": (
            "Explain the concept in their own words or through examples."
        ),
        "Apply": (
            "Use the concept in a new situation or problem."
        ),
        "Analyze": (
            "Compare, differentiate, or explain reasons."
        ),
        "Evaluate": (
            "Express opinions or judgments with reasons."
        ),
        "Create": (
            "Produce something new: a sentence, idea, role-play, or solution."
        )
    }


def generate_5e(outcomes, period_minutes):
    return {
        "Engage": (
            "Capture interest through a question, story, or surprising fact."
        ),
        "Explore": (
            "Students investigate through discussion or activity before explanation."
        ),
        "Explain": (
            "Teacher clarifies the concept using student responses."
        ),
        "Elaborate": (
            "Extend learning by applying it to new contexts."
        ),
        "Evaluate": (
            "Check understanding through questions and observation."
        )
    }


PEDAGOGY_MAP = {
    "LEARN360": generate_learn360,
    "BLOOMS": generate_blooms,
    "5E": generate_5e
}


# ================= DAY-WISE PLAN =================
def generate_daywise_plan(
    df, grade, subject, chapter, days, period_minutes, pedagogy
):
    outcomes = df[
        (df["grade"] == grade) &
        (df["subject"] == subject) &
        (df["chapter"] == chapter)
    ]["learning_outcomes"].tolist()

    plans = []
    pedagogy_func = PEDAGOGY_MAP[pedagogy]

    for day in range(1, days + 1):
        plans.append({
            "day": f"Day {day}",
            "pedagogy": pedagogy,
            "learning_outcomes": outcomes,
            "lesson_flow": pedagogy_func(outcomes, period_minutes),
            "assessment": (
                "Observation, oral responses, participation, ability to relate concept."
            ),
            "sel": (
                "Confidence building, listening to peers, expressing ideas."
            )
        })

    return plans


# ================= AI ENRICHMENT =================
def enrich_lesson_content(day_plan, grade, subject, chapter):
    if not model:
        day_plan["ai_detail"] = "AI enrichment disabled."
        return day_plan

    prompt = f"""
You are an expert Indian teacher.

Create a FULL, DETAILED teaching SCRIPT for:
Class: {grade}
Subject: {subject}
Chapter: {chapter}
Pedagogy: {day_plan['pedagogy']}

Learning Outcomes:
{day_plan['learning_outcomes']}

Requirements:
- Minute-wise teacher guidance
- Exact questions to ask
- Expected student responses
- Full stories / rhymes where suitable
- SEL moments
- Plain text only
"""

    try:
        day_plan["ai_detail"] = model.generate_content(prompt).text
    except Exception as e:
        day_plan["ai_detail"] = f"AI unavailable: {str(e)}"

    return day_plan
