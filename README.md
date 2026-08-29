# AI × ML Crossword Challenge — Engineering Day Tournament

A full-stack, competitive **AI/ML Crossword web application** designed for college Engineering Day events to test students' deep knowledge of Artificial Intelligence, Machine Learning, Deep Learning, Generative AI / LLMs, and Optimization Mathematics.

Built with **Python (FastAPI + SQLite + SQLAlchemy + Pydantic)** on the backend and **Modern HTML5, CSS3, and Vanilla JavaScript** on the frontend.

---

## 🌟 Key Features

1. **15 × 15 Verified Crossword Grids**:
   - Mathematically verified 15x15 matrix geometry where words cross at exact matching character coordinates.
   - Numbered clue cells, blocked cell circuit styling, and clear Across / Down clue navigation.
   - 3 pre-built tournament challenges:
     - 🔥 **AI & ML Championship 2026** (Hard - 20 interconnected words, 22 intersections)
     - ⚡ **Deep Learning & Neural Architectures** (Medium - 19 interconnected words)
     - 🌱 **Generative AI & LLM Frontiers** (Easy - 17 interconnected words)

2. **Unified Single-Box Answer Submission**:
   - Students **do not type letters individually into crossword cells**.
   - The student selects a word on the grid or from the clue list, analyzes the concept clue and revealed letters, and enters the **COMPLETE word or phrase into ONE answer box**.
   - Seamlessly handles casing, spaces, and hyphens (e.g. `gradient descent`, `Gradient-Descent`, `GRADIENT DESCENT`).

3. **Server-Side Security & Validation**:
   - Secret answer keys are **strictly maintained on the server**. Public API payloads only transmit masked strings and revealed letter indices to prevent cheating via browser inspection.

4. **Difficulty & Hidden Letter System**:
   - **Hard**: ~20% of letters revealed initially.
   - **Medium**: ~35% of letters revealed initially.
   - **Easy**: ~55% of letters revealed initially.
   - Solving one word instantly unlocks and displays intersecting letters on the board for other words.

5. **Countdown Timer & Limited Attempts**:
   - 10-minute competition countdown timer (`⏱ 10:00`), validated on the server with network grace.
   - 3 limited attempts (`🎯 3/3`). Wrong answers reduce remaining attempts and deduct score penalties.
   - Attempt exhaustion triggers Game Over.

6. **Hint System & Dynamic Scoring**:
   - `💡 USE HINT`: Unlocks an additional unrevealed letter for the selected word (max 3 hints, -50 pt penalty).
   - **Scoring Engine**:
     $$\text{Final Score} = \max(0, \text{Word Points} + \text{Victory Bonus} + \text{Time Bonus} - \text{Attempt Penalty} - \text{Hint Penalty})$$

7. **Event Leaderboard & Admin Panel**:
   - Real-time tournament leaderboard tracking player names, scores, completion times (`mm:ss`), attempts used, and hints used.
   - Organizer Admin panel to view live player sessions, reset leaderboards, and re-seed challenges.

8. **Web Audio API Sound & Confetti**:
   - Zero external audio assets needed — pure synthesized audio cues for selection blips, victory chords, buzzers, and hints.
   - Custom canvas confetti celebration on puzzle completion.

---

## 🛠 Tech Stack

- **Backend**: Python 3.10+, FastAPI, Uvicorn, SQLite, SQLAlchemy 2.0, Pydantic v2
- **Frontend**: HTML5, CSS3 (Custom Cyberpunk Tech Theme, Glassmorphism, CSS Grid), Vanilla ES6+ JavaScript
- **Audio**: Web Audio API (Built-in Synthesizer)
- **Testing**: Pytest, HTTPX

---

## 🚀 Quickstart & Running Instructions

### 1. Prerequisites
- Python 3.10 or higher

