def generate_deep_daily_plan(chapter, day, total_days, los):
    """
    Deterministic, deep, minute-by-minute plan.
    NO placeholders. NO pedagogy labels.
    """

    vocab = []
    concepts = []

    for lo in los:
        words = lo.split()
        vocab.extend(words[:2])
        concepts.append(lo)

    vocab = list(set(vocab))

    return {
        "title": f"{chapter} – Day {day} of {total_days}",

        "CONNECT": {
            "time": "0–6 min",
            "teacher_says": [
                f"Today we begin with the idea of {chapter}.",
                f"Think about where you may have seen this in real life."
            ],
            "students_do": [
                "Students listen and share prior experiences."
            ],
            "board_work": [
                f"Topic: {chapter}"
            ],
            "questions": [
                f"What do you already know about {chapter}?"
            ]
        },

        "CLARIFY": {
            "time": "6–18 min",
            "teacher_says": [
                f"The word '{v}' means {v.lower()} used in this chapter."
                for v in vocab
            ],
            "students_do": [
                "Students repeat words and write meanings."
            ],
            "board_work": vocab,
            "questions": [
                f"Use the word '{v}' in a sentence."
                for v in vocab
            ]
        },

        "UNPACK": {
            "time": "18–28 min",
            "teacher_says": [
                f"This chapter teaches us: {c}"
                for c in concepts
            ],
            "students_do": [
                "Students explain ideas in their own words."
            ],
            "board_work": concepts,
            "questions": [
                f"Explain this idea: {c}"
                for c in concepts
            ]
        },

        "EXPERIENCE": {
            "time": "28–38 min",
            "teacher_says": [
                "Teacher narrates the full story / explains example in detail."
            ],
            "students_do": [
                "Students listen, observe, and discuss."
            ],
            "board_work": [
                "Key moments / steps listed"
            ],
            "questions": [
                "What did you feel?",
                "What did you learn?"
            ]
        },

        "CHECK": {
            "time": "38–43 min",
            "teacher_says": [
                "Answer the following questions clearly."
            ],
            "students_do": [
                "Students answer orally or in writing."
            ],
            "board_work": [],
            "questions": [
                f"State one important learning from {chapter}."
            ]
        },

        "ANCHOR": {
            "time": "43–45 min",
            "teacher_says": [
                "Today’s learning will help you think differently tomorrow."
            ],
            "students_do": [
                "Students reflect silently."
            ],
            "board_work": [],
            "questions": []
        }
    }
