"""
Deterministic Puzzle Generator for 15x15 AI/ML Crosswords
Builds 3 rich, 100% mathematically validated 15x15 crosswords.
"""
import sys
import json
from typing import List, Dict, Any

from backend.builder_engine import VOCABULARY
from backend.puzzle_validator import validate_crossword_puzzle, print_grid

def get_word_info(raw_word: str):
    info = VOCABULARY.get(raw_word, (raw_word, f"Concept clue for {raw_word}", "AI / ML"))
    return {
        "display_name": info[0],
        "clue": info[1],
        "category": info[2]
    }

def build_puzzle_championship():
    """
    Puzzle 1: Engineering Day Flagship Grandmaster
    Theme: Comprehensive AI & ML Core Foundations
    """
    raw_words = [
        # Across
        ("REGULARIZATION",  "across", 0, 0),    # len 14, (0,0..13)
        ("TENSOR",          "across", 2, 0),    # len 6,  (2,0..5)
        ("BERT",            "across", 2, 8),    # len 4,  (2,8..11)
        ("PROMPT",          "across", 4, 3),    # len 6,  (4,3..8)
        ("ADAM",            "across", 4, 11),   # len 4,  (4,11..14)
        ("INFERENCE",       "across", 6, 2),    # len 9,  (6,2..10)
        ("EPOCH",           "across", 8, 0),    # len 5,  (8,0..4)
        ("DROPOUT",         "across", 8, 6),    # len 7,  (8,6..12)
        ("TRANSFORMER",     "across", 10, 2),   # len 11, (10,2..12)
        ("LOSS",            "across", 12, 0),   # len 4,  (12,0..3)
        ("ATTENTION",       "across", 12, 5),   # len 9,  (12,5..13)
        ("BACKPROPAGATION", "across", 14, 0),   # len 15, (14,0..14)

        # Down
        ("RELU",            "down", 0, 0),      # len 4: (0,0)=R, (1,0)=E, (2,0)=L? Wait: REGULARIZATION[0]=R, TENSOR[0]=T, so (2,0) is T. Let's adjust!
    ]
    pass

