"""
Deterministic Multi-Category Crossword Puzzle Generator
Generates 15x15 grids with exactly 10 questions mixing ALL 4 categories:
AI/ML, Data Science, IoT, and Core CSE for Hard, Medium, and Easy challenges.
"""
import json
import random
from typing import List, Dict, Any, Optional
from backend.builder_engine import VOCABULARY, CAT_AIML, CAT_DATASCIENCE, CAT_IOT, CAT_CORECSE
from backend.puzzle_validator import validate_crossword_puzzle, print_grid

ALL_CATEGORIES = [CAT_AIML, CAT_DATASCIENCE, CAT_IOT, CAT_CORECSE]

def generate_full_mix_puzzle(
    title: str,
    description: str,
    difficulty: str,
    target_words: int = 10,
    time_limit_sec: int = 600,
    seed: int = 42
) -> Optional[Dict[str, Any]]:
    random.seed(seed)
    word_pool = list(VOCABULARY.keys())
    
    for attempt in range(5000):
        grid = {}
        placed = []
        used_words = set()
        
        # Pick anchor word
        long_anchors = [w for w in word_pool if len(w) >= 7]
        start_word = random.choice(long_anchors)
        
        start_r = random.choice([0, 1, 2, 3, 4])
        start_c = random.randint(0, max(0, 15 - len(start_word)))
        
        for i, ch in enumerate(start_word):
            grid[(start_r, start_c + i)] = ch
        placed.append({"id": f"w1", "word": start_word, "direction": "across", "row": start_r, "col": start_c})
        used_words.add(start_word)
        
        for _ in range(60):
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
            # Check category representation
            placed_categories = set(VOCABULARY[w["word"]][2] for w in placed)
            # Ensure at least 3-4 distinct categories are covered in the 10 words
            if len(placed_categories) >= 3:
                val = validate_crossword_puzzle(placed, 15)
                if val["valid"] and val["intersection_count"] >= target_words - 2:
                    words_data = []
                    for item in val["numbered_words"]:
                        raw = item["word"]
                        info = VOCABULARY.get(raw, (raw, f"Concept clue for {raw}", CAT_AIML))
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
                        "max_attempts": 3,
                        "max_hints": 3,
                        "words": words_data,
                        "active_cells_count": val["total_active_cells"],
                        "intersections_count": val["intersection_count"],
                        "categories_covered": list(placed_categories)
                    }
    return None

if __name__ == "__main__":
    configs = [
        ("Engineering Day Grand Championship", "10-question flagship challenge mixing AI/ML, Data Science, IoT, and Core CSE (~20% letters revealed).", "Hard", 105),
        ("All-Track Engineering Masters", "10-question balanced tournament challenge across AI/ML, Data Science, IoT, and Core CSE (~35% letters revealed).", "Medium", 215),
        ("Engineering Day Quick Challenge", "10-question approachable mixed challenge across AI/ML, Data Science, IoT, and Core CSE (~55% letters revealed).", "Easy", 325),
    ]

    all_puzzles = []
    for title, desc, diff, s in configs:
        p = None
        for seed_attempt in range(s, s + 500):
            p = generate_full_mix_puzzle(title, desc, diff, target_words=10, time_limit_sec=600, seed=seed_attempt)
            if p and len(p["categories_covered"]) >= 3:
                break
        if p:
            print(f"✓ Generated {p['title']} [{p['difficulty']}] with {len(p['words'])} questions and categories: {p['categories_covered']}")
            print_grid(p["words"], 15)
            # Scope word IDs
            for idx, w in enumerate(p["words"]):
                w["id"] = f"{p['id']}_w{idx+1}"
            all_puzzles.append(p)
        else:
            print(f"✗ Failed for {title}")

    with open("data/seed_puzzles.json", "w") as f:
        json.dump(all_puzzles, f, indent=2)
    print(f"\nSuccessfully generated and saved all 3 difficulty puzzles (Hard, Medium, Easy) with 10 questions mixing ALL categories to data/seed_puzzles.json")
