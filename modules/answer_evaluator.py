
from services.gemini_service import generate_response


def evaluate_answer(question, candidate_answer, role):
    """
    Evaluate the candidate's answer using Gemini AI.
    """

    prompt = f"""
    Act as an experienced technical interviewer.

    Evaluate the following candidate answer.

    Job Role: {role}

    Interview Question:
    {question}

    Candidate Answer:
    {candidate_answer}

    Evaluate the answer based on these criteria:

    1. Correctness: Is the answer technically correct?
    2. Relevance: Does it address the question?
    3. Completeness: Does it cover important concepts?

    Provide your evaluation in the following format:

    Correctness Score: X/10
    Relevance Score: X/10
    Completeness Score: X/10

    Strengths:
    - Mention what the candidate explained correctly.

    Missing Concepts:
    - Mention important concepts the candidate missed.

    Feedback:
    - Give suggestions for improvement.

    Improved Answer:
    - Provide a technically correct interview-quality answer.

    Be fair, constructive and specific.
    """

    evaluation = generate_response(prompt)

    return evaluation