### 2. Setup Virtual Environment & Install Dependencies
```bash
cd ai-ml-crossword

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS / Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 3. Start the Application Server
```bash
# Start FastAPI backend with automatic reload
uvicorn backend.main:app --reload --port 8000
```

### 4. Open in Browser
Visit **[http://localhost:8000](http://localhost:8000)** in your web browser.

---

## 🧪 Running Automated Tests

Run the comprehensive unit and integration test suite:

```bash
PYTHONPATH=. pytest tests/ -v
```

All 12 test suites will run, validating:
- Crossword 15x15 geometry, boundaries, and intersection consistency (`test_validator.py`)
- Answer normalization, difficulty reveal formulas, scoring math, and hints (`test_game_logic.py`)
- FastAPI REST endpoints, answer submission lifecycle, leaderboard, and admin routes (`test_api.py`)

---

## 📁 Project Directory Structure

```
ai-ml-crossword/
│
├── backend/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app, CORS, static mounting, lifespan setup
│   ├── database.py              # SQLite engine and SQLAlchemy sessionmaker
│   ├── models.py                # Database models (Puzzle, Word, GameSession, Leaderboard)
│   ├── schemas.py               # Pydantic request/response validation models
│   ├── game_logic.py            # Game engine, normalization, hints, scoring, security
│   ├── puzzle_validator.py      # Crossword 15x15 geometry & intersection checker
│   ├── builder_engine.py        # AI/ML vocabulary bank with definitions & categories
│   ├── puzzle_generator.py      # Automated high-density crossword puzzle generator
│   └── routes/
│       ├── __init__.py
│       ├── puzzle.py            # /api/puzzles and /api/puzzles/{id}
│       ├── game.py              # /api/game/start, /submit, /hint, /state, /finish
│       ├── leaderboard.py       # /api/leaderboard and /api/leaderboard/stats
│       └── admin.py             # /api/admin/reset-leaderboard, /reseed-puzzles, /sessions
│
├── frontend/
│   ├── index.html               # Main SPA view (Landing, Arena, Modals)
│   ├── css/
│   │   ├── style.css            # Cyber theme, glassmorphism, responsive styles
│   │   ├── crossword.css        # 15x15 board layout, cell states, active glowing highlights
│   │   └── animations.css       # Keyframes, confetti, input shake, pulse glows
│   └── js/
│       ├── audio.js             # Zero-dependency Web Audio synthesizer
│       ├── api.js               # REST API fetch wrapper
│       ├── crossword.js         # Interactive 15x15 grid renderer & keyboard navigation
│       ├── game.js              # State manager, countdown timer, submission handling
│       ├── leaderboard.js       # Leaderboard fetching and filtering
│       ├── admin.js             # Organizer actions (reset, re-seed, session logs)
│       └── app.js               # Application bootstrapping and confetti system
│
├── data/
│   └── seed_puzzles.json        # Verified 15x15 AI/ML crosswords
│
├── database/
│   └── crossword.db             # SQLite database (auto-created on startup)
│
├── tests/
│   ├── test_validator.py        # Grid boundary and intersection unit tests
│   ├── test_game_logic.py       # Scoring, hints, normalization unit tests
│   └── test_api.py              # REST API endpoint integration tests
│
├── requirements.txt
└── README.md
```

---

## 📡 REST API Documentation

### Gameplay Endpoints
- `GET /api/puzzles`: Lists all tournament puzzles with word counts and difficulties.
- `POST /api/game/start`: Starts a new session with player name, puzzle ID, and difficulty mode.
- `GET /api/game/{session_id}/state`: Retrieves the public game state (masked grid, clue list, remaining time/attempts/hints).
- `POST /api/game/{session_id}/submit`: Submits a complete word answer for validation.
- `POST /api/game/{session_id}/hint`: Requests an extra letter reveal for the active word.
- `POST /api/game/{session_id}/finish`: Ends/forfeits the current session.

### Leaderboard & Admin
- `GET /api/leaderboard`: Returns ranked completions with scores, times, attempts, and hints.
- `GET /api/leaderboard/stats`: Returns competition totals and high score.
- `POST /api/admin/reset-leaderboard`: Clears the event leaderboard.
- `POST /api/admin/reseed-puzzles`: Re-populates the database with verified seed puzzles.
- `GET /api/admin/sessions`: Lists recent player sessions for event proctoring.
