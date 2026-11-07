
from database.db_manager import get_all_candidates

candidates = get_all_candidates()

print("\n========== ALL CANDIDATES ==========")

for candidate in candidates:

    print("Candidate ID:", candidate[0])
    print("Name:", candidate[1])
    print("Email:", candidate[2])
    print("Registered At:", candidate[3])

    print("-----------------------------")
