import streamlit as st
import pandas as pd
from openai import OpenAI
import math
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO

# -----------------------------------------------------------------------------
# 1. APP CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Teach+ Curriculum Director", 
    page_icon="🎓", 
    layout="wide"
)

# -----------------------------------------------------------------------------
# 2. HELPER FUNCTIONS (DEFINED FIRST TO AVOID ERRORS)
# -----------------------------------------------------------------------------

@st.cache_data
def load_data():
    # Ensure this matches your GitHub filename exactly
    file_path = "Teachshank_Master_Database_FINAL.tsv"
    try:
        df = pd.read_csv(file_path, sep='\t')
        return df
    except FileNotFoundError:
        return pd.DataFrame()

def create_word_docx(lesson_text, metadata):
    """Generates a professional Word Document from the lesson plan."""
    doc = Document()
    
    # Title
    title = doc.add_heading('Teach+ Lesson Plan', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Metadata Table
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    
    p1 = hdr_cells[0].paragraphs[0]
    p1.add_run(f"Class: {metadata['grade']} | Subject: {metadata['subject']}\n").bold = True
    p1.add_run(f"Unit: {metadata['chapter']}")
    
    p2 = hdr_cells[1].paragraphs[0]
    p2.add_run(f"Duration: {metadata['duration']} Mins | Phase: {metadata['phase']}\n").bold = True
    p2.add_run(f"Topic: {metadata['topic']}")
    
    doc.add_paragraph("") # Spacer

    # Content Parser (Markdown to Word)
    lines = lesson_text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('## '):
            # Heading 1 (Dark Blue)
            h = doc.add_heading(line.replace('## ', ''), level=1)
            if h.runs:
                h.runs[0].font.color.rgb = RGBColor(0, 51, 102)
                
        elif line.startswith('### '):
            # Heading 2 (Light Blue)
            h = doc.add_heading(line.replace('### ', ''), level=2)
            if h.runs:
                h.runs[0].font.color.rgb = RGBColor(51, 102, 153)
                
        elif line.startswith('- ') or line.startswith('* '):
            # Bullet Points
            clean_text = line.replace('- ', '').replace('* ', '')
            doc.add_paragraph(clean_text, style='List Bullet')
            
        else:
            # Normal Text
            doc.add_paragraph(line)

    # Save to Buffer
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def generate_lesson_script(grade, subject, chapter, outcome, duration, phase, api_key):
    """The AI Engine"""
    
    # Time Calculation
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
    - **Duration:** {duration} Minutes
    
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
        client = OpenAI(api_key=api_key)
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
# 3. MAIN APP LOGIC
# -----------------------------------------------------------------------------

# Load Data
df = load_data()

if df.empty:
    st.error("⚠️ Database Not Found! Please upload 'Teachshank_Master_Database_FINAL.tsv' to your GitHub.")
    st.stop()

st.title("🎓 Teach+ Curriculum Director")
st.markdown("### Strategic Pacing & Micro-Planning System")

# --- SIDEBAR ---
st.sidebar.header("1️⃣ Global Context")

# Selectors
grade_list = sorted(df['Grade'].astype(str).unique().tolist())
selected_grade = st.sidebar.selectbox("Select Grade", grade_list)

subject_list = sorted(df[df['Grade'].astype(str) == selected_grade]['Subject'].unique().tolist())
selected_subject = st.sidebar.selectbox("Select Subject", subject_list)

# Filter Data
subject_data = df[
    (df['Grade'].astype(str) == selected_grade) & 
    (df['Subject'] == selected_subject)
]

# --- TABS ---
tab1, tab2 = st.tabs(["📅 Annual Pacing Calendar", "📝 Daily Lesson Designer"])

# --- TAB 1: CALENDAR ---
with tab1:
    st.subheader(f"Annual Roadmap: {selected_grade} - {selected_subject}")
    
    if not subject_data.empty:
        # Calculate Pacing
        chapter_groups = subject_data.groupby('Chapter Name')['Learning Outcomes'].count().reset_index()
        chapter_groups.columns = ['Instructional Unit', 'Topic_Count']
        
        total_outcomes = chapter_groups['Topic_Count'].sum()
        
        if total_outcomes > 0:
            # Distribute 180 days
            chapter_groups['Allocated Days'] = (chapter_groups['Topic_Count'] / total_outcomes) * 180
            chapter_groups['Allocated Days'] = chapter_groups['Allocated Days'].apply(lambda x: math.ceil(x))
            
            st.dataframe(
                chapter_groups,
                use_container_width=True,
                height=500,
                column_config={
                    "Instructional Unit": st.column_config.TextColumn("Unit Name", width="large"),
                    "Allocated Days": st.column_config.ProgressColumn(
                        "Pacing (Days)", 
                        format="%d Days", 
                        min_value=0, 
                        max_value=int(chapter_groups['Allocated Days'].max())
                    )
                }
            )
        else:
            st.warning("No outcomes found in database for this subject.")
    else:
        st.info("Select a Grade and Subject to view the calendar.")

# --- TAB 2: LESSON DESIGNER ---
with tab2:
    st.subheader("Micro-Lesson Generator")
    
    col_input, col_action = st.columns([1, 2])
    
    with col_input:
        st.markdown("**Step 1: Lesson Context**")
        
        # Select Chapter
        chapter_list = subject_data['Chapter Name'].unique().tolist()
        if chapter_list:
            selected_chapter = st.selectbox("Select Unit / Chapter", chapter_list)
            
            # Select Outcome
            outcome_list = subject_data[subject_data['Chapter Name'] == selected_chapter]['Learning Outcomes'].dropna().tolist()
            if outcome_list:
                selected_outcome = st.selectbox("Select Focus Topic", outcome_list)
            else:
                selected_outcome = "General Overview"
        else:
            selected_chapter = "None"
            selected_outcome = "None"
            st.warning("No chapters found.")

        st.markdown("---")
        st.markdown("**Step 2: Configuration**")
        
        duration = st.slider("Duration (Mins)", 30, 90, 45)
        
        lesson_phase = st.radio(
            "Lesson Phase:",
            ["Introduction / Discovery", "Deep Dive / Explanation", "Practice / Application", "Assessment"],
            index=0
        )
        
        generate_btn = st.button("🚀 Generate Lesson Plan", type="primary")

    with col_action:
        if generate_btn:
            # Check for API Key
            if "OPENAI_API_KEY" not in st.secrets:
                st.error("⚠️ OpenAI API Key is missing! Check Streamlit Advanced Settings.")
            else:
                api_key = st.secrets["OPENAI_API_KEY"]
                
                with st.spinner(f"Designing Lesson for {selected_chapter}..."):
                    # 1. Generate Text
                    plan_text = generate_lesson_script(
                        selected_grade, 
                        selected_subject, 
                        selected_chapter, 
                        selected_outcome, 
                        duration, 
                        lesson_phase,
                        api_key
                    )
                    
                    st.success("Plan Generated!")
                    st.markdown(plan_text)
                    
                    # 2. Generate Word Doc
                    metadata = {
                        "grade": selected_grade,
                        "subject": selected_subject,
                        "chapter": selected_chapter,
                        "topic": selected_outcome,
                        "duration": duration,
                        "phase": lesson_phase
                    }
                    docx_file = create_word_docx(plan_text, metadata)
                    
                    # 3. Download Button
                    safe_name = "".join([c for c in selected_chapter if c.isalnum() or c in (' ','-')]).strip()
                    st.download_button(
                        label="📄 Download as Word Doc (.docx)",
                        data=docx_file,
                        file_name=f"TeachPlus_{safe_name}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
