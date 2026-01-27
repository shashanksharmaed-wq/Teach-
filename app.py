import streamlit as st
import os, json
from lesson_engine import (
    load_data,
    calculate_annual_plan,
    generate_daywise_plan,
    enrich_lesson_content
)
from approvals import submit_for_approval, approve_lesson, is_locked

st.set_page_config(page_title="ERPACAD", layout="wide")
st.title("ERPACAD – NCERT Academic Engine")

df = load_data()
APPROVAL_DIR = "approvals"

role = st.sidebar.selectbox("Login as", ["Teacher", "Principal"])

# ================= TEACHER =================
if role == "Teacher":
    st.subheader("👩‍🏫 Teacher Panel")

    grade = st.selectbox("Class", sorted(df["grade"].unique()))
    subject = st.selectbox("Subject", sorted(df[df["grade"] == grade]["subject"].unique()))
    annual_plan = calculate_annual_plan(df, grade, subject)

    chapter = st.selectbox("Chapter", list(annual_plan.keys()))
    meta = {"grade": grade, "subject": subject, "chapter": chapter}

    if is_locked(meta):
        st.error("🔒 Lesson plan is approved and locked.")
        st.stop()

    days = st.number_input("Number of Days", min_value=1, value=annual_plan[chapter])
    period_minutes = st.selectbox("Period Duration", [30, 35, 40, 45])
    use_ai = st.checkbox("Enrich with AI (stories / rhymes)")

    if st.button("Generate Lesson Plan"):
        plans = generate_daywise_plan(df, grade, subject, chapter, days, period_minutes)
        if use_ai:
            plans = [enrich_lesson_content(p, grade, subject, chapter) for p in plans]
        st.session_state["plans"] = plans
        st.session_state["meta"] = meta

    if "plans" in st.session_state:
        for p in st.session_state["plans"]:
            st.markdown(f"### {p['day']}")
            st.write("Learning Outcomes:", p["learning_outcomes"])
            st.table(p["time_flow"])
            st.write("TLM:", p["tlm"])
            st.write("Assessment:", p["assessment"])
            if use_ai:
                st.write(p["enriched_content"])

        if st.button("📤 Submit to Principal"):
            submit_for_approval(st.session_state["meta"], st.session_state["plans"])
            st.success("Submitted for approval")

# ================= PRINCIPAL =================
if role == "Principal":
    st.subheader("🧑‍💼 Principal Dashboard")

    records = []
    if os.path.exists(APPROVAL_DIR):
        for f in os.listdir(APPROVAL_DIR):
            if f.endswith(".json"):
                with open(f"{APPROVAL_DIR}/{f}", "r") as file:
                    records.append(json.load(file))

    pending = [r for r in records if r["status"] == "PENDING"]

    for r in pending:
        with st.expander(
            f"{r['meta']['grade']} | {r['meta']['subject']} | {r['meta']['chapter']}"
        ):
            remark = st.text_area("Principal Remark", key=r["id"])
            if st.button("Approve & Lock", key=f"a_{r['id']}"):
                approve_lesson(r["id"], remark)
                st.rerun()
