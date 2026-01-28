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
# LOAD SCHOOL DATA
# =====================================================
SCHOOL_NAME = st.secrets.get("SCHOOL_NAME", "Your School")

df = pd.read_csv("data/Teachshank_Master_Database_FINAL.tsv", sep="\t")
df.columns = [c.strip().lower() for c in df.columns]
df.rename(columns={
    "learning outcomes": "learning_outcome",
    "chapter name": "chapter"
}, inplace=True)

# =====================================================
# SESSION STATE INIT
# =====================================================
if "user" not in st.session_state:
    st.session_state.user = None

if "role" not in st.session_state:
    st.session_state.role = None

if "progress" not in st.session_state:
    st.session_state.progress = {}

# =====================================================
# LOGIN SCREEN (ID + PASSWORD)
# =====================================================
if st.session_state.user is None:
    st.title("🔐 ERPACAD Login")
    st.caption(SCHOOL_NAME)

    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Principal login
        principal = st.secrets.get("principal", {})
        if (
            user_id == principal.get("id")
            and password == principal.get("password")
        ):
            st.session_state.user = user_id
            st.session_state.role = "principal"
            st.rerun()

        # Teacher login
        for key in st.secrets.get("teachers", {}):
            teacher = st.secrets["teachers"][key]
            if (
                user_id == teacher.get("id")
                and password == teacher.get("password")
            ):
                st.session_state.user = teacher
                st.session_state.role = "teacher"
                st.rerun()

        st.error("Invalid ID or Password")
    st.stop()

# =====================================================
# LOGOUT BUTTON
# =====================================================
with st.sidebar:
    st.write(f"👤 Logged in as: **{st.session_state.user if isinstance(st.session_state.user,str) else st.session_state.user['id']}**")
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
            for chap in st.session_state.progress[cls][subj]:
                data = st.session_state.progress[cls][subj][chap]
                rows.append({
                    "Class": cls,
                    "Subject": subj,
                    "Chapter": chap,
                    "Completed Periods": data["completed"],
                    "Planned Periods": data["required"],
                    "Completion %": round((data["completed"] / data["required"]) * 100, 1)
                })

    df_dash = pd.DataFrame(rows)
    st.dataframe(df_dash, use_container_width=True)

    st.stop()

# =====================================================
# TEACHER VIEW (RESTRICTED ACCESS)
# =====================================================
teacher = st.session_state.user
allowed_classes = teacher["classes"]
allowed_subjects = teacher["subjects"]

st.title("📘 Teaching Console")

grade = st.selectbox("Class", sorted(map(int, allowed_classes)))
subject = st.selectbox(
    "Subject",
    sorted(df[(df["grade"] == grade) & (df["subject"].isin(allowed_subjects))]["subject"].unique())
)

academic_days = st.number_input(
    "Academic Working Days (School-wide)",
    min_value=160,
    max_value=210,
    value=180
)

# =====================================================
# ANNUAL PLAN (AUTO, CBSE SAFE)
# =====================================================
annual_plan = generate_annual_plan(df, grade, subject, academic_days)

chapters = annual_plan["chapters"]
chapter_names = [c["chapter"] for c in chapters]

chapter = st.selectbox("Chapter", chapter_names)
chapter_meta = next(c for c in chapters if c["chapter"] == chapter)

# Learning Outcomes
lo_list = df[
    (df["grade"] == grade) &
    (df["subject"] == subject) &
    (df["chapter"] == chapter)
]["learning_outcome"].unique().tolist()

# =====================================================
# EXECUTION PLAN (ONE PERIOD AT A TIME)
# =====================================================
key = f"{grade}-{subject}-{chapter}"

if key not in st.session_state:
    st.session_state[key] = generate_chapter_execution_plan(
        grade,
        subject,
        chapter,
        chapter_meta["required_periods"],
        "LEARN360",
        lo_list,
        "English"
    )

plan = st.session_state[key]
current_period = next((p for p in plan["periods"] if p["status"] == "unlocked"), None)

if not current_period:
    st.success("🎉 Chapter Completed")
    st.stop()

# =====================================================
# DISPLAY PERIOD
# =====================================================
st.subheader(
    f"{chapter} — Period {current_period['period_no']} of {plan['required_periods']}"
)

st.markdown("### 🗣️ Detailed Teaching Script")
st.text_area("Script", current_period["script"], height=350)

# =====================================================
# DOWNLOADS
# =====================================================
lesson_export = {
    "grade": grade,
    "subject": subject,
    "chapter": chapter,
    "day_no": current_period["period_no"],
    "total_days": plan["required_periods"],
    "pedagogy": "LEARN360",
    "integration": current_period["integration"],
    "learning_outcomes": lo_list,
    "period_structure": current_period["period_structure"],
    "script": current_period["script"]
}

col1, col2 = st.columns(2)

with col1:
    if st.button("📄 Download PDF"):
        pdf = generate_lesson_pdf(lesson_export, SCHOOL_NAME)
        with open(pdf, "rb") as f:
            st.download_button("Download PDF", f, file_name="Lesson_Plan.pdf")

with col2:
    if st.button("📝 Download Word"):
        docx = generate_lesson_word(lesson_export, SCHOOL_NAME)
        with open(docx, "rb") as f:
            st.download_button("Download Word", f, file_name="Lesson_Plan.docx")

# =====================================================
# MARK PERIOD COMPLETE + TRACK PROGRESS
# =====================================================
if st.button("✅ Mark Period Completed"):
    idx = current_period["period_no"] - 1
    plan["periods"][idx]["status"] = "completed"

    if idx + 1 < len(plan["periods"]):
        plan["periods"][idx + 1]["status"] = "unlocked"

    # Track progress
    st.session_state.progress.setdefault(str(grade), {}).setdefault(subject, {}).setdefault(
        chapter,
        {"completed": 0, "required": plan["required_periods"]}
    )
    st.session_state.progress[str(grade)][subject][chapter]["completed"] += 1

    st.success("Period marked completed.")
    st.rerun()
