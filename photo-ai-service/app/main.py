from fastapi import FastAPI
from app.api.routes import router
from app.config import logger, SERVICE_NAME

# -------------------------------------------------
# App Initialization
# -------------------------------------------------
app = FastAPI(
    title=SERVICE_NAME,
    description="AI service for event photo face matching",
    version="1.0.0"
)

# -------------------------------------------------
# Routes
# -------------------------------------------------
app.include_router(router)

# -------------------------------------------------
# Startup & Shutdown Events
# -------------------------------------------------
@app.on_event("startup")
def on_startup():
    """
    Runs once when the service starts.
    Useful for warming up models.
    """
    logger.info("Photo AI Service starting up...")

    # Importing here ensures InsightFace models are downloaded at startup
    from app.pipelines.detect_faces import FaceDetector
    from app.pipelines.generate_embed import FaceEmbedder
    from app.pipelines.match_faces import FaceMatcher

    FaceDetector()
    FaceEmbedder()
    FaceMatcher()

    logger.info("Models loaded and service ready")


@app.on_event("shutdown")
def on_shutdown():
    """
    Runs once when the service shuts down.
    """
    logger.info("Photo AI Service shutting down...")
