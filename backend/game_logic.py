"""
Game Engine and Business Logic
Handles answer normalization, masked grid rendering, hints, scoring, and session lifecycle.
"""
import re
import random
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple, Optional
from sqlalchemy.orm import Session

from backend.models import Puzzle, Word, GameSession, LeaderboardEntry
from backend.schemas import (
    GameStateResponse, PublicWordClue, PublicGridCell,
    SubmitAnswerResponse, UseHintResponse, ScoreBreakdown
)

def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)

def normalize_answer(raw: str) -> str:
    """Normalizes answer string: uppercase, removes non-alphanumeric characters."""
    if not raw:
        return ""
    return re.sub(r'[^A-Z0-9]', '', raw.upper().strip())

def compute_initial_reveals(word: str, difficulty: str, rng_seed: Optional[int] = None) -> List[int]:
    """Computes indices of letters to reveal initially based on difficulty mode."""
    length = len(word)
    if length <= 2:
        return [0]
        
    diff = (difficulty or "Medium").lower()
    if diff == "easy":
        num_reveals = max(1, round(length * 0.55))
    elif diff == "hard":
        num_reveals = max(1, round(length * 0.20))
    else:  # Medium
        num_reveals = max(1, round(length * 0.35))

    num_reveals = min(num_reveals, length - 1)
    
    rng = random.Random(rng_seed) if rng_seed is not None else random.Random()
    indices = sorted(rng.sample(range(length), num_reveals))
    return indices

def calculate_score(
    solved_count: int,
    total_words: int,
    remaining_seconds: int,
    attempts_used: int,
    hints_used: int,
    is_completed: bool = False
) -> ScoreBreakdown:
    """Computes score breakdown with base points, time bonus, and penalties."""
    base_score = solved_count * 100
    if is_completed:
        base_score += 500
        time_bonus = max(0, int(remaining_seconds * 2))
    else:
        time_bonus = 0

    attempt_penalty = attempts_used * 100
    hint_penalty = hints_used * 50
    
    raw_total = base_score + time_bonus - attempt_penalty - hint_penalty
    final_score = max(0, raw_total)
    
    return ScoreBreakdown(
        base_score=base_score,
        time_bonus=time_bonus,
        attempt_penalty=attempt_penalty,
        hint_penalty=hint_penalty,
        final_score=final_score
    )

