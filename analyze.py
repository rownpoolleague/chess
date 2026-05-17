import re
import os
from collections import Counter

# Look for any .pgn file in the directory
pgn_files = [f for f in os.listdir('.') if f.endswith('.pgn')]

if not pgn_files:
    print("Error: No .pgn file found in this folder. Please upload your file.")
    exit(1)

FILENAME = pgn_files[0]
OPENING_DEPTH_MOVES = 5  

with open(FILENAME, 'r', encoding='utf-8') as f:
    content = f.read()

games = content.split('\n\n[Event')
opening_sequences = []

for i, game in enumerate(games):
    if i > 0:
        game = '[Event' + game
        
    move_lines = [line for line in game.split('\n') if line and not line.startswith('[')]
    move_text = " ".join(move_lines).strip()
    move_text = re.sub(r'\s*(1-0|0-1|1/2-1/2)\s*$', '', move_text)
    
    if move_text:
        tokens = move_text.split()
        depth_tokens = tokens[:OPENING_DEPTH_MOVES * 3]
        short_sequence = " ".join(depth_tokens)
        
        if short_sequence:
            opening_sequences.append(short_sequence)
        
pattern_counts = Counter(opening_sequences)

print(f"Analyzed {len(opening_sequences)} total losses from {FILENAME}.\n")
print(f"--- TOP REPEATED LOSING MOVE PATTERNS (First {OPENING_DEPTH_MOVES} Moves) ---")

for pattern, count in pattern_counts.most_common(10):
    print(f"Losses: {count}x | {pattern}...")
