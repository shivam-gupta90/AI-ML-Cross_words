"""
Verified Seed Puzzles for AI/ML Crossword Tournament
"""
import json
from typing import List, Dict, Any
from backend.puzzle_validator import validate_crossword_puzzle, print_grid

GRAND_CHAMPIONSHIP_WORDS = [
    # Across
    {
        "id": "champ_a1",
        "word": "BACKPROPAGATION",
        "display_name": "Backpropagation",
        "clue": "Algorithm calculating gradients of the objective function with respect to trainable weights by propagating error signals backward via the calculus chain rule.",
        "category": "Deep Learning",
        "direction": "across",
        "row": 0,
        "col": 0
    },
    {
        "id": "champ_a2",
        "word": "ADAM",
        "display_name": "Adam",
        "clue": "Adaptive moment estimation optimizer computing individual learning rates from exponential moving averages of gradient first and second raw moments.",
        "category": "Optimization",
        "direction": "across",
        "row": 2,
        "col": 0
    },
    {
        "id": "champ_a3",
        "word": "SGD",
        "display_name": "SGD",
        "clue": "Iterative optimization baseline updating weights using loss gradients computed on stochastically sampled mini-batches.",
        "category": "Optimization",
        "direction": "across",
        "row": 3,
        "col": 0
    },
    {
        "id": "champ_a4",
        "word": "RECURRENT",
        "display_name": "Recurrent",
        "clue": "Class of neural network architectures containing cyclic feedback loops in their hidden states to maintain dynamic temporal memory.",
        "category": "Deep Learning",
        "direction": "across",
        "row": 4,
        "col": 3
    },
    {
        "id": "champ_a5",
        "word": "MATRIX",
        "display_name": "Matrix",
        "clue": "Two-dimensional rectangular array of numerical elements representing linear transformations between coordinate spaces.",
        "category": "Mathematics",
        "direction": "across",
        "row": 6,
        "col": 2
    },
    {
        "id": "champ_a6",
        "word": "TOKEN",
        "display_name": "Token",
        "clue": "Discrete atomic subword segment or numerical vocabulary identifier consumed by autoregressive language models.",
        "category": "Generative AI",
        "direction": "across",
        "row": 8,
        "col": 3
    },
    {
        "id": "champ_a7",
        "word": "CNN",
        "display_name": "CNN",
        "clue": "Deep feed-forward network topology utilizing spatially shared convolutional kernels and subsampling pooling layers.",
        "category": "Computer Vision",
        "direction": "across",
        "row": 8,
        "col": 10
    },
    {
        "id": "champ_a8",
        "word": "DROPOUT",
        "display_name": "Dropout",
        "clue": "Stochastic regularization technique setting hidden unit outputs to zero with probability p during training to prevent co-adaptation.",
        "category": "Deep Learning",
        "direction": "across",
        "row": 10,
        "col": 4
    },
    {
        "id": "champ_a9",
        "word": "PROMPT",
        "display_name": "Prompt",
        "clue": "Input text directive or contextual sequence provided to a generative foundation model to steer inference completion.",
        "category": "Generative AI",
        "direction": "across",
        "row": 12,
        "col": 3
    },
    {
        "id": "champ_a10",
        "word": "REGULARIZATION",
        "display_name": "Regularization",
        "clue": "Mathematical loss penalty (such as L1 Lasso sparsity or L2 Ridge weight decay) preventing over-parameterized models from overfitting.",
        "category": "Machine Learning",
        "direction": "across",
        "row": 14,
        "col": 0
    },
    
    # Down
    {
        "id": "champ_d1",
        "word": "BIAS",
        "display_name": "Bias",
        "clue": "Trainable additive offset vector shifting neuron activation thresholds independently of input dot products.",
        "category": "Deep Learning",
        "direction": "down",
        "row": 0,
        "col": 0
    },
    {
        "id": "champ_d2",
        "word": "PERCEPTRON",
        "display_name": "Perceptron",
        "clue": "Historic single-layer threshold neuron computing an affine combination followed by a step activation function.",
        "category": "Deep Learning",
        "direction": "down",
        "row": 0,
        "col": 4
    },
    {
        "id": "champ_d3",
        "word": "ACCURACY",
        "display_name": "Accuracy",
        "clue": "Standard metric quantifying the fraction of correct classifications over total dataset samples.",
        "category": "Evaluation",
        "direction": "down",
        "row": 0,
        "col": 8
    },
    {
        "id": "champ_d4",
        "word": "ATTENTION",
        "display_name": "Attention",
        "clue": "Mechanism computing dynamic alignment weights via scaled dot-product between Query and Key representations.",
        "category": "Generative AI",
        "direction": "down",
        "row": 0,
        "col": 10
    },
    {
        "id": "champ_d5",
        "word": "NORMALIZATION",
        "display_name": "Normalization",
        "clue": "Layer or batch operation standardizing intermediate feature distributions to zero mean and unit variance.",
        "category": "Deep Learning",
        "direction": "down",
        "row": 0,
        "col": 14
    },
    {
        "id": "champ_d6",
        "word": "TENSOR",
        "display_name": "Tensor",
        "clue": "Generalization of scalars, vectors, and matrices to higher multidimensional geometric arrays in PyTorch and JAX.",
        "category": "Mathematics",
        "direction": "down",
        "row": 9,
        "col": 0
    },
    {
        "id": "champ_d7",
        "word": "EPOCH",
        "display_name": "Epoch",
        "clue": "One full training iteration during which every mini-batch of the training dataset has been processed once.",
        "category": "Deep Learning",
        "direction": "down",
        "row": 10,
        "col": 8
    },
    {
        "id": "champ_d8",
        "word": "LOSS",
        "display_name": "Loss",
        "clue": "Differentiable scalar function measuring the quantitative discrepancy between model predictions and true labels.",
        "category": "Machine Learning",
        "direction": "down",
        "row": 11,
        "col": 4
    },
    {
        "id": "champ_d9",
        "word": "RAG",
        "display_name": "RAG",
        "clue": "Retrieval Augmented Generation: Method grounding LLM generations using semantic vector database lookups.",
        "category": "Generative AI",
        "direction": "down",
        "row": 12,
        "col": 10
    }
]

