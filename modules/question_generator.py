
import re
from services.gemini_service import generate_response


def generate_next_question(
    role,
    difficulty,
    previous_questions=None,
    question_number=1
):
    if previous_questions is None:
        previous_questions = []

    previous_text = "\n".join(
        f"- {question}" for question in previous_questions
    )

    prompt = f"""
    Act as an experienced technical interviewer.

    Generate ONE fresh interview question.

    Job Role: {role}
    Difficulty: {difficulty}
    Question Number: {question_number} out of 5.

    Previously asked questions:
    {previous_text if previous_text else "None"}

    Requirements:
    1. Generate exactly ONE question.
    2. Make it relevant to the selected job role.
    3. Match the selected difficulty.
    4. Do not repeat any previous question.
    5. Do not ask the same concept using different wording.
    6. Explore a different technical topic whenever possible.
    7. Mix conceptual, practical, scenario-based and coding questions.
    8. For coding questions, clearly state the programming task.
    9. Do not provide the answer or explanation.
    10. Do not include an introduction or conclusion.
    11. Return only the question, without numbering.

    Generate a different question from the previous ones.
    """

    response = generate_response(prompt)

    if (
        not response
        or response.startswith("Gemini API Error:")
        or response.startswith("Gemini is temporarily unavailable")
    ):
        return None

    lines = [
        line.strip()
        for line in response.splitlines()
        if line.strip()
    ]

    if not lines:
        return None

    question = lines[0]

    question = re.sub(
        r"^(question\s*)?\d+[\.\):\-]\s*",
        "",
        question,
        flags=re.IGNORECASE
    )

    question = question.strip().strip('"').strip("'")

    if not question or question.lower() in {
        q.lower().strip() for q in previous_questions
    }:
        return None

    return question
