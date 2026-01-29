def generate_daily_plan(chapter, day, total_days, subject, grade):
    """
    Generates a deeply detailed, structured daily lesson plan.
    Always returns a dictionary with a 'steps' key (no KeyError risk).
    """

    # -------------------------------
    # Time distribution (CBSE-safe)
    # -------------------------------
    steps = [
        {
            "title": "CONNECT",
            "duration": "5 minutes",
            "teacher_says": (
                f"Teacher begins by connecting the topic '{chapter}' to students’ real-life experiences. "
                f"For example, the teacher asks questions related to daily life, observations, or prior knowledge "
                f"appropriate for Class {grade} students."
            ),
            "student_does": (
                "Students respond orally, share experiences, and relate the topic to their own lives."
            ),
            "learning_intent": (
                "Activate prior knowledge and emotionally engage students with the topic."
            )
        },
        {
            "title": "UNPACK",
            "duration": "10 minutes",
            "teacher_says": (
                "Teacher introduces key words, terms, and concepts from the chapter. "
                "Each word is explained using simple language, examples, and sentence usage. "
                "Teacher checks understanding after each explanation."
            ),
            "student_does": (
                "Students listen carefully, repeat new words, ask questions, and note key ideas."
            ),
            "learning_intent": (
                "Build clear conceptual and language understanding."
            )
        },
        {
            "title": "ILLUSTRATE",
            "duration": "10 minutes",
            "teacher_says": (
                "Teacher explains the concept using a detailed example, story, or situation.\n\n"
                "Example narrative:\n"
                "“Lencho was a poor farmer who depended entirely on rain for his crops. "
                "When a storm destroyed his harvest, he wrote a letter to God asking for help…”\n\n"
                "Teacher narrates the full story slowly, pausing to explain emotions, meanings, "
                "and key moments."
            ),
            "student_does": (
                "Students listen attentively, visualize the situation, and answer short oral questions."
            ),
            "learning_intent": (
                "Help students understand the concept through storytelling and concrete examples."
            )
        },
        {
            "title": "PRACTISE",
            "duration": "10 minutes",
            "teacher_says": (
                "Teacher asks guided questions based on the explanation. "
                "Teacher writes sample answers on the board and models correct responses."
            ),
            "student_does": (
                "Students answer questions orally or in notebooks and discuss answers with peers."
            ),
            "learning_intent": (
                "Reinforce learning through guided practice."
            )
        },
        {
            "title": "INTEGRATE",
            "duration": "10 minutes",
            "teacher_says": (
                "Teacher conducts an integration activity.\n\n"
                "Art Integration Example:\n"
                "Students draw a scene from the story and label key elements.\n\n"
                "Play-Based Example:\n"
                "Students role-play characters from the lesson in small groups."
            ),
            "student_does": (
                "Students participate in drawing, role-play, or a simple game-based activity."
            ),
            "learning_intent": (
                "Deepen understanding through creative and experiential learning."
            )
        },
        {
            "title": "CHECKPOINT",
            "duration": "5 minutes",
            "teacher_says": (
                "Teacher asks short assessment questions to check understanding. "
                "Questions are oral and low-stakes."
            ),
            "student_does": (
                "Students answer questions and clarify doubts."
            ),
            "learning_intent": (
                "Assess learning progress informally."
            )
        },
        {
            "title": "CONSOLIDATE",
            "duration": "5 minutes",
            "teacher_says": (
                "Teacher summarizes the lesson, revisits key ideas, and links today’s learning "
                "to the next day’s lesson."
            ),
            "student_does": (
                "Students reflect on what they learned and share one key takeaway."
            ),
            "learning_intent": (
                "Ensure retention and closure."
            )
        }
    ]

    # -------------------------------
    # FINAL STRUCTURE (VERY IMPORTANT)
    # -------------------------------
    return {
        "chapter": chapter,
        "subject": subject,
        "grade": grade,
        "day": day,
        "total_days": total_days,
        "title": f"{chapter} – Day {day} of {total_days}",
        "steps": steps
    }
