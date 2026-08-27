"""
Automated 15x15 Crossword Builder and Validator for AI/ML Concepts
"""
import json
from typing import List, Dict, Tuple, Optional
from backend.puzzle_validator import validate_crossword_puzzle, print_grid

# Let's define verified, handcrafted 15x15 puzzles with perfect intersections

# PUZZLE 1: Engineering Day Grand Grandmaster (15x15)
# Let's verify character by character:
# Across 0: BACKPROPAGATION (len 15, row 0, col 0)
#   Indices: 0:B, 1:A, 2:C, 3:K, 4:P, 5:R, 6:O, 7:P, 8:A, 9:G, 10:A, 11:T, 12:I, 13:O, 14:N
# Down at (0, 0): B I A S (len 4) -> (0,0)=B, (1,0)=I, (2,0)=A, (3,0)=S
# Down at (0, 4): P E R C E P T R O N (len 10) -> (0,4)=P, (1,4)=E, (2,4)=R, (3,4)=C, (4,4)=E, (5,4)=P, (6,4)=T, (7,4)=R, (8,4)=O, (9,4)=N
# Down at (0, 9): G R A D I E N T (len 8) -> (0,9)=G, (1,9)=R, (2,9)=A, (3,9)=D, (4,9)=I, (5,9)=E, (6,9)=N, (7,9)=T
# Down at (0, 14): N O R M A L I Z A T I O N (len 13) -> (0,14)=N, (1,14)=O, (2,14)=R, (3,14)=M, (4,14)=A, (5,14)=L, (6,14)=I, (7,14)=Z, (8,14)=A, (9,14)=T, (10,14)=I, (11,14)=O, (12,14)=N
# Across 2: A D A M (len 4, row 2, col 7) -> (2,7)=A, (2,8)=D, (2,9)=A (matches (0,9)[2]=A!), (2,10)=M
# Across 3: S C H E D U L E R -> let's check: (3,0)=S, (3,4)=C (matches PERCEPTRON[3]=C!), (3,9)=D (matches GRADIENT[3]=D!)
#   Wait, S _ _ _ C _ _ _ _ D _ _ _ M _
#   Word of len 10 at (3,0) containing S...C...D:
#   Let's check if STOCHASTIC fits: S T O C H A S T I C (len 10). (3,0)=S, (3,3)=C? At (3,4)=H, but PERCEPTRON[3]=C.
#   Let's use a Python solver to find exact word combinations from our AI/ML lexicon!

