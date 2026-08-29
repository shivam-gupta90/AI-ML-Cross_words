/**
 * Main Application Orchestrator & View Controller
 */
class App {
    constructor() {
        this.puzzles = [];
        this.init();
    }

    async init() {
        this.bindGlobalNavigation();
        this.initConfetti();
        await this.loadPuzzleSelect();

        // Instantiate component managers
        window.gameManager = new GameManager();
        window.leaderboardManager = new LeaderboardManager();
        window.adminManager = new AdminManager();
    }

    bindGlobalNavigation() {
        // Landing Screen Buttons
        document.getElementById("btn-start-challenge")?.addEventListener("click", () => this.handleStartChallenge());
        document.getElementById("btn-view-instructions")?.addEventListener("click", () => this.showModal("modal-instructions"));
        document.getElementById("btn-view-leaderboard")?.addEventListener("click", () => this.openLeaderboard());
        document.getElementById("btn-open-admin")?.addEventListener("click", () => this.openAdmin());

        // Header Navigation Buttons (in game screen)
        document.getElementById("nav-btn-instructions")?.addEventListener("click", () => this.showModal("modal-instructions"));
        document.getElementById("nav-btn-leaderboard")?.addEventListener("click", () => this.openLeaderboard());
        document.getElementById("nav-btn-quit")?.addEventListener("click", () => this.confirmQuit());

        // Modal Close Buttons
        document.querySelectorAll(".btn-close-modal, .modal-backdrop").forEach(el => {
            el.addEventListener("click", (e) => {
                if (e.target === el || el.classList.contains("btn-close-modal")) {
                    this.closeAllModals();
                }
            });
        });

        // Win Modal Actions
        document.getElementById("btn-win-leaderboard")?.addEventListener("click", () => {
            this.closeAllModals();
            this.openLeaderboard();
        });
        document.getElementById("btn-win-play-again")?.addEventListener("click", () => {
            this.closeAllModals();
            this.showScreen("screen-start");
        });

        // Game Over Modal Actions
        document.getElementById("btn-gameover-retry")?.addEventListener("click", () => {
            this.closeAllModals();
            this.showScreen("screen-start");
        });
        document.getElementById("btn-gameover-leaderboard")?.addEventListener("click", () => {
            this.closeAllModals();
            this.openLeaderboard();
        });
    }

    async loadPuzzleSelect() {
        const select = document.getElementById("select-puzzle");
        const lbFilter = document.getElementById("lb-filter-puzzle");
        if (!select) return;

        try {
            this.puzzles = await API.getPuzzles();
            select.innerHTML = "";
            if (lbFilter) lbFilter.innerHTML = `<option value="">All Challenges</option>`;

            this.puzzles.forEach(p => {
                const opt = document.createElement("option");
                opt.value = p.id;
                opt.textContent = `${p.title} (${p.difficulty} • ${p.word_count} words)`;
                select.appendChild(opt);

                if (lbFilter) {
                    const lbOpt = document.createElement("option");
                    lbOpt.value = p.id;
                    lbOpt.textContent = p.title;
                    lbFilter.appendChild(lbOpt);
                }
            });

            // Update puzzle info card on change
            select.addEventListener("change", () => this.updateSelectedPuzzlePreview());
            this.updateSelectedPuzzlePreview();
        } catch (err) {
            console.error("Failed to load puzzles:", err);
            this.showToast("Could not connect to backend server. Make sure FastAPI is running.", "error");
        }
    }

    updateSelectedPuzzlePreview() {
        const select = document.getElementById("select-puzzle");
        const previewEl = document.getElementById("selected-puzzle-desc");
        if (!select || !previewEl) return;

        const selected = this.puzzles.find(p => p.id === select.value);
        if (selected) {
            previewEl.textContent = selected.description || `${selected.word_count} interconnected AI/ML terms.`;
        }
    }

    async handleStartChallenge() {
        const nameInput = document.getElementById("player-name-input");
        const puzzleSelect = document.getElementById("select-puzzle");
        const diffSelect = document.getElementById("select-difficulty");

        const playerName = nameInput?.value?.trim();
        if (!playerName) {
            nameInput?.focus();
            nameInput?.classList.add("shake-anim");
            setTimeout(() => nameInput?.classList.remove("shake-anim"), 600);
            this.showToast("Please enter your name or team name to begin!", "warning");
            return;
        }

        const puzzleId = puzzleSelect?.value;
        const difficulty = diffSelect?.value || "Medium";

        const btn = document.getElementById("btn-start-challenge");
        btn.disabled = true;
        btn.textContent = "Loading Challenge Matrix...";

        try {
            window.soundEngine?.init();
            const gameState = await API.startGame(playerName, puzzleId, difficulty);
            
            this.showScreen("screen-game");
            await window.gameManager.loadGameSession(gameState);
        } catch (err) {
            this.showToast(err.message || "Failed to start challenge session.", "error");
        } finally {
            btn.disabled = false;
            btn.textContent = "START CHALLENGE 🚀";
        }
    }

