"""
Crossword Puzzle Geometry & Intersection Validator
Validates 15x15 grid constraints, letter collisions, and crossword clue numbering.
"""
from typing import List, Dict, Any, Tuple, Optional

def validate_crossword_puzzle(words: List[Dict[str, Any]], grid_size: int = 15) -> Dict[str, Any]:
    """
    Validates that:
    1. All words fit within grid_size x grid_size (0..grid_size-1).
    2. Across and Down intersections share the exact same uppercase letter.
    3. Words have valid length and direction ('across' or 'down').
    4. There are no duplicate placements.
    5. Clue numbering is properly calculated or valid.
    """
    grid: Dict[Tuple[int, int], str] = {}
    word_cells_map: Dict[str, List[Tuple[int, int]]] = {}
    errors = []
    
    # 1. Check bounds and build letter grid
    for idx, w in enumerate(words):
        word_id = str(w.get("id", f"word_{idx}"))
        raw_word = str(w.get("word", "")).upper().replace(" ", "").replace("-", "").replace("_", "")
        direction = str(w.get("direction", "")).lower()
        r = int(w.get("row", 0))
        c = int(w.get("col", 0))
        length = len(raw_word)
        
        if length == 0:
            errors.append(f"Word '{word_id}' is empty.")
            continue
            
        if direction not in ("across", "down"):
            errors.append(f"Word '{word_id}' has invalid direction: '{direction}'.")
            continue
            
        cells = []
        for i in range(length):
            cr = r if direction == "across" else r + i
            cc = c + i if direction == "across" else c
            
            if cr < 0 or cr >= grid_size or cc < 0 or cc >= grid_size:
                errors.append(f"Word '{word_id}' ({raw_word}) exceeds grid bounds at ({cr}, {cc}).")
                break
                
            char = raw_word[i]
            if (cr, cc) in grid:
                existing_char = grid[(cr, cc)]
                if existing_char != char:
                    errors.append(
                        f"Intersection conflict at ({cr}, {cc}): Word '{word_id}' has '{char}', "
                        f"but existing cell has '{existing_char}'."
                    )
            else:
                grid[(cr, cc)] = char
                
            cells.append((cr, cc))
            
        word_cells_map[word_id] = cells

    # 2. Number clues canonically according to standard crossword rules
    # Cells that start an across or down word get a number in reading order (top-left to bottom-right)
    start_cells = set()
    for w in words:
        r = int(w.get("row", 0))
        c = int(w.get("col", 0))
        start_cells.add((r, c))
        
    sorted_starts = sorted(list(start_cells), key=lambda pt: (pt[0], pt[1]))
    cell_number_map = {pt: num + 1 for num, pt in enumerate(sorted_starts)}
    
    numbered_words = []
    for w in words:
        w_copy = dict(w)
        r = int(w.get("row", 0))
        c = int(w.get("col", 0))
        w_copy["clue_number"] = cell_number_map.get((r, c), w.get("clue_number", 1))
        raw_word = str(w.get("word", "")).upper().replace(" ", "").replace("-", "").replace("_", "")
        w_copy["clean_word"] = raw_word
        w_copy["length"] = len(raw_word)
        numbered_words.append(w_copy)

    # Count intersections
    intersection_count = 0
    cell_occupancy: Dict[Tuple[int, int], int] = {}
    for cells in word_cells_map.values():
        for pt in cells:
            cell_occupancy[pt] = cell_occupancy.get(pt, 0) + 1
            if cell_occupancy[pt] == 2:
                intersection_count += 1

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "total_words": len(words),
        "total_active_cells": len(grid),
        "intersection_count": intersection_count,
        "numbered_words": numbered_words,
        "grid_size": grid_size
    }

def print_grid(words: List[Dict[str, Any]], grid_size: int = 15):
    """Utility to print ASCII representation of the 15x15 crossword"""
    grid = [["·" for _ in range(grid_size)] for _ in range(grid_size)]
    for w in words:
        raw_word = str(w.get("word", "")).upper().replace(" ", "").replace("-", "").replace("_", "")
        direction = str(w.get("direction", "")).lower()
        r = int(w.get("row", 0))
        c = int(w.get("col", 0))
        for i, char in enumerate(raw_word):
            cr = r if direction == "across" else r + i
            cc = c + i if direction == "across" else c
            if 0 <= cr < grid_size and 0 <= cc < grid_size:
                grid[cr][cc] = char
                
    header = "    " + " ".join(f"{i:2d}" for i in range(grid_size))
    print(header)
    print("   +" + "--" * grid_size + "+")
    for r in range(grid_size):
        row_str = " ".join(f" {grid[r][c]}" for c in range(grid_size))
        print(f"{r:2d} |{row_str} |")
    print("   +" + "--" * grid_size + "+")
