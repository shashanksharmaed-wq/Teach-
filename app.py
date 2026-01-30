# app.py
import streamlit as st
from engine import generate_lesson

st.set_page_config(page_title="ERPACAD", layout="wide")

st.title("ERPACAD – Lesson Planner")
st.caption("Single-act lesson • Stable • Teacher-focused")

# ---------------- INPUTS ----------------

col1, col2, col3 = st.columns(3)

with col1:
    grade = st.selectbox(
        "Class",
        ["NURSERY", "LKG", "UKG", "1", "2", "3", "4", "5", "6", "7", "8"]
    )

with col2:
    subject = st.selectbox(
        "Subject",
        ["English", "Maths", "EVS", "Science", "Social Science"]
    )

with col3:
    chapter = st.text_input(
        "Chapter Name",
        value="Sample Chapter"
    )

day = st.number_input(
    "Day of Lesson",
    min_value=1,
    max_value=20,
    value=1
)

st.divider()

# ---------------- GENERATE ----------------

if st.button("Generate Lesson"):
    lesson = generate_lesson(
        grade=grade,
        subject=subject,
        chapter=chapter,
        day=day
    )

    st.subheader("🧠 Teaching Flow")

    st.markdown("### 👩‍🏫 Teacher Flow")
    st.write(lesson["teacher_flow"])

    st.markdown("### 🧒 Student Flow")
    st.write(lesson["student_flow"])

    st.markdown("### 🧾 TLM / Board Work")
    st.write(lesson["tlm"])

    st.markdown("### ✅ Expected Learning Outcome")
    st.write(lesson["outcome_check"])
