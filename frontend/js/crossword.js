/**
 * Crossword Grid Component & Interactive Renderer
 */
class CrosswordGrid {
    constructor(containerElement, onSelectWordCallback) {
        this.container = containerElement;
        this.onSelectWord = onSelectWordCallback;
        
        this.gridSize = 15;
        this.gridData = []; // 2D array of PublicGridCell
        this.wordsData = []; // list of PublicWordClue
        this.selectedWordId = null;
        this.selectedCellPos = null; // {row, col}
        this.cellElements = {}; // "r,c" -> DOM element
        
        this.initKeyboardEvents();
    }

    render(gridSize, gridData, wordsData, defaultSelectedWordId = null) {
        this.gridSize = gridSize || 15;
        this.gridData = gridData;
        this.wordsData = wordsData;
        this.cellElements = {};
        this.container.innerHTML = "";
        
        this.container.style.gridTemplateColumns = `repeat(${this.gridSize}, 1fr)`;
        this.container.style.gridTemplateRows = `repeat(${this.gridSize}, 1fr)`;

        for (let r = 0; r < this.gridSize; r++) {
            for (let c = 0; c < this.gridSize; c++) {
                const cellData = gridData[r][c];
                const cellEl = document.createElement("div");
                cellEl.className = "crossword-cell";
                cellEl.dataset.row = r;
                cellEl.dataset.col = c;

                if (cellData.is_blocked) {
                    cellEl.classList.add("cell-blocked");
                } else {
                    cellEl.classList.add("cell-active");

                    // Clue Number Label
                    if (cellData.clue_number) {
                        const numEl = document.createElement("span");
                        numEl.className = "cell-number";
                        numEl.textContent = cellData.clue_number;
                        cellEl.appendChild(numEl);
                    }

                    // Letter Container
                    const letterEl = document.createElement("span");
                    letterEl.className = "cell-letter";
                    letterEl.textContent = cellData.char || "";
                    cellEl.appendChild(letterEl);

                    if (cellData.char) {
                        cellEl.classList.add("has-letter");
                    }

                    // Cell Click Listener
                    cellEl.addEventListener("click", () => this.handleCellClick(r, c));
                }

                this.cellElements[`${r},${c}`] = cellEl;
                this.container.appendChild(cellEl);
            }
        }

        // Auto-select initial word
        if (defaultSelectedWordId) {
            this.selectWord(defaultSelectedWordId);
        } else if (wordsData && wordsData.length > 0) {
            this.selectWord(wordsData[0].id);
        }
    }

    handleCellClick(row, col) {
        const cellData = this.gridData[row]?.[col];
        if (!cellData || cellData.is_blocked || !cellData.word_ids || cellData.word_ids.length === 0) {
            return;
        }

        window.soundEngine?.playSelect();

        // If clicking on an intersection of the current word, toggle between Across and Down
        if (this.selectedWordId && cellData.word_ids.includes(this.selectedWordId) && cellData.word_ids.length > 1) {
            const nextWordId = cellData.word_ids.find(id => id !== this.selectedWordId);
            this.selectWord(nextWordId, { row, col });
            return;
        }

        // Otherwise select the primary word for this cell
        const targetWordId = cellData.word_ids[0];
        this.selectWord(targetWordId, { row, col });
    }

    selectWord(wordId, focusPos = null) {
        const word = this.wordsData.find(w => w.id === wordId);
        if (!word) return;

        this.selectedWordId = wordId;
        this.selectedCellPos = focusPos || { row: word.row, col: word.col };

        this.updateHighlights();

        if (this.onSelectWord) {
            this.onSelectWord(word);
        }
    }

