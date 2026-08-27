"""
Backtracking Crossword Generator & Solver
Generates 15x15 crossword grids from AI/ML dictionary with guaranteed valid intersections.
"""
import random
from typing import List, Dict, Tuple, Optional
from backend.generate_puzzles import WORDS_DB
from backend.puzzle_validator import validate_crossword_puzzle, print_grid

def solve_crossword():
    # List of available terms
    word_list = list(WORDS_DB.keys())
    
    # We want a 15x15 grid with 12 to 18 interconnected words
    # Let's define grid templates (slots for across and down) and solve matching words
    # Slot: (id, direction, row, col, length)
    
    templates = [
        # Template 1: Balanced symmetrical 15x15 grid
        {
            "name": "Championship 15x15",
            "slots": [
                # Across
                ("a1", "across", 0, 0, 7),   # len 7
                ("a2", "across", 0, 8, 7),   # len 7
                ("a3", "across", 2, 0, 11),  # len 11
                ("a4", "across", 4, 3, 9),   # len 9
                ("a5", "across", 6, 0, 6),   # len 6
                ("a6", "across", 6, 8, 7),   # len 7
                ("a7", "across", 8, 0, 7),   # len 7
                ("a8", "across", 8, 9, 6),   # len 6
                ("a9", "across", 10, 3, 9),  # len 9
                ("a10", "across", 12, 4, 11),# len 11
                ("a11", "across", 14, 0, 7), # len 7
                ("a12", "across", 14, 8, 7), # len 7
                # Down
                ("d1", "down", 0, 0, 7),     # len 7
                ("d2", "down", 0, 4, 11),    # len 11
                ("d3", "down", 0, 10, 11),   # len 11
                ("d4", "down", 0, 14, 7),    # len 7
                ("d5", "down", 4, 6, 7),     # len 7
                ("d6", "down", 4, 8, 7),     # len 7
                ("d7", "down", 8, 0, 7),     # len 7
                ("d8", "down", 4, 12, 11),   # len 11
                ("d9", "down", 4, 2, 11),    # len 11
                ("d10", "down", 8, 14, 7),   # len 7
            ]
        }
    ]

    # Let's test placing words into slots with constraint matching
    # Map words by length
    by_len = {}
    for w in word_list:
        by_len.setdefault(len(w), []).append(w)
        
    print("Words available by length:", {k: len(v) for k, v in by_len.items()})

if __name__ == "__main__":
    solve_crossword()
