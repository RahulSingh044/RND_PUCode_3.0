from typing import Optional
from app.schemas.internal import (
    HostRiskSignals,
    VenueRiskSignals,
    EventContextSignals
)


def calculate_confidence(
    host_risk: HostRiskSignals,
    venue_risk: Optional[VenueRiskSignals],
    context_signals: EventContextSignals
) -> float:
    """
    Calculates confidence score (0.0 – 1.0) for host recommendations.

    Philosophy:
    - More historical data → higher confidence
    - Clear recurring issues → higher confidence
    - Stable or improving trends → higher confidence
    - High uncertainty contexts → lower confidence
    """

    score = 0.0
    weight_sum = 0.0

    # --------------------------------------------------
    # 1️⃣ Data Volume Confidence
    # --------------------------------------------------
    # More events = better pattern reliability
    if host_risk.event_count >= 5:
        score += 0.25
        weight_sum += 0.25
    elif host_risk.event_count >= 3:
        score += 0.18
        weight_sum += 0.25
    elif host_risk.event_count >= 1:
        score += 0.10
        weight_sum += 0.25
    else:
        weight_sum += 0.25

    # --------------------------------------------------
    # 2️⃣ Issue Consistency Confidence
    # --------------------------------------------------
    # Repeated issues → clearer guidance
    issue_variety = len(host_risk.common_issues)

    if issue_variety >= 3:
        score += 0.20
        weight_sum += 0.20
    elif issue_variety == 2:
        score += 0.14
        weight_sum += 0.20
    elif issue_variety == 1:
        score += 0.08
        weight_sum += 0.20
    else:
        weight_sum += 0.20

    # --------------------------------------------------
    # 3️⃣ Incident Trend Confidence
    # --------------------------------------------------
    if host_risk.incident_trend == "improving":
        score += 0.20
        weight_sum += 0.20
    elif host_risk.incident_trend == "stable":
        score += 0.14
        weight_sum += 0.20
    elif host_risk.incident_trend == "worsening":
        score += 0.10
        weight_sum += 0.20
    else:
        weight_sum += 0.20

    # --------------------------------------------------
    # 4️⃣ Context Predictability
    # --------------------------------------------------
    # Predictable contexts = higher confidence
    context_score = 0.0

    if context_signals.is_indoor:
        context_score += 0.05

    if context_signals.is_free_event and context_signals.is_student_audience:
        context_score += 0.05

    if context_signals.participant_load == "high":
        context_score += 0.05

    score += min(context_score, 0.15)
    weight_sum += 0.15

    # --------------------------------------------------
    # 5️⃣ Venue Signal Reinforcement (optional)
    # --------------------------------------------------
    if venue_risk:
        if venue_risk.event_count >= 3:
            score += 0.10
            weight_sum += 0.10
        else:
            weight_sum += 0.10
    else:
        weight_sum += 0.10

    # --------------------------------------------------
    # Final Normalization
    # --------------------------------------------------
    if weight_sum == 0:
        return 0.5  # neutral fallback

    final_confidence = score / weight_sum

    # Clamp to safe range
    return round(min(max(final_confidence, 0.35), 0.95), 2)
