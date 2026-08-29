/**
 * Game Session Controller & UI Orchestrator
 */
class GameManager {
    constructor() {
        this.sessionId = null;
        this.state = null;
        this.activeWord = null;
        this.timerInterval = null;
        this.grid = null;

        this.initDOMElements();
        this.bindEvents();
    }

    initDOMElements() {
        // HUD elements
        this.elTimer = document.getElementById("hud-timer");
        this.elAttempts = document.getElementById("hud-attempts");
        this.elHints = document.getElementById("hud-hints");
        this.elScore = document.getElementById("hud-score");
        this.elProgress = document.getElementById("hud-progress-bar");
        this.elProgressText = document.getElementById("hud-progress-text");
        this.elPlayerBadge = document.getElementById("hud-player-name");
        this.elPuzzleBadge = document.getElementById("hud-puzzle-title");
        this.elAudioBtn = document.getElementById("btn-toggle-audio");

        // Clue and Input elements
        this.elClueNum = document.getElementById("active-clue-num");
        this.elClueDir = document.getElementById("active-clue-dir");
        this.elClueCat = document.getElementById("active-clue-category");
        this.elClueLength = document.getElementById("active-clue-length");
        this.elClueText = document.getElementById("active-clue-text");
        this.elMaskedPattern = document.getElementById("active-masked-pattern");
        this.elAnswerInput = document.getElementById("answer-input");
        this.elSubmitBtn = document.getElementById("btn-submit-answer");
        this.elHintBtn = document.getElementById("btn-use-hint");
        this.elHintBtnText = document.getElementById("hint-btn-text");

        // Clue lists
        this.elAcrossList = document.getElementById("clues-across-list");
        this.elDownList = document.getElementById("clues-down-list");

        // Grid Container
        this.elGridContainer = document.getElementById("crossword-grid");
        this.grid = new CrosswordGrid(this.elGridContainer, (word) => this.onSelectWord(word));
    }

