from typing import List, Dict, Optional
from pydantic import BaseModel, Field


# -----------------------------
# Assets (PDF, future files)
# -----------------------------
class PDFAsset(BaseModel):
    title: str = Field(..., description="Title of the PDF")
    description: str = Field(..., description="Short description of the PDF")
    file_type: str = Field(..., description="MIME type of the file")
    download_url: str = Field(..., description="Download URL/path for the PDF")


class Assets(BaseModel):
    checklist_pdf: PDFAsset


# -----------------------------
# Operational Guidance
# -----------------------------
class VolunteerPlan(BaseModel):
    recommended_ratio: str
    total_volunteers_required: int
    role_distribution: Dict[str, int]


class FoodManagementPlan(BaseModel):
    recommended_buffer_minutes: str
    serving_strategy: str
    distribution_method: str
    important_note: str


class OperationalGuidance(BaseModel):
    volunteer_plan: VolunteerPlan
    food_management_plan: Optional[FoodManagementPlan] = None


# -----------------------------
# Recommendations
# -----------------------------
class HostSuccessRecommendations(BaseModel):
    before_event: List[str]
    during_event: List[str]
    after_event: List[str]


# -----------------------------
# Main Response Schema
# -----------------------------
class HostRecommendationResponse(BaseModel):
    host_id: str
    confidence: float = Field(..., ge=0.0, le=1.0)

    event_context: Dict[str, object]

    operational_guidance: OperationalGuidance
    host_success_recommendations: HostSuccessRecommendations

    assets: Assets
