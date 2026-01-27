import numpy as np
from typing import List
from insightface.app import FaceAnalysis

from app.config import logger, FACE_DETECTION_THRESHOLD


class FaceDetector:
    """
    Wrapper around InsightFace RetinaFace detector.
    Initializes once and reused across requests.
    """

    def __init__(self):
        logger.info("Initializing FaceDetector (RetinaFace via InsightFace)")

        self.app = FaceAnalysis(
            name="buffalo_l",
            providers=["CPUExecutionProvider"]
        )

        self.app.prepare(
            ctx_id=0,
            det_size=(640, 640)
        )

        logger.info("FaceDetector initialized successfully")

    def detect(self, image: np.ndarray) -> List[dict]:
        """
        Detect faces in an image.

        Returns a list of dicts:
        {
            "bbox": [x1, y1, x2, y2],
            "confidence": float,
            "face": insightface Face object
        }
        """
        try:
            faces = self.app.get(image)

            results = []
            for face in faces:
                if face.det_score < FACE_DETECTION_THRESHOLD:
                    continue

                results.append({
                    "bbox": face.bbox.astype(int).tolist(),
                    "confidence": float(face.det_score),
                    "face": face   
                })

            logger.info(f"Detected {len(results)} valid faces")
            return results

        except Exception as e:
            logger.exception("Face detection failed")
            return []
