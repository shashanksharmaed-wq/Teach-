import pandas as pd
import os
from math import floor
from openai import OpenAI

DATA_PATH = "data/master.tsv"

# ================= OPENAI CONFIG =================
OPENAI_API_KEY = os.environ.get("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")
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


# ================= ANNUAL PLAN ENGINE =================
def generate_annual_plan(df, grade, subject, total_days):
    filtered = df[(df["grade"] == grade) & (df["subject"] == subject)]

    chapter_weights = (
        filtered.groupby("chapter")["learning_outcomes"]
        .count()
        .to_dict()
    )

    total_weight = sum(chapter_weights.values())

    allocation = {
        ch: max(1, floor((w / total_weight) * total_days))
        for ch, w in chapter_weights.items()
    }

    # Fix rounding drift
    diff = total_days - sum(allocation.values())
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
        "Launch – engage with students’ life and emotions",
        "Explore – guided discovery through story or activity",
        "Anchor – explicit concept explanation",
        "Relate – connect to real life and self",
        "Nurture – practice and support",
        "Apply & Reflect – consolidation and reflection"
    ]


def pedagogy_blooms():
    return [
        "Remember – recall facts",
        "Understand – explain ideas",
        "Apply – use knowledge",
        "Analyze – break down ideas",
        "Evaluate – justify opinions",
        "Create – produce something new"
    ]


def pedagogy_5e():
    return [
        "Engage – capture curiosity",
        "Explore – investigate before explanation",
        "Explain – clarify concepts",
        "Elaborate – extend learning",
        "Evaluate – check understanding"
    ]


PEDAGOGY_MAP = {
    "LEARN360": pedagogy_learn360,
    "BLOOMS": pedagogy_blooms,
    "5E": pedagogy_5e
}


# ================= DAILY PLAN =================
def generate_daily_plans(df, grade, subject, chapter, days, pedagogy):
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
            "learning_outcomes": outcomes
        })

    return plans


# ================= AI TEACHING SCRIPT =================
def enrich_with_ai(plan, grade, subject, chapter):
    if not client:
        plan["ai_script"] = (
            "Detailed teaching guidance can be generated when AI services are available.\n"
            "The lesson structure above is fully valid for classroom use."
        )
        return plan

    prompt = f"""
You are a senior Indian school teacher.

Create a FULL, DETAILED, minute-wise teaching script.

Class: {grade}
Subject: {subject}
Chapter: {chapter}
Day: {plan['day']}
Pedagogy: {plan['pedagogy']}

Learning Outcomes:
{plan['learning_outcomes']}

Pedagogical Flow:
{plan['structure']}

Requirements:
- Minute-wise narration
- Exact questions teacher should ask
- Expected student responses
- Stories/examples where appropriate
- Plain text only
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        plan["ai_script"] = response.choices[0].message.content
    except Exception as e:
        plan["ai_script"] = f"AI temporarily unavailable: {str(e)}"

    return plan
