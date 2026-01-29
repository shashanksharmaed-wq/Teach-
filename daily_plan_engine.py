# daily_plan_engine.py
# ERPACAD – DEPTH++ Daily Lesson Planning Engine
# Author: ERPACAD Core Engine
# Purpose: Generate PERFORMANCE-READY lesson scripts (not instructions)

from typing import Dict, List


# -------------------------------
# DEPTH PROFILE (Grade-sensitive)
# -------------------------------

def get_depth_profile(grade: str) -> Dict:
    """
    Determines cognitive and instructional depth based on grade band.
    Grade is treated as STRING to avoid Nursery / KG errors.
    """

    grade_upper = str(grade).upper()

    if grade_upper in ["NURSERY", "LKG", "UKG"]:
        return {
            "question_style": "oral, concrete, gesture-based",
            "language_level": "simple, repetitive",
            "abstract_allowed": False
        }

    try:
        g = int(grade)
        if g <= 3:
            return {
                "question_style": "guided oral + visual",
                "language_level": "simple with examples",
                "abstract_allowed": False
            }
        elif g <= 5:
            return {
                "question_style": "why/how with examples",
                "language_level": "structured sentences",
                "abstract_allowed": True
            }
        else:
            return {
                "question_style": "analytical, inferential",
                "language_level": "academic but accessible",
                "abstract_allowed": True
            }
    except ValueError:
        return {
            "question_style": "guided",
            "language_level": "simple",
            "abstract_allowed": False
        }


# -------------------------------
# CORE ENGINE
# -------------------------------

def generate_daily_plan(
    grade: str,
    subject: str,
    chapter: str,
    day: int,
    total_days: int
) -> Dict:
    """
    Generates ONE FULL DAY lesson plan using DEPTH++ framework.
    """

    depth = get_depth_profile(grade)

    return {
        "metadata": {
            "grade": grade,
            "subject": subject,
            "chapter": chapter,
            "day": day,
            "total_days": total_days,
            "period_duration_minutes": 40
        },

        "learning_focus": [
            f"Build conceptual understanding from '{chapter}' (Day {day})",
            "Surface misconceptions and replace with accurate reasoning"
        ],

        "phases": [

            # ---------------- ATTUNE ----------------
            {
                "phase": "ATTUNE",
                "duration_min": 5,
                "teacher_says": (
                    "Teacher pauses, looks at students, and sets the tone.\n"
                    "Teacher says: 'Before we begin, let us think quietly for a moment.'"
                ),
                "student_response": (
                    "Students settle, focus attention, and mentally prepare."
                ),
                "purpose": "Emotional and cognitive readiness",
                "diagram_required": False
            },

            # ---------------- ANCHOR ----------------
            {
                "phase": "ANCHOR",
                "duration_min": 6,
                "teacher_says": (
                    "Teacher connects the chapter to a familiar experience.\n"
                    "Teacher narrates a short, concrete situation related to the chapter.\n"
                    "Teacher asks one open-ended question and waits."
                ),
                "student_response": (
                    "Students share prior ideas, including partially correct or incorrect beliefs."
                ),
                "common_misconception": (
                    "Students may explain using everyday logic rather than subject reasoning."
                ),
                "teacher_correction": (
                    "Teacher does not correct immediately.\n"
                    "Teacher acknowledges responses and says: 'Let us explore this together.'"
                ),
                "purpose": "Activate prior knowledge",
                "diagram_required": False
            },

            # ---------------- UNPACK ----------------
            {
                "phase": "UNPACK",
                "duration_min": 10,
                "teacher_says": (
                    "Teacher breaks the concept into small ideas.\n"
                    "Teacher explains each idea slowly, using clear language.\n"
                    f"Teacher asks {depth['question_style']} questions after each idea."
                ),
                "student_response": (
                    "Students respond orally, ask questions, and clarify meaning."
                ),
                "key_vocabulary": [
                    "Important terms from the chapter are introduced explicitly",
                    "Teacher uses each word in a sentence",
                    "Students repeat and rephrase"
                ],
                "purpose": "Concept construction",
                "diagram_required": True,
                "diagram_instruction": (
                    "Teacher draws a simple labeled diagram on the board.\n"
                    "Teacher explains each label while drawing.\n"
                    "Students observe and verbally explain what each part shows."
                )
            },

            # ---------------- CONFRONT ----------------
            {
                "phase": "CONFRONT",
                "duration_min": 6,
                "teacher_says": (
                    "Teacher presents a common incorrect idea related to the topic.\n"
                    "Teacher asks: 'Does this always happen? Why or why not?'"
                ),
                "student_response": (
                    "Students initially agree or disagree.\n"
                    "Some students revise their thinking."
                ),
                "teacher_correction": (
                    "Teacher uses evidence, example, or board explanation to resolve confusion."
                ),
                "purpose": "Misconception correction",
                "diagram_required": True,
                "diagram_instruction": (
                    "Teacher modifies or adds to the existing diagram to show correct logic."
                )
            },

            # ---------------- STRUCTURE ----------------
            {
                "phase": "STRUCTURE",
                "duration_min": 6,
                "teacher_says": (
                    "Teacher organizes ideas into clear steps or points on the board.\n"
                    "Teacher numbers or boxes the logic clearly."
                ),
                "student_response": (
                    "Students copy selectively and ask clarifying questions."
                ),
                "purpose": "Mental organization of knowledge",
                "diagram_required": False
            },

            # ---------------- TRANSFER ----------------
            {
                "phase": "TRANSFER",
                "duration_min": 4,
                "teacher_says": (
                    "Teacher poses a new situation different from the textbook.\n"
                    "Teacher asks students to apply today’s idea to this new context."
                ),
                "student_response": (
                    "Students attempt reasoning, even if unsure."
                ),
                "purpose": "Application beyond textbook",
                "diagram_required": False
            },

            # ---------------- EVIDENCE ----------------
            {
                "phase": "EVIDENCE",
                "duration_min": 3,
                "teacher_says": (
                    "Teacher asks two precise questions that reveal understanding.\n"
                    "Teacher listens for reasoning, not memorized answers."
                ),
                "student_response": (
                    "Students explain ideas in their own words."
                ),
                "evidence_of_learning": [
                    "Student explains concept without prompting",
                    "Student refers correctly to diagram or example"
                ],
                "purpose": "Verify learning",
                "diagram_required": False
            }
        ]
    }
