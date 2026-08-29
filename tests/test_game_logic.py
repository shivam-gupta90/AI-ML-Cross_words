"""
Unit tests for Game Engine Logic
"""
import pytest
from backend.game_logic import (
    normalize_answer, compute_initial_reveals, calculate_score
)

def test_normalize_answer():
    # Case insensitivity
    assert normalize_answer("gradient descent") == "GRADIENTDESCENT"
    assert normalize_answer("Gradient Descent") == "GRADIENTDESCENT"
    assert normalize_answer("GRADIENT DESCENT") == "GRADIENTDESCENT"
    
    # Hyphens and punctuation
    assert normalize_answer("k-nearest neighbors") == "KNEARESTNEIGHBORS"
    assert normalize_answer("  backpropagation   ") == "BACKPROPAGATION"
    assert normalize_answer("L1-L2 Regularization!") == "L1L2REGULARIZATION"
    assert normalize_answer("") == ""

def test_initial_reveals_difficulty():
    word = "TRANSFORMER" # len 11
    
    easy_rev = compute_initial_reveals(word, "Easy", rng_seed=42)
    med_rev = compute_initial_reveals(word, "Medium", rng_seed=42)
    hard_rev = compute_initial_reveals(word, "Hard", rng_seed=42)
    
    # Easy reveals more letters than Medium, Medium more than Hard
    assert len(easy_rev) > len(med_rev)
    assert len(med_rev) > len(hard_rev)
    assert len(hard_rev) >= 1
    assert max(easy_rev) < len(word)

def test_scoring_formula():
    # 5 words solved, 300s remaining, 1 wrong attempt, 1 hint used, not completed
    score_mid = calculate_score(
        solved_count=5,
        total_words=10,
        remaining_seconds=300,
        attempts_used=1,
        hints_used=1,
        is_completed=False
    )
    assert score_mid.base_score == 500
    assert score_mid.attempt_penalty == 100
    assert score_mid.hint_penalty == 50
    assert score_mid.time_bonus == 0
    assert score_mid.final_score == 350

    # Game completed with time bonus
    score_win = calculate_score(
        solved_count=10,
        total_words=10,
        remaining_seconds=200,
        attempts_used=0,
        hints_used=0,
        is_completed=True
    )
    # base: 10*100 + 500 bonus = 1500, time bonus = 200 * 2 = 400
    assert score_win.base_score == 1500
    assert score_win.time_bonus == 400
    assert score_win.final_score == 1900
