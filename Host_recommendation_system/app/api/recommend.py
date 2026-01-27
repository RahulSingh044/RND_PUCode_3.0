from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.schemas.request import HostRecommendationRequest
from app.schemas.response import HostRecommendationResponse
from app.services.recommendation_engine import generate_host_recommendation
from app.pdf.checklist_generator import generate_checklist_pdf

router = APIRouter(prefix="/host", tags=["Host Recommendations"])


@router.post(
    "/recommend",
    response_model=HostRecommendationResponse,
    summary="Generate host event recommendations with checklist PDF"
)
def recommend_host(request: HostRecommendationRequest):
    """
    Main API endpoint used by backend.

    Flow:
    1. Validate backend input
    2. Generate host recommendations (Repo-1 + context)
    3. Generate checklist PDF with same points
    4. Return JSON + PDF download URL
    """

    try:
        # 1️⃣ Generate recommendations (core AI logic)
        recommendation_output = generate_host_recommendation(
            host_id=request.host_id,
            event_context=request.event_context
        )

        # 2️⃣ Generate checklist PDF using same recommendation points
        pdf_path = generate_checklist_pdf(
            host_id=request.host_id,
            event_context=request.event_context.model_dump(),
            checklist_items=recommendation_output["_checklist_items"]
        )

        # 3️⃣ Attach PDF metadata to response
        recommendation_output["assets"] = {
            "checklist_pdf": {
                "title": "Host Event Success Checklist",
                "description": "Printable checklist with checkbox items generated from AI recommendations",
                "file_type": "application/pdf",
                "download_url": pdf_path
            }
        }

        return JSONResponse(content=recommendation_output)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate host recommendation: {str(e)}"
        )
