import re
import os
from collections import Counter

# Find the PGN file
pgn_files = [f for f in os.listdir('.') if f.endswith('.pgn')]

if not pgn_files:
    print("Error: No .pgn file found.")
    exit(1)

FILENAME = pgn_files[0]
MY_USERNAME = "MichaelTUhlean"

with open(FILENAME, 'r', encoding='utf-8') as f:
    content = f.read()

# Split into individual games
games = content.split('\n\n[Event')
white_openings = []
black_openings = []

for i, game in enumerate(games):
    if i > 0:
        game = '[Event' + game
        
    # Extract White and Black players
    white_match = re.search(r'\[White "(.*?)"\]', game)
    black_match = re.search(r'\[Black "(.*?)"\]', game)
    
    if not (white_match and black_match):
        continue
        
    white_player = white_match.group(1)
    black_player = black_match.group(1)
    
    # Determine your color
    your_color = "Unknown"
    if white_player == MY_USERNAME:
        your_color = "White"
    elif black_player == MY_USERNAME:
        your_color = "Black"
        
    # Extract the Opening Name and ECO Code from the PGN tags
    opening_match = re.search(r'\[Opening "(.*?)"\]', game)
    eco_match = re.search(r'\[ECO "(.*?)"\]', game)
    
    opening_name = opening_match.group(1) if opening_match else "Unknown Opening"
    eco_code = eco_match.group(1) if eco_match else ""
    
    # Create a clean label (e.g., "B01 Scandinavian Defense")
    full_opening_label = f"{eco_code} {opening_name}".strip()
    
    if your_color == "White":
        white_openings.append(full_opening_label)
    elif your_color == "Black":
        black_openings.append(full_opening_label)

# Count the frequency of each opening disaster
white_counts = Counter(white_openings)
black_counts = Counter(black_openings)

print(f"Analyzed {len(white_openings) + len(black_openings)} standard chess losses from {FILENAME}.\n")

print("=== TOP OPENINGS WHERE YOU LOSE AS WHITE ===")
if white_counts:
    for opening, count in white_counts.most_common(10):
        print(f"Losses: {count}x | {opening}")
else:
    print("No games found playing as White.")

print("\n=== TOP OPENINGS WHERE YOU LOSE AS BLACK ===")
if black_counts:
    for opening, count in black_counts.most_common(10):
        print(f"Losses: {count}x | {opening}")
else:
    print("No games found playing as Black.")
