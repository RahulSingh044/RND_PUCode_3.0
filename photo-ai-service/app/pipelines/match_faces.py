import numpy as np
from typing import List, Dict

from app.config import FACE_MATCH_THRESHOLD, logger
from app.utils.similarity import cosine_similarity


class FaceMatcher:
    """
    Matches user face embeddings with detected face embeddings from photos.
    """

    def __init__(self, threshold: float = FACE_MATCH_THRESHOLD):
        self.threshold = threshold
        logger.info(f"FaceMatcher initialized with threshold={self.threshold}")

    def match(
        self,
        user_embeddings: Dict[str, np.ndarray],
        photo_faces: List[Dict]
    ) -> List[Dict]:
        """
        Match user embeddings against faces detected in a single photo.

        Args:
        - user_embeddings:
            {
              "user_id": np.ndarray(512,)
            }

        - photo_faces:
            [
              {
                "embedding": np.ndarray(512,)
              }
            ]

        Returns:
        [
          {
            "user_id": str,
            "confidence": float
          }
        ]
        """
        matches = []

        for user_id, user_emb in user_embeddings.items():
            for face in photo_faces:
                face_emb = face.get("embedding")
                if face_emb is None:
                    continue

                score = cosine_similarity(user_emb, face_emb)

                if score >= self.threshold:
                    matches.append({
                        "user_id": user_id,
                        "confidence": float(score)
                    })

        return matches
