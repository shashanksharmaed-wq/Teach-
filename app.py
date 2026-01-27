import streamlit as st
from lesson_engine import (
    load_data,
    generate_chapter_plan
)

st.set_page_config(page_title="ERPACAD", layout="wide")

# ================= SESSION STATE =================
if "chapter_plan" not in st.session_state:
    st.session_state.chapter_plan = None

# ================= HEADER =================
st.title("ERPACAD – Academic Execution Engine")

# ================= LOAD DATA =================
df = load_data()

# ================= TEACHER INPUT =================
st.sidebar.header("Lesson Setup")

grade = st.sidebar.selectbox("Class", sorted(df["grade"].unique()))
subject = st.sidebar.selectbox(
    "Subject",
    sorted(df[df["grade"] == grade]["subject"].unique())
)
chapter = st.sidebar.selectbox(
    "Chapter",
    sorted(
        df[
            (df["grade"] == grade) &
            (df["subject"] == subject)
        ]["chapter"].unique()
    )
)

total_days = st.sidebar.number_input(
    "Total Days for Chapter",
    min_value=1,
    max_value=10,
    value=3
)

pedagogy = st.sidebar.selectbox(
    "Pedagogy",
    ["LEARN360", "BLOOMS", "5E"]
)

# ================= GENERATE CHAPTER =================
if st.sidebar.button("Generate Chapter Lesson Plan"):
    with st.spinner("Generating complete chapter plan..."):
        st.session_state.chapter_plan = generate_chapter_plan(
            df, grade, subject, chapter, total_days, pedagogy
        )

# ================= DISPLAY CURRENT DAY =================
if st.session_state.chapter_plan:
    plan = st.session_state.chapter_plan

    # Find first unlocked & not completed day
    current_day = None
    for d in plan["days"]:
        if d["status"] == "unlocked":
            current_day = d
            break

    if current_day:
        st.subheader(
            f"{plan['chapter']} – Day {current_day['day_no']} of {plan['total_days']}"
        )

        st.markdown("### Period Structure (CBSE)")
        for seg, mins in current_day["period_structure"]:
            st.write(f"- **{seg}**: {mins} minutes")

        st.markdown("### Learning Outcomes")
        for lo in current_day["learning_outcomes"]:
            st.write(f"- {lo}")

        if current_day["integration"]:
            st.markdown(
                f"### Integration Focus: **{current_day['integration']}**"
            )

        st.markdown("### Teaching Script (Execute as-is)")
        st.text(current_day["teaching_script"])

        # ================= MARK COMPLETED =================
        if st.button("Mark Day as Completed"):
            idx = current_day["day_no"] - 1
            plan["days"][idx]["status"] = "completed"

            # Unlock next day if exists
            if idx + 1 < len(plan["days"]):
                plan["days"][idx + 1]["status"] = "unlocked"

            st.success("Day marked as completed. Next day unlocked.")
            st.experimental_rerun()

    else:
        st.success("🎉 Chapter completed successfully!")
