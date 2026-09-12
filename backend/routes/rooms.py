"""
Game Room Routes — Organizer Mode
Handles room creation, joining, starting, live scores, and player management.
"""
import uuid
import random
import string
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Puzzle, GameRoom, GameSession
from backend.schemas import (
    CreateRoomRequest, CreateRoomResponse,
    JoinRoomRequest, JoinRoomResponse,
    RoomInfoResponse, RoomPlayersResponse, PlayerInRoom,
    StartRoomResponse,
)
from backend.game_logic import compute_initial_reveals, utc_now

router = APIRouter(prefix="/api/rooms", tags=["Rooms"])

ROOM_EXPIRY_HOURS = 2


# ─────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────

def _generate_join_code(db: Session) -> str:
    """Generates a unique 6-character uppercase alphanumeric join code."""
    for _ in range(100):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not db.query(GameRoom).filter(GameRoom.join_code == code).first():
            return code
    raise RuntimeError("Could not generate a unique join code after 100 attempts.")


def _require_organizer(room: GameRoom, secret: str):
    """Raises 403 if secret doesn't match the room's organizer_secret."""
    if not secret or secret.strip() != room.organizer_secret:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid organizer secret. Only the room creator can perform this action."
        )


def _room_or_404(db: Session, code: str) -> GameRoom:
    room = db.query(GameRoom).filter(GameRoom.join_code == code.upper().strip()).first()
    if not room:
        raise HTTPException(status_code=404, detail=f"Room with code '{code}' not found.")
    # Expiry handling
    if room.expires_at and room.expires_at < utc_now():
        # Optionally delete expired room
        db.delete(room)
        db.commit()
        raise HTTPException(status_code=404, detail="Room has expired.")
    return room


# ─────────────────────────────────────────────────
# POST /api/rooms/create  — Organizer creates a room
# ─────────────────────────────────────────────────
@router.post("/create", response_model=CreateRoomResponse, status_code=201)
def create_room(payload: CreateRoomRequest, db: Session = Depends(get_db)):
    puzzle = db.query(Puzzle).filter(Puzzle.id == payload.puzzle_id).first()
    if not puzzle:
        puzzle = db.query(Puzzle).first()
        if not puzzle:
            raise HTTPException(status_code=404, detail="No puzzles available.")

    room_id = str(uuid.uuid4())
    organizer_secret = str(uuid.uuid4())
    join_code = _generate_join_code(db)
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    room = GameRoom(
        id=room_id,
        join_code=join_code,
        organizer_name=payload.organizer_name.strip(),
        organizer_secret=organizer_secret,
        puzzle_id=puzzle.id,
        difficulty=payload.difficulty or "Medium",
        status="waiting",
        max_players=payload.max_players or 50,
        organizer_can_play=payload.organizer_can_play if payload.organizer_can_play is not None else False,
        created_at=now,
        expires_at=now + timedelta(hours=ROOM_EXPIRY_HOURS),
    )
    db.add(room)
    db.commit()

    return CreateRoomResponse(
        room_id=room_id,
        join_code=join_code,
        organizer_secret=organizer_secret,
        organizer_name=room.organizer_name,
        puzzle_title=puzzle.title,
        difficulty=room.difficulty,
        status=room.status,
    )


# ─────────────────────────────────────────────────
# GET /api/rooms/{code}/info  — Room info for join screen
# ─────────────────────────────────────────────────
@router.get("/{code}/info", response_model=RoomInfoResponse)
def get_room_info(code: str, db: Session = Depends(get_db)):
    room = _room_or_404(db, code)
    puzzle = db.query(Puzzle).filter(Puzzle.id == room.puzzle_id).first()
    player_count = db.query(GameSession).filter(GameSession.room_id == room.id).count()

    return RoomInfoResponse(
        room_id=room.id,
        join_code=room.join_code,
        organizer_name=room.organizer_name,
        puzzle_id=room.puzzle_id,
        puzzle_title=puzzle.title if puzzle else "Unknown",
        difficulty=room.difficulty,
        status=room.status,
        player_count=player_count,
        max_players=room.max_players,
        created_at=room.created_at.isoformat(),
    )