    updateHighlights() {
        const word = this.wordsData.find(w => w.id === this.selectedWordId);
        if (!word) return;

        // Clear previous highlight classes
        Object.values(this.cellElements).forEach(el => {
            el.classList.remove("cell-highlight-word", "cell-focus");
        });

        // Compute cells belonging to selected word
        const dir = word.direction.toLowerCase();
        for (let i = 0; i < word.length; i++) {
            const cr = dir === "across" ? word.row : word.row + i;
            const cc = dir === "across" ? word.col + i : word.col;
            const el = this.cellElements[`${cr},${cc}`];
            if (el) {
                el.classList.add("cell-highlight-word");
                if (this.selectedCellPos && this.selectedCellPos.row === cr && this.selectedCellPos.col === cc) {
                    el.classList.add("cell-focus");
                }
            }
        }
    }

    updateLetters(newlyRevealedCells) {
        if (!newlyRevealedCells || newlyRevealedCells.length === 0) return;

        newlyRevealedCells.forEach(item => {
            const { row, col, char } = item;
            const el = this.cellElements[`${row},${col}`];
            if (el) {
                const letterSpan = el.querySelector(".cell-letter");
                if (letterSpan) {
                    letterSpan.textContent = char;
                    el.classList.add("has-letter", "cell-just-revealed");
                    setTimeout(() => {
                        el.classList.remove("cell-just-revealed");
                    }, 1200);
                }
                if (this.gridData[row] && this.gridData[row][col]) {
                    this.gridData[row][col].char = char;
                }
            }
        });
    }

    markWordSolved(wordId) {
        const word = this.wordsData.find(w => w.id === wordId);
        if (!word) return;
        word.is_solved = true;

        const dir = word.direction.toLowerCase();
        for (let i = 0; i < word.length; i++) {
            const cr = dir === "across" ? word.row : word.row + i;
            const cc = dir === "across" ? word.col + i : word.col;
            const el = this.cellElements[`${cr},${cc}`];
            if (el) {
                el.classList.add("cell-solved");
            }
        }
    }

    initKeyboardEvents() {
        window.addEventListener("keydown", (e) => {
            // Don't intercept if typing inside an active text input or textarea
            const isTyping = ["INPUT", "TEXTAREA"].includes(document.activeElement?.tagName);
            if (isTyping && e.key !== "Tab" && e.key !== "Escape") {
                return;
            }

            if (!this.selectedWordId || !this.selectedCellPos) return;

            if (e.key === "ArrowRight") {
                this.moveCursor(0, 1);
                e.preventDefault();
            } else if (e.key === "ArrowLeft") {
                this.moveCursor(0, -1);
                e.preventDefault();
            } else if (e.key === "ArrowDown") {
                this.moveCursor(1, 0);
                e.preventDefault();
            } else if (e.key === "ArrowUp") {
                this.moveCursor(-1, 0);
                e.preventDefault();
            } else if (e.key === " " && !isTyping) {
                // Space toggles direction on intersection
                this.handleCellClick(this.selectedCellPos.row, this.selectedCellPos.col);
                e.preventDefault();
            } else if (e.key === "Tab") {
                // Tab jumps to next/prev clue
                e.preventDefault();
                this.cycleWord(e.shiftKey ? -1 : 1);
            }
        });
    }

    moveCursor(dr, dc) {
        let nr = this.selectedCellPos.row + dr;
        let nc = this.selectedCellPos.col + dc;

        if (nr >= 0 && nr < this.gridSize && nc >= 0 && nc < this.gridSize) {
            const cell = this.gridData[nr][nc];
            if (!cell.is_blocked && cell.word_ids && cell.word_ids.length > 0) {
                // If the new cell belongs to the current word, keep word and move cursor
                if (cell.word_ids.includes(this.selectedWordId)) {
                    this.selectedCellPos = { row: nr, col: nc };
                    this.updateHighlights();
                } else {
                    // Switch to the first word in that cell
                    this.selectWord(cell.word_ids[0], { row: nr, col: nc });
                }
            }
        }
    }

    cycleWord(delta) {
        if (!this.wordsData || this.wordsData.length === 0) return;
        const currentIdx = this.wordsData.findIndex(w => w.id === this.selectedWordId);
        let nextIdx = (currentIdx + delta + this.wordsData.length) % this.wordsData.length;
        this.selectWord(this.wordsData[nextIdx].id);
    }
}

window.CrosswordGrid = CrosswordGrid;
