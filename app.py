import streamlit as st
from daily_plan_engine import generate_daily_plan

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ERPACAD – Academic Planning Engine",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("📘 ERPACAD – Academic Planning Engine")
st.caption("CBSE-aligned • Deep lesson planning • Teacher-ready")

# ---------------- INPUTS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    grade = st.selectbox(
        "Class",
        ["NURSERY", "KG", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    )

with col2:
    subject = st.selectbox(
        "Subject",
        ["English", "Hindi", "Maths", "EVS", "Science", "Social Science"]
    )

with col3:
    chapter = st.text_input("Chapter Name", "A Letter to God")

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

# ---------------- GENERATE ----------------
if st.button("✨ Generate Detailed Daily Lesson Plan"):

    plan = generate_daily_plan(
        grade=grade,
        subject=subject,
        chapter=chapter,
        day=day,
        total_days=total_days
    )

    st.divider()
    st.subheader(f"🧠 {chapter} — Day {day} of {total_days}")

    # ---------------- META ----------------
    meta = plan.get("meta", {})
    st.markdown(
        f"""
        **Class:** {meta.get("grade")}  
        **Subject:** {meta.get("subject")}  
        **Duration:** {meta.get("duration")}  
        """
    )

    st.divider()

    # ---------------- MAIN CONTENT ----------------
    st.header("📚 Detailed Teaching Script")

    for step in plan["flow"]:
        with st.expander(step["phase"], expanded=True):

            st.markdown("**🧑‍🏫 Teacher says:**")
            st.write(step["teacher_says"])

            st.markdown("**👩‍🎓 Students do:**")
            st.write(step["students_do"])

            st.markdown("**🎯 Purpose:**")
            st.write(step["purpose"])

    st.divider()

    st.success("✅ Lesson plan generated successfully")
