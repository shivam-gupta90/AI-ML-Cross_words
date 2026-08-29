"""
AI/ML Crossword Challenge - FastAPI Backend Application
"""
import os
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.database import Base, engine, SessionLocal
from backend.models import Puzzle, Word
from backend.routes import puzzle, game, leaderboard, admin

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
DATA_DIR = os.path.join(BASE_DIR, "data")

def seed_default_puzzles():
    """Seeds default verified puzzles if database is empty."""
    db = SessionLocal()
    try:
        puzzle_count = db.query(Puzzle).count()
        if puzzle_count == 0:
            seed_file = os.path.join(DATA_DIR, "seed_puzzles.json")
            if os.path.exists(seed_file):
                with open(seed_file, "r") as f:
                    puzzles_data = json.load(f)
                
                for p_data in puzzles_data:
                    p = Puzzle(
                        id=p_data["id"],
                        title=p_data["title"],
                        description=p_data.get("description", ""),
                        difficulty=p_data.get("difficulty", "Medium"),
                        grid_size=p_data.get("grid_size", 15),
                        time_limit=p_data.get("time_limit", 600),
                        max_attempts=p_data.get("max_attempts", 10),
                        max_hints=p_data.get("max_hints", 3)
                    )
                    db.add(p)
                    db.flush()

                    for w_data in p_data.get("words", []):
                        w = Word(
                            id=w_data["id"],
                            puzzle_id=p.id,
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
                        db.add(w)
                db.commit()
                print(f"[Seed] Successfully seeded {len(puzzles_data)} default tournament puzzles into database.")
    except Exception as e:
        print(f"[Seed Error] Could not seed database: {e}")
        db.rollback()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables and seed default puzzles
    Base.metadata.create_all(bind=engine)
    seed_default_puzzles()
    yield

app = FastAPI(
    title="AI/ML & CSE Crossword Challenge API",
    description="Backend for Engineering Day Multi-Track Crossword Competition",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(puzzle.router)
app.include_router(game.router)
app.include_router(leaderboard.router)
app.include_router(admin.router)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "AI/ML & CSE Crossword Challenge"}

# Serve Frontend Static Files
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
