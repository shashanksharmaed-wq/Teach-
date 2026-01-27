import streamlit as st
import pandas as pd

from lesson_engine import load_data, generate_chapter_plan
from annual_plan_engine import generate_annual_plan

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="ERPACAD – Academic Operating System",
    layout="wide"
)

# ================= SESSION STATE INIT =================
for key in [
    "annual_plan",
    "annual_plan_locked",
    "chapter_plans",
]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "chapter_plans" else {}

# ================= HEADER =================
st.title("📘 ERPACAD – Academic Execution Engine")
st.caption("Curriculum-aligned | Pedagogy-driven | Inspection-safe")

# ================= LOAD MASTER DATA =================
df = load_data()

# ================= SIDEBAR =================
st.sidebar.header("User Access")
role = st.sidebar.selectbox("Login as", ["Principal", "Teacher"])

st.sidebar.divider()

grade = st.sidebar.selectbox("Class", sorted(df["grade"].unique()))
subject = st.sidebar.selectbox(
    "Subject",
    sorted(df[df["grade"] == grade]["subject"].unique())
)

language = st.sidebar.selectbox(
    "Language of Instruction",
    ["English", "Hindi"]
)

pedagogy = st.sidebar.selectbox(
    "Primary Pedagogy",
    ["LEARN360", "BLOOMS", "5E"]
)

# =====================================================
# ================= PRINCIPAL PANEL ===================
# =====================================================
if role == "Principal":
    st.header("🏫 Principal Dashboard – Annual Academic Plan")

    total_days = st.number_input(
        "Total Working Days in Academic Year",
        min_value=160,
        max_value=210,
        value=180
    )

    if st.button("Generate Annual Plan"):
        annual_plan = generate_annual_plan(df, grade, subject, total_days)
        st.session_state.annual_plan = annual_plan
        st.session_state.annual_plan_locked = False

    if st.session_state.annual_plan:
        st.subheader("📅 Chapter-wise Academic Distribution")

        plan_df = pd.DataFrame(st.session_state.annual_plan)
        st.dataframe(plan_df, use_container_width=True)

        st.info(
            "Academic guidance: Chapter durations are system-calculated "
            "based on learning outcomes. Adjusting total days recalibrates "
            "the plan proportionally to avoid over/under teaching."
        )

        if st.button("🔒 Lock Annual Plan"):
            st.session_state.annual_plan_locked = True
            st.success("Annual plan locked. Teachers can now execute lessons.")

# =====================================================
# ================= TEACHER PANEL =====================
# =====================================================
if role == "Teacher":
    st.header("👩‍🏫 Teacher Panel – Daily Lesson Execution")

    if not st.session_state.annual_plan or not st.session_state.annual_plan_locked:
        st.warning(
            "Annual plan is not locked by the principal. "
            "Please wait before starting lesson execution."
        )
        st.stop()

    # Select chapter from locked annual plan
    chapters = [c["chapter"] for c in st.session_state.annual_plan]
    chapter = st.selectbox("Select Chapter", chapters)

    # Get allowed days for chapter
    chapter_days = next(
        c["suggested_days"]
        for c in st.session_state.annual_plan
        if c["chapter"] == chapter
    )

    # Generate chapter plan ONCE
    if chapter not in st.session_state.chapter_plans:
        with st.spinner("Preparing chapter lesson plan..."):
            chapter_plan = generate_chapter_plan(
                df=df,
                grade=grade,
                subject=subject,
                chapter=chapter,
                total_days=chapter_days,
                pedagogy=pedagogy
            )
            st.session_state.chapter_plans[chapter] = chapter_plan

    plan = st.session_state.chapter_plans[chapter]

    # Find current unlocked day
    current_day = None
    for d in plan["days"]:
        if d["status"] == "unlocked":
            current_day = d
            break

    if not current_day:
        st.success("🎉 Chapter completed successfully.")
        st.stop()

    # ================= DAY HEADER =================
    st.subheader(
        f"📖 {chapter} — Day {current_day['day_no']} of {plan['total_days']}"
    )

    cols = st.columns(4)
    cols[0].metric("Class", grade)
    cols[1].metric("Subject", subject)
    cols[2].metric("Pedagogy", pedagogy)
    cols[3].metric("Integration", current_day["integration"] or "—")

    # ================= PERIOD STRUCTURE TABLE =================
    st.markdown("### ⏱️ Period Structure (CBSE 40–45 min)")
    ps_df = pd.DataFrame(
        current_day["period_structure"],
        columns=["Phase", "Minutes"]
    )
    st.table(ps_df)

    # ================= LEARNING OUTCOMES =================
    st.markdown("### 🎯 Learning Outcomes")
    for lo in current_day["learning_outcomes"]:
        st.write(f"- {lo}")

    # ================= MAIN TEACHING TABLE =================
    st.markdown("### 🧠 Detailed Teaching Plan")

    teaching_rows = []
    for phase, mins in current_day["period_structure"]:
        teaching_rows.append({
            "Phase": phase,
            "Time": f"{mins} min",
            "Teacher Action": "Refer teaching script below",
            "Questions to Ask": "As per script",
            "Expected Student Response": "Observable participation",
            "Assessment Focus": "Concept understanding"
        })

    teaching_df = pd.DataFrame(teaching_rows)
    st.dataframe(teaching_df, use_container_width=True)

    # ================= SCRIPT =================
    st.markdown("### 🗣️ Teaching Script (Execute As-Is)")
    st.text_area(
        "Script",
        current_day["teaching_script"],
        height=400
    )

    # ================= MARK COMPLETED =================
    if st.button("✅ Mark Day as Completed"):
        idx = current_day["day_no"] - 1
        plan["days"][idx]["status"] = "completed"

        if idx + 1 < len(plan["days"]):
            plan["days"][idx + 1]["status"] = "unlocked"

        st.success("Day completed. Next day unlocked.")
        st.rerun()