    confirmQuit() {
        if (confirm("Are you sure you want to exit to the main menu? Current session progress will be ended.")) {
            if (window.gameManager?.sessionId) {
                API.finishGame(window.gameManager.sessionId).catch(() => {});
            }
            this.showScreen("screen-start");
        }
    }

    showScreen(screenId) {
        document.querySelectorAll(".app-screen").forEach(s => s.classList.remove("active"));
        const target = document.getElementById(screenId);
        if (target) {
            target.classList.add("active");
            window.scrollTo(0, 0);
        }
    }

    showModal(modalId) {
        this.closeAllModals();
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add("active");
        }
    }

    closeAllModals() {
        document.querySelectorAll(".modal-overlay").forEach(m => m.classList.remove("active"));
    }

    openLeaderboard() {
        this.showModal("modal-leaderboard");
        window.leaderboardManager?.refresh();
    }

    openAdmin() {
        this.showModal("modal-admin");
        window.adminManager?.refreshSessions();
    }

    showWinModal(stats) {
        document.getElementById("win-final-score").textContent = stats.score.toLocaleString();
        document.getElementById("win-base-score").textContent = `+${stats.baseScore}`;
        document.getElementById("win-time-bonus").textContent = `+${stats.timeBonus}`;
        document.getElementById("win-attempt-penalty").textContent = `-${stats.attemptPenalty}`;
        document.getElementById("win-hint-penalty").textContent = `-${stats.hintPenalty}`;
        document.getElementById("win-time-remaining").textContent = stats.remainingTime;
        document.getElementById("win-attempts-used").textContent = `${stats.attemptsUsed}`;
        document.getElementById("win-hints-used").textContent = `${stats.hintsUsed}`;

        this.showModal("modal-win");
    }

    showGameOverModal(info) {
        document.getElementById("gameover-title").textContent = info.title;
        document.getElementById("gameover-reason").textContent = info.reason;
        document.getElementById("gameover-score").textContent = info.score.toLocaleString();
        document.getElementById("gameover-solved-count").textContent = `${info.wordsSolved} / ${info.totalWords}`;

        this.showModal("modal-gameover");
    }

    showToast(message, type = "info") {
        const container = document.getElementById("toast-container");
        if (!container) return;

        const toast = document.createElement("div");
        toast.className = `toast toast-${type} toast-enter`;
        
        let icon = "ℹ️";
        if (type === "success") icon = "✅";
        else if (type === "error") icon = "❌";
        else if (type === "warning") icon = "⚠️";

        toast.innerHTML = `<span class="toast-icon">${icon}</span> <span class="toast-text">${message}</span>`;
        container.appendChild(toast);

        setTimeout(() => {
            toast.classList.remove("toast-enter");
            toast.classList.add("toast-exit");
            setTimeout(() => toast.remove(), 400);
        }, 3500);
    }

    // Confetti System
    initConfetti() {
        this.canvas = document.getElementById("confetti-canvas");
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext("2d");
        this.particles = [];
        this.isConfettiActive = false;

        window.addEventListener("resize", () => {
            if (this.canvas) {
                this.canvas.width = window.innerWidth;
                this.canvas.height = window.innerHeight;
            }
        });
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    triggerConfetti() {
        if (!this.canvas || !this.ctx) return;
        this.particles = [];
        this.isConfettiActive = true;
        const colors = ["#00f0ff", "#a855f7", "#10b981", "#f59e0b", "#ec4899", "#3b82f6", "#ffffff"];

        for (let i = 0; i < 180; i++) {
            this.particles.push({
                x: window.innerWidth / 2,
                y: window.innerHeight / 2,
                vx: (Math.random() - 0.5) * 22,
                vy: (Math.random() - 0.7) * 22,
                size: Math.random() * 8 + 4,
                color: colors[Math.floor(Math.random() * colors.length)],
                rotation: Math.random() * 360,
                rSpeed: (Math.random() - 0.5) * 12,
                gravity: 0.35,
                opacity: 1
            });
        }

        const renderFrame = () => {
            if (!this.isConfettiActive || this.particles.length === 0) {
                this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                return;
            }

            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            this.particles.forEach((p, idx) => {
                p.x += p.vx;
                p.y += p.vy;
                p.vy += p.gravity;
                p.rotation += p.rSpeed;
                p.opacity -= 0.006;

                if (p.opacity <= 0 || p.y > window.innerHeight + 20) {
                    this.particles.splice(idx, 1);
                    return;
                }

                this.ctx.save();
                this.ctx.translate(p.x, p.y);
                this.ctx.rotate((p.rotation * Math.PI) / 180);
                this.ctx.fillStyle = p.color;
                this.ctx.globalAlpha = Math.max(0, p.opacity);
                this.ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
                this.ctx.restore();
            });

            requestAnimationFrame(renderFrame);
        };

        requestAnimationFrame(renderFrame);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    window.App = new App();
});
