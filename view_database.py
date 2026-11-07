
import sqlite3

from database.db_manager import DATABASE_PATH


connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()


# Display candidate records
print("\n========== CANDIDATES ==========")

cursor.execute("SELECT * FROM candidates")

for row in cursor.fetchall():
    print(row)


# Display interview records
print("\n========== INTERVIEWS ==========")

cursor.execute("SELECT * FROM interviews")

for row in cursor.fetchall():
    print(row)


# Display questions and evaluation records
print("\n========== INTERVIEW QUESTIONS ==========")

cursor.execute("""
    SELECT
        question_id,
        interview_id,
        question_text,
        candidate_answer,
        evaluation,
        correctness_score,
        relevance_score,
        completeness_score
    FROM interview_questions
""")

for row in cursor.fetchall():
    print(row)


connection.close()
