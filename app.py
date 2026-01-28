import streamlit as st
import pandas as pd

from lesson_engine import load_data, generate_chapter_plan
from annual_plan_engine import generate_annual_plan
from export_utils import generate_lesson_pdf, generate_lesson_word

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="ERPACAD", layout="wide")

# =====================================================
# SIMPLE PASSWORD GATE (2 PASSWORD MODEL)
# =====================================================
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "admin123")
TEACHER_PASSWORD = st.secrets.get("TEACHER_PASSWORD", "teacher123")
SCHOOL_NAME = st.secrets.get("SCHOOL_NAME", "Your School")

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

# =====================================================
# LOAD DATA (SAFE POINT)
# =====================================================
df = load_data()

# =====================================================
# SESSION STATE
# =====================================================
for key in [
    "total_academic_days",
    "annual_plan",
    "chapter_plans"
]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "chapter_plans" else {}

# =====================================================
# SIDEBAR (COMMON)
# =====================================================
st.sidebar.title("ERPACAD")
st.sidebar.caption(SCHOOL_NAME)
st.sidebar.divider()
st.sidebar.write(f"Logged in as: **{st.session_state.role}**")

grade = st.sidebar.selectbox("Class", sorted(df["grade"].unique()))
subject = st.sidebar.selectbox(
    "Subject",
    sorted(df[df["grade"] == grade]["subject"].unique())
)

pedagogy = st.sidebar.selectbox(
    "Pedagogy",
    ["LEARN360", "BLOOMS", "5E"]
)

language = st.sidebar.selectbox(
    "Language of Instruction",
    ["English", "Hindi"]
)

# =====================================================
# ADMIN VIEW (ONLY TOTAL DAYS)
# =====================================================
if st.session_state.role == "Admin":
    st.header("📅 Academic Configuration")

    total_days = st.number_input(
        "Total Academic Days (School Level)",
        min_value=160,
        max_value=210,
        value=st.session_state.total_academic_days or 180
    )

    if st.button("Save Academic Days"):
        st.session_state.total_academic_days = total_days
        st.session_state.annual_plan = generate_annual_plan(
            df, grade, subject, total_days
        )
        st.success("Academic days saved successfully.")

    if st.session_state.annual_plan:
        st.subheader("📊 Chapter-wise Academic Distribution")
        st.dataframe(
            pd.DataFrame(st.session_state.annual_plan),
            use_container_width=True
        )

    st.stop()

# =====================================================
# TEACHER VIEW
# =====================================================
st.header("📘 Daily Lesson Execution")

if not st.session_state.total_academic_days:
    st.warning("Admin has not configured total academic days yet.")
    st.stop()

# Generate annual plan if not exists
if not st.session_state.annual_plan:
    st.session_state.annual_plan = generate_annual_plan(
        df, grade, subject, st.session_state.total_academic_days
    )

chapters = [c["chapter"] for c in st.session_state.annual_plan]
chapter = st.selectbox("Select Chapter", chapters)

allowed_days = next(
    c["suggested_days"]
    for c in st.session_state.annual_plan
    if c["chapter"] == chapter
)

# Generate chapter plan ONCE
if chapter not in st.session_state.chapter_plans:
    st.session_state.chapter_plans[chapter] = generate_chapter_plan(
        df=df,
        grade=grade,
        subject=subject,
        chapter=chapter,
        total_days=allowed_days,
        pedagogy=pedagogy,
        language=language
    )

plan = st.session_state.chapter_plans[chapter]

current_day = next(
    (d for d in plan["days"] if d["status"] == "unlocked"),
    None
)

if not current_day:
    st.success("🎉 Chapter completed successfully.")
    st.stop()

# =====================================================
# DISPLAY CURRENT DAY
# =====================================================
st.subheader(
    f"{chapter} – Day {current_day['day_no']} of {plan['total_days']}"
)

st.markdown(
    f"""
**Class:** {grade}  
**Subject:** {subject}  
**Pedagogy:** {pedagogy}  
**Integration:** {current_day['integration'] or "—"}
"""
)

# Period structure table
st.markdown("### ⏱️ Period Structure")
st.table(
    pd.DataFrame(
        current_day["period_structure"],
        columns=["Phase", "Minutes"]
    )
)

# Learning outcomes
st.markdown("### 🎯 Learning Outcomes")
for lo in current_day["learning_outcomes"]:
    st.write(f"- {lo}")

# Teaching flow table
st.markdown("### 🧠 Lesson Flow (Execution View)")
flow_rows = []
for phase, mins in current_day["period_structure"]:
    flow_rows.append({
        "Phase": phase,
        "Time": f"{mins} min",
        "Teacher Action": "Refer teaching script",
        "Assessment": "Formative"
    })

st.dataframe(pd.DataFrame(flow_rows), use_container_width=True)

# Teaching script
st.markdown("### 🗣️ Detailed Teaching Script")
st.text_area(
    "Script",
    current_day["script"],
    height=350
)

# =====================================================
# DOWNLOAD SECTION (PDF + WORD)
# =====================================================
st.markdown("### 📥 Download Lesson Plan")

lesson_export = {
    "grade": plan["grade"],
    "subject": plan["subject"],
    "chapter": plan["chapter"],
    "day_no": current_day["day_no"],
    "total_days": plan["total_days"],
    "pedagogy": plan["pedagogy"],
    "integration": current_day["integration"],
    "learning_outcomes": current_day["learning_outcomes"],
    "period_structure": current_day["period_structure"],
    "script": current_day["script"]
}

col1, col2 = st.columns(2)

with col1:
    if st.button("📄 Generate Colourful PDF"):
        pdf_path = generate_lesson_pdf(lesson_export, SCHOOL_NAME)
        with open(pdf_path, "rb") as f:
            st.download_button(
                "Download PDF",
                f,
                file_name="Lesson_Plan.pdf",
                mime="application/pdf"
            )

with col2:
    if st.button("📝 Generate Word File"):
        docx_path = generate_lesson_word(lesson_export, SCHOOL_NAME)
        with open(docx_path, "rb") as f:
            st.download_button(
                "Download Word",
                f,
                file_name="Lesson_Plan.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

# =====================================================
# MARK DAY COMPLETE
# =====================================================
if st.button("✅ Mark Day Completed"):
    idx = current_day["day_no"] - 1
    plan["days"][idx]["status"] = "completed"

    if idx + 1 < len(plan["days"]):
        plan["days"][idx + 1]["status"] = "unlocked"

    st.success("Day marked as completed.")
    st.rerun()
