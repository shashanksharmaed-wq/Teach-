import streamlit as st
import pandas as pd
from openai import OpenAI
import math
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO
import re

# -----------------------------------------------------------------------------
# 1. APP CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Teach+ Curriculum Manager", 
    page_icon="📅", 
    layout="wide"
)

st.title("📅 Teach+ Curriculum Manager")
st.markdown("### Flexible Lesson Architect")

# -----------------------------------------------------------------------------
# 2. LOAD DATABASE
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    file_path = "Teachshank_Master_Database_FINAL.tsv"
    try:
        df = pd.read_csv(file_path, sep='\t')
        return df
    except FileNotFoundError:
        st.error(f"⚠️ Critical Error: Could not find '{file_path}'. Please upload it to your GitHub repository.")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()

# -----------------------------------------------------------------------------
# 3. SIDEBAR: SELECTORS
# -----------------------------------------------------------------------------
st.sidebar.header("1️⃣ Curriculum Controls")

# A. Grade Selection
grade_list = sorted(df['Grade'].astype(str).unique().tolist())
selected_grade = st.sidebar.selectbox("Select Grade", grade_list)

# B. Subject Selection
subject_list = sorted(df[df['Grade'].astype(str) == selected_grade]['Subject'].unique().tolist())
selected_subject = st.sidebar.selectbox("Select Subject", subject_list)

# Filter Data
subject_data = df[
    (df['Grade'].astype(str) == selected_grade) & 
    (df['Subject'] == selected_subject)
]

# C. Chapter Selection
chapter_list = subject_data['Chapter Name'].unique().tolist()
selected_chapter = st.sidebar.selectbox("Select Lesson / Chapter", chapter_list)

# D. Topic / Outcome Selection
outcome_list = subject_data[subject_data['Chapter Name'] == selected_chapter]['Learning Outcomes'].dropna().tolist()

if outcome_list:
    selected_outcome = st.sidebar.selectbox("Select Specific Learning Focus", outcome_list)
else:
    selected_outcome = "General Chapter Overview"

st.sidebar.markdown("---")
st.sidebar.header("2️⃣ Planner Settings")
duration = st.sidebar.slider("Duration (Mins)", 30, 90, 45)
lesson_phase = st.sidebar.radio(
    "Lesson Phase:",
    ["Introduction / Discovery", "Deep Dive / Explanation", "Practice / Application", "Assessment"],
    index=0
)

# -----------------------------------------------------------------------------
# 4. DOCUMENT ENGINE (Creates the Word Doc)
# -----------------------------------------------------------------------------
def create_word_docx(lesson_text, metadata):
    doc = Document()
    
    # 1. Title Section
    title = doc.add_heading(f"Teach+ Lesson Plan: {metadata['subject']}", 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 2. Metadata Table
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    
    # Left Column
    p1 = hdr_cells[0].paragraphs[0]
    p1.add_run(f"Class: {metadata['grade']}\n").bold = True
    p1.add_run(f"Unit: {metadata['chapter']}\n")
    p1.add_run(f"Phase: {metadata['phase']}")
    
    # Right Column
    p2 = hdr_cells[1].paragraphs[0]
    p2.add_run(f"Duration: {metadata['duration']} Mins\n").bold = True
    p2.add_run(f"Topic: {metadata['topic']}")
    
    doc.add_paragraph("") # Spacer

    # 3. Parse and Format the AI Text
    # This simple parser looks for Markdown headers and converts them to Word styles
    lines = lesson_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect Headers (## or ###)
        if line.startswith('## '):
            heading = line.replace('## ', '')
            h = doc.add_heading(heading, level=1)
            run = h.runs[0]
            run.font.color.rgb = RGBColor(0, 51, 102) # Dark Blue
            
        elif line.startswith('### '):
            heading = line.replace('### ', '')
            h = doc.add_heading(heading, level=2)
            run = h.runs[0]
            run.font.color.rgb = RGBColor(51, 102, 153) # Lighter Blue
            
        # Detect Bullet Points
        elif line.startswith('- ') or line.startswith('* '):
            clean_line = line.replace('- ', '').replace('* ', '')
            p = doc.add_paragraph(clean_line, style='List Bullet')
            
        # Standard Text
        else:
            doc.add_paragraph(line)

    # 4. Save to Memory Stream
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# -----------------------------------------------------------------------------
# 5. AI GENERATION ENGINE
# -----------------------------------------------------------------------------
def generate_lesson_script(grade, subject, chapter, outcome, duration, phase):
    
    t_engage = int(duration * 0.15)
    t_explore = int(duration * 0.30)
    t_explain = int(duration * 0.25)
    
    prompt = f"""
    You are the 'Teach+' Lesson Architect.
    
    TASK:
    Generate a deep, scripted lesson plan for:
    - **Grade:** {grade}
    - **Subject:** {subject}
    - **Lesson Unit:** {chapter}
    - **Focus Topic:** {outcome}
    - **Phase:** {phase}
    
    OUTPUT FORMAT (Markdown):

    ## 1. Context
    - **Topic:** (Specific Focus)
    - **Goal:** (What specifically will be mastered?)

    ## 2. The Micro-Script ({duration} Mins)

    ### ⏰ 00:00 - 00:{t_engage:02d} | I. ENGAGE
    - **Script:** "Teacher says..."
    - **Action:** (Prop/Movement)

    ### ⏰ 00:{t_engage:02d} - 00:{t_engage+t_explore:02d} | II. EXPLORE
    - **Activity:** ...
    - **Scripted Instruction:** ...

    ### ⏰ 00:{t_engage+t_explore:02d} - 00:{t_engage+t_explore+t_explain:02d} | III. EXPLAIN
    - **Concept:** ...
    - **Script:** ...

    ### ⏰ 00:{t_engage+t_explore+t_explain:02d} - 00:{duration:02d} | IV. ELABORATE & EVALUATE
    - **Application Task:** ...
    - **Exit Ticket:** ...
    """
    
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert pedagogue."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# -----------------------------------------------------------------------------
# 6. GENERATE & DOWNLOAD
# -----------------------------------------------------------------------------
if st.button("🚀 Generate Lesson Plan"):
    if "OPENAI_API_KEY" not in st.secrets:
        st.error("⚠️ OpenAI API Key is missing!")
    else:
        with st.spinner(f"Designing Lesson for: {selected_chapter}..."):
            # 1. Generate Text
            plan_text = generate_lesson_script(
                selected_grade, 
                selected_subject, 
                selected_chapter, 
                selected_outcome, 
                duration,
                lesson_phase
            )
            
            # 2. Show Preview
            st.markdown("---")
            st.markdown(plan_text)
            
            # 3. Create Word Document
            metadata = {
                "grade": selected_grade,
                "subject": selected_subject,
                "chapter": selected_chapter,
                "topic": selected_outcome,
                "duration": duration,
                "phase": lesson_phase
            }
            
            docx_file = create_word_docx(plan_text, metadata)
            
            # 4. Sanitize Filename
            safe_chapter = "".join([c for c in selected_chapter if c.isalnum() or c in (' ','-')]).strip()
            
            # 5. Download Button
            st.download_button(
                label="📄 Download as Word Doc (.docx)",
                data=docx_file,
                file_name=f"TeachPlus_{safe_chapter}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
