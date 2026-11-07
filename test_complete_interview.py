
from database.db_manager import (
    complete_interview,
    get_candidate_interviews
)

# Complete interview ID 3
result = complete_interview(3)

if result:

    print("Interview completed successfully!")

else:

    print("Interview not found!")


# Verify updated interview
interviews = get_candidate_interviews(4)

print("\n========== UPDATED INTERVIEW ==========")

for interview in interviews:

    print("Interview ID:", interview[0])
    print("Job Role:", interview[1])
    print("Difficulty:", interview[2])
    print("Started At:", interview[3])
    print("Completed At:", interview[4])
