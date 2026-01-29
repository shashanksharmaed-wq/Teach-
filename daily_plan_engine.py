def generate_daily_plan(grade, subject, chapter, day, total_days):

    lesson = {
        "meta": {
            "grade": grade,
            "subject": subject,
            "chapter": chapter,
            "day": day,
            "total_days": total_days,
            "duration": "45 minutes"
        },

        "flow": [
            {
                "phase": "ANCHOR (5 minutes)",
                "teacher_says": (
                    "Today we will explore a story where a man writes a letter — "
                    "not to a person, but to God. Before we begin, tell me: "
                    "When you are in trouble, whom do you trust the most and why?"
                ),
                "students_do": (
                    "Students share short personal responses. "
                    "Teacher listens without judging and acknowledges emotions."
                ),
                "purpose": "Emotionally anchor students to the theme of faith and trust."
            },

            {
                "phase": "EXPOSE – TEXT IMMERSION (10 minutes)",
                "teacher_says": (
                    "Teacher reads the story aloud with pauses:\n\n"
                    "“Lencho was a poor farmer who lived in a small house on the crest of a low hill. "
                    "From his fields, he could see the river and the ripe cornfields dotted with flowers "
                    "that always promised a good harvest…”\n\n"
                    "Teacher uses voice modulation and pauses after key lines."
                ),
                "students_do": (
                    "Students listen silently, follow the text, and imagine the scene."
                ),
                "purpose": "Immerse learners in authentic literary language."
            },

            {
                "phase": "UNPACK – WORDS & IDEAS (10 minutes)",
                "teacher_says": (
                    "Let us understand some important words:\n\n"
                    "• Faith – strong belief without proof\n"
                    "• Hailstorm – sudden storm with ice stones\n"
                    "• Charity – helping others willingly\n\n"
                    "Teacher uses examples from daily life."
                ),
                "students_do": (
                    "Students write meanings, use words in sentences, "
                    "and ask doubts."
                ),
                "purpose": "Build vocabulary and conceptual clarity."
            },

            {
                "phase": "THINK – REASONING (8 minutes)",
                "teacher_says": (
                    "Why did Lencho write to God instead of villagers?\n"
                    "Was Lencho right to be angry later?\n"
                    "What does this story say about humans and faith?"
                ),
                "students_do": (
                    "Students think, respond, agree/disagree respectfully."
                ),
                "purpose": "Develop critical thinking and moral reasoning."
            },

            {
                "phase": "TRANSFER – LIFE LINK (7 minutes)",
                "teacher_says": (
                    "Think of a time when belief helped someone act bravely. "
                    "It could be real or imagined."
                ),
                "students_do": (
                    "Students share experiences or short stories."
                ),
                "purpose": "Apply learning beyond the classroom."
            },

            {
                "phase": "CLOSE – RETENTION (5 minutes)",
                "teacher_says": (
                    "Today we learned that faith can give strength, "
                    "but humans must also support one another."
                ),
                "students_do": (
                    "Students summarize the lesson in one sentence."
                ),
                "purpose": "Consolidate understanding."
            }
        ]
    }

    return lesson
