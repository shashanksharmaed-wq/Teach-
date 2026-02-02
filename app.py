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
st.set_page_config(page_title="Teach+ Pro", page_icon="⏱️", layout="wide")

# -----------------------------------------------------------------------------
# 2. HELPER FUNCTIONS
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Teachshank_Master_Database_FINAL.tsv", sep='\t')
        return df
    except FileNotFoundError:
        return pd.DataFrame()

def calculate_pacing(df):
    """Calculates Allocated Days per Chapter based on 180-Day Year."""
    if df.empty: return pd.DataFrame()
    
    groups = df.groupby('Chapter Name')['Learning Outcomes'].count().reset_index()
    groups.columns = ['Chapter', 'Topic_Count']
    total_topics = groups['Topic_Count'].sum()
    
    if total_topics > 0:
        groups['Allocated_Days'] = (groups['Topic_Count'] / total_topics) * 180
        groups['Allocated_Days'] = groups['Allocated_Days'].apply(lambda x: max(1, math.ceil(x))) # Min 1 day
    return groups

def create_word_docx(lesson_text, metadata):
    doc = Document()
    title = doc.add_heading('Teach+ Lesson Plan', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    table = doc.add_table(rows=2, cols=2)
    table.style = 'Table Grid'
    
    r1 = table.rows[0].cells
    r1[0].paragraphs[0].add_run(f"Class: {metadata['grade']} | Subject: {metadata['subject']}").bold = True
    r1[1].paragraphs[0].add_run(f"Lesson: {metadata['lesson_num']} of {metadata['total_days']}").bold = True
    
    r2 = table.rows[1].cells
    r2[0].paragraphs[0].add_run(f"Unit: {metadata['chapter']}\nTopic: {metadata['topic']}")
    r2[1].paragraphs[0].add_run(f"Phase: {metadata['phase']} ({metadata['duration']} mins)")
    
    doc.add_paragraph("") 

    for line in lesson_text.split('\n'):
        line = line.strip()
        if not line: continue
        if line.startswith('## '):
            h = doc.add_heading(line.replace('## ', ''), level=1)
            h.runs[0].font.color.rgb = RGBColor(0, 51, 102)
        elif line.startswith('### '):
            h = doc.add_heading(line.replace('### ', ''), level=2)
            h.runs[0].font.color.rgb = RGBColor(51, 102, 153)
        elif line.startswith('- ') or line.startswith('* '):
            doc.add_paragraph(line.replace('- ', '').replace('* ', ''), style='List Bullet')
        else:
            doc.add_paragraph(line)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def generate_strict_lesson(grade, subject, chapter, outcome, duration, lesson_num, total_days, api_key):
    
    # --- STRICT PACING LOGIC ---
    # This logic forces the AI to stick to the specific "Day Type"
    
    progress_ratio = lesson_num / total_days
    
    if lesson_num == 1:
        phase = "PHASE 1: ENGAGE & HOOK (Introduction)"
        instruction = "This is Day 1. Focus ONLY on sparking curiosity and defining basic terms. DO NOT go deep yet."
    elif lesson_num == total_days:
        phase = "PHASE 4: EVALUATE (Assessment & Exit)"
        instruction = "This is the FINAL Day. Focus on consolidating learning and summative assessment. No new concepts."
    elif progress_ratio <= 0.5:
        phase = "PHASE 2: EXPLORE (Deep Dive)"
        instruction = "This is the core instructional day. Focus on 'How' and 'Why'. Use hands-on exploration."
    else:
        phase = "PHASE 3: ELABORATE (Application)"
        instruction = "This is an Application day. Move from theory to practice/workbook/real-life scenarios."

    t_engage = int(duration * 0.15)
    t_explore = int(duration * 0.35)
    t_explain = int(duration * 0.25)
    
    prompt = f"""
    You are the 'Teach+' Strict Pacing Engine.
    
    CRITICAL CONTEXT:
    - **Grade/Subject:** {grade} - {subject}
    - **Unit:** {chapter} (Allocated: {total_days} Days)
    - **Current Lesson:** Day {lesson_num} of {total_days}
    - **Strict Phase:** {phase}
    - **Topic Focus:** {outcome}
    
    INSTRUCTION:
    {instruction}
    
    Do NOT repeat content from other phases. If this is Day 1, do not assess. If this is the last day, do not introduce new hooks.
    
    OUTPUT (Markdown):
    ## 1. Lesson Metadata
    - **Lesson Position:** {lesson_num}/{total_days} ({phase})
    - **Goal:** (Specific to this phase)

    ## 2. Micro-Script ({duration} Mins)

    ### ⏰ 00:00 - 00:{t_engage:02d} | I. START
    - **Script:** ...

    ### ⏰ 00:{t_engage:02d} - 00:{t_engage+t_explore:02d} | II. CORE ACTIVITY
    - **Activity:** ...
    - **Instruction:** ...

    ### ⏰ 00:{t_engage+t_explore:02d} - 00:{t_engage+t_explore+t_explain:02d} | III. EXPLANATION
    - **Concept:** ...

    ### ⏰ 00:{t_engage+t_explore+t_explain:02d} - 00:{duration:02d} | IV. CLOSE
    - **Task:** ...
    """
    
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5 # Lower temp for stricter adherence
        )
        return response.choices[0].message.content, phase
    except Exception as e:
        return f"Error: {str(e)}", "Error"

