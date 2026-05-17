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
OPENING_DEPTH_MOVES = 3  # Looks at the first 3 full moves of the game

with open(FILENAME, 'r', encoding='utf-8') as f:
    content = f.read()

# Split into individual games
games = content.split('\n\n[Event')
white_sequences = []
black_sequences = []

for i, game in enumerate(games):
    if i > 0:
        game = '[Event' + game
        
    white_match = re.search(r'\[White "(.*?)"\]', game)
    black_match = re.search(r'\[Black "(.*?)"\]', game)
    
    if not (white_match and black_match):
        continue
        
    white_player = white_match.group(1)
    black_player = black_match.group(1)
    
    your_color = "Unknown"
    if white_player == MY_USERNAME:
        your_color = "White"
    elif black_player == MY_USERNAME:
        your_color = "Black"
        
    # Isolate the moves line
    move_lines = [line for line in game.split('\n') if line and not line.startswith('[')]
    move_text = " ".join(move_lines).strip()
    move_text = re.sub(r'\s*(1-0|0-1|1/2-1/2)\s*$', '', move_text)
    
    if move_text:
        tokens = move_text.split()
        # Extract the first 3 full moves (3 tokens per move: e.g., "1.", "d4", "d5")
        depth_tokens = tokens[:OPENING_DEPTH_MOVES * 3]
        short_sequence = " ".join(depth_tokens)
        
        if short_sequence:
            if your_color == "White":
                white_sequences.append(short_sequence)
            elif your_color == "Black":
                black_sequences.append(short_sequence)

# Count patterns
white_counts = Counter(white_sequences)
black_counts = Counter(black_sequences)

print(f"Analyzed {len(white_sequences) + len(black_sequences)} standard chess losses from {FILENAME}.\n")
print(f"Showing recurring sequences (filtered out lines with only 1 loss):\n")

print("=== REPEATED LOSING MOVES AS WHITE ===")
white_found = False
for pattern, count in white_counts.most_common():
    if count > 1:  # Only show patterns with MORE than 1 loss
        print(f"Losses: {count}x | Moves: {pattern}...")
        white_found = True
if not white_found:
    print("No repeated losing patterns found as White (all sequences were unique 1x losses).")

print("\n=== REPEATED LOSING MOVES AS BLACK ===")
black_found = False
for pattern, count in black_counts.most_common():
    if count > 1:  # Only show patterns with MORE than 1 loss
        print(f"Losses: {count}x | Moves: {pattern}...")
        black_found = True
if not black_found:
    print("No repeated losing patterns found as Black (all sequences were unique 1x losses).")
