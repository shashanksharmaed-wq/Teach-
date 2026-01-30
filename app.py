import streamlit as st
from daily_plan_engine import generate_daily_plan

st.set_page_config(page_title="ERPACAD – DEPTH++", layout="wide")

st.title("📘 ERPACAD – Academic Planning Engine")
st.caption("Deep lesson planning • Teacher-performance focused • DEPTH++")

# ----------------------------
# HARD-CODED SAFE DATA (NO FILE ERRORS)
# ----------------------------

DATA = {
    "NURSERY": {
        "English": ["Rhymes and Sounds"]
    },
    "1": {
        "English": ["A Letter to God"],
        "Maths": ["Numbers up to 10"]
    },
    "7": {
        "English": [
            "The Cop and the Anthem",
            "The Shed",
            "The Story of Cricket"
        ]
    }
}

# ----------------------------
# SELECTORS
# ----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    grade = st.selectbox("Class", list(DATA.keys()))

with col2:
    subject = st.selectbox("Subject", list(DATA[grade].keys()))

with col3:
    total_days = st.number_input(
        "Academic Working Days (School-wide)",
        min_value=100,
        max_value=240,
        value=180
    )

chapter = st.selectbox(
    "Chapter",
    DATA[grade][subject]
)

day = st.number_input(
    "Day of Chapter",
    min_value=1,
    max_value=20,
    value=1
)

st.divider()

# ----------------------------
# GENERATE PLAN
# ----------------------------

if st.button("Generate Daily Lesson Plan"):
    plan = generate_daily_plan(
        grade=grade,
        subject=subject,
        chapter=chapter,
        day=day,
        total_days=total_days
    )

    st.subheader("🧠 Detailed Teaching Script (DEPTH++)")

    for section in plan["sections"]:
        with st.expander(section["title"], expanded=True):
            st.markdown("**👩‍🏫 Teacher does:**")
            st.write(section["teacher"])

            st.markdown("**🧒 Students do:**")
            st.write(section["students"])

            st.markdown("**🎯 Purpose:**")
            st.write(section["purpose"])
