"""
Integration tests for FastAPI REST Endpoints
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app, seed_default_puzzles
from backend.database import Base, engine, SessionLocal
from backend.models import Puzzle, Word, GameSession

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    seed_default_puzzles()
    with TestClient(app) as c:
        yield c

def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_list_puzzles(client):
    response = client.get("/api/puzzles")
    assert response.status_code == 200
    puzzles = response.json()
    assert len(puzzles) >= 3
    assert puzzles[0]["grid_size"] == 15
    assert puzzles[0]["word_count"] == 10
    assert puzzles[0]["time_limit"] == 600
    assert puzzles[0]["max_attempts"] == 10

def test_start_game_session(client):
    puzzles = client.get("/api/puzzles").json()
    p_id = puzzles[0]["id"]
    
    response = client.post("/api/game/start", json={
        "player_name": "Test Player",
        "puzzle_id": p_id,
        "difficulty": "Medium"
    })
    assert response.status_code == 201
    data = response.json()
    assert "session_id" in data
    assert data["player_name"] == "Test Player"
    assert data["status"] == "in_progress"
    assert len(data["grid"]) == 15
    assert len(data["grid"][0]) == 15
    assert len(data["words"]) == 10
    assert data["time_limit_seconds"] == 600
    assert data["max_attempts"] == 10
    assert data["remaining_attempts"] == 10
    
    # Verify answers are NOT exposed in public words payload
    for w in data["words"]:
        assert "word" not in w  # Secret answer must never be leaked

def test_game_answer_flow(client):
    db = SessionLocal()
    puzzle = db.query(Puzzle).first()
    first_word = puzzle.words[0]
    p_id = puzzle.id
    target_word_id = first_word.id
    correct_word = first_word.word
    db.close()

    # 1. Start game
    start_res = client.post("/api/game/start", json={
        "player_name": "Engineer 42",
        "puzzle_id": p_id,
        "difficulty": "Hard"
    }).json()
    session_id = start_res["session_id"]
    assert start_res["remaining_attempts"] == 10

    # 2. Submit wrong answer
    wrong_res = client.post(f"/api/game/{session_id}/submit", json={
        "word_id": target_word_id,
        "answer": "WRONGANSWERXYZ"
    }).json()
    assert wrong_res["correct"] is False
    assert wrong_res["remaining_attempts"] == 9
    assert "Incorrect" in wrong_res["message"]

    # 3. Request hint
    hint_res = client.post(f"/api/game/{session_id}/hint", json={
        "word_id": target_word_id
    }).json()
    assert hint_res["success"] is True
    assert hint_res["remaining_hints"] == 2
    assert hint_res["revealed_char"] is not None

    # 4. Submit correct answer with different case and formatting
    correct_res = client.post(f"/api/game/{session_id}/submit", json={
        "word_id": target_word_id,
        "answer": f"  {correct_word.lower()}  "
    }).json()
    assert correct_res["correct"] is True
    assert target_word_id in correct_res["word_id"]
    assert correct_res["solved_words_count"] == 1

def test_leaderboard(client):
    response = client.get("/api/leaderboard")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_admin_reset_leaderboard(client):
    response = client.post("/api/admin/reset-leaderboard")
    assert response.status_code == 200
    assert response.json()["success"] is True
