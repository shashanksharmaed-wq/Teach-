import streamlit as st
from lesson_engine import (
    load_data,
    get_classes,
    get_subjects,
    get_chapters,
    get_learning_outcomes,
    generate_daily_plan
)

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="ERPACAD – Academic Planning Engine",
    layout="wide"
)

st.title("📘 ERPACAD – Academic Planning Engine")
st.caption("Deep lesson planning • CBSE-aligned • Teacher-ready")

# ---------------------------------
# LOAD DATA
# ---------------------------------
df = load_data()

# ---------------------------------
# SELECTION PANEL
# ---------------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    grade = st.selectbox("Class", get_classes(df))

with c2:
    subject = st.selectbox("Subject", get_subjects(df, grade))

with c3:
    chapter = st.selectbox("Chapter", get_chapters(df, grade, subject))

with c4:
    total_days = st.number_input(
        "Total Days for Chapter",
        min_value=1,
        max_value=20,
        value=5
    )

st.divider()

# ---------------------------------
# DAILY PLAN VIEW
# ---------------------------------
day = st.selectbox(
    "Select Day to View",
    list(range(1, total_days + 1))
)

if st.button("Generate Daily Lesson Plan"):
    plan = generate_daily_plan(
        chapter=chapter,
        day=day,
        total_days=total_days,
        subject=subject,
        grade=grade
    )

    st.markdown(f"## 📖 {plan['title']}")

    # -------------------------------
    # LEARNING OUTCOMES
    # -------------------------------
    st.markdown("### 🎯 Learning Outcomes")
    los = get_learning_outcomes(df, grade, subject, chapter)
    for lo in los:
        st.write("•", lo)

    st.divider()

    # -------------------------------
    # TEACHING SCRIPT (DEEP)
    # -------------------------------
    st.markdown("### 🧠 Detailed Teaching Script")

    for step in plan["steps"]:
        with st.expander(f"{step['title']} ({step['duration']})"):
            st.markdown("**Teacher says:**")
            st.write(step["teacher_says"])

            st.markdown("**Students do:**")
            st.write(step["student_does"])

            st.markdown("**Learning Intent:**")
            st.write(step["learning_intent"])

    st.success("✅ Daily lesson plan generated successfully")
