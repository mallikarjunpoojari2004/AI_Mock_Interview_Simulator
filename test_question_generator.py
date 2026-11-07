
from modules.question_generator import generate_questions

questions = generate_questions(
    role="Java Developer",
    difficulty="Beginner",
    number_of_questions=5
)

print("\nGENERATED INTERVIEW QUESTIONS\n")

for index, question in enumerate(questions, start=1):
    print(f"Question {index}: {question}")

print("\nTotal Questions:", len(questions))
