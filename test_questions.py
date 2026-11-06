from modules.question_generator import generate_questions

questions = generate_questions(
    role="Java Developer",
    difficulty="Intermediate",
    number_of_questions=5
)

print("\nGenerated Interview Questions:")
print(questions)
