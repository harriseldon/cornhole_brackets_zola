import os

MATCHES_DIR = os.path.join("content", "brackets")

# Define the 10 Byes in a standard 32-slot single-elimination bracket
BYE_MATCHES = [
    {"match_id": "r1-m03", "next_match": "r2-m02", "team_a": "ill_take_3", "weight": 1030},
    {"match_id": "r1-m04", "next_match": "r2-m04", "team_a": "merch_mavericks", "weight": 1040},
    {"match_id": "r1-m05", "next_match": "r2-m05", "team_a": "diamon_status_bronze_skills", "weight": 1050},
    {"match_id": "r1-m06", "next_match": "r2-m06", "team_a": "corn_stars", "weight": 1060},
    {"match_id": "r1-m07", "next_match": "r2-m07", "team_a": "the_cloud_conspirators", "weight": 1070},
    {"match_id": "r1-m08", "next_match": "r2-m08", "team_a": "silk_and_destroy", "weight": 1080},
    {"match_id": "r1-m09", "next_match": "r2-m01", "team_a": "bbq_boys", "weight": 1090},
    {"match_id": "r1-m10", "next_match": "r2-m02", "team_a": "scrum_bags", "weight": 1100},
    {"match_id": "r1-m11", "next_match": "r2-m03", "team_a": "immortal_eas", "weight": 1110},
    {"match_id": "r1-m12", "next_match": "r2-m04", "team_a": "hole_in_one", "weight": 1120},
]

def create_bye_files():
    os.makedirs(MATCHES_DIR, exist_ok=True)
    count = 0
    for match in BYE_MATCHES:
        file_path = os.path.join(MATCHES_DIR, f"{match['match_id']}.md")
        
        # Avoid overwriting existing played matches
        if os.path.exists(file_path):
            print(f"Skipping existing file: {file_path}")
            continue

        front_matter = f"""+++
title = "Round 1 - Match {match['match_id'][-2:]}"
template = "page.html"
weight = {match['weight']}

[extra]
round = 1
match_id = "{match['match_id']}"
next_match = "{match['next_match']}"
station = ""
status = "bye"

[extra.team_a]
id = "{match['team_a']}"
score = "0"
is_winner = true

[extra.team_b]
id = "bye"
score = "0"
is_winner = false
+++
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(front_matter)
        print(f"✓ Created Bye match: {file_path}")
        count += 1

    print(f"\nGenerated {count} Bye match files!")

if __name__ == "__main__":
    create_bye_files()
