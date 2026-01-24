import logging
import os

# -------------------------------------------------
# Service Metadata
# -------------------------------------------------
SERVICE_NAME = "photo-ai-service"

# -------------------------------------------------
# Logging Configuration
# -------------------------------------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(SERVICE_NAME)

# -------------------------------------------------
# Face Detection Configuration
# -------------------------------------------------
# Minimum confidence score for a detected face
FACE_DETECTION_THRESHOLD = float(
    os.getenv("FACE_DETECTION_THRESHOLD", 0.6)
)

# -------------------------------------------------
# Face Matching Configuration
# -------------------------------------------------
# Cosine similarity threshold for face match
FACE_MATCH_THRESHOLD = float(
    os.getenv("FACE_MATCH_THRESHOLD", 0.65)
)

# -------------------------------------------------
# Image Download Configuration
# -------------------------------------------------
# Timeout (seconds) for downloading images
IMAGE_DOWNLOAD_TIMEOUT = int(
    os.getenv("IMAGE_DOWNLOAD_TIMEOUT", 10)
)

# -------------------------------------------------
# Model Configuration
# -------------------------------------------------
# InsightFace model name (ArcFace + RetinaFace)
INSIGHTFACE_MODEL_NAME = os.getenv(
    "INSIGHTFACE_MODEL_NAME", "buffalo_l"
)

# Optional: force InsightFace model cache directory
# Uncomment if you want models inside project folder
# INSIGHTFACE_MODEL_DIR = os.getenv(
#     "INSIGHTFACE_MODEL_DIR",
#     os.path.join(os.getcwd(), "models")
# )
