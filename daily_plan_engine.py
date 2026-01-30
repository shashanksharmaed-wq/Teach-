def generate_daily_plan(
    grade,
    subject,
    chapter,
    day,
    total_days,
    learning_outcomes=None
):
    """
    Returns a DEPTH++ daily lesson plan.
    NO external dependencies.
    NO missing keys.
    """

    sections = [
        {
            "title": "Context Setting (5 min)",
            "teacher": (
                f"Teacher sets context for the chapter '{chapter}'. "
                "Teacher narrates the background slowly, connects it to students' lived experiences, "
                "and clearly states why this chapter matters in real life."
            ),
            "students": (
                "Students listen, recall prior knowledge, and respond verbally to warm-up questions."
            ),
            "purpose": "Activate background knowledge and emotional readiness."
        },
        {
            "title": "Core Concept Unpacking (15 min)",
            "teacher": (
                "Teacher explains each core idea step-by-step using simple language. "
                "Teacher pauses after every major idea and checks understanding. "
                "If a diagram is required, teacher draws it clearly on the board and labels it."
            ),
            "students": (
                "Students observe, ask clarification questions, and copy diagrams where required."
            ),
            "purpose": "Build accurate conceptual understanding."
        },
        {
            "title": "Guided Thinking & Reasoning (10 min)",
            "teacher": (
                "Teacher asks probing ‘why’ and ‘how’ questions. "
                "Teacher encourages multiple answers and models correct reasoning aloud."
            ),
            "students": (
                "Students explain ideas in their own words and justify their thinking."
            ),
            "purpose": "Develop reasoning and articulation."
        },
        {
            "title": "Application & Real-Life Link (10 min)",
            "teacher": (
                "Teacher presents a real-life situation related to the concept and explains how the concept applies. "
                "Teacher explicitly connects textbook learning to everyday observations."
            ),
            "students": (
                "Students share examples from daily life and discuss in pairs."
            ),
            "purpose": "Transfer learning beyond the classroom."
        },
        {
            "title": "Check for Understanding & Closure (5 min)",
            "teacher": (
                "Teacher summarizes key points, corrects misconceptions, and clearly states what students learned today."
            ),
            "students": (
                "Students verbally summarize learning and ask final questions."
            ),
            "purpose": "Consolidate learning and ensure clarity."
        }
    ]

    return {
        "meta": {
            "grade": grade,
            "subject": subject,
            "chapter": chapter,
            "day": day,
            "total_days": total_days
        },
        "sections": sections
    }
