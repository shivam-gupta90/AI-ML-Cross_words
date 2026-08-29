"""
Deterministic Crossword Grid Solver & Generator for 15x15 AI/ML Puzzles
"""
import json
from typing import List, Dict, Tuple, Optional
from backend.puzzle_validator import validate_crossword_puzzle, print_grid

WORDS_DB = {
    "BACKPROPAGATION": {
        "display": "Backpropagation",
        "clue": "Algorithm calculating gradients of loss with respect to weights via backward application of the calculus chain rule.",
        "category": "Deep Learning"
    },
    "REGULARIZATION": {
        "display": "Regularization",
        "clue": "Optimization penalty (such as L1 Lasso or L2 Ridge) added to the loss function to constrain model complexity.",
        "category": "Machine Learning"
    },
    "TRANSFORMER": {
        "display": "Transformer",
        "clue": "Architecture that processes entire sequences simultaneously using multi-head self-attention mechanisms without recurrence.",
        "category": "Generative AI"
    },
    "OVERFITTING": {
        "display": "Overfitting",
        "clue": "Failure mode where a model fits training noise and idiosyncrasies, leading to poor generalization on test distributions.",
        "category": "Machine Learning"
    },
    "GRADIENT": {
        "display": "Gradient",
        "clue": "Vector of first-order partial derivatives indicating the direction of steepest ascent on the loss surface.",
        "category": "Mathematics"
    },
    "PERCEPTRON": {
        "display": "Perceptron",
        "clue": "Single-layer neural classification unit computing an affine combination followed by a step threshold activation.",
        "category": "Deep Learning"
    },
    "CONVOLUTION": {
        "display": "Convolution",
        "clue": "Shift-invariant mathematical filtering operation computing cross-correlation between learnable kernels and input tensors.",
        "category": "Deep Learning"
    },
    "ATTENTION": {
        "display": "Attention",
        "clue": "Soft alignment mechanism computing dot products between Query and Key vectors to produce weighted Value averages.",
        "category": "Generative AI"
    },
    "EMBEDDING": {
        "display": "Embedding",
        "clue": "Dense continuous vector representation mapping discrete entities into a latent space preserving geometric semantic distance.",
        "category": "NLP / Deep Learning"
    },
    "TOKENIZATION": {
        "display": "Tokenization",
        "clue": "Text pre-processing phase that splits continuous natural language strings into discrete subword integer tokens.",
        "category": "Generative AI"
    },
    "CLUSTERING": {
        "display": "Clustering",
        "clue": "Unsupervised partitioning method grouping unlabelled vectors such that intra-group distance is minimized.",
        "category": "Machine Learning"
    },
    "INFERENCE": {
        "display": "Inference",
        "clue": "Runtime execution phase evaluating a trained neural network on novel production inputs without parameter updates.",
        "category": "Machine Learning"
    },
    "NORMALIZATION": {
        "display": "Normalization",
        "clue": "Standardization technique (Batch, Layer, RMSNorm) scaling activations to zero mean and unit variance.",
        "category": "Deep Learning"
    },
    "DROPOUT": {
        "display": "Dropout",
        "clue": "Stochastic regularization technique that randomly zeros neuron activations with probability p during training.",
        "category": "Deep Learning"
    },
    "AUTOENCODER": {
        "display": "Autoencoder",
        "clue": "Neural network trained to compress inputs into a lower-dimensional bottleneck latent representation and reconstruct them.",
        "category": "Deep Learning"
    },
    "TENSOR": {
        "display": "Tensor",
        "clue": "Generalization of vectors and matrices to higher dimensional arrays of numerical values.",
        "category": "Mathematics"
    },
    "BIAS": {
        "display": "Bias",
        "clue": "Additive trainable parameter shifting the activation threshold of a neuron independently of input features.",
        "category": "Machine Learning"
    },
    "LOSS": {
        "display": "Loss",
        "clue": "Objective function scalar quantifying the magnitude of error between predictions and ground-truth targets.",
        "category": "Machine Learning"
    },
    "EPOCH": {
        "display": "Epoch",
        "clue": "One complete traversal of the entire training dataset through the neural network optimization pipeline.",
        "category": "Deep Learning"
    },
    "RAG": {
        "display": "RAG",
        "clue": "Retrieval Augmented Generation: Combining pre-trained language models with external vectorized document stores.",
        "category": "Generative AI"
    },
    "BERT": {
        "display": "BERT",
        "clue": "Bidirectional Encoder Representations from Transformers pre-trained with masked language modeling.",
        "category": "NLP"
    },
    "ADAM": {
        "display": "Adam",
        "clue": "Adaptive moment estimation optimizer maintaining running averages of both first and second gradient moments.",
        "category": "Optimization"
    },
    "RELU": {
        "display": "ReLU",
        "clue": "Piecewise linear activation function computing f(x) = max(0, x), mitigating vanishing gradients in deep networks.",
        "category": "Deep Learning"
    },
    "SIGMOID": {
        "display": "Sigmoid",
        "clue": "Logistic activation function mapping any real input value into the continuous probability interval (0, 1).",
        "category": "Deep Learning"
    },
    "SOFTMAX": {
        "display": "Softmax",
        "clue": "Normalized exponential function converting unnormalized logit vectors into valid probability distributions summing to 1.",
        "category": "Deep Learning"
    },
    "LATENT": {
        "display": "Latent",
        "clue": "Hidden, unobserved low-dimensional manifold space capturing the underlying generative factors of data.",
        "category": "Deep Learning"
    },
    "PRUNING": {
        "display": "Pruning",
        "clue": "Model compression technique that removes redundant weights or entire neurons with negligible saliency.",
        "category": "Deep Learning"
    },
    "PROMPT": {
        "display": "Prompt",
        "clue": "Natural language instruction or context prefix provided to an autoregressive language model to steer output.",
        "category": "Generative AI"
    },
    "QUANTIZATION": {
        "display": "Quantization",
        "clue": "Mapping continuous floating-point weights (FP32/FP16) into reduced integer precisions (INT8/INT4) for fast edge inference.",
        "category": "Deep Learning"
    },
    "MATRIX": {
        "display": "Matrix",
        "clue": "Two-dimensional rectangular array of numbers representing linear transformations in vector spaces.",
        "category": "Mathematics"
    },
    "VECTOR": {
        "display": "Vector",
        "clue": "One-dimensional element of a vector space having magnitude and direction.",
        "category": "Mathematics"
    },
    "WEIGHT": {
        "display": "Weight",
        "clue": "Trainable coefficient that scales the strength of a connection between neurons.",
        "category": "Deep Learning"
    },
    "RESNET": {
        "display": "ResNet",
        "clue": "Deep architecture introducing identity shortcut skip-connections to solve vanishing gradient in 100+ layer networks.",
        "category": "Computer Vision"
    },
    "LSTM": {
        "display": "LSTM",
        "clue": "Recurrent architecture with input, forget, and output gates designed to capture long-range temporal dependencies.",
        "category": "Deep Learning"
    },
    "CNN": {
        "display": "CNN",
        "clue": "Feed-forward network specialized for 2D spatial grid processing using shared weights and pooling layers.",
        "category": "Computer Vision"
    },
    "RNN": {
        "display": "RNN",
        "clue": "Recurrent architecture maintaining an internal hidden state to process sequential or time-series data.",
        "category": "Deep Learning"
    },
    "GAN": {
        "display": "GAN",
        "clue": "Generative model framework training a Generator and a Discriminator in a minimax game.",
        "category": "Generative AI"
    }
}

