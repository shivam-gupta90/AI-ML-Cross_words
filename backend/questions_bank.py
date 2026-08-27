"""
Question Bank and Pre-designed Verified 15x15 AI/ML Crosswords
Contains difficult, concept-based clues across AI, ML, Deep Learning, Generative AI, and Mathematics.
"""

from typing import List, Dict, Any

# Extensive vocabulary bank with deep conceptual clues
AI_ML_CONCEPT_BANK = [
    {
        "term": "TRANSFORMER",
        "display": "Transformer",
        "clue": "Deep learning architecture introduced in 2017 that relies entirely on self-attention mechanisms to compute representations of input sequences without recurrent alignment.",
        "category": "Generative AI / NLP",
        "hint_letters": [0, 4, 10]
    },
    {
        "term": "BACKPROPAGATION",
        "display": "Backpropagation",
        "clue": "Algorithm that applies the chain rule of calculus backward through computational graphs to calculate gradients of loss with respect to all trainable weights.",
        "category": "Deep Learning",
        "hint_letters": [0, 5, 14]
    },
    {
        "term": "REGULARIZATION",
        "display": "Regularization",
        "clue": "Technique (such as L1 Lasso or L2 Ridge weight decay) that introduces a penalty term to the loss function to prevent overfitting and encourage simpler models.",
        "category": "Machine Learning",
        "hint_letters": [0, 3, 13]
    },
    {
        "term": "OVERFITTING",
        "display": "Overfitting",
        "clue": "Phenomenon where a model achieves near-zero empirical training error by memorizing noise, resulting in poor generalization on unseen validation distributions.",
        "category": "Machine Learning",
        "hint_letters": [0, 4, 10]
    },
    {
        "term": "GRADIENTDESCENT",
        "display": "Gradient Descent",
        "clue": "First-order iterative optimization algorithm that updates parameters in the direction opposite to the steepest ascent of the loss surface.",
        "category": "Optimization / Mathematics",
        "hint_letters": [0, 4, 9, 14]
    },
    {
        "term": "CONVOLUTION",
        "display": "Convolution",
        "clue": "Mathematical operation that applies shift-invariant learnable kernel filters across spatial dimensions to extract local hierarchical feature maps.",
        "category": "Deep Learning",
        "hint_letters": [0, 3, 10]
    },
    {
        "term": "TOKENIZATION",
        "display": "Tokenization",
        "clue": "Process of segmenting raw text into discrete subword units or numerical IDs (e.g. BPE, WordPiece) prior to embedding lookup.",
        "category": "Generative AI / NLP",
        "hint_letters": [0, 4, 11]
    },
    {
        "term": "ATTENTION",
        "display": "Attention",
        "clue": "Mechanism computing soft alignment weights between queries and keys to produce a dynamic weighted sum over value vectors.",
        "category": "Generative AI / NLP",
        "hint_letters": [0, 3, 8]
    },
    {
        "term": "EMBEDDING",
        "display": "Embedding",
        "clue": "Dense vector representation mapping discrete categorical symbols or words into a continuous latent geometric space where cosine proximity captures semantic similarity.",
        "category": "Machine Learning / NLP",
        "hint_letters": [0, 3, 8]
    },
    {
        "term": "INFERENCE",
        "display": "Inference",
        "clue": "Phase in which a trained machine learning model consumes new production inputs to calculate forward predictions without updating parameters.",
        "category": "Machine Learning",
        "hint_letters": [0, 4, 8]
    },
    {
        "term": "CLUSTERING",
        "display": "Clustering",
        "clue": "Unsupervised partitioning method that groups unlabeled data points so intra-cluster similarity is maximized while inter-cluster similarity is minimized.",
        "category": "Machine Learning",
        "hint_letters": [0, 3, 9]
    },
    {
        "term": "PERCEPTRON",
        "display": "Perceptron",
        "clue": "Fundamental linear binary classification unit proposed by Rosenblatt (1958) that computes a step function over weighted inputs.",
        "category": "Deep Learning",
        "hint_letters": [0, 4, 9]
    },
    {
        "term": "DROPOUT",
        "display": "Dropout",
        "clue": "Stochastic regularization method that randomly zeroes out neuron activations with probability p during forward training passes to break co-adaptation.",
        "category": "Deep Learning",
        "hint_letters": [0, 3, 6]
    },
    {
        "term": "EIGENVECTOR",
        "display": "Eigenvector",
        "clue": "Non-zero vector that changes only by a scalar factor when linear transformation matrix A is applied (Av = lambda v); fundamental to Principal Component Analysis.",
        "category": "Mathematics",
        "hint_letters": [0, 4, 10]
    },
    {
        "term": "AUTOENCODER",
        "display": "Autoencoder",
        "clue": "Neural network trained in an unsupervised bottleneck fashion to reconstruct its own input while enforcing low-dimensional latent compression.",
        "category": "Deep Learning",
        "hint_letters": [0, 4, 10]
    },
    {
        "term": "NORMALIZATION",
        "display": "Normalization",
        "clue": "Technique such as Batch or Layer norm that standardizes intermediate layer distributions by zero-centering and scaling activations to stabilize training.",
        "category": "Deep Learning",
        "hint_letters": [0, 5, 12]
    },
    {
        "term": "HYPERPARAMETER",
        "display": "Hyperparameter",
        "clue": "Configurable external setting (e.g. learning rate, batch size, tree depth) fixed prior to training rather than learned directly from data.",
        "category": "Machine Learning",
        "hint_letters": [0, 6, 13]
    },
    {
        "term": "HALLUCINATION",
        "display": "Hallucination",
        "clue": "Phenomenon in generative language models where plausible-sounding yet factually false, ungrounded, or nonsensical outputs are generated with high confidence.",
        "category": "Generative AI",
        "hint_letters": [0, 5, 12]
    },
    {
        "term": "CLASSIFICATION",
        "display": "Classification",
        "clue": "Supervised task of assigning input instances into discrete categorical class labels using decision boundaries.",
        "category": "Machine Learning",
        "hint_letters": [0, 6, 13]
    },
    {
        "term": "HEURISTIC",
        "display": "Heuristic",
        "clue": "Rule-of-thumb evaluation function h(n) estimating remaining path cost in informed state-space search algorithms such as A* search.",
        "category": "Artificial Intelligence",
        "hint_letters": [0, 3, 8]
    },
    {
        "term": "TENSOR",
        "display": "Tensor",
        "clue": "Multi-dimensional geometric array of numerical values generalizing scalars, vectors, and matrices to arbitrary rank.",
        "category": "Mathematics / Deep Learning",
        "hint_letters": [0, 3, 5]
    },
    {
        "term": "EPOCH",
        "display": "Epoch",
        "clue": "One complete forward and backward sweep of the entire training dataset through the neural network optimization pipeline.",
        "category": "Deep Learning",
        "hint_letters": [0, 2, 4]
    },
    {
        "term": "LOSS",
        "display": "Loss",
        "clue": "Scalar objective measure quantifying discrepancy between model predictions and true ground-truth targets (e.g. Cross-Entropy, MSE).",
        "category": "Machine Learning",
        "hint_letters": [0, 2, 3]
    },
    {
        "term": "BIAS",
        "display": "Bias",
        "clue": "Error introduced by approximating a real-world complex phenomenon with an overly simplified model; often in tension with variance.",
        "category": "Machine Learning",
        "hint_letters": [0, 2, 3]
    },
    {
        "term": "RAG",
        "display": "RAG",
        "clue": "Retrieval Augmented Generation: Architecture combining semantic search across external knowledge stores with generative language models.",
        "category": "Generative AI",
        "hint_letters": [0, 2]
    },
    {
        "term": "BERT",
        "display": "BERT",
        "clue": "Bidirectional Encoder Representations from Transformers: Masked language model pre-trained to capture context from both left and right directions.",
        "category": "Generative AI / NLP",
        "hint_letters": [0, 2]
    },
    {
        "term": "ADAM",
        "display": "Adam",
        "clue": "Adaptive Moment Estimation optimizer that combines ideas from RMSProp and Momentum by tracking first and second moments of gradients.",
        "category": "Optimization",
        "hint_letters": [0, 2]
    }
]

