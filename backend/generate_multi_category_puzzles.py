"""
Deterministic Multi-Category Crossword Puzzle Generator
Generates 15x15 grids with exactly 10 questions mixing AI/ML, Data Science, IoT, and Core CSE with 10-min timer.
"""
import json
import random
from typing import List, Dict, Any, Optional
from backend.builder_engine import VOCABULARY, CAT_AIML, CAT_DATASCIENCE, CAT_IOT, CAT_CORECSE
from backend.puzzle_validator import validate_crossword_puzzle, print_grid

def generate_multi_category_puzzle(
    title: str,
    description: str,
    difficulty: str,
    category_filter: Optional[List[str]] = None,
    target_words: int = 10,
    time_limit_sec: int = 600,
    max_attempts: int = 3,
    max_hints: int = 3,
    seed: int = 42
) -> Optional[Dict[str, Any]]:
    random.seed(seed)
    
    # Filter words if category_filter is specified
    if category_filter:
        word_pool = [k for k, v in VOCABULARY.items() if v[2] in category_filter]
    else:
        word_pool = list(VOCABULARY.keys())
        
    for attempt in range(4000):
        grid = {}
        placed = []
        used_words = set()
        
        # Pick anchor word
        long_anchors = [w for w in word_pool if len(w) >= 7]
        if not long_anchors:
            long_anchors = word_pool
        start_word = random.choice(long_anchors)
        
        start_r = random.choice([0, 2, 4, 6])
        start_c = random.randint(0, max(0, 15 - len(start_word)))
        
        for i, ch in enumerate(start_word):
            grid[(start_r, start_c + i)] = ch
        placed.append({"id": f"w1", "word": start_word, "direction": "across", "row": start_r, "col": start_c})
        used_words.add(start_word)
        
        for _ in range(50):
            if not placed or len(placed) >= target_words:
                break
            ref = random.choice(placed)
            ref_dir = ref["direction"]
            target_dir = "down" if ref_dir == "across" else "across"
            ref_word = ref["word"]
            
            char_idx = random.randint(0, len(ref_word) - 1)
            char = ref_word[char_idx]
            
            pivot_r = ref["row"] + (0 if ref_dir == "across" else char_idx)
            pivot_c = ref["col"] + (char_idx if ref_dir == "across" else 0)
            
            candidates = [w for w in word_pool if w not in used_words and char in w]
            random.shuffle(candidates)
            
            for cand in candidates:
                cpos_list = [i for i, c in enumerate(cand) if c == char]
                random.shuffle(cpos_list)
                for cpos in cpos_list:
                    cand_r = pivot_r - cpos if target_dir == "down" else pivot_r
                    cand_c = pivot_c if target_dir == "down" else pivot_c - cpos
                    l = len(cand)
                    
                    if cand_r < 0 or cand_c < 0:
                        continue
                    if target_dir == "across" and cand_c + l > 15:
                        continue
                    if target_dir == "down" and cand_r + l > 15:
                        continue
                        
                    # Boundary check
                    valid = True
                    has_intersect = False
                    if target_dir == "across":
                        if cand_c > 0 and (cand_r, cand_c - 1) in grid: valid = False
                        if cand_c + l < 15 and (cand_r, cand_c + l) in grid: valid = False
                    else:
                        if cand_r > 0 and (cand_r - 1, cand_c) in grid: valid = False
                        if cand_r + l < 15 and (cand_r + l, cand_c) in grid: valid = False
                        
                    if not valid:
                        continue
                        
                    for i, ch in enumerate(cand):
                        pos = (cand_r, cand_c + i) if target_dir == "across" else (cand_r + i, cand_c)
                        if pos in grid:
                            if grid[pos] != ch:
                                valid = False
                                break
                            has_intersect = True
                            
                    if valid and has_intersect:
                        for i, ch in enumerate(cand):
                            pos = (cand_r, cand_c + i) if target_dir == "across" else (cand_r + i, cand_c)
                            grid[pos] = ch
                        placed.append({
                            "id": f"w{len(placed)+1}",
                            "word": cand,
                            "direction": target_dir,
                            "row": cand_r,
                            "col": cand_c
                        })
                        used_words.add(cand)
                        break
                if cand in used_words or len(placed) >= target_words:
                    break

        if len(placed) == target_words:
            val = validate_crossword_puzzle(placed, 15)
            if val["valid"] and val["intersection_count"] >= target_words - 2:
                words_data = []
                for item in val["numbered_words"]:
                    raw = item["word"]
                    info = VOCABULARY.get(raw, (raw, f"Concept clue for {raw}", "AI / ML"))
                    words_data.append({
                        "id": item["id"],
                        "clue_number": item["clue_number"],
                        "word": raw,
                        "display_name": info[0],
                        "clue": info[1],
                        "category": info[2],
                        "direction": item["direction"],
                        "row": item["row"],
                        "col": item["col"],
                        "length": item["length"]
                    })
                return {
                    "id": f"puzzle_{difficulty.lower()}_{seed}",
                    "title": title,
                    "description": description,
                    "difficulty": difficulty,
                    "grid_size": 15,
                    "time_limit": time_limit_sec,
                    "max_attempts": max_attempts,
                    "max_hints": max_hints,
                    "words": words_data,
                    "active_cells_count": val["total_active_cells"],
                    "intersections_count": val["intersection_count"]
                }
    return None

if __name__ == "__main__":
    configs = [
        ("Engineering Day Grand Mix (AI/ML + DS + IoT + CSE)", "The flagship multi-category tournament challenge featuring 10 questions mixed across AI/ML, Data Science, IoT, and Core CSE.", "Hard", None, 101),
        ("AI, Machine Learning & Data Science Challenge", "10 conceptual questions spanning Deep Learning, Neural Networks, Clustering, Regression, and PCA.", "Medium", [CAT_AIML, CAT_DATASCIENCE], 202),
        ("IoT & Computer Systems Engineering", "10 systems-level questions exploring Sensors, Microcontrollers, Deadlock, Threads, MQTT, and Caching.", "Easy", [CAT_IOT, CAT_CORECSE, CAT_DATASCIENCE], 303),
    ]

    all_puzzles = []
    for title, desc, diff, cats, s in configs:
        p = None
        for seed_attempt in range(s, s + 300):
            p = generate_multi_category_puzzle(title, desc, diff, cats, target_words=10, time_limit_sec=600, seed=seed_attempt)
            if p:
                break
        if p:
            print(f"✓ Generated {p['title']} with {len(p['words'])} questions and {p['intersections_count']} intersections.")
            print_grid(p["words"], 15)
            # Scope word IDs
            for idx, w in enumerate(p["words"]):
                w["id"] = f"{p['id']}_w{idx+1}"
            all_puzzles.append(p)
        else:
            print(f"✗ Failed for {title}")

    with open("data/seed_puzzles.json", "w") as f:
        json.dump(all_puzzles, f, indent=2)
    print(f"Successfully saved {len(all_puzzles)} verified 10-question tournament puzzles to data/seed_puzzles.json")
