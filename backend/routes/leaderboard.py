"""
Leaderboard Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.database import get_db
from backend.models import LeaderboardEntry
from backend.schemas import LeaderboardItem

router = APIRouter(prefix="/api/leaderboard", tags=["Leaderboard"])

@router.get("", response_model=List[LeaderboardItem])
def get_leaderboard(
    puzzle_id: Optional[str] = Query(None, description="Filter by puzzle ID"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Retrieves ranked leaderboard entries with scores and times."""
    query = db.query(LeaderboardEntry)
    
    if puzzle_id:
        query = query.filter(LeaderboardEntry.puzzle_id == puzzle_id)
    if difficulty:
        query = query.filter(LeaderboardEntry.difficulty == difficulty)
        
    entries = query.order_by(
        desc(LeaderboardEntry.score),
        LeaderboardEntry.time_taken_seconds.asc(),
        LeaderboardEntry.attempts_used.asc()
    ).limit(limit).all()

    items = []
    for idx, entry in enumerate(entries):
        mins = entry.time_taken_seconds // 60
        secs = entry.time_taken_seconds % 60
        time_formatted = f"{mins:02d}:{secs:02d}"
        
        items.append(LeaderboardItem(
            rank=idx + 1,
            player_name=entry.player_name,
            puzzle_title=entry.puzzle_title,
            difficulty=entry.difficulty,
            score=entry.score,
            time_taken_seconds=entry.time_taken_seconds,
            time_taken_formatted=time_formatted,
            attempts_used=entry.attempts_used,
            hints_used=entry.hints_used,
            words_solved=entry.words_solved,
            total_words=entry.total_words,
            completed_at=entry.completed_at.strftime("%Y-%m-%d %H:%M")
        ))
        
    return items

@router.get("/stats")
def get_leaderboard_stats(db: Session = Depends(get_db)):
    """Returns general competition statistics."""
    total_entries = db.query(LeaderboardEntry).count()
    top_entry = db.query(LeaderboardEntry).order_by(desc(LeaderboardEntry.score)).first()
    
    return {
        "total_completions": total_entries,
        "high_score": top_entry.score if top_entry else 0,
        "top_player": top_entry.player_name if top_entry else "N/A"
    }