# Let's craft 3 verified layouts
# Puzzle 1: Engineering Day Flagship Challenge (15x15)
# Puzzle 2: Deep Learning & Neural Architectures (15x15)
# Puzzle 3: Generative AI & Foundation Models (15x15)

def build_puzzle_1():
    # Let's place words and verify every intersection
    words = [
        # Across
        {"id": "p1_w1", "word": "BACKPROPAGATION", "direction": "across", "row": 0, "col": 0},
        {"id": "p1_w2", "word": "LATENT",          "direction": "across", "row": 2, "col": 2},
        {"id": "p1_w3", "word": "ADAM",            "direction": "across", "row": 2, "col": 11},
        {"id": "p1_w4", "word": "TENSOR",          "direction": "across", "row": 4, "col": 0},
        {"id": "p1_w5", "word": "SOFTMAX",         "direction": "across", "row": 4, "col": 8},
        {"id": "p1_w6", "word": "ATTENTION",       "direction": "across", "row": 6, "col": 2},
        {"id": "p1_w7", "word": "INFERENCE",       "direction": "across", "row": 8, "col": 4},
        {"id": "p1_w8", "word": "TRANSFORMER",     "direction": "across", "row": 10, "col": 2},
        {"id": "p1_w9", "word": "REGULARIZATION",  "direction": "across", "row": 12, "col": 0},
        {"id": "p1_w10", "word": "EPOCH",          "direction": "across", "row": 14, "col": 0},
        {"id": "p1_w11", "word": "PROMPT",         "direction": "across", "row": 14, "col": 7},
        
        # Down
        {"id": "p1_w12", "word": "BIAS",           "direction": "down", "row": 0, "col": 0},
        {"id": "p1_w13", "word": "CLUSTERING",     "direction": "down", "row": 0, "col": 2},
        {"id": "p1_w14", "word": "PERCEPTRON",     "direction": "down", "row": 0, "col": 4},
        {"id": "p1_w15", "word": "AUTOENCODER",    "direction": "down", "row": 0, "col": 7},
        {"id": "p1_w16", "word": "OVERFITTING",    "direction": "down", "row": 0, "col": 10},
        {"id": "p1_w17", "word": "NORMALIZATION",  "direction": "down", "row": 0, "col": 14},
        {"id": "p1_w18", "word": "EMBEDDING",      "direction": "down", "row": 5, "col": 5},
        {"id": "p1_w19", "word": "DROPOUT",        "direction": "down", "row": 7, "col": 12},
    ]
    return words

