from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.schemas.event_payload import EventPayload, ProcessResponse
from app.pipelines.process_event import process_event_pipeline
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health", tags=["health"])
def health_check():
    """
    Health check endpoint to verify the service is running.
    Used by load balancers, Docker, and monitoring tools.
    """
    return {"status": "ok", "service": "photo-ai-service"}


@router.post(
    "/process-event",
    tags=["processing"]
)
async def process_event(
    payload: EventPayload
):
    """
    Synchronous processing:
    Waits for the entire AI pipeline to finish and returns 
    all matches directly in the response.
    """
    try:
        # Basic sanity checks
        if not payload.photos:
            raise HTTPException(status_code=400, detail="No photos provided")
        if not payload.users:
            raise HTTPException(status_code=400, detail="No users provided")

        logger.info(f"Starting synchronous processing for event: {payload.event_id}")

        # Call pipeline directly and wait for results
        from app.pipelines.process_event import process_event_pipeline
        results = process_event_pipeline(payload)

        return {
            "event_id": payload.event_id,
            "status": "completed",
            "total_matches": len(results),
            "matches": results
        }

    except Exception as e:
        logger.exception("Processing failed")
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )

