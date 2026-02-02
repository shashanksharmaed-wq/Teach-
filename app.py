# app.py
import streamlit as st
from preprimary_engine import generate_preprimary_lesson

st.set_page_config(page_title="ERPACAD – Pre-Primary", layout="wide")

st.title("ERPACAD – Pre-Primary Readiness Engine")
st.caption("One complete teaching script • No steps • No errors")

class_name = st.selectbox("Class", ["NURSERY", "LKG", "UKG"])
subject = st.selectbox("Subject", ["Literacy", "Numeracy"])

st.divider()

if st.button("Generate Readiness Experience"):
    lesson = generate_preprimary_lesson(class_name, subject)

    st.subheader(lesson["title"])
    st.write(f"**Duration:** {lesson['duration']}")

    st.divider()

    st.markdown("### Teaching Script")
    st.write(lesson["script"])
