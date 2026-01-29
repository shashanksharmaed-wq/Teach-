import streamlit as st

from data_loader import load_data
from daily_plan_engine import generate_deep_daily_plan

st.set_page_config(
    page_title="ERPACAD – Academic Planning Engine",
    layout="wide"
)

st.title("📘 ERPACAD – Academic Planning Engine")
st.caption("CBSE-aligned • Deep lesson planning • Teacher-ready")

# ---------------- LOAD DATA ----------------
df = load_data()

# ---------------- SELECTORS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    grade = st.selectbox("Class", sorted(df["grade"].unique()))

with col2:
    subject = st.selectbox(
        "Subject",
        sorted(df[df["grade"] == grade]["subject"].unique())
    )

with col3:
    academic_days = st.number_input(
        "Academic Working Days (School-wide)",
        min_value=160,
        max_value=210,
        value=180
    )

# ---------------- CHAPTER LIST ----------------
chapter_df = df[
    (df["grade"] == grade) &
    (df["subject"] == subject)
]

st.subheader("📚 Chapters Covered")

chapters = chapter_df["chapter name"].unique().tolist()
st.write(chapters)

# ---------------- DAILY PLAN ----------------
st.divider()
st.subheader("🗓️ Generate Daily Lesson Plan")

chapter = st.selectbox("Select Chapter", chapters)

total_days = st.number_input(
    "Total Days for this Chapter",
    min_value=1,
    max_value=10,
    value=5
)

day = st.selectbox(
    "Select Day",
    list(range(1, total_days + 1))
)

if st.button("Generate Daily Plan"):
    los = chapter_df[
        chapter_df["chapter name"] == chapter
    ]["learning outcomes"].tolist()

    plan = generate_deep_daily_plan(
        grade=grade,
        subject=subject,
        chapter=chapter,
        learning_outcomes=los,
        day=day,
        total_days=total_days
    )

    st.subheader(f"📖 {chapter} — Day {day} of {total_days}")

    for block in plan["lesson_flow"]:
        with st.expander(
            f"{block['phase']} ({block['minutes']} min)",
            expanded=True
        ):
            st.markdown(f"**Teacher says:** {block['teacher_says']}")
            st.markdown(f"**Students do:** {block['students_do']}")
            st.markdown(f"**Purpose:** {block['purpose']}")
