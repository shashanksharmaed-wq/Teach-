import streamlit as st
import pandas as pd
from annual_plan_engine import generate_annual_plan

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config("ERPACAD", layout="wide")

DATA_PATH = "data/Teachshank_Master_Database_FINAL_v2.tsv"

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH, sep="\t")

df = load_data()

# -----------------------------
# UI
# -----------------------------
st.title("📘 ERPACAD – Academic Planning Engine")

col1, col2, col3 = st.columns(3)

with col1:
    grade = st.selectbox("Class", sorted(df["class"].unique()))

with col2:
    subject = st.selectbox(
        "Subject",
        sorted(df[df["class"] == grade]["subject"].unique())
    )

with col3:
    academic_days = st.number_input(
        "Academic Working Days (School-wide)",
        min_value=160,
        max_value=210,
        value=180
    )

# -----------------------------
# GENERATE
# -----------------------------
if st.button("Generate Annual Plan"):
    plan = generate_annual_plan(df, grade, subject, academic_days)

    if not plan["chapters"]:
        st.warning(plan.get("message", "No plan generated"))
    else:
        st.success("Annual plan generated (CBSE-safe, period-based)")

        st.markdown(f"""
        **Weekly Periods:** {plan["weekly_periods"]}  
        **Total Periods (Year):** {plan["total_periods"]}
        """)

        plan_df = pd.DataFrame(plan["chapters"])
        st.dataframe(plan_df, use_container_width=True)
