import streamlit as st
from lesson_engine import load_data, get_chapters, get_learning_outcomes
import openai
import os

st.set_page_config("ERPACAD", layout="wide")

# OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("📘 ERPACAD – Academic Planning Engine")

df = load_data()

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
        "Academic Working Days",
        min_value=160,
        max_value=210,
        value=180
    )

if st.button("Generate Annual Plan"):
    chapters = get_chapters(df, grade, subject)
    st.success(f"✔ {len(chapters)} chapters found")

    for ch in chapters:
        los = get_learning_outcomes(df, grade, subject, ch)
        st.markdown(f"### 📗 {ch}")
        st.write(f"Learning Outcomes: {len(los)}")
