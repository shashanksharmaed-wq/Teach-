import streamlit as st
import pandas as pd
from daily_plan_engine import generate_daily_plan

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ERPACAD – Academic Planning Engine",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/master.tsv", sep="\t")
    df.columns = [c.strip().lower() for c in df.columns]
    return df

df = load_data()

# ---------------- HEADER ----------------
st.title("📘 ERPACAD – Academic Planning Engine")
st.caption("CBSE-aligned • Deep lesson planning • Teacher-ready")

# ---------------- CLASS / SUBJECT / CHAPTER ----------------
col1, col2, col3 = st.columns(3)

with col1:
    grade = st.selectbox(
        "Class",
        sorted(df["grade"].astype(str).unique())
    )

with col2:
    subject_list = (
        df[df["grade"].astype(str) == grade]["subject"]
        .dropna()
        .unique()
        .tolist()
    )
    subject = st.selectbox("Subject", sorted(subject_list))

with col3:
    chapter_list = (
        df[
            (df["grade"].astype(str) == grade) &
            (df["subject"] == subject)
        ]["chapter name"]
        .dropna()
        .unique()
        .tolist()
    )

    if chapter_list:
        chapter = st.selectbox("Chapter", sorted(chapter_list))
    else:
        chapter = None
        st.warning("No chapters found for this selection.")

st.divider()

# ---------------- DAY CONTROLS ----------------
day_col1, day_col2 = st.columns(2)

with day_col1:
    total_days = st.number_input(
        "Total Days for this Chapter",
        min_value=1,
        max_value=15,
        value=7
    )

with day_col2:
    day = st.number_input(
        "Day Number",
        min_value=1,
        max_value=total_days,
        value=1
    )

st.divider()

# ---------------- GENERATE PLAN ----------------
if chapter and st.button("✨ Generate Detailed Daily Lesson Plan"):

    learning_outcomes = (
        df[
            (df["grade"].astype(str) == grade) &
            (df["subject"] == subject) &
            (df["chapter name"] == chapter)
        ]["learning outcomes"]
        .dropna()
        .tolist()
    )

    plan = generate_daily_plan(
        grade=grade,
        subject=subject,
        chapter=chapter,
        learning_outcomes=learning_outcomes,
        day=day,
        total_days=total_days
    )

    st.subheader(f"🧠 {chapter} — Day {day} of {total_days}")

    # ---------------- META ----------------
    meta = plan.get("meta", {})
    st.markdown(
        f"""
        **Class:** {meta.get("grade")}  
        **Subject:** {meta.get("subject")}  
        **Grade Band:** {meta.get("band")}  
        """
    )

    st.divider()

    # ---------------- LESSON FLOW ----------------
    st.header("📚 Detailed Teaching Script")

    for step in plan["flow"]:
        with st.expander(step["phase"], expanded=True):

            st.markdown("**🧑‍🏫 Teacher says:**")
            st.write(step["teacher_says"])

            st.markdown("**👩‍🎓 Students do:**")
            st.write(step["students_do"])

            st.markdown("**🎯 Purpose:**")
            st.write(step["purpose"])

    st.success("✅ Lesson plan generated successfully")