def build_game_state_response(session: GameSession, puzzle: Puzzle) -> GameStateResponse:
    """Constructs the secure public view of the game state."""
    now = utc_now()
    session_start = session.start_time.replace(tzinfo=None) if session.start_time else now
    elapsed = max(0, int((now - session_start).total_seconds()))
    time_limit = session.time_limit_seconds
    remaining = max(0, time_limit - elapsed)
    
    if session.status == "in_progress" and remaining <= 0:
        session.status = "time_up"
        session.end_time = now

    grid_size = puzzle.grid_size or 15
    words_db: List[Word] = puzzle.words
    solved_set = set(session.solved_words)
    revealed_map = session.revealed_positions

    cell_char_map: Dict[Tuple[int, int], str] = {}
    active_cells: Dict[Tuple[int, int], List[str]] = {}
    clue_number_map: Dict[Tuple[int, int], int] = {}

    for w in words_db:
        w_id = w.id
        clean_word = normalize_answer(w.word)
        r, c = w.row, w.col
        dir_ = w.direction.lower()
        clue_number_map[(r, c)] = w.clue_number
        is_word_solved = w_id in solved_set
        rev_indices = set(revealed_map.get(w_id, []))

        for idx, char in enumerate(clean_word):
            cr = r if dir_ == "across" else r + idx
            cc = c + idx if dir_ == "across" else c
            active_cells.setdefault((cr, cc), []).append(w_id)
            
            if is_word_solved or idx in rev_indices:
                cell_char_map[(cr, cc)] = char

    grid_cells: List[List[PublicGridCell]] = []
    for r in range(grid_size):
        row_list = []
        for c in range(grid_size):
            pos = (r, c)
            is_active = pos in active_cells
            char = cell_char_map.get(pos, "")
            clue_num = clue_number_map.get(pos, None)
            w_ids = active_cells.get(pos, [])
            
            row_list.append(PublicGridCell(
                row=r,
                col=c,
                char=char,
                is_blocked=not is_active,
                clue_number=clue_num,
                word_ids=w_ids
            ))
        grid_cells.append(row_list)

    public_words: List[PublicWordClue] = []
    for w in words_db:
        w_id = w.id
        clean_word = normalize_answer(w.word)
        r, c = w.row, w.col
        dir_ = w.direction.lower()
        is_word_solved = w_id in solved_set
        
        pattern_chars = []
        for idx, char in enumerate(clean_word):
            cr = r if dir_ == "across" else r + idx
            cc = c + idx if dir_ == "across" else c
            if (cr, cc) in cell_char_map:
                pattern_chars.append(cell_char_map[(cr, cc)])
            else:
                pattern_chars.append("_")
                
        masked_pattern = " ".join(pattern_chars)
        
        public_words.append(PublicWordClue(
            id=w_id,
            clue_number=w.clue_number,
            direction=w.direction,
            row=w.row,
            col=w.col,
            length=w.length,
            clue=w.clue,
            category=w.category or "AI / ML",
            masked_pattern=masked_pattern,
            is_solved=is_word_solved
        ))

    public_words.sort(key=lambda x: (0 if x.direction.lower() == "across" else 1, x.clue_number))

    score_bd = calculate_score(
        solved_count=len(solved_set),
        total_words=len(words_db),
        remaining_seconds=remaining,
        attempts_used=session.attempts_used,
        hints_used=session.hints_used,
        is_completed=(session.status == "completed")
    )
    session.score = score_bd.final_score

    return GameStateResponse(
        session_id=session.id,
        player_name=session.player_name,
        puzzle_id=puzzle.id,
        puzzle_title=puzzle.title,
        difficulty=session.difficulty,
        status=session.status,
        grid_size=grid_size,
        time_limit_seconds=time_limit,
        elapsed_seconds=elapsed,
        remaining_seconds=remaining,
        score=score_bd.final_score,
        max_attempts=session.max_attempts,
        attempts_used=session.attempts_used,
        remaining_attempts=max(0, session.max_attempts - session.attempts_used),
        max_hints=session.max_hints,
        hints_used=session.hints_used,
        remaining_hints=max(0, session.max_hints - session.hints_used),
        total_words=len(words_db),
        solved_words_count=len(solved_set),
        grid=grid_cells,
        words=public_words,
        score_breakdown=score_bd,
        created_at=session.start_time.isoformat() if session.start_time else now.isoformat()
    )

