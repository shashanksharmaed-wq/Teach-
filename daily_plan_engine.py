def generate_daily_plan(chapter, day_no, total_days, subject, grade):
    """
    Generates a structured, detailed daily lesson plan
    """

    return {
        "day": day_no,
        "title": f"{chapter} – Day {day_no} of {total_days}",
        "structure": [
            {
                "phase": "Engage",
                "time": "5 min",
                "teacher_script": (
                    f"Begin the class by connecting the topic '{chapter}' "
                    f"to students’ prior knowledge. Ask 2–3 recall questions."
                ),
                "student_activity": "Students respond orally and share examples."
            },
            {
                "phase": "Concept Building",
                "time": "15 min",
                "teacher_script": (
                    f"Explain the core concept of '{chapter}' using examples "
                    f"appropriate for Class {grade}. Use board work and questioning."
                ),
                "student_activity": "Students listen, observe, and note key points."
            },
            {
                "phase": "Guided Practice",
                "time": "10 min",
                "teacher_script": (
                    "Conduct a short guided activity related to the concept."
                ),
                "student_activity": "Students perform the activity individually or in pairs."
            },
            {
                "phase": "Assessment",
                "time": "5 min",
                "teacher_script": (
                    "Ask oral questions to check understanding."
                ),
                "student_activity": "Students answer orally or in writing."
            },
            {
                "phase": "Closure",
                "time": "5 min",
                "teacher_script": (
                    "Summarize the key learning and explain what will be covered next."
                ),
                "student_activity": "Students reflect and ask doubts."
            }
        ]
    }
