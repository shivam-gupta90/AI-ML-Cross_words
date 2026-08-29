"""
AI/ML, Data Science, IoT & Core CSE Question Bank
Comprehensive vocabulary across all 4 engineering categories with conceptual clues.
"""

# Category Constants
CAT_AIML = "AI / ML"
CAT_DATASCIENCE = "Data Science"
CAT_IOT = "IoT"
CAT_CORECSE = "Core CSE"

# Multi-Category Question Bank
VOCABULARY = {
    # -------------------------------------------------------------
    # 1. AI / ML
    # -------------------------------------------------------------
    "TRANSFORMER": ("Transformer", "Deep learning sequence model relying entirely on self-attention mechanisms without recurrent alignment.", CAT_AIML),
    "BACKPROPAGATION": ("Backpropagation", "Calculates loss gradients backward through computational graphs via the calculus chain rule.", CAT_AIML),
    "OVERFITTING": ("Overfitting", "Pathology where high model variance fits training sample noise, degrading unseen validation performance.", CAT_AIML),
    "GRADIENT": ("Gradient", "Vector of first-order partial derivatives pointing in the direction of steepest loss ascent.", CAT_AIML),
    "PERCEPTRON": ("Perceptron", "Historic linear binary classification unit computing an affine step-activation threshold.", CAT_AIML),
    "ATTENTION": ("Attention", "Query-Key-Value dynamic alignment mechanism computing pairwise weighted token relevance.", CAT_AIML),
    "EMBEDDING": ("Embedding", "Dense continuous vector mapping discrete symbols into semantic geometric space.", CAT_AIML),
    "TOKENIZATION": ("Tokenization", "Splitting raw text into discrete subword IDs or integer tokens prior to embedding lookup.", CAT_AIML),
    "DROPOUT": ("Dropout", "Stochastic regularization randomly zeroing unit activations with probability p during training.", CAT_AIML),
    "INFERENCE": ("Inference", "Forward evaluation stage executing a trained model on new queries without updating weights.", CAT_AIML),
    "AUTOENCODER": ("Autoencoder", "Bottleneck neural network trained to compress and reconstruct its own inputs.", CAT_AIML),
    "REGULARIZATION": ("Regularization", "Technique introducing loss penalties (L1/L2) to prevent over-parameterization.", CAT_AIML),
    "CONVOLUTION": ("Convolution", "Mathematical filtering operation extracting spatial feature maps using learnable sliding kernels.", CAT_AIML),
    "EPOCH": ("Epoch", "One full forward and backward pass of the entire training dataset through the network.", CAT_AIML),
    "LATENT": ("Latent", "Hidden, unobserved compressed manifold space capturing intrinsic data representations.", CAT_AIML),
    "PROMPT": ("Prompt", "Natural language instruction prefix provided to an autoregressive foundation model.", CAT_AIML),
    "RAG": ("RAG", "Retrieval Augmented Generation: Combining semantic vector search retrieval with generative LLMs.", CAT_AIML),
    "BERT": ("BERT", "Bidirectional Encoder Representations from Transformers pre-trained with masked language modeling.", CAT_AIML),
    "ADAM": ("Adam", "Adaptive moment estimation optimizer tracking 1st and 2nd moments of loss gradients.", CAT_AIML),
    "SGD": ("SGD", "Stochastic Gradient Descent updating model weights on random mini-batches.", CAT_AIML),
    "CNN": ("CNN", "Feed-forward convolutional network specialized for 2D/3D spatial grid patterns.", CAT_AIML),
    "RNN": ("RNN", "Recurrent neural network with internal cyclical feedback loops for sequential inputs.", CAT_AIML),
    "GAN": ("GAN", "Generative Adversarial Network pitting a generator against a discriminator network.", CAT_AIML),
    "RESNET": ("ResNet", "Deep convolutional architecture using residual skip connections to bypass layers.", CAT_AIML),
    "LOSS": ("Loss", "Scalar objective penalty quantifying prediction discrepancy from true ground-truth targets.", CAT_AIML),
    "BIAS": ("Bias", "Additive trainable parameter shifting the activation threshold of a neuron.", CAT_AIML),
    "WEIGHT": ("Weight", "Learnable multiplicative coefficient scaling neural connection strength.", CAT_AIML),
    "RELU": ("ReLU", "Piecewise linear activation function computing f(x) = max(0, x).", CAT_AIML),
    "SOFTMAX": ("Softmax", "Function converting raw logit vectors into normalized probability distributions summing to 1.", CAT_AIML),
    "SIGMOID": ("Sigmoid", "S-shaped activation function mapping real numbers into probability interval (0, 1).", CAT_AIML),

    # -------------------------------------------------------------
    # 2. DATA SCIENCE
    # -------------------------------------------------------------
    "CLUSTERING": ("Clustering", "Unsupervised partitioning method grouping unlabelled vectors by spatial distance metrics.", CAT_DATASCIENCE),
    "REGRESSION": ("Regression", "Supervised task predicting continuous real-valued quantitative targets from features.", CAT_DATASCIENCE),
    "PRECISION": ("Precision", "Ratio of correctly predicted positive observations to total predicted positive observations.", CAT_DATASCIENCE),
    "RECALL": ("Recall", "Ratio of true positive detections over total actual positive ground truth instances.", CAT_DATASCIENCE),
    "ACCURACY": ("Accuracy", "Proportion of correct classifications over the total number of evaluated samples.", CAT_DATASCIENCE),
    "VARIANCE": ("Variance", "Sensitivity of model predictions to random fluctuations and noise in the training set.", CAT_DATASCIENCE),
    "DATASET": ("Dataset", "Structured collection of sample instances used for model training, validation, and testing.", CAT_DATASCIENCE),
    "ENTROPY": ("Entropy", "Information-theoretic measure of unpredictability and uncertainty in a probability distribution.", CAT_DATASCIENCE),
    "EIGENVECTOR": ("Eigenvector", "Vector whose direction is invariant under a given linear matrix transformation (Av = lambda v).", CAT_DATASCIENCE),
    "OPTIMIZATION": ("Optimization", "Mathematical process of finding parameter values that minimize an objective loss function.", CAT_DATASCIENCE),
    "PCA": ("PCA", "Principal Component Analysis reducing dimensionality by projecting onto orthogonal axes of maximum variance.", CAT_DATASCIENCE),
    "KNN": ("K-NN", "K-Nearest Neighbors non-parametric classification algorithm voting by Euclidean or cosine distance.", CAT_DATASCIENCE),
    "SVM": ("SVM", "Support Vector Machine finding the optimal separating hyperplane with maximum margin.", CAT_DATASCIENCE),
    "ROC": ("ROC", "Receiver Operating Characteristic curve plotting True Positive Rate versus False Positive Rate.", CAT_DATASCIENCE),
    "AUC": ("AUC", "Area Under the ROC Curve measuring aggregate classification performance across all thresholds.", CAT_DATASCIENCE),
    "MATRIX": ("Matrix", "Two-dimensional rectangular numerical array representing linear operators in vector spaces.", CAT_DATASCIENCE),
    "VECTOR": ("Vector", "One-dimensional array with magnitude and direction in a vector space.", CAT_DATASCIENCE),
    "OUTLIER": ("Outlier", "Data point that differs significantly from other observations in the distribution.", CAT_DATASCIENCE),
    "CORRELATION": ("Correlation", "Bivariate statistical metric quantifying the linear relationship between two variables.", CAT_DATASCIENCE),

    # -------------------------------------------------------------
    # 3. INTERNET OF THINGS (IoT)
    # -------------------------------------------------------------
    "MQTT": ("MQTT", "Lightweight publish-subscribe network protocol designed for constrained IoT devices and low bandwidth.", CAT_IOT),
    "SENSOR": ("Sensor", "Hardware transducer converting physical environmental phenomena (temp, light, pressure) into electrical signals.", CAT_IOT),
    "ACTUATOR": ("Actuator", "Mechanism that converts control signals into physical movement or action (motors, relays, valves).", CAT_IOT),
    "GATEWAY": ("Gateway", "Bridge device connecting local edge sensor networks to external cloud infrastructure.", CAT_IOT),
    "ZIGBEE": ("Zigbee", "Low-power, low data-rate wireless mesh network standard for home automation and smart energy.", CAT_IOT),
    "BLUETOOTH": ("Bluetooth", "Short-range wireless standard operating in 2.4 GHz ISM band for peer-to-peer device communication.", CAT_IOT),
    "FIRMWARE": ("Firmware", "Low-level embedded software programmed directly onto a microcontroller's non-volatile ROM/flash memory.", CAT_IOT),
    "TELEMETRY": ("Telemetry", "Automated collection and transmission of remote sensor measurements to receiving systems for monitoring.", CAT_IOT),
    "LORA": ("LoRa", "Long Range chirp spread-spectrum wireless technology enabling low-power wide-area network (LPWAN) IoT links.", CAT_IOT),
    "LATENCY": ("Latency", "Time delay elapsed between data packet transmission from a sensor and its reception by the endpoint.", CAT_IOT),
    "BANDWIDTH": ("Bandwidth", "Maximum rate of data transfer across a network communication channel per unit time.", CAT_IOT),
    "EMBEDDED": ("Embedded", "Dedicated microprocessor-based computer system engineered to perform specific dedicated control functions.", CAT_IOT),
    "PROTOCOL": ("Protocol", "Standardized set of communication rules governing data formatting, transmission, and error checking.", CAT_IOT),

    # -------------------------------------------------------------
    # 4. CORE CSE (Computer Science Engineering)
    # -------------------------------------------------------------
    "DEADLOCK": ("Deadlock", "Concurrency anomaly where two or more processes are permanently blocked waiting for resources held by each other.", CAT_CORECSE),
    "SEMAPHORE": ("Semaphore", "Synchronization variable used to control concurrent access to common shared resources in multi-programming.", CAT_CORECSE),
    "COMPILER": ("Compiler", "Software transforming source code written in high-level programming language into target machine assembly.", CAT_CORECSE),
    "CACHE": ("Cache", "High-speed temporary hardware memory buffer storing frequently accessed data to reduce main memory latency.", CAT_CORECSE),
    "THREAD": ("Thread", "Lightweight unit of CPU execution sharing code, data, and OS resources with sibling threads in a process.", CAT_CORECSE),
    "STACK": ("Stack", "LIFO (Last-In-First-Out) linear data structure supporting push and pop operations at a single top boundary.", CAT_CORECSE),
    "QUEUE": ("Queue", "FIFO (First-In-First-Out) linear data structure where elements are inserted at rear and removed from front.", CAT_CORECSE),
    "GRAPH": ("Graph", "Non-linear data structure comprising vertices (nodes) interconnected by directed or undirected edges.", CAT_CORECSE),
    "RECURSION": ("Recursion", "Algorithmic technique where a function solves a problem by calling sub-instances of itself until a base case.", CAT_CORECSE),
    "PIPELINING": ("Pipelining", "CPU microarchitecture technique overlapping execution of multiple instructions across consecutive clock cycles.", CAT_CORECSE),
    "SOCKET": ("Socket", "Endpoint abstraction for two-way network communication between programs over IP networks.", CAT_CORECSE),
    "INDEXING": ("Indexing", "Database optimization structure (e.g. B-Tree) accelerating record retrieval without scanning full tables.", CAT_CORECSE),
    "DATABASE": ("Database", "Organized collection of structured data managed by a DBMS supporting ACID transactions.", CAT_CORECSE),
    "ALGORITHM": ("Algorithm", "Finite sequence of well-defined computer-implementable instructions to solve a class of specific problems.", CAT_CORECSE),
    "MUTEX": ("Mutex", "Mutual exclusion lock ensuring that only one thread can execute a critical section at a given instant.", CAT_CORECSE),
    "HASHING": ("Hashing", "Mapping arbitrary-sized key data into fixed-size values using hash functions for O(1) average dictionary lookups.", CAT_CORECSE),
    "PROCESS": ("Process", "Instance of a computer program in active execution containing address space, registers, and program counter.", CAT_CORECSE),
    "NODE": ("Node", "Individual basic computational unit or element in data structures such as linked lists, trees, and graphs.", CAT_CORECSE),
    "TREE": ("Tree", "Hierarchical acyclic data structure composed of nodes connected by directed or undirected parent-child edges.", CAT_CORECSE),
    "COST": ("Cost", "Cumulative loss penalty calculated across the entire dataset or batch.", CAT_CORECSE)
}
