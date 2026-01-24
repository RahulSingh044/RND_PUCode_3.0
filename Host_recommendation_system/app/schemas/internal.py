from typing import List, Dict, Literal, Optional
from pydantic import BaseModel


# -----------------------------
# Repo-1 Derived Signals
# -----------------------------
class HostRiskSignals(BaseModel):
    """
    Signals derived from Repo-1 host_risks.json
    """
    avg_incident_score: float
    last_event_score: float
    event_count: int
    risk_level: Literal["low", "medium", "high"]
    common_issues: List[str]
    issue_counts: Dict[str, int]
    incident_trend: Literal["improving", "stable", "worsening"]


class VenueRiskSignals(BaseModel):
    """
    Signals derived from Repo-1 venue_risks.json
    """
    avg_incident_score: float
    event_count: int
    risk_level: Literal["low", "medium", "high"]
    common_issues: List[str]
    issue_counts: Dict[str, int]


# -----------------------------
# Context Analysis (Backend Input)
# -----------------------------
class EventContextSignals(BaseModel):
    """
    Signals inferred from backend-provided event context
    """
    participant_load: Literal["low", "medium", "high"]
    is_free_event: bool
    is_student_audience: bool
    is_indoor: bool
    has_food: bool
    duration_bucket: Literal["short", "medium", "long"]


# -----------------------------
# Recommendation Building Blocks
# -----------------------------
class VolunteerPlanInternal(BaseModel):
    ratio: str
    total_required: int
    role_distribution: Dict[str, int]


class FoodPlanInternal(BaseModel):
    buffer_minutes: str
    serve_after_event: bool
    batch_distribution: bool
    counters_required: int



class RecommendationBuckets(BaseModel):
    """
    Raw recommendation buckets before formatting
    """
    before_event: List[str]
    during_event: List[str]
    after_event: List[str]


# -----------------------------
# Final Internal Aggregation
# -----------------------------
class InternalRecommendationResult(BaseModel):
    """
    Final internal object passed to response builder and PDF generator
    """
    host_id: str
    confidence: float

    host_risk: HostRiskSignals
    venue_risk: Optional[VenueRiskSignals]

    context_signals: EventContextSignals

    volunteer_plan: VolunteerPlanInternal
    food_plan: Optional[FoodPlanInternal]

    recommendations: RecommendationBuckets
