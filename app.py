import streamlit as st
import pandas as pd

from annual_plan_engine import generate_annual_plan
from lesson_engine import generate_chapter_execution_plan
from export_utils import generate_lesson_pdf, generate_lesson_word

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="ERPACAD", layout="wide")

# =====================================================
# LOAD DATA
# =====================================================
DATA_PATH = "data/Teachshank_Master_Database_FINAL.tsv"

df = pd.read_csv(DATA_PATH, sep="\t")
df.columns = [c.strip().lower() for c in df.columns]
df.rename(columns={"learning outcomes": "learning_outcome"}, inplace=True)

# =====================================================
# SESSION STATE
# =====================================================
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None
if "progress" not in st.session_state:
    st.session_state.progress = {}

# =====================================================
# LOGIN (ID + PASSWORD)
# =====================================================
if st.session_state.user is None:
    st.title("🔐 ERPACAD Login")

    uid = st.text_input("User ID")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        # Principal
        principal = st.secrets.get("principal", {})
        if uid == principal.get("id") and pwd == principal.get("password"):
            st.session_state.user = uid
            st.session_state.role = "principal"
            st.rerun()

        # Teacher (ANY teacher)
        for t in st.secrets.get("teachers", {}).values():
            if uid == t.get("id") and pwd == t.get("password"):
                st.session_state.user = uid
                st.session_state.role = "teacher"
                st.rerun()

        st.error("Invalid ID or Password")

    st.stop()

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.write(f"👤 Logged in as **{st.session_state.user}**")
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

# =====================================================
# PRINCIPAL DASHBOARD (READ-ONLY)
# =====================================================
if st.session_state.role == "principal":
    st.title("📊 Principal Dashboard")

    if not st.session_state.progress:
        st.info("No teaching activity recorded yet.")
        st.stop()

    rows = []
    for cls in st.session_state.progress:
        for subj in st.session_state.progress[cls]:
            for chap, data in st.session_state.progress[cls][subj].items():
                rows.append({
                    "Class": cls,
                    "Subject": subj,
                    "Chapter": chap,
                    "Completed Periods": data["completed"],
                    "Planned Periods": data["required"],
                    "Completion %": round(
                        (data["completed"] / data["required"]) * 100, 1
                    )
                })

    st.dataframe(pd.DataFrame(rows), use_container_width=True)
    st.stop()

# =====================================================
# TEACHER CONSOLE (OPEN ACCESS)
# =====================================================
st.title("📘 Teaching Console")

# -----------------------------------------------------
# CLASS & SUBJECT (NO RESTRICTION)
# -----------------------------------------------------
grade = st.selectbox("Class", sorted(df["grade"].unique()))

subjects = (
    df[df["grade"] == grade]["subject"]
    .dropna()
    .unique()
    .tolist()
)

subject = st.selectbox("Subject", subjects)

if not subject:
    st.warning("Please select a subject.")
    st.stop()

# -----------------------------------------------------
# ACADEMIC DAYS (USER SELECTABLE)
# -----------------------------------------------------
academic_days = st.number_input(
    "Academic Working Days (School-wide)",
    min_value=160,
    max_value=210,
    value=180
)

# -----------------------------------------------------
# ANNUAL PLAN (AUTO, CBSE SAFE)
# -----------------------------------------------------
annual_plan = generate_annual_plan(df, grade, subject, academic_days)
chapters = annual_plan.get("chapters", [])

if not chapters:
    st.warning("No chapters found.")
    st.stop()

chapter = st.selectbox("Chapter", [c["chapter"] for c in chapters])
chapter_meta = next(c for c in chapters if c["chapter"] == chapter)

# -----------------------------------------------------
# LEARNING OUTCOMES
# -----------------------------------------------------
learning_outcomes = (
    df[
        (df["grade"] == grade) &
        (df["subject"] == subject) &
        (df["chapter"] == chapter)
    ]["learning_outcome"]
    .unique()
    .tolist()
)

# -----------------------------------------------------
# EXECUTION PLAN (ONE PERIOD AT A TIME)
# -----------------------------------------------------
plan_key = f"{grade}-{subject}-{chapter}"

if plan_key not in st.session_state:
    st.session_state[plan_key] = generate_chapter_execution_plan(
        grade=grade,
        subject=subject,
        chapter=chapter,
        total_periods=chapter_meta["required_periods"],
        pedagogy="LEARN360",
        learning_outcomes=learning_outcomes,
        language="English"
    )

plan = st.session_state[plan_key]

current_period = next(
    (p for p in plan["periods"] if p["status"] == "unlocked"),
    None
)

if not current_period:
    st.success("🎉 Chapter completed.")
    st.stop()

# -----------------------------------------------------
# DISPLAY PERIOD
# -----------------------------------------------------
st.subheader(
    f"{chapter} — Period {current_period['period_no']} "
    f"of {plan['required_periods']}"
)

st.markdown("### 🗣️ Detailed Teaching Script")
st.text_area(
    "Teaching Script",
    current_period["script"],
    height=350
)

# -----------------------------------------------------
# DOWNLOADS
# -----------------------------------------------------
export_payload = {
    "grade": grade,
    "subject": subject,
    "chapter": chapter,
    "period_no": current_period["period_no"],
    "total_periods": plan["required_periods"],
    "learning_outcomes": learning_outcomes,
    "script": current_period["script"],
}

c1, c2 = st.columns(2)

with c1:
    if st.button("📄 Download PDF"):
        path = generate_lesson_pdf(export_payload)
        with open(path, "rb") as f:
            st.download_button("Download PDF", f, file_name="Lesson_Plan.pdf")

with c2:
    if st.button("📝 Download Word"):
        path = generate_lesson_word(export_payload)
        with open(path, "rb") as f:
            st.download_button("Download Word", f, file_name="Lesson_Plan.docx")

# -----------------------------------------------------
# MARK PERIOD COMPLETE + TRACK PROGRESS
# -----------------------------------------------------
if st.button("✅ Mark Period Completed"):
    idx = current_period["period_no"] - 1
    plan["periods"][idx]["status"] = "completed"

    if idx + 1 < len(plan["periods"]):
        plan["periods"][idx + 1]["status"] = "unlocked"

    st.session_state.progress \
        .setdefault(str(grade), {}) \
        .setdefault(subject, {}) \
        .setdefault(
            chapter,
            {"completed": 0, "required": plan["required_periods"]}
        )

    st.session_state.progress[str(grade)][subject][chapter]["completed"] += 1
    st.rerun()
