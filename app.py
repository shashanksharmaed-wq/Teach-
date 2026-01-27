import streamlit as st
import os, json
from lesson_engine import (
    load_data,
    generate_annual_plan,
    generate_daily_plans,
    enrich_with_ai
)
from approvals import submit_for_approval, approve_lesson, is_locked

st.set_page_config(page_title="ERPACAD", layout="wide")
st.title("ERPACAD – Academic Orchestration Engine")

df = load_data()
APPROVAL_DIR = "approvals"

role = st.sidebar.selectbox("Login as", ["Teacher", "Principal"])

# ================= TEACHER =================
if role == "Teacher":
    st.subheader("👩‍🏫 Teacher Panel")

    grade = st.selectbox("Class", sorted(df["grade"].unique()))
    subject = st.selectbox(
        "Subject", sorted(df[df["grade"] == grade]["subject"].unique())
    )

    total_days = st.slider(
        "Total Working Days in Academic Year",
        min_value=160,
        max_value=210,
        value=210
    )

    pedagogy = st.selectbox(
        "Pedagogy Framework",
        ["LEARN360", "BLOOMS", "5E"]
    )

    annual_plan = generate_annual_plan(df, grade, subject, total_days)

    st.markdown("## 📅 Annual Academic Plan")
    st.table(
        [{"Chapter": k, "Days": v} for k, v in annual_plan.items()]
    )

    chapter = st.selectbox("Select Chapter", list(annual_plan.keys()))
    days = annual_plan[chapter]

    meta = {
        "grade": grade,
        "subject": subject,
        "chapter": chapter,
        "pedagogy": pedagogy,
        "days": days
    }

    if is_locked(meta):
        st.error("🔒 Lesson plan already approved and locked.")
        st.stop()

    use_ai = st.checkbox("Generate detailed teaching script (AI)")

    if st.button("Generate Daily Lesson Plans"):
        plans = generate_daily_plans(
            df, grade, subject, chapter, days, pedagogy
        )

        if use_ai:
            plans = [enrich_with_ai(p, grade, subject, chapter) for p in plans]

        st.session_state["plans"] = plans
        st.session_state["meta"] = meta

    if "plans" in st.session_state:
        for p in st.session_state["plans"]:
            st.markdown(f"## {p['day']} ({p['pedagogy']})")
            st.write("Learning Outcomes:", p["learning_outcomes"])
            st.write("Pedagogical Flow:", p["structure"])
            st.write("Assessment:", p["assessment"])
            if use_ai:
                st.markdown("### Detailed Teaching Script")
                st.write(p["ai_script"])

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
            f"{r['meta']['grade']} | {r['meta']['subject']} | "
            f"{r['meta']['chapter']} ({r['meta']['pedagogy']})"
        ):
            remark = st.text_area("Principal Remark", key=r["id"])
            if st.button("Approve & Lock", key=f"a_{r['id']}"):
                approve_lesson(r["id"], remark)
                st.rerun()
