import numpy as np


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Compute cosine similarity between two vectors.

    Assumes vectors are already L2-normalized (as ArcFace provides).

    Returns:
        float: similarity score in range [-1, 1]
    """

    if vec1 is None or vec2 is None:
        return -1.0

    if vec1.shape != vec2.shape:
        raise ValueError(
            f"Vector shape mismatch: {vec1.shape} vs {vec2.shape}"
        )

    # Fast cosine similarity for normalized vectors
    return float(np.dot(vec1, vec2))
