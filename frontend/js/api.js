/**
 * REST API Client for AI/ML Crossword Challenge
 */
const API_BASE = "";

const API = {
    async request(endpoint, options = {}) {
        const url = `${API_BASE}${endpoint}`;
        const headers = {
            "Content-Type": "application/json",
            ...(options.headers || {})
        };

        try {
            const response = await fetch(url, { ...options, headers });
            const data = await response.json();

            if (!response.ok) {
                const errorDetail = data.detail || data.message || "An unexpected error occurred.";
                const error = new Error(typeof errorDetail === "string" ? errorDetail : JSON.stringify(errorDetail));
                error.status = response.status;
                error.data = data;
                throw error;
            }

            return data;
        } catch (err) {
            console.error(`API Error on ${endpoint}:`, err);
            throw err;
        }
    },

    // Puzzles
    async getPuzzles() {
        return this.request("/api/puzzles");
    },

    async getPuzzle(puzzleId) {
        return this.request(`/api/puzzles/${puzzleId}`);
    },

    // Game
    async startGame(playerName, puzzleId, difficulty = "Medium") {
        return this.request("/api/game/start", {
            method: "POST",
            body: JSON.stringify({
                player_name: playerName,
                puzzle_id: puzzleId,
                difficulty: difficulty
            })
        });
    },

    async getGameState(sessionId) {
        return this.request(`/api/game/${sessionId}/state`);
    },

    async submitAnswer(sessionId, wordId, answer) {
        return this.request(`/api/game/${sessionId}/submit`, {
            method: "POST",
            body: JSON.stringify({
                word_id: wordId,
                answer: answer
            })
        });
    },

    async requestHint(sessionId, wordId) {
        return this.request(`/api/game/${sessionId}/hint`, {
            method: "POST",
            body: JSON.stringify({
                word_id: wordId
            })
        });
    },

    async finishGame(sessionId) {
        return this.request(`/api/game/${sessionId}/finish`, {
            method: "POST"
        });
    },

    // Leaderboard
    async getLeaderboard(puzzleId = null, difficulty = null) {
        let qs = "";
        const params = [];
        if (puzzleId) params.push(`puzzle_id=${encodeURIComponent(puzzleId)}`);
        if (difficulty) params.push(`difficulty=${encodeURIComponent(difficulty)}`);
        if (params.length > 0) qs = `?${params.join("&")}`;
        return this.request(`/api/leaderboard${qs}`);
    },

    async getLeaderboardStats() {
        return this.request("/api/leaderboard/stats");
    },

    // Admin
    async resetLeaderboard() {
        return this.request("/api/admin/reset-leaderboard", { method: "POST" });
    },

    async reseedPuzzles() {
        return this.request("/api/admin/reseed-puzzles", { method: "POST" });
    },

    async getRecentSessions() {
        return this.request("/api/admin/sessions");
    }
};

window.API = API;
