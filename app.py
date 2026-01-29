import streamlit as st
from lesson_engine import (
    load_data,
    get_classes,
    get_subjects,
    get_chapters
)

st.set_page_config(
    page_title="ERPACAD – Academic Planning Engine",
    layout="wide"
)

st.title("📘 ERPACAD – Academic Planning Engine")
st.caption("CBSE-aligned • Deep lesson planning • Teacher-ready")

# ---------------- LOAD DATA ----------------
df = load_data()

# ---------------- SELECTION BAR ----------------
col1, col2, col3 = st.columns(3)

with col1:
    grade = st.selectbox("Class", get_classes(df))

with col2:
    subject = st.selectbox("Subject", get_subjects(df, grade))

with col3:
    academic_days = st.number_input(
        "Academic Working Days (School-wide)",
        min_value=160,
        max_value=210,
        value=180
    )

st.divider()

# ---------------- CHAPTERS ----------------
st.subheader("📚 Chapters Covered")
chapters = get_chapters(df, grade, subject)

if not chapters:
    st.warning("No chapters found.")
    st.stop()

selected_chapter = st.selectbox(
    "Select Chapter to Plan",
    chapters
)

# ---------------- ANNUAL PLAN ----------------
if st.button("📅 Generate Annual Plan"):
    st.session_state["annual_plan"] = {
        "chapter": selected_chapter,
        "total_days": 5  # placeholder logic
    }

if "annual_plan" in st.session_state:
    st.success(
        f"Annual plan generated for **{selected_chapter}** "
        f"({st.session_state['annual_plan']['total_days']} days)"
    )

    # ---------------- DAILY PLAN ----------------
    day = st.selectbox(
        "Select Day",
        list(range(1, st.session_state["annual_plan"]["total_days"] + 1))
    )

    if st.button("🧠 Generate Daily Lesson Plan"):
        st.session_state["daily_plan"] = {
            "chapter": selected_chapter,
            "day": day
        }

# ---------------- DAILY PLAN DISPLAY ----------------
if "daily_plan" in st.session_state:
    st.divider()
    st.header(
        f"📖 {st.session_state['daily_plan']['chapter']} "
        f"— Day {st.session_state['daily_plan']['day']}"
    )

    st.info(
        "Deep minute-wise lesson plan generation will appear here next."
    )