# ─────────────────────────────────────────────────
# POST /api/rooms/{code}/join  — Player joins a room
# ─────────────────────────────────────────────────
@router.post("/{code}/join", response_model=JoinRoomResponse, status_code=201)
def join_room(code: str, payload: JoinRoomRequest, db: Session = Depends(get_db)):
    room = _room_or_404(db, code)

    if room.status == "finished":
        raise HTTPException(status_code=400, detail="This game room has already finished.")
    if room.status == "active":
        raise HTTPException(status_code=400, detail="Game already started. You cannot join a room in progress.")

    # Check capacity
    player_count = db.query(GameSession).filter(GameSession.room_id == room.id).count()
    if player_count >= room.max_players:
        raise HTTPException(status_code=400, detail=f"Room is full ({room.max_players} players max).")

    puzzle = db.query(Puzzle).filter(Puzzle.id == room.puzzle_id).first()
    if not puzzle:
        raise HTTPException(status_code=404, detail="Room puzzle not found.")

    # Pre-compute revealed positions so they're consistent for all players
    revealed_positions = {}
    for w in puzzle.words:
        revealed_positions[w.id] = compute_initial_reveals(w.word, room.difficulty)

    session_id = str(uuid.uuid4())
    session = GameSession(
        id=session_id,
        player_name=payload.player_name.strip(),
        puzzle_id=puzzle.id,
        room_id=room.id,
        difficulty=room.difficulty,
        start_time=utc_now(),          # Will be overwritten when organizer starts
        time_limit_seconds=puzzle.time_limit or 600,
        max_attempts=puzzle.max_attempts or 10,
        max_hints=puzzle.max_hints or 3,
        status="waiting",              # Waiting for organizer to start
        solved_words=[],
        revealed_positions=revealed_positions,
    )
    db.add(session)
    db.commit()

    return JoinRoomResponse(
        session_id=session_id,
        player_name=session.player_name,
        room_id=room.id,
        join_code=room.join_code,
        puzzle_title=puzzle.title,
        difficulty=room.difficulty,
        room_status=room.status,
        message=f"Joined room '{room.join_code}' as {session.player_name}. Waiting for organizer to start the game...",
    )


# ─────────────────────────────────────────────────
# GET /api/rooms/{code}/players  — Live player list (poll)
# ─────────────────────────────────────────────────
@router.get("/{code}/players", response_model=RoomPlayersResponse)
def get_room_players(code: str, db: Session = Depends(get_db)):
    room = _room_or_404(db, code)
    sessions = db.query(GameSession).filter(GameSession.room_id == room.id).all()

    players = []
    for s in sessions:
        solved_count = len(s.solved_words)
        puzzle = db.query(Puzzle).filter(Puzzle.id == s.puzzle_id).first()
        total = len(puzzle.words) if puzzle else 0

        players.append(PlayerInRoom(
            session_id=s.id,
            player_name=s.player_name,
            status=s.status,
            score=s.score,
            words_solved=solved_count,
            total_words=total,
            joined_at=s.start_time.isoformat(),
        ))

    # Sort: completed first by score, then in_progress, then waiting
    status_order = {"completed": 0, "in_progress": 1, "waiting": 2, "game_over": 3, "time_up": 4}
    players.sort(key=lambda p: (status_order.get(p.status, 5), -p.score))

    return RoomPlayersResponse(
        room_id=room.id,
        join_code=room.join_code,
        status=room.status,
        players=players,
        total_players=len(players),
    )


