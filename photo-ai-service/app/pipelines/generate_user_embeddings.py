from typing import Dict
import numpy as np

from app.config import logger
from app.services.image_loader import load_image_from_url
from app.pipelines.detect_faces import FaceDetector
from app.pipelines.generate_embed import FaceEmbedder
from app.schemas.event_payload import UserPayload


def generate_user_embeddings(
    users: list[UserPayload],
    detector: FaceDetector,
    embedder: FaceEmbedder
) -> Dict[str, np.ndarray]:
    """
    Generate face embeddings for users from their selfie image URLs.

    Returns:
        {
          "user_id": np.ndarray(512,)
        }
    """

    user_embeddings: Dict[str, np.ndarray] = {}

    for user in users:
        logger.info(f"Generating embedding for user_id={user.user_id}")

        # -------------------------
        # Load user selfie
        # -------------------------
        image = load_image_from_url(user.image_url)
        if image is None:
            logger.warning(
                f"Failed to load selfie for user_id={user.user_id}"
            )
            continue

        # -------------------------
        # Detect face (expect 1 face)
        # -------------------------
        faces = detector.detect(image)

        if not faces:
            logger.warning(
                f"No face detected in selfie for user_id={user.user_id}"
            )
            continue

        if len(faces) > 1:
            logger.warning(
                f"Multiple faces detected in selfie for user_id={user.user_id} "
                f"(using highest confidence face)"
            )

        # Pick the face with highest detection confidence
        best_face = max(
            faces,
            key=lambda f: f["confidence"]
        )

        # -------------------------
        # Generate embedding
        # -------------------------
        embedding = embedder.embed(best_face["face"])
        if embedding is None:
            logger.warning(
                f"Failed to generate embedding for user_id={user.user_id}"
            )
            continue

        user_embeddings[user.user_id] = embedding

    logger.info(
        f"Generated embeddings for {len(user_embeddings)} users "
        f"out of {len(users)}"
    )

    return user_embeddings
