from typing import Dict, List
import numpy as np

from app.services.image_loader import load_image_from_url
from app.pipelines.detect_faces import FaceDetector
from app.pipelines.generate_embed import FaceEmbedder
from app.pipelines.match_faces import FaceMatcher


def process_photo_batch(
    photo_batch,
    user_embeddings: Dict[str, np.ndarray],
    event_id: str
) -> List[dict]:
    """
    Worker process: handles a batch of photos.
    Models are initialized INSIDE the process.
    """

    detector = FaceDetector()
    embedder = FaceEmbedder()
    matcher = FaceMatcher()

    results = []

    for photo in photo_batch:
        image = load_image_from_url(photo.url)
        if image is None:
            continue

        faces = detector.detect(image)
        if not faces:
            continue

        photo_faces = []
        for face_data in faces:
            emb = embedder.embed(face_data["face"])
            if emb is not None:
                photo_faces.append({"embedding": emb})

        matches = matcher.match(user_embeddings, photo_faces)

        for match in matches:
            results.append({
                "event_id": event_id,
                "photo_id": photo.photo_id,
                "user_id": match["user_id"],
                "confidence": match["confidence"]
            })

    return results

