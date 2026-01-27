from typing import Dict, List
import os
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

from app.config import logger
from app.pipelines.detect_faces import FaceDetector
from app.pipelines.generate_embed import FaceEmbedder
from app.pipelines.match_faces import FaceMatcher
from app.pipelines.generate_user_embeddings import generate_user_embeddings
from app.schemas.event_payload import EventPayload
from app.utils.batching import batchify
from app.workers.photo_worker import process_photo_batch



PHOTO_BATCH_SIZE = 8
MAX_WORKERS = max(1, os.cpu_count() - 1)


def process_event_pipeline(payload: EventPayload) -> List[Dict]:
    logger.info(f"Starting processing for event_id={payload.event_id}")

    # -------------------------------------------------
    # 1. Init base components
    # -------------------------------------------------
    detector = FaceDetector()
    embedder = FaceEmbedder()
    matcher = FaceMatcher()

    # -------------------------------------------------
    # 2. Generate ALL user embeddings (ONCE)
    # -------------------------------------------------
    user_embeddings: Dict[str, np.ndarray] = generate_user_embeddings(
        users=payload.users,
        detector=detector,
        embedder=embedder
    )

    if not user_embeddings:
        logger.warning("No valid user embeddings. Aborting event.")
        return []

    all_matches: List[Dict] = []
    futures = []

    # -------------------------------------------------
    # 3. Parallel photo processing
    # -------------------------------------------------
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for photo_batch in batchify(payload.photos, PHOTO_BATCH_SIZE):
            futures.append(
                executor.submit(
                    process_photo_batch,
                    photo_batch,
                    user_embeddings,
                    payload.event_id
                )
            )

        for future in as_completed(futures):
            try:
                all_matches.extend(future.result())
            except Exception:
                logger.exception("Photo batch failed")

    logger.info(
        f"Completed processing for event_id={payload.event_id} | "
        f"total_matches={len(all_matches)}"
    )

    return all_matches

