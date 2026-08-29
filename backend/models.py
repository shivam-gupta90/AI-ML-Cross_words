"""
SQLAlchemy ORM Models for AI/ML Crossword Challenge
"""
from datetime import datetime, timezone
import json
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class Puzzle(Base):
    __tablename__ = "puzzles"

    id = Column(String(64), primary_key=True, index=True)
    title = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    difficulty = Column(String(32), default="Medium")
    grid_size = Column(Integer, default=15)
    time_limit = Column(Integer, default=600)
    max_attempts = Column(Integer, default=10)
    max_hints = Column(Integer, default=3)
    created_at = Column(DateTime, default=utc_now)

    words = relationship("Word", back_populates="puzzle", cascade="all, delete-orphan")

class Word(Base):
    __tablename__ = "words"

    id = Column(String(64), primary_key=True, index=True)
    puzzle_id = Column(String(64), ForeignKey("puzzles.id", ondelete="CASCADE"), nullable=False)
    clue_number = Column(Integer, nullable=False)
    word = Column(String(64), nullable=False)  # Stored server-side only
    display_name = Column(String(64), nullable=True)
    clue = Column(Text, nullable=False)
    category = Column(String(64), default="AI / ML")
    direction = Column(String(16), nullable=False)  # "across" or "down"
    row = Column(Integer, nullable=False)
    col = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)

    puzzle = relationship("Puzzle", back_populates="words")

class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(String(64), primary_key=True, index=True)
    player_name = Column(String(64), nullable=False)
    puzzle_id = Column(String(64), ForeignKey("puzzles.id"), nullable=False)
    difficulty = Column(String(32), default="Medium")
    start_time = Column(DateTime, default=utc_now, nullable=False)
    end_time = Column(DateTime, nullable=True)
    time_limit_seconds = Column(Integer, default=600)
    max_attempts = Column(Integer, default=10)
    max_hints = Column(Integer, default=3)
    attempts_used = Column(Integer, default=0)
    hints_used = Column(Integer, default=0)
    score = Column(Integer, default=0)
    status = Column(String(32), default="in_progress")  # in_progress, completed, game_over, time_up
    
    # Serialized JSON structures
    solved_words_json = Column(Text, default="[]")
    revealed_positions_json = Column(Text, default="{}")
    submission_log_json = Column(Text, default="[]")

    @property
    def solved_words(self):
        try:
            return json.loads(self.solved_words_json or "[]")
        except Exception:
            return []

    @solved_words.setter
    def solved_words(self, val):
        self.solved_words_json = json.dumps(val)

    @property
    def revealed_positions(self):
        try:
            return json.loads(self.revealed_positions_json or "{}")
        except Exception:
            return {}

    @revealed_positions.setter
    def revealed_positions(self, val):
        self.revealed_positions_json = json.dumps(val)

    @property
    def submission_log(self):
        try:
            return json.loads(self.submission_log_json or "[]")
        except Exception:
            return []

    @submission_log.setter
    def submission_log(self, val):
        self.submission_log_json = json.dumps(val)

class LeaderboardEntry(Base):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(64), nullable=False, index=True)
    player_name = Column(String(64), nullable=False)
    puzzle_id = Column(String(64), nullable=False)
    puzzle_title = Column(String(128), nullable=False)
    difficulty = Column(String(32), default="Medium")
    score = Column(Integer, nullable=False)
    time_taken_seconds = Column(Integer, nullable=False)
    attempts_used = Column(Integer, default=0)
    hints_used = Column(Integer, default=0)
    words_solved = Column(Integer, default=0)
    total_words = Column(Integer, default=0)
    completed_at = Column(DateTime, default=utc_now, nullable=False)
