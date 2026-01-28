def generate_daily_plan(chapter, day, total_days, subject, grade):

    return {
        "title": f"{chapter} – Day {day} of {total_days}",
        "steps": [
            ("Engage", "5 min",
             "Begin with a question or real-life connection.",
             "Students respond orally."),
            ("Concept Build", "15 min",
             "Explain core concept using board and examples.",
             "Students listen and note key ideas."),
            ("Guided Practice", "10 min",
             "Conduct activity or worksheet discussion.",
             "Students work individually or in pairs."),
            ("Assessment", "5 min",
             "Ask oral or written questions.",
             "Students answer."),
            ("Closure", "5 min",
             "Summarize and link to next lesson.",
             "Students reflect.")
        ]
    }