def handle_submission(
    db: Session,
    session: GameSession,
    puzzle: Puzzle,
    word_id: str,
    submitted_answer: str
) -> SubmitAnswerResponse:
    """Validates user answer, updates session score/status/attempts."""
    now = utc_now()
    session_start = session.start_time.replace(tzinfo=None) if session.start_time else now
    elapsed = max(0, int((now - session_start).total_seconds()))
    
    # 1. Timer Expiry Check
    if elapsed > session.time_limit_seconds + 5:
        session.status = "time_up"
        session.end_time = now
        db.commit()
        return SubmitAnswerResponse(
            correct=False,
            message="Time's Up! The challenge countdown has expired.",
            word_id=word_id,
            is_game_won=False,
            is_game_over=True,
            score=session.score,
            remaining_attempts=0,
            solved_words_count=len(session.solved_words),
            total_words=len(puzzle.words)
        )

    # 2. Check if game already finished
    if session.status != "in_progress":
        return SubmitAnswerResponse(
            correct=False,
            message=f"Game has already ended with status '{session.status}'.",
            word_id=word_id,
            is_game_won=(session.status == "completed"),
            is_game_over=True,
            score=session.score,
            remaining_attempts=max(0, session.max_attempts - session.attempts_used),
            solved_words_count=len(session.solved_words),
            total_words=len(puzzle.words)
        )

    # 3. Find target word
    target_word: Optional[Word] = None
    for w in puzzle.words:
        if w.id == word_id:
            target_word = w
            break

    if not target_word:
        return SubmitAnswerResponse(
            correct=False,
            message=f"Word with ID '{word_id}' not found.",
            word_id=word_id,
            is_game_won=False,
            is_game_over=False,
            score=session.score,
            remaining_attempts=max(0, session.max_attempts - session.attempts_used),
            solved_words_count=len(session.solved_words),
            total_words=len(puzzle.words)
        )

    solved_list = list(session.solved_words)
    if word_id in solved_list:
        return SubmitAnswerResponse(
            correct=True,
            message=f"'{target_word.display_name or target_word.word}' is already solved!",
            word_id=word_id,
            revealed_word=target_word.display_name or target_word.word,
            is_game_won=(len(solved_list) == len(puzzle.words)),
            is_game_over=False,
            score=session.score,
            remaining_attempts=max(0, session.max_attempts - session.attempts_used),
            solved_words_count=len(solved_list),
            total_words=len(puzzle.words)
        )

    # 4. Normalize & Compare Answers
    norm_submitted = normalize_answer(submitted_answer)
    norm_correct = normalize_answer(target_word.word)

    if norm_submitted == norm_correct:
        solved_list.append(word_id)
        session.solved_words = solved_list
        
        rev_map = dict(session.revealed_positions)
        rev_map[word_id] = list(range(len(norm_correct)))
        session.revealed_positions = rev_map
        
        dir_ = target_word.direction.lower()
        newly_revealed = []
        for idx, char in enumerate(norm_correct):
            cr = target_word.row if dir_ == "across" else target_word.row + idx
            cc = target_word.col + idx if dir_ == "across" else target_word.col
            newly_revealed.append({"row": cr, "col": cc, "char": char})
            
        is_won = len(solved_list) == len(puzzle.words)
        if is_won:
            session.status = "completed"
            session.end_time = now
            
        remaining_seconds = max(0, session.time_limit_seconds - elapsed)
        score_bd = calculate_score(
            solved_count=len(solved_list),
            total_words=len(puzzle.words),
            remaining_seconds=remaining_seconds,
            attempts_used=session.attempts_used,
            hints_used=session.hints_used,
            is_completed=is_won
        )
        session.score = score_bd.final_score
        
        if is_won:
            time_taken = max(1, elapsed)
            entry = LeaderboardEntry(
                session_id=session.id,
                player_name=session.player_name,
                puzzle_id=puzzle.id,
                puzzle_title=puzzle.title,
                difficulty=session.difficulty,
                score=session.score,
                time_taken_seconds=time_taken,
                attempts_used=session.attempts_used,
                hints_used=session.hints_used,
                words_solved=len(solved_list),
                total_words=len(puzzle.words),
                completed_at=now
            )
            db.add(entry)
            
        db.commit()

        return SubmitAnswerResponse(
            correct=True,
            message=f"🎉 Correct! Solved '{target_word.display_name or target_word.word}'.",
            word_id=word_id,
            revealed_word=target_word.display_name or target_word.word,
            newly_revealed_cells=newly_revealed,
            is_game_won=is_won,
            is_game_over=False,
            score=session.score,
            remaining_attempts=max(0, session.max_attempts - session.attempts_used),
            solved_words_count=len(solved_list),
            total_words=len(puzzle.words),
            score_breakdown=score_bd
        )
    else:
        session.attempts_used += 1
        rem_attempts = max(0, session.max_attempts - session.attempts_used)
        is_over = rem_attempts <= 0
        if is_over:
            session.status = "game_over"
            session.end_time = now

        remaining_seconds = max(0, session.time_limit_seconds - elapsed)
        score_bd = calculate_score(
            solved_count=len(solved_list),
            total_words=len(puzzle.words),
            remaining_seconds=remaining_seconds,
            attempts_used=session.attempts_used,
            hints_used=session.hints_used,
            is_completed=False
        )
        session.score = score_bd.final_score
        db.commit()

        msg = f"❌ Incorrect — Try Again ({rem_attempts} attempt{'s' if rem_attempts != 1 else ''} left)"
        if is_over:
            msg = "❌ Incorrect. GAME OVER — You have used all your attempts."

        return SubmitAnswerResponse(
            correct=False,
            message=msg,
            word_id=word_id,
            is_game_won=False,
            is_game_over=is_over,
            score=session.score,
            remaining_attempts=rem_attempts,
            solved_words_count=len(solved_list),
            total_words=len(puzzle.words),
            score_breakdown=score_bd
        )