# -----------------------------------------------------------------------------
# 3. MAIN UI
# -----------------------------------------------------------------------------
df = load_data()
if df.empty:
    st.error("Upload 'Teachshank_Master_Database_FINAL.tsv' to GitHub.")
    st.stop()

st.title("🎓 Teach+ Precision Pacing Engine")

# --- SIDEBAR (Global Context) ---
st.sidebar.header("1️⃣ Select Class & Subject")
grade = st.sidebar.selectbox("Grade", sorted(df['Grade'].astype(str).unique()))
subject = st.sidebar.selectbox("Subject", sorted(df[df['Grade'].astype(str)==grade]['Subject'].unique()))

# Filter Data & Calculate Pacing
subject_data = df[(df['Grade'].astype(str)==grade) & (df['Subject']==subject)]
pacing_df = calculate_pacing(subject_data)

# --- TABS ---
tab1, tab2 = st.tabs(["📅 Annual Pacing (Read-Only)", "📝 Pacing-Guarded Planner"])

# TAB 1: CALENDAR
with tab1:
    st.subheader(f"Annual Budget: {grade} - {subject}")
    if not pacing_df.empty:
        st.dataframe(pacing_df, use_container_width=True, 
                     column_config={"Allocated_Days": st.column_config.ProgressColumn("Days", format="%d", max_value=30)})
    else:
        st.info("No data available.")

# TAB 2: PACING-GUARDED DESIGNER
with tab2:
    st.subheader("Strict Pacing Planner")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 1. Select Chapter
        chapters = pacing_df['Chapter'].tolist()
        if not chapters: st.stop()
        
        sel_chapter = st.selectbox("Select Unit", chapters)
        
        # 2. GET ALLOCATED DAYS (The Guardrail)
        total_days = int(pacing_df[pacing_df['Chapter'] == sel_chapter]['Allocated_Days'].values[0])
        st.info(f"📅 This Chapter is budgeted for **{total_days} Days**.")
        
        # 3. Select Lesson Number (The Slider enforces the limit)
        lesson_num = st.number_input(
            f"Which Lesson are you planning? (1 to {total_days})", 
            min_value=1, 
            value=1
        )
        
        # Pacing Check
        if lesson_num > total_days:
            st.error(f"⚠️ OVERRUN! You are planning Day {lesson_num}, but the budget is {total_days} days.")
        
        # 4. Select Outcome
        outcomes = subject_data[subject_data['Chapter Name'] == sel_chapter]['Learning Outcomes'].tolist()
        sel_outcome = st.selectbox("Topic Focus", outcomes)
        
        duration = st.slider("Duration", 30, 90, 45)
        
        btn = st.button("🚀 Generate Strict Plan", type="primary")

    with col2:
        if btn:
            if "OPENAI_API_KEY" not in st.secrets:
                st.error("API Key Missing.")
            else:
                with st.spinner(f"Enforcing Pacing for Lesson {lesson_num}/{total_days}..."):
                    
                    script, phase_name = generate_strict_lesson(
                        grade, subject, sel_chapter, sel_outcome, duration, 
                        lesson_num, total_days, st.secrets["OPENAI_API_KEY"]
                    )
                    
                    st.success(f"Generated: {phase_name}")
                    st.markdown(script)
                    
                    # Word Doc
                    meta = {
                        "grade": grade, "subject": subject, "chapter": sel_chapter,
                        "topic": sel_outcome, "duration": duration, 
                        "lesson_num": lesson_num, "total_days": total_days, "phase": phase_name
                    }
                    docx = create_word_docx(script, meta)
                    
                    safe_name = "".join([c for c in sel_chapter if c.isalnum()]).strip()
                    st.download_button(
                        f"📄 Download Lesson {lesson_num} (.docx)", 
                        docx, 
                        f"Lesson_{lesson_num}_{safe_name}.docx",
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
