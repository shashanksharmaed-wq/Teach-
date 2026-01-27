import streamlit as st
import os
import json
from lesson_engine import (
    load_data,
    calculate_annual_plan,
    generate_daywise_plan,
    enrich_lesson_content,
    generate_pdf
)
from approvals import submit_for_approval, approve_lesson, is_locked

# ================= BRAND CONFIG =================
SCHOOL_NAME = "ERPACAD"
TAGLINE = "NEP & NCERT Aligned Academic Engine"
LOGO_PATH = "assets/logo.png"  # optional

PRIMARY_COLOR = "#1f4fd8"

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title=SCHOOL_NAME,
    layout="wide"
)

# ================= HEADER =================
col1, col2 = st.columns([1, 6])

with col1:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=90)

with col2:
    st.markdown(f"""
    <h1 style="color:{PRIMARY_COLOR}; margin-bottom:0;">
        {SCHOOL_NAME}
    </h1>
    <p style="margin-top:0;">{TAGLINE}</p>
    """, unsafe_allow_html=True)

st.divider()

# ================= DATA =================
APPROVAL_DIR = "approvals"
df = load_data()

# ================= ROLE =================
role = st.sidebar.selectbox("Login as", ["Teacher", "Principal"])

# =========================================================
# ======================= TEACHER =========================
# =========================================================
if role == "Teacher":
    st.subheader("👩‍🏫 Teacher Panel")

    board = st.selectbox("Board", sorted(df["board"].unique()))
    grade = st.selectbox("Class", sorted(df[df["board"] == board]["grade"].unique()))
    subject = st.selectbox(
        "Subject",
        sorted(df[(df["board"] == board) & (df["grade"] == grade)]["subject"].unique())
    )

    annual_plan = calculate_annual_plan(df, board, grade, subject)
    chapter = st.selectbox("Chapter", list(annual_plan.keys()))

    meta = {
        "board": board,
        "grade": grade,
        "subject": subject,
        "chapter": chapter
    }

    # -------- LOCK CHECK --------
    if is_locked(meta):
        st.error("🔒 This lesson plan is APPROVED and LOCKED.")
        st.info("Please contact the Principal for the approved copy.")
        st.stop()

    days = st.number_input("Number of Days", min_value=1, value=annual_plan[chapter])
    period_minutes = st.selectbox("Period Duration (minutes)", [30, 35, 40, 45, 60])
    use_ai = st.checkbox("Enrich lesson with stories / rhymes (AI)")

    if st.button("Generate Lesson Plan"):
        plans = generate_daywise_plan(
            df, board, grade, subject, chapter, days, period_minutes
        )

        if use_ai:
            plans = [
                enrich_lesson_content(p, grade, subject, chapter)
                for p in plans
            ]

        st.session_state["plans"] = plans
        st.session_state["meta"] = {
            **meta,
            "period": period_minutes
        }

    if "plans" in st.session_state:
        st.divider()
        st.subheader("📘 Generated Lesson Plan")

        pdf_path = generate_pdf(
            st.session_state["plans"],
            st.session_state["meta"]
        )

        with open(pdf_path, "rb") as f:
            st.download_button(
                "⬇️ Download Lesson Plan PDF",
                f,
                file_name="ERPACAD_Lesson_Plan.pdf"
            )

        if st.button("📤 Submit to Principal for Approval"):
            approval_id = submit_for_approval(
                st.session_state["meta"],
                st.session_state["plans"]
            )
            if approval_id is None:
                st.error("This lesson is already approved and locked.")
            else:
                st.success("Lesson submitted for approval.")

# =========================================================
# ===================== PRINCIPAL =========================
# =========================================================
if role == "Principal":
    st.subheader("🧑‍💼 Principal Dashboard")

    records = []
    if os.path.exists(APPROVAL_DIR):
        for f in os.listdir(APPROVAL_DIR):
            if f.endswith(".json"):
                with open(f"{APPROVAL_DIR}/{f}", "r", encoding="utf-8") as file:
                    records.append(json.load(file))

    pending = [r for r in records if r["status"] == "PENDING"]
    approved = [r for r in records if r["status"] == "APPROVED"]

    col1, col2 = st.columns(2)
    col1.metric("Pending Approvals", len(pending))
    col2.metric("Approved Lessons", len(approved))

    st.divider()
    st.subheader("Pending Approval")

    for r in pending:
        with st.expander(
            f"{r['meta']['subject']} | Class {r['meta']['grade']} | {r['meta']['chapter']}"
        ):
            remark = st.text_area("Principal Remark", key=r["id"])
            if st.button("✅ Approve & Lock", key=f"approve_{r['id']}"):
                approve_lesson(r["id"], remark)
                st.success("Approved and locked.")
                st.rerun()

    st.divider()
    st.subheader("Approved Lessons (Locked)")
    for r in approved:
        st.write(
            f"✔ {r['meta']['subject']} | Class {r['meta']['grade']} | {r['meta']['chapter']}"
        )

# ================= FOOTER =================
st.divider()
st.caption(
    "ERPACAD • NEP 2020 & NCERT aligned • "
    "Lesson planning, assessment & academic governance platform"
)
