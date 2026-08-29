"""
Unit tests for Crossword Validator
"""
import pytest
from backend.puzzle_validator import validate_crossword_puzzle

def test_valid_intersection():
    words = [
        {"id": "w1", "word": "TRANSFORMER", "direction": "across", "row": 0, "col": 0},
        {"id": "w2", "word": "TENSOR", "direction": "down", "row": 0, "col": 0}, # 'T' at (0, 0)
        {"id": "w3", "word": "ATTENTION", "direction": "down", "row": 0, "col": 2} # 'A' at (0, 2)
    ]
    result = validate_crossword_puzzle(words, 15)
    assert result["valid"] is True
    assert result["intersection_count"] == 2
    assert result["total_words"] == 3

def test_conflicting_intersection():
    words = [
        {"id": "w1", "word": "TRANSFORMER", "direction": "across", "row": 0, "col": 0},
        {"id": "w2", "word": "PERCEPTRON", "direction": "down", "row": 0, "col": 0} # 'P' vs 'T' at (0,0)
    ]
    result = validate_crossword_puzzle(words, 15)
    assert result["valid"] is False
    assert len(result["errors"]) > 0

def test_out_of_bounds():
    words = [
        {"id": "w1", "word": "BACKPROPAGATION", "direction": "across", "row": 0, "col": 5} # len 15 + 5 = 20 > 15
    ]
    result = validate_crossword_puzzle(words, 15)
    assert result["valid"] is False
    assert "exceeds grid bounds" in result["errors"][0]
