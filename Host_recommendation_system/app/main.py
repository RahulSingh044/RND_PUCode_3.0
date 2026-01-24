from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.recommend import router as host_recommendation_router


def create_app() -> FastAPI:
    """
    Application factory.
    Keeps startup clean and testable.
    """

    app = FastAPI(
        title="Host AI Recommendation Engine",
        description=(
            "AI-powered system that generates operational recommendations "
            "and execution checklists for event hosts using incident intelligence."
        ),
        version="1.0.0"
    )

    # --------------------------------------------------
    # CORS (safe defaults, adjustable later)
    # --------------------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],          # tighten in prod
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --------------------------------------------------
    # Routers
    # --------------------------------------------------
    app.include_router(
        host_recommendation_router,
        prefix="/api"
    )

    # --------------------------------------------------
    # Health Check
    # --------------------------------------------------
    @app.get("/health", tags=["Health"])
    def health_check():
        return {
            "status": "ok",
            "service": "host-ai-recommendation-engine"
        }

    return app


# ------------------------------------------------------
# ASGI entrypoint
# ------------------------------------------------------
app = create_app()
