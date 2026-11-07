
import sqlite3
from pathlib import Path


# ==========================================
# 1. DATABASE CONFIGURATION
# ==========================================

DATABASE_PATH = Path(__file__).resolve().parent / "interview.db"


# ==========================================
# 2. DATABASE CONNECTION
# ==========================================

def get_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ==========================================
# 3. CREATE DATABASE TABLES
# ==========================================

def initialize_db():

    connection = get_connection()

    cursor = connection.cursor()

    # Candidates Table

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (

            candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # Interviews Table

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interviews (

            interview_id INTEGER PRIMARY KEY AUTOINCREMENT,

            candidate_id INTEGER NOT NULL,

            job_role TEXT NOT NULL,

            difficulty TEXT NOT NULL,

            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            completed_at TIMESTAMP,

            FOREIGN KEY (candidate_id)
            REFERENCES candidates(candidate_id)

        )
    """)

    # Interview Questions Table

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_questions (

            question_id INTEGER PRIMARY KEY AUTOINCREMENT,

            interview_id INTEGER NOT NULL,

            question_text TEXT NOT NULL,

            candidate_answer TEXT,

            evaluation TEXT,

            correctness_score REAL,

            relevance_score REAL,

            completeness_score REAL,

            FOREIGN KEY (interview_id)
            REFERENCES interviews(interview_id)

        )
    """)

    connection.commit()

    connection.close()


# ==========================================
# 4. INSERT CANDIDATE DETAILS
# ==========================================

def add_candidate(name, email=None):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO candidates (name, email)
        VALUES (?, ?)
        """,
        (name, email)
    )

    candidate_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return candidate_id


# ==========================================
# 5. CREATE INTERVIEW SESSION
# ==========================================

def create_interview(candidate_id, job_role, difficulty):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO interviews (
            candidate_id,
            job_role,
            difficulty
        )
        VALUES (?, ?, ?)
        """,
        (candidate_id, job_role, difficulty)
    )

    interview_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return interview_id


# ==========================================
# 6. SAVE INTERVIEW QUESTION AND ANSWER
# ==========================================

def save_question(
    interview_id,
    question_text,
    candidate_answer=None
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO interview_questions (
            interview_id,
            question_text,
            candidate_answer
        )
        VALUES (?, ?, ?)
        """,
        (
            interview_id,
            question_text,
            candidate_answer
        )
    )

    question_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return question_id

# ==========================================
# 7. SAVE AI EVALUATION RESULTS
# ==========================================

def save_evaluation(
    question_id,
    evaluation,
    correctness_score,
    relevance_score,
    completeness_score
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE interview_questions

        SET
            evaluation = ?,
            correctness_score = ?,
            relevance_score = ?,
            completeness_score = ?

        WHERE question_id = ?
        """,
        (
            evaluation,
            correctness_score,
            relevance_score,
            completeness_score,
            question_id
        )
    )

    connection.commit()

    connection.close()


# ==========================================
# 8. GET CANDIDATE INTERVIEW HISTORY
# ==========================================

def get_candidate_interviews(candidate_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            interview_id,
            job_role,
            difficulty,
            started_at,
            completed_at

        FROM interviews

        WHERE candidate_id = ?

        ORDER BY started_at DESC
        """,
        (candidate_id,)
    )

    interviews = cursor.fetchall()

    connection.close()

    return interviews

# ==========================================
# 9. GET INTERVIEW DETAILS
# ==========================================

def get_interview_details(interview_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            question_id,
            question_text,
            candidate_answer,
            evaluation,
            correctness_score,
            relevance_score,
            completeness_score

        FROM interview_questions

        WHERE interview_id = ?

        ORDER BY question_id
        """,
        (interview_id,)
    )

    details = cursor.fetchall()

    connection.close()

    return details


# ==========================================
# 10. GET ALL CANDIDATES
# ==========================================

def get_all_candidates():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            candidate_id,
            name,
            email,
            created_at

        FROM candidates

        ORDER BY candidate_id
        """
    )

    candidates = cursor.fetchall()

    connection.close()

    return candidates


# ==========================================
# 11. COMPLETE INTERVIEW SESSION
# ==========================================

def complete_interview(interview_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE interviews

        SET completed_at = CURRENT_TIMESTAMP

        WHERE interview_id = ?
        """,
        (interview_id,)
    )

    updated_rows = cursor.rowcount

    connection.commit()

    connection.close()

    return updated_rows > 0


def get_recent_questions(job_role, limit=30):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT iq.question_text
        FROM interview_questions iq
        JOIN interviews i
        ON iq.interview_id = i.interview_id
        WHERE LOWER(i.job_role) = LOWER(?)
        ORDER BY i.started_at DESC, iq.question_id DESC
        LIMIT ?
        """,
        (job_role, limit)
    )

    rows = cursor.fetchall()
    connection.close()

    return [row[0] for row in rows]

# ==========================================
# 7. MAIN EXECUTION
# ==========================================

if __name__ == "__main__":

    initialize_db()

    print("Database initialized successfully!")

    print("Database location:", DATABASE_PATH)