# ─────────────────────────────────────────────────
# POST /api/rooms/{code}/start  — Organizer starts game
# ─────────────────────────────────────────────────
@router.post("/{code}/start", response_model=StartRoomResponse)
def start_room(
    code: str,
    db: Session = Depends(get_db),
    x_organizer_secret: str = Header(..., description="Organizer secret token"),
):
    room = _room_or_404(db, code)
    _require_organizer(room, x_organizer_secret)

    if room.status != "waiting":
        raise HTTPException(status_code=400, detail=f"Room is already '{room.status}'. Cannot start again.")

    player_sessions = db.query(GameSession).filter(
        GameSession.room_id == room.id,
        GameSession.status == "waiting"
    ).all()

    if not player_sessions:
        raise HTTPException(status_code=400, detail="No players have joined yet. Share the join code and wait for players.")

    now = utc_now()
    room.status = "active"
    room.started_at = now
    # Set all waiting player sessions to in_progress with a fresh start_time
    for s in player_sessions:
        s.status = "in_progress"
        s.start_time = now

    # If organizer wants to play, create a session for the organizer
    if room.organizer_can_play:
        # Fetch puzzle for time limits etc.
        puzzle_obj = db.query(Puzzle).filter(Puzzle.id == room.puzzle_id).first()
        org_session = GameSession(
            id=str(uuid.uuid4()),
            player_name=room.organizer_name,
            puzzle_id=room.puzzle_id,
            room_id=room.id,
            difficulty=room.difficulty,
            start_time=now,
            time_limit_seconds=puzzle_obj.time_limit or 600,
            max_attempts=puzzle_obj.max_attempts or 10,
            max_hints=puzzle_obj.max_hints or 3,
            status="in_progress",
            solved_words=[],
            revealed_positions={},
        )
        db.add(org_session)
        player_sessions.append(org_session)

    db.commit()

    return StartRoomResponse(
        success=True,
        message=f"Game started! {len(player_sessions)} player(s) are now playing.",
        room_id=room.id,
        started_at=now.isoformat(),
        players_started=len(player_sessions),
    )


# ─────────────────────────────────────────────────
# GET /api/rooms/{code}/live-scores  — Live scoreboard
# ─────────────────────────────────────────────────
@router.get("/{code}/live-scores")
def get_live_scores(code: str, db: Session = Depends(get_db)):
    room = _room_or_404(db, code)
    sessions = db.query(GameSession).filter(GameSession.room_id == room.id).all()

    scores = []
    for s in sessions:
        solved_count = len(s.solved_words)
        puzzle = db.query(Puzzle).filter(Puzzle.id == s.puzzle_id).first()
        total = len(puzzle.words) if puzzle else 0

        scores.append({
            "player_name": s.player_name,
            "status": s.status,
            "score": s.score,
            "words_solved": solved_count,
            "total_words": total,
            "progress_pct": round((solved_count / total * 100) if total > 0 else 0),
        })

    scores.sort(key=lambda x: (-x["score"], -x["words_solved"]))
    for i, entry in enumerate(scores):
        entry["rank"] = i + 1

    return {
        "room_id": room.id,
        "join_code": room.join_code,
        "room_status": room.status,
        "scores": scores,
    }


# ─────────────────────────────────────────────────
# DELETE /api/rooms/{code}/kick/{session_id}  — Kick player
# ─────────────────────────────────────────────────
@router.delete("/{code}/kick/{session_id}")
def kick_player(
    code: str,
    session_id: str,
    db: Session = Depends(get_db),
    x_organizer_secret: str = Header(..., description="Organizer secret token"),
):
    room = _room_or_404(db, code)
    _require_organizer(room, x_organizer_secret)

    session = db.query(GameSession).filter(
        GameSession.id == session_id,
        GameSession.room_id == room.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Player session not found in this room.")

    player_name = session.player_name
    db.delete(session)
    db.commit()

    return {"success": True, "message": f"Player '{player_name}' has been removed from the room."}


# ─────────────────────────────────────────────────
# POST /api/rooms/{code}/finish  — Organizer ends room
# ─────────────────────────────────────────────────
@router.post("/{code}/finish")
def finish_room(
    code: str,
    db: Session = Depends(get_db),
    x_organizer_secret: str = Header(..., description="Organizer secret token"),
):
    room = _room_or_404(db, code)
    _require_organizer(room, x_organizer_secret)

    room.status = "finished"
    # End all still-active sessions
    active_sessions = db.query(GameSession).filter(
        GameSession.room_id == room.id,
        GameSession.status == "in_progress"
    ).all()
    for s in active_sessions:
        s.status = "time_up"
        s.end_time = utc_now()

    db.commit()
    return {"success": True, "message": "Room finished. All active sessions have been ended."}
