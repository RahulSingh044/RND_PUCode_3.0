import numpy as np
from typing import List
from insightface.app.common import Face

from app.config import logger


class FaceEmbedder:
    """
    Generates face embeddings using ArcFace (InsightFace).
    Assumes face detection is already done.
    """

    def __init__(self):
        logger.info("Initializing FaceEmbedder (ArcFace via InsightFace)")
        # No model init here — embeddings come from detected Face object
        logger.info("FaceEmbedder initialized successfully")

    def embed(self, face: Face) -> np.ndarray:
        """
        Generate a normalized embedding for a single detected face.

        Returns:
        - numpy.ndarray of shape (512,)
        """
        try:
            embedding = face.normed_embedding

            if embedding is None:
                raise ValueError("Embedding generation failed")

            return embedding.astype(np.float32)

        except Exception:
            logger.exception("Failed to generate face embedding")
            return None

    def embed_many(self, faces: List[Face]) -> List[np.ndarray]:
        """
        Generate embeddings for multiple faces.
        """
        embeddings = []

        for face in faces:
            emb = self.embed(face)
            if emb is not None:
                embeddings.append(emb)

        logger.info(f"Generated {len(embeddings)} face embeddings")
        return embeddings
