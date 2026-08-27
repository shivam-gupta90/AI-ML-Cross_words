/**
 * Leaderboard Component & View Manager
 */
class LeaderboardManager {
    constructor() {
        this.elTableBody = document.getElementById("leaderboard-tbody");
        this.elTotalCompletions = document.getElementById("lb-stat-completions");
        this.elHighScore = document.getElementById("lb-stat-highscore");
        this.elTopPlayer = document.getElementById("lb-stat-top-player");
        this.elDifficultyFilter = document.getElementById("lb-filter-difficulty");
        this.elPuzzleFilter = document.getElementById("lb-filter-puzzle");

        this.bindEvents();
    }

    bindEvents() {
        if (this.elDifficultyFilter) {
            this.elDifficultyFilter.addEventListener("change", () => this.refresh());
        }
        if (this.elPuzzleFilter) {
            this.elPuzzleFilter.addEventListener("change", () => this.refresh());
        }
    }

    async refresh() {
        if (!this.elTableBody) return;

        this.elTableBody.innerHTML = `<tr><td colspan="8" class="text-center py-6 text-muted">Loading leaderboard data...</td></tr>`;

        try {
            const diff = this.elDifficultyFilter?.value || "";
            const puzzleId = this.elPuzzleFilter?.value || "";

            const [entries, stats] = await Promise.all([
                API.getLeaderboard(puzzleId || null, diff || null),
                API.getLeaderboardStats()
            ]);

            if (this.elTotalCompletions) this.elTotalCompletions.textContent = stats.total_completions || 0;
            if (this.elHighScore) this.elHighScore.textContent = (stats.high_score || 0).toLocaleString();
            if (this.elTopPlayer) this.elTopPlayer.textContent = stats.top_player || "None yet";

            if (!entries || entries.length === 0) {
                this.elTableBody.innerHTML = `
                    <tr>
                        <td colspan="8" class="text-center py-8 text-muted">
                            <div class="empty-state">
                                <span class="empty-icon">🏆</span>
                                <p>No completions recorded yet for this filter.</p>
                                <p class="text-sm">Be the first to finish the challenge and claim rank #1!</p>
                            </div>
                        </td>
                    </tr>
                `;
                return;
            }

            this.elTableBody.innerHTML = "";
            entries.forEach(item => {
                const tr = document.createElement("tr");
                if (item.rank === 1) tr.className = "rank-gold";
                else if (item.rank === 2) tr.className = "rank-silver";
                else if (item.rank === 3) tr.className = "rank-bronze";

                let rankBadge = `<span class="rank-num">#${item.rank}</span>`;
                if (item.rank === 1) rankBadge = `<span class="medal-badge medal-gold">🥇 1</span>`;
                else if (item.rank === 2) rankBadge = `<span class="medal-badge medal-silver">🥈 2</span>`;
                else if (item.rank === 3) rankBadge = `<span class="medal-badge medal-bronze">🥉 3</span>`;

                tr.innerHTML = `
                    <td class="col-rank">${rankBadge}</td>
                    <td class="col-player font-bold">${this.escapeHtml(item.player_name)}</td>
                    <td class="col-puzzle">${this.escapeHtml(item.puzzle_title)}</td>
                    <td class="col-diff"><span class="badge-diff badge-${item.difficulty.toLowerCase()}">${item.difficulty}</span></td>
                    <td class="col-score font-mono text-cyan">${item.score.toLocaleString()}</td>
                    <td class="col-time font-mono">⏱ ${item.time_taken_formatted}</td>
                    <td class="col-stats text-sm">${item.attempts_used} att &bull; ${item.hints_used} hint</td>
                    <td class="col-date text-xs text-muted">${item.completed_at}</td>
                `;
                this.elTableBody.appendChild(tr);
            });
        } catch (err) {
            console.error("Leaderboard error:", err);
            this.elTableBody.innerHTML = `<tr><td colspan="8" class="text-center py-6 text-danger">Failed to load leaderboard.</td></tr>`;
        }
    }

    escapeHtml(text) {
        if (!text) return "";
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }
}

window.LeaderboardManager = LeaderboardManager;
