from typing import Dict, List, Optional
from collections import OrderedDict

from app.schemas.internal import (
    RecommendationBuckets,
    VolunteerPlanInternal,
    FoodPlanInternal
)


def build_checklist_items(
    recommendations: RecommendationBuckets,
    volunteer_plan: VolunteerPlanInternal,
    food_plan: Optional[FoodPlanInternal] = None
) -> Dict[str, List[str]]:
    """
    Builds a structured, execution-ready checklist from internal recommendations.

    Design goals:
    - Actionable (imperative verbs)
    - Deduplicated
    - Ordered logically for event-day usage
    - Safe against missing / partial data
    """

    checklist: Dict[str, List[str]] = OrderedDict()

    # --------------------------------------------------
    # Volunteer Planning
    # --------------------------------------------------
    checklist["volunteer_planning"] = _dedupe([
        f"Confirm volunteer ratio ({volunteer_plan.ratio}) and availability",
        f"Ensure total volunteers assigned: {volunteer_plan.total_required}",
        "Assign fixed responsibilities to each volunteer (entry, seating, food)",
        "Nominate one lead volunteer for coordination and escalation",
        "Share emergency contact and escalation flow with all volunteers"
    ])

    # --------------------------------------------------
    # Food Management (only if applicable)
    # --------------------------------------------------
    if food_plan:
        checklist["food_management"] = _dedupe([
            f"Add a {food_plan.buffer_minutes} minute buffer before food distribution",
            "Confirm food is served only after the main session ends",
            "Plan batch-wise or row-wise release for food distribution",
            "Position volunteers near food counters to manage queues",
            "Ensure food counters do not block entry or exit paths"
        ])

    # --------------------------------------------------
    # Before Event
    # --------------------------------------------------
    checklist["before_event"] = _prepare_phase_items(
        recommendations.before_event,
        default_items=[
            "Open entry at least 30 minutes before the scheduled start time",
            "Test audio, microphone, and presentation setup before doors open",
            "Brief volunteers and security together on roles and flow",
            "Prepare announcement scripts for delays and food instructions"
        ]
    )

    # --------------------------------------------------
    # During Event
    # --------------------------------------------------
    checklist["during_event"] = _prepare_phase_items(
        recommendations.during_event,
        default_items=[
            "Guide seating actively to minimize disturbance during sessions",
            "Monitor crowd density near entry and exit points",
            "Make calm and proactive announcements if timelines shift",
            "Prevent unnecessary movement during speaker sessions"
        ]
    )

    # --------------------------------------------------
    # After Event
    # --------------------------------------------------
    checklist["after_event"] = _prepare_phase_items(
        recommendations.after_event,
        default_items=[
            "Release attendees gradually instead of allowing mass exit",
            "Thank attendees, speakers, and volunteers before exit",
            "Observe and note entry, seating, and food bottlenecks",
            "Document learnings for future similar events"
        ]
    )

    return checklist


# ======================================================
# Helper Functions
# ======================================================

def _prepare_phase_items(
    primary_items: List[str],
    default_items: List[str]
) -> List[str]:
    """
    Combines AI-generated recommendations with safe defaults,
    enforces action wording, and removes duplicates.
    """
    combined = []

    for item in primary_items:
        combined.append(_normalize_action(item))

    for item in default_items:
        combined.append(_normalize_action(item))

    return _dedupe(combined)


def _normalize_action(text: str) -> str:
    """
    Ensures checklist items read like clear actions.
    """
    text = text.strip()

    # If already action-oriented, keep as is
    action_prefixes = (
        "open", "ensure", "assign", "confirm", "monitor",
        "guide", "prepare", "share", "plan", "test", "review"
    )

    if text.lower().startswith(action_prefixes):
        return text

    # Otherwise, convert to imperative style
    return f"Ensure {text[0].lower() + text[1:]}"


def _dedupe(items: List[str]) -> List[str]:
    """
    Removes duplicates while preserving order.
    """
    seen = set()
    unique_items = []

    for item in items:
        normalized = item.lower()
        if normalized not in seen:
            seen.add(normalized)
            unique_items.append(item)

    return unique_items
