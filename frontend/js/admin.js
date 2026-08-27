/**
 * Event Organizer / Admin Component
 */
class AdminManager {
    constructor() {
        this.elSessionsBody = document.getElementById("admin-sessions-tbody");
        this.elResetBtn = document.getElementById("btn-admin-reset-lb");
        this.elReseedBtn = document.getElementById("btn-admin-reseed");
        this.elRefreshBtn = document.getElementById("btn-admin-refresh");

        this.bindEvents();
    }

    bindEvents() {
        if (this.elResetBtn) {
            this.elResetBtn.addEventListener("click", () => this.handleResetLeaderboard());
        }
        if (this.elReseedBtn) {
            this.elReseedBtn.addEventListener("click", () => this.handleReseedPuzzles());
        }
        if (this.elRefreshBtn) {
            this.elRefreshBtn.addEventListener("click", () => this.refreshSessions());
        }
    }

    async handleResetLeaderboard() {
        if (!confirm("Are you sure you want to reset the event leaderboard? This cannot be undone.")) {
            return;
        }

        try {
            const res = await API.resetLeaderboard();
            window.App?.showToast(res.message || "Leaderboard cleared.", "success");
            window.leaderboardManager?.refresh();
        } catch (err) {
            window.App?.showToast(err.message || "Failed to reset leaderboard.", "error");
        }
    }

    async handleReseedPuzzles() {
        try {
            const res = await API.reseedPuzzles();
            window.App?.showToast(res.message || "Puzzles re-seeded.", "success");
            window.App?.loadPuzzleSelect();
        } catch (err) {
            window.App?.showToast(err.message || "Failed to re-seed puzzles.", "error");
        }
    }

    async refreshSessions() {
        if (!this.elSessionsBody) return;
        this.elSessionsBody.innerHTML = `<tr><td colspan="7" class="text-center py-4 text-muted">Loading player sessions...</td></tr>`;

        try {
            const sessions = await API.getRecentSessions();
            if (!sessions || sessions.length === 0) {
                this.elSessionsBody.innerHTML = `<tr><td colspan="7" class="text-center py-4 text-muted">No active or past sessions found.</td></tr>`;
                return;
            }

            this.elSessionsBody.innerHTML = "";
            sessions.forEach(s => {
                const tr = document.createElement("tr");
                let statusBadge = `<span class="badge-status badge-${s.status}">${s.status}</span>`;
                
                tr.innerHTML = `
                    <td class="font-bold">${this.escapeHtml(s.player_name)}</td>
                    <td>${this.escapeHtml(s.puzzle_id)}</td>
                    <td>${s.difficulty}</td>
                    <td>${statusBadge}</td>
                    <td class="font-mono text-cyan">${s.score}</td>
                    <td>${s.words_solved_count}</td>
                    <td class="text-xs text-muted">${new Date(s.start_time).toLocaleTimeString()}</td>
                `;
                this.elSessionsBody.appendChild(tr);
            });
        } catch (err) {
            this.elSessionsBody.innerHTML = `<tr><td colspan="7" class="text-center py-4 text-danger">Failed to load sessions.</td></tr>`;
        }
    }

    escapeHtml(text) {
        if (!text) return "";
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }
}

window.AdminManager = AdminManager;