    bindEvents() {
        // Answer submission via button or Enter key
        this.elSubmitBtn.addEventListener("click", () => this.handleSubmit());
        this.elAnswerInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                this.handleSubmit();
            }
        });

        // Hint button
        this.elHintBtn.addEventListener("click", () => this.handleHint());

        // Audio toggle
        this.elAudioBtn.addEventListener("click", () => {
            const isMuted = window.soundEngine?.toggleMute();
            this.updateAudioButtonState(isMuted);
        });

        // Tab switching for Across / Down lists
        document.querySelectorAll(".clue-tab-btn").forEach(btn => {
            btn.addEventListener("click", (e) => {
                const target = btn.dataset.tab;
                document.querySelectorAll(".clue-tab-btn").forEach(b => b.classList.remove("active"));
                btn.classList.add("active");

                if (target === "across") {
                    this.elAcrossList.classList.remove("hidden");
                    this.elDownList.classList.add("hidden");
                } else {
                    this.elAcrossList.classList.add("hidden");
                    this.elDownList.classList.remove("hidden");
                }
            });
        });
    }

    updateAudioButtonState(isMuted) {
        if (isMuted) {
            this.elAudioBtn.innerHTML = `<span>🔇</span> Muted`;
            this.elAudioBtn.classList.add("muted");
        } else {
            this.elAudioBtn.innerHTML = `<span>🔊</span> Sound ON`;
            this.elAudioBtn.classList.remove("muted");
        }
    }

    async loadGameSession(gameState) {
        this.state = gameState;
        this.sessionId = gameState.session_id;

        // Populate HUD
        this.elPlayerBadge.textContent = gameState.player_name;
        this.elPuzzleBadge.textContent = `${gameState.puzzle_title} (${gameState.difficulty})`;
        this.updateHUD();

        // Render Crossword Grid
        this.grid.render(gameState.grid_size, gameState.grid, gameState.words);

        // Render Clue Lists
        this.renderClueLists();

        // Start Countdown Timer
        this.startTimer(gameState.remaining_seconds);

        // Set initial sound state
        this.updateAudioButtonState(window.soundEngine?.muted);

        // Auto focus input
        setTimeout(() => this.elAnswerInput?.focus(), 300);
    }

    startTimer(initialRemaining) {
        if (this.timerInterval) clearInterval(this.timerInterval);

        let remaining = initialRemaining;
        this.updateTimerDisplay(remaining);

        this.timerInterval = setInterval(() => {
            remaining -= 1;
            this.state.remaining_seconds = remaining;
            this.updateTimerDisplay(remaining);

            if (remaining <= 0) {
                clearInterval(this.timerInterval);
                this.handleTimeUp();
            }
        }, 1000);
    }

    updateTimerDisplay(seconds) {
        const mins = Math.floor(Math.max(0, seconds) / 60);
        const secs = Math.max(0, seconds) % 60;
        const formatted = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
        
        this.elTimer.textContent = formatted;

        // Warning highlights
        if (seconds <= 30) {
            this.elTimer.className = "hud-value timer-critical";
        } else if (seconds <= 120) {
            this.elTimer.className = "hud-value timer-warning";
        } else {
            this.elTimer.className = "hud-value";
        }
    }

    updateHUD() {
        this.elAttempts.textContent = `${this.state.remaining_attempts} / ${this.state.max_attempts}`;
        this.elHints.textContent = `${this.state.remaining_hints} / ${this.state.max_hints}`;
        this.elScore.textContent = this.state.score.toLocaleString();

        const solved = this.state.solved_words_count;
        const total = this.state.total_words;
        const pct = total > 0 ? Math.round((solved / total) * 100) : 0;
        
        this.elProgress.style.width = `${pct}%`;
        this.elProgressText.textContent = `${solved} / ${total} Solved (${pct}%)`;

        // Update Hint button availability
        if (this.state.remaining_hints <= 0) {
            this.elHintBtn.disabled = true;
            this.elHintBtnText.textContent = "No Hints Left";
        } else {
            this.elHintBtn.disabled = false;
            this.elHintBtnText.textContent = `💡 Use Hint (${this.state.remaining_hints} left)`;
        }
    }

    renderClueLists() {
        this.elAcrossList.innerHTML = "";
        this.elDownList.innerHTML = "";

        this.state.words.forEach(w => {
            const item = document.createElement("div");
            item.className = "clue-item";
            item.id = `clue-list-item-${w.id}`;
            if (w.is_solved) item.classList.add("solved");
            if (this.activeWord && this.activeWord.id === w.id) item.classList.add("active");

            item.innerHTML = `
                <div class="clue-item-header">
                    <span class="clue-item-number">${w.clue_number}. ${w.direction.toUpperCase()}</span>
                    <span class="clue-item-cat">${w.category}</span>
                    ${w.is_solved ? '<span class="clue-solved-badge">✓ SOLVED</span>' : ''}
                </div>
                <div class="clue-item-text">${w.clue}</div>
                <div class="clue-item-meta">Length: ${w.length} letters &bull; Pattern: <code>${w.masked_pattern}</code></div>
            `;

            item.addEventListener("click", () => {
                this.grid.selectWord(w.id);
            });

            if (w.direction.toLowerCase() === "across") {
                this.elAcrossList.appendChild(item);
            } else {
                this.elDownList.appendChild(item);
            }
        });
    }

    onSelectWord(word) {
        this.activeWord = word;

        // Update Active Clue Card
        this.elClueNum.textContent = `#${word.clue_number}`;
        this.elClueDir.textContent = word.direction.toUpperCase();
        this.elClueCat.textContent = word.category;
        this.elClueLength.textContent = `${word.length} letters`;
        this.elClueText.textContent = word.clue;
        this.elMaskedPattern.textContent = word.masked_pattern;

        // Clear and focus input
        this.elAnswerInput.value = "";
        this.elAnswerInput.placeholder = `Enter answer for ${word.clue_number} ${word.direction.toUpperCase()} (${word.length} letters)...`;
        this.elAnswerInput.focus();

        // Update active class in clue list
        document.querySelectorAll(".clue-item").forEach(el => el.classList.remove("active"));
        const activeListItem = document.getElementById(`clue-list-item-${word.id}`);
        if (activeListItem) {
            activeListItem.classList.add("active");
            activeListItem.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }

        // Switch to the matching tab if needed
        if (word.direction.toLowerCase() === "across") {
            document.querySelector('[data-tab="across"]')?.click();
        } else {
            document.querySelector('[data-tab="down"]')?.click();
        }
    }

    async handleSubmit() {
        if (!this.activeWord) {
            window.App?.showToast("Please select a word on the crossword grid first.", "warning");
            return;
        }

        const rawAnswer = this.elAnswerInput.value.trim();
        if (!rawAnswer) {
            this.shakeElement(this.elAnswerInput);
            window.App?.showToast("Please enter an answer before submitting.", "warning");
            return;
        }

        this.elSubmitBtn.disabled = true;
        this.elSubmitBtn.textContent = "Verifying...";

        try {
            const res = await API.submitAnswer(this.sessionId, this.activeWord.id, rawAnswer);

            if (res.correct) {
                window.soundEngine?.playCorrect();
                window.App?.showToast(res.message, "success");

                // Update Grid Letters & Word State
                this.grid.updateLetters(res.newly_revealed_cells);
                this.grid.markWordSolved(res.word_id);

                // Update Local State
                this.state.score = res.score;
                this.state.solved_words_count = res.solved_words_count;
                this.state.remaining_attempts = res.remaining_attempts;
                
                // Update Word in state list
                const wObj = this.state.words.find(w => w.id === res.word_id);
                if (wObj) {
                    wObj.is_solved = true;
                    wObj.masked_pattern = res.revealed_word;
                }

                // Update Masked Pattern on active card
                this.elMaskedPattern.textContent = res.revealed_word || rawAnswer.toUpperCase();
                this.elAnswerInput.value = "";

                this.updateHUD();
                this.renderClueLists();

                if (res.is_game_won) {
                    this.handleWin(res);
                } else {
                    // Auto-advance to next unsolved word
                    setTimeout(() => this.selectNextUnsolvedWord(), 600);
                }
            } else {
                window.soundEngine?.playWrong();
                this.shakeElement(this.elAnswerInput);
                window.App?.showToast(res.message, "error");

                this.state.remaining_attempts = res.remaining_attempts;
                this.state.score = res.score;
                this.updateHUD();

                if (res.is_game_over) {
                    this.handleGameOver(res.message);
                }
            }
        } catch (err) {
            window.App?.showToast(err.message || "Failed to submit answer.", "error");
        } finally {
            this.elSubmitBtn.disabled = false;
            this.elSubmitBtn.textContent = "Submit Answer";
        }
    }

    async handleHint() {
        if (!this.activeWord) {
            window.App?.showToast("Select a word to request a hint.", "warning");
            return;
        }

        if (this.state.remaining_hints <= 0) {
            window.App?.showToast("No hints remaining!", "warning");
            return;
        }

        this.elHintBtn.disabled = true;

        try {
            const res = await API.requestHint(this.sessionId, this.activeWord.id);
            if (res.success) {
                window.soundEngine?.playHint();
                window.App?.showToast(res.message, "info");

                if (res.revealed_cell) {
                    this.grid.updateLetters([res.revealed_cell]);
                }

                this.state.remaining_hints = res.remaining_hints;
                this.state.score = res.score;
                this.updateHUD();

                // Refresh masked pattern
                const updatedState = await API.getGameState(this.sessionId);
                this.state.words = updatedState.words;
                const active = this.state.words.find(w => w.id === this.activeWord.id);
                if (active) {
                    this.elMaskedPattern.textContent = active.masked_pattern;
                }
                this.renderClueLists();
            } else {
                window.App?.showToast(res.message, "warning");
            }
        } catch (err) {
            window.App?.showToast(err.message || "Could not use hint.", "error");
        } finally {
            if (this.state.remaining_hints > 0) {
                this.elHintBtn.disabled = false;
            }
        }
    }

    selectNextUnsolvedWord() {
        const nextUnsolved = this.state.words.find(w => !w.is_solved);
        if (nextUnsolved) {
            this.grid.selectWord(nextUnsolved.id);
        }
    }

    shakeElement(el) {
        el.classList.remove("shake-anim");
        void el.offsetWidth; // Trigger reflow
        el.classList.add("shake-anim");
    }

    handleWin(res) {
        if (this.timerInterval) clearInterval(this.timerInterval);
        window.soundEngine?.playWin();
        window.App?.triggerConfetti();

        const bd = res.score_breakdown || {};
        window.App?.showWinModal({
            score: res.score,
            baseScore: bd.base_score || 0,
            timeBonus: bd.time_bonus || 0,
            attemptPenalty: bd.attempt_penalty || 0,
            hintPenalty: bd.hint_penalty || 0,
            remainingTime: this.elTimer.textContent,
            attemptsUsed: this.state.max_attempts - res.remaining_attempts,
            hintsUsed: this.state.max_hints - this.state.remaining_hints,
            wordsSolved: res.solved_words_count
        });
    }

    handleGameOver(reason) {
        if (this.timerInterval) clearInterval(this.timerInterval);
        window.soundEngine?.playGameOver();
        window.App?.showGameOverModal({
            title: "GAME OVER",
            reason: reason || "You have exhausted all your attempts.",
            score: this.state.score,
            wordsSolved: this.state.solved_words_count,
            totalWords: this.state.total_words
        });
    }

    handleTimeUp() {
        window.soundEngine?.playGameOver();
        window.App?.showGameOverModal({
            title: "⏰ TIME'S UP!",
            reason: "The 10-minute challenge countdown has ended.",
            score: this.state.score,
            wordsSolved: this.state.solved_words_count,
            totalWords: this.state.total_words
        });
    }
}

window.GameManager = GameManager;
