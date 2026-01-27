from typing import Dict, Any, Optional, List, Tuple

from app.schemas.request import EventContext
from app.schemas.internal import (
    HostRiskSignals,
    VenueRiskSignals,
    RecommendationBuckets,
    VolunteerPlanInternal,
)

from app.services.repo1_loader import load_host_risk, load_venue_risk
from app.services.context_analyzer import analyze_event_context
from app.services.volunteer_calculator import calculate_volunteer_plan
from app.services.food_planner import build_food_plan
from app.services.constraint_filter import filter_recommendations
from app.services.checklist_builder import build_checklist_items
from app.services.confidence_calculator import calculate_confidence


# =====================================================
# PUBLIC ENTRY
# =====================================================

def generate_host_recommendation(
    host_id: str,
    event_context: EventContext
) -> Dict[str, Any]:
    """
    GOD-LEVEL recommendation engine.

    Responsibilities:
    - Interpret historical risk patterns
    - Understand current event dynamics
    - Predict operational failure modes
    - Generate realistic, venue-safe guidance
    - Produce execution-ready output + checklist
    """

    # -------------------------------------------------
    # 1️⃣ Load historical intelligence (Repo-1)
    # -------------------------------------------------
    host_risk: HostRiskSignals = load_host_risk(host_id)
    venue_risk: Optional[VenueRiskSignals] = load_venue_risk(host_id)

    # -------------------------------------------------
    # 2️⃣ Normalize backend context
    # -------------------------------------------------
    context_signals = analyze_event_context(event_context)

    # -------------------------------------------------
    # 3️⃣ Operational planning
    # -------------------------------------------------
    volunteer_plan = calculate_volunteer_plan(
        participant_count=event_context.participant_count
    )

    food_plan = build_food_plan(event_context)

    # -------------------------------------------------
    # 4️⃣ Detect likely failure modes
    # -------------------------------------------------
    failure_modes = _detect_failure_modes(
        host_risk=host_risk,
        context=context_signals,
        event_context=event_context
    )

    # -------------------------------------------------
    # 5️⃣ Generate raw recommendations (reasoned)
    # -------------------------------------------------
    raw_recommendations = _generate_recommendations_from_failures(
        failure_modes=failure_modes,
        context=context_signals
    )

    # -------------------------------------------------
    # 6️⃣ Constraint filtering (reality check)
    # -------------------------------------------------
    filtered_recommendations = RecommendationBuckets(
        before_event=filter_recommendations(
            raw_recommendations.before_event, context_signals
        ),
        during_event=filter_recommendations(
            raw_recommendations.during_event, context_signals
        ),
        after_event=filter_recommendations(
            raw_recommendations.after_event, context_signals
        )
    )

    # -------------------------------------------------
    # 7️⃣ Confidence calculation
    # -------------------------------------------------
    confidence = calculate_confidence(
        host_risk=host_risk,
        venue_risk=venue_risk,
        context_signals=context_signals
    )

    # -------------------------------------------------
    # 8️⃣ Build checklist (single source of truth)
    # -------------------------------------------------
    checklist_items = build_checklist_items(
        recommendations=filtered_recommendations,
        volunteer_plan=volunteer_plan,
        food_plan=food_plan
    )

    # -------------------------------------------------
    # 9️⃣ Assemble final response
    # -------------------------------------------------
    response: Dict[str, Any] = {
        "host_id": host_id,
        "confidence": confidence,

        "event_context": event_context.model_dump(),

        "operational_guidance": {
            "volunteer_plan": {
                "recommended_ratio": volunteer_plan.ratio,
                "total_volunteers_required": volunteer_plan.total_required,
                "role_distribution": volunteer_plan.role_distribution
            }
        },

        "host_success_recommendations": {
            "before_event": filtered_recommendations.before_event,
            "during_event": filtered_recommendations.during_event,
            "after_event": filtered_recommendations.after_event
        },

        # Internal → used by PDF generator
        "_checklist_items": checklist_items
    }

    if food_plan:
        response["operational_guidance"]["food_management_plan"] = {
            "recommended_buffer_minutes": food_plan.buffer_minutes,
            "serving_strategy": "Serve food only after the main session",
            "distribution_method": "Batch / row-wise release",
            "important_note": "Announce food timing clearly to avoid crowd rush",
            "counters_required": food_plan.counters_required
        }

    return response


# =====================================================
# FAILURE MODE INTELLIGENCE (THE REAL MAGIC)
# =====================================================

def _detect_failure_modes(
    host_risk: HostRiskSignals,
    context,
    event_context: EventContext
) -> List[str]:
    """
    Predicts *how this event can fail*.
    This is more powerful than reacting to issues.
    """

    modes: List[str] = []

    # Historical patterns
    if "entry" in host_risk.common_issues:
        modes.append("entry_congestion")

    if "crowd" in host_risk.common_issues:
        modes.append("crowd_pressure")

    if "security" in host_risk.common_issues:
        modes.append("security_coordination_gap")

    # Context amplification
    if context.is_free_event and context.is_student_audience:
        modes.append("late_arrivals_and_rush")

    if context.participant_load == "high":
        modes.append("resource_overstretch")

    if context.has_food:
        modes.append("post_event_food_rush")

    # Duration-based risks
    if context.duration_bucket == "long":
        modes.append("attention_drop_and_movement")

    return list(set(modes))


# =====================================================
# RECOMMENDATION GENERATION (REASONED)
# =====================================================

def _generate_recommendations_from_failures(
    failure_modes: List[str],
    context
) -> RecommendationBuckets:
    """
    Converts failure modes into actionable guidance.
    """

    before, during, after = [], [], []

    for mode in failure_modes:

        if mode == "entry_congestion":
            before.append("Design entry flow and volunteer placement in advance")
            during.append("Actively manage queues and slow entry if congestion builds")

        if mode == "crowd_pressure":
            before.append("Assign volunteers specifically for crowd guidance")
            during.append("Monitor crowd density and redistribute volunteers dynamically")

        if mode == "security_coordination_gap":
            before.append("Brief security and volunteers together with clear escalation flow")
            during.append("Maintain continuous communication with security staff")

        if mode == "late_arrivals_and_rush":
            before.append("Communicate clear entry timing expectations to attendees")
            during.append("Use calm announcements to manage late-arrival crowd behavior")

        if mode == "resource_overstretch":
            before.append("Open entry earlier to distribute arrival load")
            during.append("Prevent crowd buildup near exits and aisles")

        if mode == "post_event_food_rush":
            before.append("Clearly communicate food timing before the event starts")
            after.append("Release attendees in controlled batches for food distribution")

        if mode == "attention_drop_and_movement":
            during.append("Minimize movement during sessions using volunteer guidance")

    after.extend([
        "Review operational bottlenecks observed during the event",
        "Document learnings and reuse the same playbook for similar future events"
    ])

    return RecommendationBuckets(
        before_event=_dedupe(before),
        during_event=_dedupe(during),
        after_event=_dedupe(after)
    )


# =====================================================
# UTIL
# =====================================================

def _dedupe(items: List[str]) -> List[str]:
    seen = set()
    out = []
    for i in items:
        k = i.lower()
        if k not in seen:
            seen.add(k)
            out.append(i)
    return out
