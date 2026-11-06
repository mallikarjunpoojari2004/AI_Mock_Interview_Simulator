from modules.answer_evaluator import evaluate_answer

question = "What is HashMap in Java?"

candidate_answer = """
HashMap is a collection in Java that stores data
in key-value pairs. Keys are unique, and values
can be duplicated. It uses hashing to store data.
"""

result = evaluate_answer(
    question,
    candidate_answer,
    "Java Developer"
)

print("\nAI Answer Evaluation:")
print(result)