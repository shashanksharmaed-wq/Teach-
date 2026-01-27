import pandas as pd
import os
import google.generativeai as genai

DATA_PATH = "data/master.tsv"

# ---------- AI SETUP ----------
API_KEY = os.environ.get("AIzaSyADIu5q3vVQicvpFSj5ZIzMLlPf5OKMziQ")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-pro")
else:
    model = None


# ---------- LOAD DATA ----------
def load_data():
    return pd.read_csv(DATA_PATH, sep="\t")


# ---------- ANNUAL PLAN ----------
def calculate_annual_plan(df, board, grade, subject):
    filtered = df[
        (df["board"] == board) &
        (df["grade"] == grade) &
        (df["subject"] == subject)
    ]

    plan = {}
    for chapter in filtered["chapter"].unique():
        chapter_df = filtered[filtered["chapter"] == chapter]
        days = 0
        for d in chapter_df["difficulty"]:
            if d == "Easy":
                days += 1
            elif d == "Medium":
                days += 2
            else:
                days += 3
        plan[chapter] = days

    return plan


# ---------- DAY-WISE LESSON PLAN ----------
def generate_daywise_plan(df, board, grade, subject, chapter, total_days, period_minutes):
    chapter_df = df[
        (df["board"] == board) &
        (df["grade"] == grade) &
        (df["subject"] == subject) &
        (df["chapter"] == chapter)
    ]

    learning_outcomes = chapter_df["learning_outcome_text"].unique().tolist()
    subtopics = chapter_df["subtopic"].unique().tolist()
    pedagogies = chapter_df["pedagogy"].unique().tolist()

    plans = []

    for day in range(1, total_days + 1):
        plan = {
            "day": f"Day {day}",
            "learning_outcomes": learning_outcomes,
            "learning_indicators": [
                f"Demonstrates understanding of {lo.lower()}"
                for lo in learning_outcomes
            ],
            "subtopics": subtopics,
            "micro_subtopics": [f"Key idea of {s.lower()}" for s in subtopics],
            "time_flow": [
                {"Time": "5 min", "Activity": "Warm-up / recall", "Pedagogy": "Discussion"},
                {"Time": f"{period_minutes - 15} min", "Activity": "Concept building", "Pedagogy": "Experiential"},
                {"Time": "5 min", "Activity": "Practice activity", "Pedagogy": "Activity-based"},
                {"Time": "5 min", "Activity": "Reflection & closure", "Pedagogy": "Reflection"},
            ],
            "pedagogies": pedagogies,
            "tlm": [
                "Textbook",
                "Blackboard",
                "Charts / Flashcards",
                "Notebook"
            ],
            "assessment": [
                "Oral questioning",
                "Worksheet",
                "Observation"
            ]
        }

        plans.append(plan)

    return plans


# ---------- AI ENRICHMENT ----------
def enrich_lesson_content(day_plan, grade, subject, chapter):
    if not model:
        day_plan["enriched_content"] = "AI enrichment disabled."
        return day_plan

    prompt = f"""
Create enriched teaching content for an Indian classroom.

Class: {grade}
Subject: {subject}
Chapter: {chapter}

Learning Outcomes:
{day_plan["learning_outcomes"]}

Rules:
- Include FULL stories, rhymes, examples (write full text)
- Do NOT say 'teacher should'
- Plain text only
- Age appropriate
- No HTML
"""

    try:
        response = model.generate_content(prompt).text
        day_plan["enriched_content"] = response
    except Exception:
        day_plan["enriched_content"] = "AI content could not be generated."

    return day_plan
    from fpdf import FPDF

def generate_pdf(plans, meta):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Header
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "ERPACAD – Lesson Plan", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, f"""
Board: {meta['board']}
Class: {meta['grade']}
Subject: {meta['subject']}
Chapter: {meta['chapter']}
Period Duration: {meta['period']} minutes
""")

    for p in plans:
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, p["day"], ln=True)

        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 7, "Learning Outcomes:\n" + "\n".join(p["learning_outcomes"]))
        pdf.ln(2)

        pdf.multi_cell(0, 7, "Learning Indicators:\n" + "\n".join(p["learning_indicators"]))
        pdf.ln(2)

        pdf.multi_cell(0, 7, "Subtopics:\n" + "\n".join(p["subtopics"]))
        pdf.ln(2)

        pdf.multi_cell(
            0, 7,
            "Time-wise Flow:\n" +
            "\n".join([f"{r['Time']} – {r['Activity']} ({r['Pedagogy']})" for r in p["time_flow"]])
        )
        pdf.ln(2)

        pdf.multi_cell(0, 7, "Pedagogies:\n" + ", ".join(p["pedagogies"]))
        pdf.ln(2)

        pdf.multi_cell(0, 7, "Teaching Learning Materials:\n" + ", ".join(p["tlm"]))
        pdf.ln(2)

        pdf.multi_cell(0, 7, "Assessment:\n" + ", ".join(p["assessment"]))
        pdf.ln(2)

        if "enriched_content" in p:
            pdf.multi_cell(0, 7, "Enriched Teaching Content:\n" + p["enriched_content"])

    file_path = "lesson_plan.pdf"
    pdf.output(file_path)
    return file_path

