"""
Admin and Organizer Management Endpoints
"""
import os
import json
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.database import get_db, Base, engine
from backend.models import Puzzle, Word, GameSession, LeaderboardEntry
from backend.puzzle_validator import validate_crossword_puzzle

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.post("/reset-leaderboard")
def reset_leaderboard(db: Session = Depends(get_db)):
    """Clears all entries from the event leaderboard."""
    count = db.query(LeaderboardEntry).delete()
    db.commit()
    return {"success": True, "message": f"Successfully deleted {count} leaderboard entries."}

@router.post("/reseed-puzzles")
def reseed_puzzles(db: Session = Depends(get_db)):
    """Re-reads and seeds pre-validated puzzles into the database."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    seed_file = os.path.join(base_dir, "data", "seed_puzzles.json")
    
    if not os.path.exists(seed_file):
        raise HTTPException(status_code=404, detail="seed_puzzles.json not found")
        
    with open(seed_file, "r") as f:
        puzzles_data = json.load(f)

    # Delete existing puzzles and words
    db.query(Word).delete()
    db.query(Puzzle).delete()
    db.commit()

    created_count = 0
    for p_data in puzzles_data:
        puzzle = Puzzle(
            id=p_data["id"],
            title=p_data["title"],
            description=p_data.get("description", ""),
            difficulty=p_data.get("difficulty", "Medium"),
            grid_size=p_data.get("grid_size", 15),
            time_limit=p_data.get("time_limit", 600),
            max_attempts=p_data.get("max_attempts", 3),
            max_hints=p_data.get("max_hints", 3)
        )
        db.add(puzzle)
        db.flush()

        for w_data in p_data.get("words", []):
            word = Word(
                id=w_data["id"],
                puzzle_id=puzzle.id,
                clue_number=w_data.get("clue_number", 1),
                word=w_data["word"].upper().strip(),
                display_name=w_data.get("display_name", w_data["word"]),
                clue=w_data["clue"],
                category=w_data.get("category", "AI / ML"),
                direction=w_data["direction"].lower(),
                row=w_data["row"],
                col=w_data["col"],
                length=w_data.get("length", len(w_data["word"]))
            )
            db.add(word)
        created_count += 1

    db.commit()
    return {"success": True, "message": f"Successfully re-seeded {created_count} tournament puzzles."}

@router.get("/sessions")
def get_recent_sessions(limit: int = 50, db: Session = Depends(get_db)):
    """Lists recent player sessions for event organizers."""
    sessions = db.query(GameSession).order_by(desc(GameSession.start_time)).limit(limit).all()
    results = []
    for s in sessions:
        results.append({
            "session_id": s.id,
            "player_name": s.player_name,
            "puzzle_id": s.puzzle_id,
            "difficulty": s.difficulty,
            "status": s.status,
            "score": s.score,
            "attempts_used": s.attempts_used,
            "hints_used": s.hints_used,
            "words_solved_count": len(s.solved_words),
            "start_time": s.start_time.isoformat()
        })
    return results

@router.post("/puzzles/create")
def create_custom_puzzle(payload: Dict[str, Any], db: Session = Depends(get_db)):
    """Validates and creates a custom crossword puzzle."""
    words = payload.get("words", [])
    validation = validate_crossword_puzzle(words, payload.get("grid_size", 15))
    if not validation["valid"]:
        raise HTTPException(status_code=400, detail={"errors": validation["errors"]})

    puzzle = Puzzle(
        id=payload["id"],
        title=payload["title"],
        description=payload.get("description", ""),
        difficulty=payload.get("difficulty", "Medium"),
        grid_size=payload.get("grid_size", 15),
        time_limit=payload.get("time_limit", 600),
        max_attempts=payload.get("max_attempts", 3),
        max_hints=payload.get("max_hints", 3)
    )
    db.add(puzzle)
    db.flush()

    for w_data in validation["numbered_words"]:
        word = Word(
            id=w_data["id"],
            puzzle_id=puzzle.id,
            clue_number=w_data["clue_number"],
            word=w_data["clean_word"],
            display_name=w_data.get("display_name", w_data["clean_word"]),
            clue=w_data.get("clue", f"Clue for {w_data['clean_word']}"),
            category=w_data.get("category", "AI / ML"),
            direction=w_data["direction"],
            row=w_data["row"],
            col=w_data["col"],
            length=w_data["length"]
        )
        db.add(word)

    db.commit()
    return {"success": True, "puzzle_id": puzzle.id, "word_count": len(words)}
