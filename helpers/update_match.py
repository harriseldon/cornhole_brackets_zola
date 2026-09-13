#!/usr/bin/env python3
import sys
import os
import re
import argparse

BRACKETS_DIR = os.path.join("content", "brackets")

def parse_toml_front_matter(content):
    pattern = r"^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n(.*)$"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return None, content
    return match.group(1), match.group(2)

def read_match_file(match_id):
    filepath = os.path.join(BRACKETS_DIR, f"{match_id.lower()}.md")
    if not os.path.exists(filepath):
        print(f"❌ Match file not found: {filepath}")
        return None, None
    with open(filepath, "r", encoding="utf-8") as f:
        return filepath, f.read()

def update_match_data(match_id, score_a=None, score_b=None, winner=None, station=None, note=None):
    filepath, content = read_match_file(match_id)
    if not content:
        return None

    front_matter, body = parse_toml_front_matter(content)
    
    # Update scores & winner flag
    is_a_winner = (winner != None and winner.lower() == "a")
    is_b_winner = (winner != None and winner.lower() == "b")

    if score_a != None:
        front_matter = re.sub(r'score\s*=\s*".*?"', f'score = "{score_a}"', front_matter, count=1)

    # Target second score instance for team_b
    parts = front_matter.split("[extra.team_b]")
    if len(parts) == 2 and score_b != None:
        parts[1] = re.sub(r'score\s*=\s*".*?"', f'score = "{score_b}"', parts[1], count=1)
        front_matter = "[extra.team_b]".join(parts)

    front_matter = re.sub(r'is_winner\s*=\s*(true|false)', f'is_winner = {"true" if is_a_winner else "false"}', front_matter, count=1)
    parts = front_matter.split("[extra.team_b]")
    if len(parts) == 2:
        parts[1] = re.sub(r'is_winner\s*=\s*(true|false)', f'is_winner = {"true" if is_b_winner else "false"}', parts[1], count=1)
        front_matter = "[extra.team_b]".join(parts)

    # Set status
    # If no winnder, than just update the status it in_progress otherwise completed
    if is_a_winner or is_b_winner:
        front_matter = re.sub(r'status\s*=\s*".*?"', 'status = "completed"', front_matter)
    else:
        front_matter = re.sub(r'status\s*=\s*".*?"', 'status = "in_progress"', front_matter)

    # Update Station Location if provided
    if station:
        front_matter = re.sub(r'station\s*=\s*".*?"', f'station = "{station}"', front_matter)

    # Append summary note to markdown content body
    summary_text = note if note else f"Match {match_id.upper()} {'completed' if is_a_winner or is_b_winner else 'updated'}: Team A ({score_a}) vs Team B ({score_b})."
    new_body = f"\n\n### Match Summary\n> {summary_text}\n"

    # Save updated match file
    new_content = f"+++\n{front_matter.strip()}\n+++\n{new_body}"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✓ Match {match_id.upper()} updated successfully.")

    # Extract team ID of the winner for advancement
    if is_a_winner or is_b_winner:
        winner_team_id_match = re.search(r'\[extra\.team_' + winner.lower() + r'\]\s*\nid\s*=\s*"(.*?)"', front_matter)
        winner_team_id = winner_team_id_match.group(1) if winner_team_id_match else None

        # Advance winner to Next Match if designated
        next_match_search = re.search(r'next_match\s*=\s*"(.*?)"', front_matter)
        if next_match_search and next_match_search.group(1):
            next_match_id = next_match_search.group(1)
            advance_winner(match_id, next_match_id, winner_team_id)

    return summary_text

def advance_winner(current_match_id, next_match_id, winner_team_id):
    filepath, content = read_match_file(next_match_id)
    if not content or not winner_team_id:
        return

    front_matter, body = parse_toml_front_matter(content)
    
    # Determine slotting (Odd match number -> team_a, Even match number -> team_b)
    m_num = int(re.search(r'm(\d+)', current_match_id.lower()).group(1))
    target_slot = "team_a" if (m_num % 2 != 0) else "team_b"

    parts = front_matter.split(f"[extra.{target_slot}]")
    if len(parts) == 2:
        parts[1] = re.sub(r'id\s*=\s*".*?"', f'id = "{winner_team_id}"', parts[1], count=1)
        front_matter = f"[extra.{target_slot}]".join(parts)

    new_content = f"+++\n{front_matter.strip()}\n+++\n{body}"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✓ Winner ({winner_team_id}) advanced to {next_match_id.upper()} ({target_slot}).")

if __name__ == "__main__":
    print("Brackets Directory is: " + BRACKETS_DIR)
    
    parser = argparse.ArgumentParser(description="Update tournament match state.")
    parser.add_argument("--match", required=True, help="Match ID (e.g. r1-m01)")
    parser.add_argument("--score-a", required=False, help="Team A score")
    parser.add_argument("--score-b", required=False, help="Team B score")
    parser.add_argument("--winner", required=False, choices=["a", "b"], help="Winner designation (a or b)")
    parser.add_argument("--station", help="Station/Court ID (e.g. the_barnyard)")
    parser.add_argument("--note", help="Match summary note")

    args = parser.parse_args()
    update_match_data(args.match, args.score_a, args.score_b, args.winner, args.station, args.note)
