# preprimary_engine.py
# ERPACAD – Pre-Primary Readiness Engine
# Philosophy: One continuous teaching performance that guarantees child readiness

def generate_preprimary_lesson(class_name, subject, focus):
    """
    Returns ONE complete readiness experience as a single script.
    No steps, no phases, no dynamic structure.
    """

    title = f"{class_name} {subject} – Readiness Experience"
    duration = "Flexible (ends when readiness is observed, not by clock)"

    # ---------------- LKG LITERACY ----------------
    if class_name == "LKG" and subject == "Literacy":
        script = f"""
The teacher waits until all children are seated comfortably. She does not rush silence.
She stands in a position where every child can clearly see her face and mouth.

She smiles gently and speaks in a calm, slow voice:

"Children… today we are going to listen very carefully."

She pauses. She models listening by touching her ear lightly.
She waits until the room naturally settles.

She produces the sound /b/ clearly, exaggerating lip movement.
She does not say the letter name.
She repeats the sound slowly two times: /b/ … /b/.

Some children may say "B".
The teacher does not correct immediately.
She gently says, "Only sound. Not name."

She repeats the sound once more and pauses.

She asks softly, "Where have you heard this sound?"
She listens patiently to all responses.
If a child says an unrelated word, she does not say wrong.
She simply repeats the sound again and contrasts it gently.

Only after sound familiarity is visible does the teacher draw a simple ball on the board.
She points and says slowly, "Ball… /b/."

She removes the drawing from focus and places two pictures:
one of a ball and one of an apple.

She says nothing for a few seconds.
She then produces the sound /b/ once and waits.

Children begin to point.
The teacher observes silently.

She then calls one child at a time.
She places three pictures.
She produces one sound and waits without helping.

If the child responds correctly, she nods gently.
If the child hesitates, she repeats the sound once and gives time.
No child is rushed or corrected harshly.

The lesson ends quietly.
The teacher says, "Your ears worked very hard today."
She smiles and allows children to relax.

By the end of this experience, the child can independently hear a beginning sound
and identify a matching object without prompting.
"""

    # ---------------- LKG NUMERACY ----------------
    elif class_name == "LKG" and subject == "Numeracy":
        script = f"""
The teacher ensures children are seated comfortably with hands free.
She places a small bowl of counters in front of her.

She does not speak immediately.
She picks up one counter and places it slowly on the table.

She says softly, "One."

She pauses.
She places another counter beside it.

She says, "One… two."

She does not ask children to repeat yet.

She then gives three counters to a child and says,
"Place them like I did."

She watches silently.

If the child places two or four, the teacher does not correct verbally.
She models again beside the child.

She gradually steps back and allows children to try independently.

She then mixes counters and asks individual children to give "two" or "three".
She waits patiently for independent response.

The lesson ends when children can give the correct quantity
without copying others.

By the end of this experience, the child demonstrates
one-to-one correspondence and basic number sense independently.
"""

    # ---------------- NURSERY LITERACY ----------------
    elif class_name == "NURSERY" and subject == "Literacy":
        script = f"""
The teacher sits at the children's eye level.
She uses facial expressions rather than words initially.

She produces a familiar sound slowly.
She repeats it with rhythm.

She encourages children to listen and feel the sound.
She does not demand repetition.

She uses objects and gestures to anchor sound recognition.

The experience ends when children show recognition through pointing,
smiling, or vocal attempts.

Readiness is observed through engagement, not verbal accuracy.
"""

    # ---------------- UKG LITERACY ----------------
    elif class_name == "UKG" and subject == "Literacy":
        script = f"""
The teacher begins by reading a short sentence aloud with expression.
She asks, "What did you hear first?"

She allows children to answer freely.
She introduces sound-symbol connection gently.

She draws the letter and traces it while speaking the sound.
Children attempt independently on air or slate.

The lesson ends when children can connect sound to symbol
without teacher cues.
"""

    else:
        script = """
This readiness experience is under preparation.
The teacher focuses on calm engagement, observation,
and independent child response.
"""

    return {
        "title": title,
        "duration": duration,
        "script": script.strip()
    }
