"""
Puzzle Endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Puzzle
from backend.schemas import PuzzleSummary

router = APIRouter(prefix="/api/puzzles", tags=["Puzzles"])

@router.get("", response_model=List[PuzzleSummary])
def list_puzzles(db: Session = Depends(get_db)):
    """Lists all available crossword challenges."""
    puzzles = db.query(Puzzle).all()
    results = []
    for p in puzzles:
        results.append(PuzzleSummary(
            id=p.id,
            title=p.title,
            description=p.description,
            difficulty=p.difficulty,
            grid_size=p.grid_size,
            time_limit=p.time_limit,
            max_attempts=p.max_attempts,
            max_hints=p.max_hints,
            word_count=len(p.words)
        ))
    return results

@router.get("/{puzzle_id}", response_model=PuzzleSummary)
def get_puzzle_detail(puzzle_id: str, db: Session = Depends(get_db)):
    """Retrieves metadata for a specific puzzle."""
    p = db.query(Puzzle).filter(Puzzle.id == puzzle_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    return PuzzleSummary(
        id=p.id,
        title=p.title,
        description=p.description,
        difficulty=p.difficulty,
        grid_size=p.grid_size,
        time_limit=p.time_limit,
        max_attempts=p.max_attempts,
        max_hints=p.max_hints,
        word_count=len(p.words)
    )
