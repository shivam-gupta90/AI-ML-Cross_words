"""
Pydantic Schemas for Request & Response validation
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

class PuzzleSummary(BaseModel):
    id: str
    title: str
    description: Optional[str]
    difficulty: str
    grid_size: int
    time_limit: int
    max_attempts: int
    max_hints: int
    word_count: int

class StartGameRequest(BaseModel):
    player_name: str = Field(..., min_length=1, max_length=64, description="Student / Team name")
    puzzle_id: str = Field(..., description="Selected puzzle identifier")
    difficulty: Optional[str] = Field("Medium", description="Difficulty mode (Easy, Medium, Hard)")

class SubmitAnswerRequest(BaseModel):
    word_id: str = Field(..., description="Target word ID on the crossword")
    answer: str = Field(..., min_length=1, max_length=100, description="Complete word or phrase")

class UseHintRequest(BaseModel):
    word_id: str = Field(..., description="Word ID to reveal an extra letter for")

class PublicWordClue(BaseModel):
    id: str
    clue_number: int
    direction: str  # "across" or "down"
    row: int
    col: int
    length: int
    clue: str
    category: str
    masked_pattern: str  # e.g. "T _ A N _ F _ R M _ R"
    is_solved: bool

class PublicGridCell(BaseModel):
    row: int
    col: int
    char: str  # Letter if revealed/solved, otherwise ""
    is_blocked: bool
    clue_number: Optional[int] = None
    word_ids: List[str] = []

class ScoreBreakdown(BaseModel):
    base_score: int
    time_bonus: int
    attempt_penalty: int
    hint_penalty: int
    final_score: int

class GameStateResponse(BaseModel):
    session_id: str
    player_name: str
    puzzle_id: str
    puzzle_title: str
    difficulty: str
    status: str
    grid_size: int
    time_limit_seconds: int
    elapsed_seconds: int
    remaining_seconds: int
    score: int
    max_attempts: int
    attempts_used: int
    remaining_attempts: int
    max_hints: int
    hints_used: int
    remaining_hints: int
    total_words: int
    solved_words_count: int
    grid: List[List[PublicGridCell]]
    words: List[PublicWordClue]
    score_breakdown: Optional[ScoreBreakdown] = None
    created_at: str

class SubmitAnswerResponse(BaseModel):
    correct: bool
    message: str
    word_id: str
    revealed_word: Optional[str] = None
    newly_revealed_cells: List[Dict[str, Any]] = []
    is_game_won: bool
    is_game_over: bool
    score: int
    remaining_attempts: int
    solved_words_count: int
    total_words: int
    score_breakdown: Optional[ScoreBreakdown] = None

class UseHintResponse(BaseModel):
    success: bool
    message: str
    word_id: str
    revealed_index: Optional[int] = None
    revealed_char: Optional[str] = None
    revealed_cell: Optional[Dict[str, Any]] = None
    remaining_hints: int
    score: int

class LeaderboardItem(BaseModel):
    rank: int
    player_name: str
    puzzle_title: str
    difficulty: str
    score: int
    time_taken_seconds: int
    time_taken_formatted: str
    attempts_used: int
    hints_used: int
    words_solved: int
    total_words: int
    completed_at: str
