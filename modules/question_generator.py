
from services.gemini_service import generate_response


def generate_questions(role, difficulty, number_of_questions=5):
    """
    Generate interview questions based on job role and difficulty.
    """

    prompt = f"""
    Act as an experienced technical interviewer.

    Generate {number_of_questions} technical interview questions
    for the following candidate:

    Job Role: {role}
    Difficulty Level: {difficulty}

    Instructions:
    1. Generate only technical interview questions.
    2. Make questions relevant to the selected job role.
    3. Match the selected difficulty level.
    4. Avoid duplicate questions.
    5. Number each question.
    6. Do not provide answers.
    7. Return only the questions.
    """

    response = generate_response(prompt)

    return response
