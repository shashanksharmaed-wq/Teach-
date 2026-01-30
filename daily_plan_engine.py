def generate_daily_plan(
    grade,
    subject,
    chapter,
    day,
    total_days,
    learning_outcomes=None
):
    """
    DEPTH++ Daily Lesson Generator
    Stable for ALL grades including NURSERY / KG
    """

    plan = {
        "meta": {
            "grade": str(grade),
            "subject": subject,
            "chapter": chapter,
            "day": day,
            "total_days": total_days
        },
        "blocks": []
    }

    # ---------- BLOCK 1 ----------
    plan["blocks"].append({
        "title": "Context Setting & Emotional Readiness",
        "minutes": 5,
        "teacher_says": (
            "Children, today we are going to listen carefully to sounds. "
            "Close your eyes for a moment. Can you hear my clap?"
        ),
        "teacher_does": (
            "Teacher claps softly, then loudly. "
            "Pauses between each sound."
        ),
        "students_expected": (
            "Students say 'Yes', some say 'loud', some repeat the sound."
        ),
        "students_misconceptions": (
            "Some students may shout randomly or copy without listening."
        ),
        "teacher_correction": (
            "Teacher calmly says: 'We listen first, then we speak. "
            "Let us try again slowly.'"
        ),
        "tlm_or_boardwork": (
            "No diagram. Use body movements and sound play."
        )
    })

    # ---------- BLOCK 2 ----------
    plan["blocks"].append({
        "title": "Core Concept Unpacking – Sound Differences",
        "minutes": 10,
        "teacher_says": (
            "Listen carefully: clap… tap… snap. "
            "Each sound is different. Which one was loudest?"
        ),
        "teacher_does": (
            "Teacher demonstrates sounds using hands and desk."
        ),
        "students_expected": (
            "Students say 'clap' or point to hands."
        ),
        "students_misconceptions": (
            "Students may focus on action, not sound."
        ),
        "teacher_correction": (
            "Teacher says: 'We are not watching hands. "
            "We are listening to ears.' Repeats sounds."
        ),
        "tlm_or_boardwork": (
            "Teacher draws ear symbol on board (simple)."
        )
    })

    # ---------- BLOCK 3 ----------
    plan["blocks"].append({
        "title": "Guided Practice – Rhyme Exposure",
        "minutes": 8,
        "teacher_says": (
            "Teacher recites the rhyme slowly and clearly:\n\n"
            "'Clap your hands, tap your feet,\n"
            "Listen close to sounds you meet.'"
        ),
        "teacher_does": (
            "Teacher uses hand actions matching rhyme."
        ),
        "students_expected": (
            "Students repeat words and actions."
        ),
        "students_misconceptions": (
            "Some students may shout without rhythm."
        ),
        "teacher_correction": (
            "Teacher slows pace and models correct rhythm again."
        ),
        "tlm_or_boardwork": (
            "No diagram. Teacher models actions."
        )
    })

    # ---------- BLOCK 4 ----------
    plan["blocks"].append({
        "title": "Assessment & Closure",
        "minutes": 5,
        "teacher_says": (
            "Today we learned that sounds can be loud or soft. "
            "Tell me one sound you heard today."
        ),
        "teacher_does": (
            "Teacher points to ear symbol on board."
        ),
        "students_expected": (
            "Students say 'clap', 'tap', or mimic sounds."
        ),
        "students_misconceptions": (
            "Some students may stay silent."
        ),
        "teacher_correction": (
            "Teacher encourages gently and repeats sound options."
        ),
        "tlm_or_boardwork": (
            "Board symbol remains for recall."
        )
    })

    return plan
