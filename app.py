import streamlit as st
import pandas as pd

from annual_plan_engine import generate_annual_plan
from lesson_engine import generate_chapter_execution_plan
from export_utils import generate_lesson_pdf, generate_lesson_word

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="ERPACAD", layout="wide")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
DATA_PATH = "data/Teachshank_Master_Database_FINAL.tsv"

df = pd.read_csv(DATA_PATH, sep="\t")
df.columns = [c.strip().lower() for c in df.columns]
df.rename(columns={"learning outcomes": "learning_outcome"}, inplace=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
for key in ["user", "role", "progress"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "progress" else {}

# --------------------------------------------------
# LOGIN
# --------------------------------------------------
if st.session_state.user is None:
    st.title("🔐 ERPACAD Login")

    uid = st.text_input("User ID")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        # Principal
        p = st.secrets.get("principal", {})
        if uid == p.get("id") and pwd == p.get("password"):
            st.session_state.user = "principal"
            st.session_state.role = "principal"
            st.rerun()

        # Teachers
        for t in st.secrets.get("teachers", {}).values():
            if uid == t["id"] and pwd == t["password"]:
                st.session_state.user = t
                st.session_state.role = "teacher"
                st.rerun()

        st.error("Invalid credentials")

    st.stop()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.write(f"👤 Logged in as **{st.session_state.user if isinstance(st.session_state.user,str) else st.session_state.user['id']}**")
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# --------------------------------------------------
# PRINCIPAL DASHBOARD
# --------------------------------------------------
if st.session_state.role == "principal":
    st.title("📊 Principal Dashboard")

    if not st.session_state.progress:
        st.info("No teaching data yet.")
        st.stop()

    rows = []
    for g in st.session_state.progress:
        for s in st.session_state.progress[g]:
            for c, v in st.session_state.progress[g][s].items():
                rows.append({
                    "Class": g,
                    "Subject": s,
                    "Chapter": c,
                    "Completed": v["completed"],
                    "Required": v["required"],
                    "Progress %": round(v["completed"] / v["required"] * 100, 1)
                })

    st.dataframe(pd.DataFrame(rows), use_container_width=True)
    st.stop()

# --------------------------------------------------
# TEACHER CONSOLE
# --------------------------------------------------
teacher = st.session_state.user
allowed_classes = list(map(int, teacher["classes"]))
allowed_subjects = teacher["subjects"]

st.title("📘 Teaching Console")

grade = st.selectbox("Class", sorted(allowed_classes))

subjects = df[
    (df["grade"] == grade) &
    (df["subject"].isin(allowed_subjects))
]["subject"].unique().tolist()

subject = st.selectbox("Subject", subjects)

if not subject:
    st.warning("Please select subject")
    st.stop()

academic_days = st.number_input(
    "Academic Working Days",
    min_value=160,
    max_value=210,
    value=180
)

annual_plan = generate_annual_plan(df, grade, subject, academic_days)
chapters = annual_plan["chapters"]

if not chapters:
    st.warning("No chapters found")
    st.stop()

chapter = st.selectbox("Chapter", [c["chapter"] for c in chapters])
meta = next(c for c in chapters if c["chapter"] == chapter)

# --------------------------------------------------
# LEARNING OUTCOMES
# --------------------------------------------------
los = df[
    (df["grade"] == grade) &
    (df["subject"] == subject) &
    (df["chapter"] == chapter)
]["learning_outcome"].unique().tolist()

key = f"{grade}-{subject}-{chapter}"

if key not in st.session_state:
    st.session_state[key] = generate_chapter_execution_plan(
        grade=grade,
        subject=subject,
        chapter=chapter,
        total_periods=meta["required_periods"],
        pedagogy="LEARN360",
        learning_outcomes=los,
        language="English"
    )

plan = st.session_state[key]

current = next((p for p in plan["periods"] if p["status"] == "unlocked"), None)

if not current:
    st.success("🎉 Chapter Completed")
    st.stop()

# --------------------------------------------------
# DISPLAY PERIOD
# --------------------------------------------------
st.subheader(f"{chapter} – Period {current['period_no']} / {plan['required_periods']}")
st.text_area("Teaching Script", current["script"], height=350)

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------
export_data = {
    "grade": grade,
    "subject": subject,
    "chapter": chapter,
    "period": current["period_no"],
    "total": plan["required_periods"],
    "script": current["script"],
    "learning_outcomes": los,
}

c1, c2 = st.columns(2)
with c1:
    if st.button("📄 Download PDF"):
        path = generate_lesson_pdf(export_data)
        with open(path, "rb") as f:
            st.download_button("Download PDF", f, file_name="lesson.pdf")

with c2:
    if st.button("📝 Download Word"):
        path = generate_lesson_word(export_data)
        with open(path, "rb") as f:
            st.download_button("Download Word", f, file_name="lesson.docx")

# --------------------------------------------------
# MARK COMPLETE
# --------------------------------------------------
if st.button("✅ Mark Period Completed"):
    idx = current["period_no"] - 1
    plan["periods"][idx]["status"] = "completed"

    if idx + 1 < len(plan["periods"]):
        plan["periods"][idx + 1]["status"] = "unlocked"

    st.session_state.progress.setdefault(str(grade), {}) \
        .setdefault(subject, {}) \
        .setdefault(chapter, {"completed": 0, "required": plan["required_periods"]})

    st.session_state.progress[str(grade)][subject][chapter]["completed"] += 1
    st.rerun()
