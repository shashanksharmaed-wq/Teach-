# daily_plan_engine.py
# ERPACAD – DEPTH-CYCLE™ Lesson Generator
# Authoritative version – DO NOT MODIFY STRUCTURE

from typing import Dict, List

# -------------------------------------------------
# DEPTH PROFILE
# -------------------------------------------------

def get_depth_profile(grade: int) -> str:
    if grade <= 3:
        return "PRIMARY"
    elif grade <= 5:
        return "UPPER_PRIMARY"
    elif grade <= 8:
        return "MIDDLE"
    else:
        return "SECONDARY"


# -------------------------------------------------
# CORE GENERATOR
# -------------------------------------------------

def generate_daily_plan(
    grade: int,
    subject: str,
    chapter: str,
    learning_outcomes: List[str],
    day: int,
    total_days: int,
    period_minutes: int = 40
) -> Dict:
    """
    Generates ONE DAY lesson plan.
    Engine guarantees DEPTH, ADAPTATION, and SAFETY.
    """

    depth = get_depth_profile(grade)
    exam_mode = grade >= 9

    plan = {
        "meta": {
            "grade": grade,
            "subject": subject,
            "chapter": chapter,
            "day": day,
            "total_days": total_days,
            "period_minutes": period_minutes,
            "depth_profile": depth,
            "exam_relevance": exam_mode
        },
        "phases": []
    }

    # -------------------------------
    # D — DISCOVER CONTEXT
    # -------------------------------

    plan["phases"].append({
        "code": "D",
        "name": "Discover Context",
        "minutes": 6,
        "teacher_script": [
            f"Before we begin, think about a real-life situation related to '{chapter}'.",
            "I want you to imagine yourself in such a situation and observe how people react."
        ],
        "expected_student_responses": [
            "Students share experiences or observations.",
            "Students connect the topic with daily life."
        ],
        "misconceptions": [
            "Students may think the lesson is only about the story, not life."
        ],
        "teacher_interventions": [
            "Guide students to see how real-life situations shape decisions and thinking."
        ],
        "assessment_evidence": [
            "Students verbally connect topic with lived experience."
        ]
    })

    # -------------------------------
    # E — EXPOSE CORE CONTENT
    # -------------------------------

    plan["phases"].append({
        "code": "E",
        "name": "Expose Core Content",
        "minutes": 10,
        "teacher_script": [
            f"I will now read and explain the key portion of '{chapter}'.",
            "Listen carefully to the language, emotions, and ideas."
        ],
        "expected_student_responses": [
            "Students listen attentively.",
            "Students identify key events or ideas."
        ],
        "misconceptions": [
            "Students may focus only on plot, not meaning."
        ],
        "teacher_interventions": [
            "Pause reading to clarify meanings and context.",
            "Explain difficult words using examples."
        ],
        "assessment_evidence": [
            "Students can retell the idea in their own words."
        ]
    })

    # -------------------------------
    # P — PROBE THINKING
    # -------------------------------

    probe_questions = [
        f"Why do you think the characters act the way they do in '{chapter}'?",
        "What would you have done differently in the same situation?"
    ]

    if depth in ["MIDDLE", "SECONDARY"]:
        probe_questions.append(
            "What does this situation reveal about human nature or society?"
        )

    plan["phases"].append({
        "code": "P",
        "name": "Probe Thinking",
        "minutes": 8,
        "teacher_script": probe_questions,
        "expected_student_responses": [
            "Students justify answers with reasons.",
            "Students refer to events or ideas from the chapter."
        ],
        "misconceptions": [
            "Students may give moral answers without explanation."
        ],
        "teacher_interventions": [
            "Ask follow-up 'why' and 'how' questions.",
            "Encourage evidence-based responses."
        ],
        "assessment_evidence": [
            "Students explain reasoning, not just opinions."
        ]
    })

    # -------------------------------
    # T — TRANSFORM UNDERSTANDING
    # -------------------------------

    transform_tasks = [
        "Students write one sentence connecting the lesson to their own life.",
        "Students discuss how the idea applies beyond the classroom."
    ]

    if depth == "SECONDARY":
        transform_tasks.append(
            "Students link the theme with possible examination questions."
        )

    plan["phases"].append({
        "code": "T",
        "name": "Transform Understanding",
        "minutes": 10,
        "teacher_script": [
            "Let us now apply what we learned in a meaningful way."
        ],
        "expected_student_responses": transform_tasks,
        "misconceptions": [
            "Students may repeat textbook language instead of original thinking."
        ],
        "teacher_interventions": [
            "Encourage originality and clarity.",
            "Model one strong example."
        ],
        "assessment_evidence": [
            "Written or spoken responses showing application."
        ]
    })

    # -------------------------------
    # H — HARVEST EVIDENCE
    # -------------------------------

    harvest_notes = [
        "Students summarise the lesson in one sentence.",
        "Teacher observes participation and clarity."
    ]

    if exam_mode:
        harvest_notes.append(
            "Teacher highlights how this learning may appear in board exams."
        )

    plan["phases"].append({
        "code": "H",
        "name": "Harvest Evidence",
        "minutes": 6,
        "teacher_script": [
            "Let us reflect on what we learned today."
        ],
        "expected_student_responses": [
            "Students summarise key understanding."
        ],
        "misconceptions": [
            "Students may recall facts but miss meaning."
        ],
        "teacher_interventions": [
            "Rephrase student responses to reinforce clarity."
        ],
        "assessment_evidence": harvest_notes
    })

    return plan