def handle_hint(
    db: Session,
    session: GameSession,
    puzzle: Puzzle,
    word_id: str
) -> UseHintResponse:
    """Reveals one additional letter for the requested word."""
    now = utc_now()
    session_start = session.start_time.replace(tzinfo=None) if session.start_time else now
    elapsed = max(0, int((now - session_start).total_seconds()))
    
    if session.status != "in_progress":
        return UseHintResponse(
            success=False,
            message="Cannot use hints on a finished game.",
            word_id=word_id,
            remaining_hints=max(0, session.max_hints - session.hints_used),
            score=session.score
        )

    if session.hints_used >= session.max_hints:
        return UseHintResponse(
            success=False,
            message="No hints remaining! (Limit reached)",
            word_id=word_id,
            remaining_hints=0,
            score=session.score
        )

    target_word: Optional[Word] = None
    for w in puzzle.words:
        if w.id == word_id:
            target_word = w
            break

    if not target_word:
        return UseHintResponse(
            success=False,
            message=f"Word '{word_id}' not found.",
            word_id=word_id,
            remaining_hints=max(0, session.max_hints - session.hints_used),
            score=session.score
        )

    if word_id in session.solved_words:
        return UseHintResponse(
            success=False,
            message="This word is already completely solved!",
            word_id=word_id,
            remaining_hints=max(0, session.max_hints - session.hints_used),
            score=session.score
        )

    clean_word = normalize_answer(target_word.word)
    rev_map = dict(session.revealed_positions)
    current_reveals = set(rev_map.get(word_id, []))
    
    unrevealed = [i for i in range(len(clean_word)) if i not in current_reveals]
    if not unrevealed:
        return UseHintResponse(
            success=False,
            message="All letters for this word are already revealed!",
            word_id=word_id,
            remaining_hints=max(0, session.max_hints - session.hints_used),
            score=session.score
        )

    chosen_idx = random.choice(unrevealed)
    current_reveals.add(chosen_idx)
    rev_map[word_id] = sorted(list(current_reveals))
    session.revealed_positions = rev_map
    session.hints_used += 1

    remaining_seconds = max(0, session.time_limit_seconds - elapsed)
    score_bd = calculate_score(
        solved_count=len(session.solved_words),
        total_words=len(puzzle.words),
        remaining_seconds=remaining_seconds,
        attempts_used=session.attempts_used,
        hints_used=session.hints_used,
        is_completed=False
    )
    session.score = score_bd.final_score
    db.commit()

    char = clean_word[chosen_idx]
    dir_ = target_word.direction.lower()
    cr = target_word.row if dir_ == "across" else target_word.row + chosen_idx
    cc = target_word.col + chosen_idx if dir_ == "across" else target_word.col
    
    return UseHintResponse(
        success=True,
        message=f"💡 Hint revealed '{char}' at letter {chosen_idx + 1} (-50 pts)",
        word_id=word_id,
        revealed_index=chosen_idx,
        revealed_char=char,
        revealed_cell={"row": cr, "col": cc, "char": char},
        remaining_hints=max(0, session.max_hints - session.hints_used),
        score=session.score
    )