def generate_and_save_all_puzzles():
    # Validate Championship Puzzle
    val = validate_crossword_puzzle(GRAND_CHAMPIONSHIP_WORDS, 15)
    print("Grand Championship Validation:", val["valid"], "Errors:", val.get("errors", []))
    if not val["valid"]:
        raise ValueError(f"Grand Championship validation failed: {val['errors']}")
    
    print_grid(val["numbered_words"], 15)
    
    p1 = {
        "id": "champ_2026",
        "title": "AI & ML Championship 2026",
        "description": "The premier 15x15 competition crossword for Engineering Day testing deep knowledge in Neural Networks, Optimization, and Foundation Models.",
        "difficulty": "Hard",
        "grid_size": 15,
        "time_limit": 600,
        "max_attempts": 3,
        "max_hints": 3,
        "words": val["numbered_words"],
        "active_cells_count": val["total_active_cells"],
        "intersections_count": val["intersection_count"]
    }
    
    # Load previously generated puzzles from JSON if available, or combine them
    with open("data/seed_puzzles.json", "r") as f:
        existing = json.load(f)
        
    all_puzzles = [p1]
    for p in existing:
        if p["id"] != "champ_2026":
            all_puzzles.append(p)
            
    with open("data/seed_puzzles.json", "w") as f:
        json.dump(all_puzzles, f, indent=2)
        
    print(f"Successfully configured {len(all_puzzles)} verified 15x15 tournament puzzles!")

if __name__ == "__main__":
    generate_and_save_all_puzzles()
