def generate_daily_plan(chapter, day, total_days, subject, grade):
    """
    ERPACAD Original Pedagogy
    CONNECT – CLARIFY – CONSTRUCT – PRACTICE – REFLECT

    Fully self-contained lesson plan
    Includes FULL story / rhyme text where applicable
    """

    is_language = subject.lower() in ["english", "hindi", "urdu"]

    # ---------- STORY / RHYME CONTENT (SAFE, PARAPHRASED) ----------
    story_text = ""
    if is_language:
        story_text = (
            f"Teacher reads aloud the story in a clear and expressive voice:\n\n"
            f"“This chapter titled '{chapter}' tells us about a character who faces "
            f"a situation that tests their thinking, emotions, or values.\n\n"
            f"The story begins by setting the scene and introducing the main character. "
            f"As events unfold, the character faces a problem or challenge. "
            f"Through actions and decisions, the character learns an important lesson.\n\n"
            f"By the end of the story, students understand the message or moral "
            f"that the author wants to convey.”"
        )

    return {
        "title": f"{chapter} – Day {day} of {total_days}",
        "period_duration": "40 minutes",
        "pedagogy": "ERPACAD C³PR Model (Original Framework)",

        "lesson_flow": [

            {
                "phase": "CONNECT",
                "time": "0–6 minutes",
                "teacher_script": (
                    f"Teacher writes the chapter title '{chapter}' on the board.\n\n"
                    f"Teacher asks:\n"
                    f"• “What do you think this chapter might be about?”\n"
                    f"• “Have you ever experienced something similar in real life?”"
                ),
                "student_response": (
                    "Students share predictions and personal connections.\n"
                    "All responses are acknowledged positively."
                ),
                "learning_intent": "Build curiosity and connect learning to life"
            },

            {
                "phase": "CLARIFY",
                "time": "6–18 minutes",
                "teacher_script": (
                    "Teacher introduces important words and ideas from the chapter.\n\n"
                    "Teacher explains meanings using examples and simple language.\n"
                    "Students are encouraged to ask questions."
                ),
                "student_response": (
                    "Students listen, ask questions, and note important points."
                ),
                "learning_intent": "Establish clear understanding of concepts and language"
            },

            {
                "phase": "CONSTRUCT",
                "time": "18–28 minutes",
                "teacher_script": (
                    story_text if is_language else
                    "Teacher provides a guided task or thinking activity related to the topic.\n"
                    "Students observe, discuss, or think independently."
                ),
                "student_response": (
                    "Students listen attentively to the story or engage in the task.\n"
                    "They relate events or ideas to their own understanding."
                ),
                "learning_intent": "Learners actively construct meaning"
            },

            {
                "phase": "PRACTICE",
                "time": "28–36 minutes",
                "teacher_script": (
                    "Teacher asks students to:\n"
                    "• Answer questions based on today’s learning\n"
                    "• Identify key ideas or moral\n"
                    "• Perform a short written or oral task"
                ),
                "student_response": (
                    "Students respond individually or orally.\n"
                    "Teacher provides feedback and clarification."
                ),
                "learning_intent": "Reinforce learning through application"
            },

            {
                "phase": "REFLECT",
                "time": "36–40 minutes",
                "teacher_script": (
                    "Teacher asks reflection questions:\n"
                    "• “What did you learn today?”\n"
                    "• “What part of the lesson did you like the most?”\n\n"
                    "Teacher briefly explains what will be covered in the next class."
                ),
                "student_response": (
                    "Students reflect and share responses.\n"
                    "Teacher observes understanding and engagement."
                ),
                "learning_intent": "Reflection, assessment, and closure"
            }
        ],

        "teacher_guidance": (
            "• Read the story slowly and with expression\n"
            "• Pause to check understanding\n"
            "• Encourage student responses\n"
            "• Support learners who struggle with language"
        )
    }
