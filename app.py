import streamlit as st
import pandas as pd

from lesson_engine import generate_chapter_execution_plan
from annual_plan_engine import generate_annual_plan
from export_utils import generate_lesson_pdf, generate_lesson_word

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(page_title="ERPACAD", layout="wide")

# -------------------------------------------------
# PASSWORDS (PER SCHOOL)
# -------------------------------------------------

ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "admin123")
TEACHER_PASSWORD = st.secrets.get("TEACHER_PASSWORD", "teacher123")
SCHOOL_NAME = st.secrets.get("SCHOOL_NAME", "Your School")

# -------------------------------------------------
# LOGIN
# -------------------------------------------------

if "role" not in st.session_state:
    st.session_state.role = None

if st.session_state.role is None:
    st.title("🔐 ERPACAD Login")
    pwd = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        if pwd == ADMIN_PASSWORD:
            st.session_state.role = "Admin"
            st.rerun()
        elif pwd == TEACHER_PASSWORD:
            st.session_state.role = "Teacher"
            st.rerun()
        else:
            st.error("Invalid password")
    st.stop()

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

df = pd.read_csv(
    "data/Teachshank_Master_Database_FINAL.tsv",
    sep="\t"
)

df.columns = [c.strip().lower() for c in df.columns]
df.rename(columns={
    "learning outcomes": "learning_outcome",
    "chapter name": "chapter"
}, inplace=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "total_days" not in st.session_state:
    st.session_state.total_days = None

if "annual_plan" not in st.session_state:
    st.session_state.annual_plan = None

if "chapter_execution" not in st.session_state:
    st.session_state.chapter_execution = {}

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title("ERPACAD")
st.sidebar.caption(SCHOOL_NAME)
st.sidebar.write(f"Role: {st.session_state.role}")

grade = st.sidebar.selectbox("Class", sorted(df["grade"].unique()))
subject = st.sidebar.selectbox(
    "Subject",
    sorted(df[df["grade"] == grade]["subject"].unique())
)

pedagogy = st.sidebar.selectbox("Pedagogy", ["LEARN360", "BLOOMS", "5E"])
language = st.sidebar.selectbox("Language", ["English", "Hindi"])

# -------------------------------------------------
# ADMIN VIEW
# -------------------------------------------------

if st.session_state.role == "Admin":
    st.header("📅 Academic Configuration")

    days = st.number_input(
        "Total Working Days for the Class",
        min_value=160,
        max_value=210,
        value=st.session_state.total_days or 180
    )

    if st.button("Save Academic Days"):
        st.session_state.total_days = days
        st.session_state.annual_plan = generate_annual_plan(
            df, grade, subject, days
        )
        st.success("Academic days saved.")

    if st.session_state.annual_plan:
        st.subheader("📊 Chapter Planning (Period-Based)")
        st.dataframe(
            pd.DataFrame(st.session_state.annual_plan["chapters"]),
            use_container_width=True
        )

    st.stop()

# -------------------------------------------------
# TEACHER VIEW
# -------------------------------------------------

if not st.session_state.total_days:
    st.warning("Admin has not configured academic days yet.")
    st.stop()

if not st.session_state.annual_plan:
    st.session_state.annual_plan = generate_annual_plan(
        df, grade, subject, st.session_state.total_days
    )

chapters = st.session_state.annual_plan["chapters"]
chapter_names = [c["chapter"] for c in chapters]

chapter = st.selectbox("Select Chapter", chapter_names)

chapter_meta = next(c for c in chapters if c["chapter"] == chapter)

# Learning outcomes for chapter
lo_list = df[
    (df["grade"] == grade) &
    (df["subject"] == subject) &
    (df["chapter"] == chapter)
]["learning_outcome"].unique().tolist()

# Generate execution plan ONCE
if chapter not in st.session_state.chapter_execution:
    st.session_state.chapter_execution[chapter] = generate_chapter_execution_plan(
        grade=grade,
        subject=subject,
        chapter=chapter,
        required_periods=chapter_meta["required_periods"],
        pedagogy=pedagogy,
        learning_outcomes=lo_list,
        language=language
    )

plan = st.session_state.chapter_execution[chapter]

current_period = next(
    (p for p in plan["periods"] if p["status"] == "unlocked"),
    None
)

if not current_period:
    st.success("🎉 Chapter completed.")
    st.stop()

# -------------------------------------------------
# DISPLAY PERIOD
# -------------------------------------------------

st.subheader(
    f"{chapter} — Period {current_period['period_no']} "
    f"of {plan['required_periods']}"
)

st.markdown(f"""
**Class:** {grade}  
**Subject:** {subject}  
**Pedagogy:** {pedagogy}  
**Integration:** {current_period['integration'] or "—"}
""")

st.markdown("### ⏱️ Period Structure")
st.table(
    pd.DataFrame(
        current_period["period_structure"],
        columns=["Phase", "Minutes"]
    )
)

st.markdown("### 🎯 Learning Outcomes")
for lo in current_period["learning_outcomes"]:
    st.write(f"- {lo}")

st.markdown("### 🗣️ Detailed Teaching Script")
st.text_area(
    "Script",
    current_period["script"],
    height=350
)

# -------------------------------------------------
# DOWNLOAD
# -------------------------------------------------

lesson_export = {
    "grade": grade,
    "subject": subject,
    "chapter": chapter,
    "day_no": current_period["period_no"],
    "total_days": plan["required_periods"],
    "pedagogy": pedagogy,
    "integration": current_period["integration"],
    "learning_outcomes": current_period["learning_outcomes"],
    "period_structure": current_period["period_structure"],
    "script": current_period["script"]
}

col1, col2 = st.columns(2)

with col1:
    if st.button("📄 Generate Colourful PDF"):
        pdf = generate_lesson_pdf(lesson_export, SCHOOL_NAME)
        with open(pdf, "rb") as f:
            st.download_button("Download PDF", f, file_name="Lesson_Plan.pdf")

with col2:
    if st.button("📝 Generate Word File"):
        docx = generate_lesson_word(lesson_export, SCHOOL_NAME)
        with open(docx, "rb") as f:
            st.download_button("Download Word", f, file_name="Lesson_Plan.docx")

# -------------------------------------------------
# MARK PERIOD COMPLETE
# -------------------------------------------------

if st.button("✅ Mark Period Completed"):
    idx = current_period["period_no"] - 1
    plan["periods"][idx]["status"] = "completed"

    if idx + 1 < len(plan["periods"]):
        plan["periods"][idx + 1]["status"] = "unlocked"

    st.success("Period marked completed.")
    st.rerun()