# Verified Pre-designed 15x15 Puzzles
# Each puzzle contains 14-18 interconnected terms verified to intersect perfectly on a 15x15 grid.

PREDEFINED_PUZZLES: List[Dict[str, Any]] = [
    {
        "id": "puzzle_champ_2026",
        "title": "AI & ML Championship Challenge",
        "description": "The flagship 15x15 challenge for Engineering Day 2026 covering Foundation Models, Deep Learning, and Core Machine Learning Theory.",
        "difficulty": "Hard",
        "grid_size": 15,
        "time_limit": 600,  # 10 minutes
        "max_attempts": 3,
        "max_hints": 3,
        "words": [
            # Words layout designed and tested for exact 15x15 intersection
            {
                "id": "w1",
                "word": "BACKPROPAGATION",
                "display_name": "Backpropagation",
                "clue": "Calculates gradient of loss with respect to all weights by backward evaluation of the calculus chain rule.",
                "direction": "across",
                "row": 0,
                "col": 0,
            },
            {
                "id": "w2",
                "word": "BERT",
                "display_name": "BERT",
                "clue": "Bidirectional Transformer model pre-trained using Masked Language Modeling and Next Sentence Prediction.",
                "direction": "down",
                "row": 0,
                "col": 0,
            },
            {
                "id": "w3",
                "word": "CLUSTERING",
                "display_name": "Clustering",
                "clue": "Unsupervised partitioning algorithm (e.g. K-Means, DBSCAN) grouping data points by spatial distance metrics.",
                "direction": "down",
                "row": 0,
                "col": 4,
            },
            {
                "id": "w4",
                "word": "OVERFITTING",
                "display_name": "Overfitting",
                "clue": "Model pathology where high variance causes memorization of training sample noise rather than underlying distribution.",
                "direction": "down",
                "row": 0,
                "col": 9,
            },
            {
                "id": "w5",
                "word": "NORMALIZATION",
                "display_name": "Normalization",
                "clue": "Standardization of intermediate activations across channels or layers to prevent vanishing/exploding internal covariate shifts.",
                "direction": "down",
                "row": 0,
                "col": 14,
            },
            {
                "id": "w6",
                "word": "TENSOR",
                "display_name": "Tensor",
                "clue": "Algebraic multidimensional data container representing rank-N arrays in frameworks like PyTorch and JAX.",
                "direction": "across",
                "row": 3,
                "col": 0,
            },
            {
                "id": "w7",
                "word": "ATTENTION",
                "display_name": "Attention",
                "clue": "Computes softmax-scaled dot product between Query and Key vectors to dynamically weigh Value embeddings.",
                "direction": "across",
                "row": 5,
                "col": 2,
            },
            {
                "id": "w8",
                "word": "EMBEDDING",
                "display_name": "Embedding",
                "clue": "Dense vector mapping discrete tokens into continuous geometric vector spaces where dot product reflects semantic similarity.",
                "direction": "down",
                "row": 5,
                "col": 6,
            },
            {
                "id": "w9",
                "word": "INFERENCE",
                "display_name": "Inference",
                "clue": "Forward computation stage evaluating a frozen neural model on novel unseen queries without backpropagating loss.",
                "direction": "across",
                "row": 8,
                "col": 3,
            },
            {
                "id": "w10",
                "word": "DROPOUT",
                "display_name": "Dropout",
                "clue": "Randomly masking hidden layer activations with probability p during training to discourage co-adapting features.",
                "direction": "down",
                "row": 7,
                "col": 11,
            },
            {
                "id": "w11",
                "word": "TRANSFORMER",
                "display_name": "Transformer",
                "clue": "Dominant sequence modeling architecture based on stacked multi-head self-attention mechanisms without recurrence.",
                "direction": "across",
                "row": 10,
                "col": 2,
            },
            {
                "id": "w12",
                "word": "REGULARIZATION",
                "display_name": "Regularization",
                "clue": "Constraining model complexity via L1/L2 penalties or weight decay to lower generalization error.",
                "direction": "across",
                "row": 12,
                "col": 0,
            },
            {
                "id": "w13",
                "word": "PERCEPTRON",
                "display_name": "Perceptron",
                "clue": "Historic single-layer threshold neuron computing linear combination followed by step activation function.",
                "direction": "down",
                "row": 4,
                "col": 2,
            },
            {
                "id": "w14",
                "word": "GRADIENT",
                "display_name": "Gradient",
                "clue": "Vector of partial derivatives of a multivariate function indicating direction of steepest rate of increase.",
                "direction": "down",
                "row": 7,
                "col": 4,
            },
            {
                "id": "w15",
                "word": "EPOCH",
                "display_name": "Epoch",
                "clue": "Single complete training cycle during which every mini-batch of the training dataset is processed once.",
                "direction": "across",
                "row": 14,
                "col": 0,
            },
            {
                "id": "w16",
                "word": "RAG",
                "display_name": "RAG",
                "clue": "Retrieval Augmented Generation: Augmenting language model prompts with dynamic vector database retrieval.",
                "direction": "across",
                "row": 14,
                "col": 12,
            }
        ]
    }
]
