
from database.db_manager import (
    get_candidate_interviews,
    get_interview_details
)


# ==========================================
# 1. RETRIEVE CANDIDATE INTERVIEW HISTORY
# ==========================================

candidate_id = 4

interviews = get_candidate_interviews(candidate_id)

print("\n========== INTERVIEW HISTORY ==========")

if interviews:

    for interview in interviews:

        print("Interview ID:", interview[0])
        print("Job Role:", interview[1])
        print("Difficulty:", interview[2])
        print("Started At:", interview[3])
        print("Completed At:", interview[4])

        print("--------------------------------")


else:

    print("No interviews found!")


# ==========================================
# 2. RETRIEVE INTERVIEW DETAILS
# ==========================================

interview_id = 3

details = get_interview_details(interview_id)

print("\n========== INTERVIEW DETAILS ==========")

if details:

    for question in details:

        print("Question ID:", question[0])
        print("Question:", question[1])
        print("Candidate Answer:", question[2])
        print("Evaluation:", question[3])
        print("Correctness:", question[4])
        print("Relevance:", question[5])
        print("Completeness:", question[6])

        print("--------------------------------")


else:

    print("No question records found!")
