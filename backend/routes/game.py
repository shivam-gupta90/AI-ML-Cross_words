"""
Game Session and Gameplay REST Endpoints
"""
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Puzzle, Word, GameSession
from backend.schemas import (
    StartGameRequest, GameStateResponse, SubmitAnswerRequest,
    SubmitAnswerResponse, UseHintRequest, UseHintResponse
)
from backend.game_logic import (
    compute_initial_reveals, build_game_state_response,
    handle_submission, handle_hint, utc_now
)

router = APIRouter(prefix="/api/game", tags=["Game"])

@router.post("/start", response_model=GameStateResponse, status_code=status.HTTP_201_CREATED)
def start_game(payload: StartGameRequest, db: Session = Depends(get_db)):
    """
    Initializes a new game session.
    Hides answers and reveals a percentage of letters based on selected difficulty.
    """
    puzzle = db.query(Puzzle).filter(Puzzle.id == payload.puzzle_id).first()
    if not puzzle:
        puzzle = db.query(Puzzle).first()
        if not puzzle:
            raise HTTPException(status_code=404, detail="No puzzles available in database")

    session_id = str(uuid.uuid4())
    difficulty = payload.difficulty or puzzle.difficulty or "Medium"

    revealed_positions = {}
    for w in puzzle.words:
        revealed_positions[w.id] = compute_initial_reveals(w.word, difficulty)

    game_session = GameSession(
        id=session_id,
        player_name=payload.player_name.strip(),
        puzzle_id=puzzle.id,
        difficulty=difficulty,
        start_time=utc_now(),
        time_limit_seconds=puzzle.time_limit or 600,
        max_attempts=puzzle.max_attempts or 3,
        max_hints=puzzle.max_hints or 3,
        attempts_used=0,
        hints_used=0,
        score=0,
        status="in_progress",
        solved_words=[],
        revealed_positions=revealed_positions
    )
    
    db.add(game_session)
    db.commit()
    db.refresh(game_session)

    return build_game_state_response(game_session, puzzle)

@router.get("/{session_id}/state", response_model=GameStateResponse)
def get_game_state(session_id: str, db: Session = Depends(get_db)):
    """Retrieves current public game state for a session."""
    session = db.query(GameSession).filter(GameSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Game session not found")

    puzzle = db.query(Puzzle).filter(Puzzle.id == session.puzzle_id).first()
    if not puzzle:
        raise HTTPException(status_code=404, detail="Associated puzzle not found")

    return build_game_state_response(session, puzzle)

@router.post("/{session_id}/submit", response_model=SubmitAnswerResponse)
def submit_word_answer(session_id: str, payload: SubmitAnswerRequest, db: Session = Depends(get_db)):
    """Submits a full word answer for validation."""
    session = db.query(GameSession).filter(GameSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Game session not found")

    puzzle = db.query(Puzzle).filter(Puzzle.id == session.puzzle_id).first()
    if not puzzle:
        raise HTTPException(status_code=404, detail="Associated puzzle not found")

    return handle_submission(db, session, puzzle, payload.word_id, payload.answer)

@router.post("/{session_id}/hint", response_model=UseHintResponse)
def request_hint(session_id: str, payload: UseHintRequest, db: Session = Depends(get_db)):
    """Requests a hint for the specified word."""
    session = db.query(GameSession).filter(GameSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Game session not found")

    puzzle = db.query(Puzzle).filter(Puzzle.id == session.puzzle_id).first()
    if not puzzle:
        raise HTTPException(status_code=404, detail="Associated puzzle not found")

    return handle_hint(db, session, puzzle, payload.word_id)

@router.post("/{session_id}/finish", response_model=GameStateResponse)
def finish_game(session_id: str, db: Session = Depends(get_db)):
    """Concludes or forfeits a game session early."""
    session = db.query(GameSession).filter(GameSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Game session not found")

    puzzle = db.query(Puzzle).filter(Puzzle.id == session.puzzle_id).first()
    if not puzzle:
        raise HTTPException(status_code=404, detail="Associated puzzle not found")

    if session.status == "in_progress":
        session.status = "game_over"
        session.end_time = utc_now()
        db.commit()

    return build_game_state_response(session, puzzle)
