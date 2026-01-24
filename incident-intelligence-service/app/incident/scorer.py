def clamp(value: float, min_v: float = 0.0, max_v: float = 1.0) -> float:
    return max(min_v, min(value, max_v))


def normalize_schedule_delay(minutes: int) -> float:
    if minutes <= 0:
        return 0.0
    if minutes >= 60:
        return 1.0
    return round(minutes / 60, 3)


def compute_incident_score(signals: dict) -> dict:
    # --- Sanitize inputs ---
    incident_hint_rate = clamp(signals.get("incidentHintRate", 0))
    negative_feedback_rate = clamp(signals.get("negativeFeedbackRate", 0))
    high_severity_ratio = clamp(signals.get("highSeverityRatio", 0))
    early_exit_rate = clamp(signals.get("earlyExitRate", 0))
    refund_rate = clamp(signals.get("refundRate", 0))

    schedule_delay = normalize_schedule_delay(
        signals.get("scheduleDeviationMinutes", 0)
    )

    # --- Weighted scoring ---
    components = {
        "incidentHint": 0.30 * incident_hint_rate,
        "negativeFeedback": 0.20 * negative_feedback_rate,
        "highSeverity": 0.20 * high_severity_ratio,
        "earlyExit": 0.15 * early_exit_rate,
        "scheduleDelay": 0.10 * schedule_delay,
        "refunds": 0.05 * refund_rate,
    }

    raw_score = sum(components.values())
    score = clamp(raw_score)

    return {
        "incidentScore": round(score, 3),
        "incidentLevel": classify_incident(score),
        "confidence": compute_confidence(signals),
        "scoreBreakdown": {k: round(v, 3) for k, v in components.items()}
    }


def classify_incident(score: float) -> str:
    if score >= 0.7:
        return "high"
    if score >= 0.4:
        return "medium"
    return "low"


def compute_confidence(signals: dict) -> float:
    """
    Confidence based on signal availability.
    Stronger signals contribute more confidence.
    """
    weights = {
        "incidentHintRate": 0.25,
        "negativeFeedbackRate": 0.2,
        "highSeverityRatio": 0.2,
        "earlyExitRate": 0.2,
        "scheduleDeviationMinutes": 0.1,
        "refundRate": 0.05
    }

    confidence = 0.4  # base confidence

    for key, w in weights.items():
        if key in signals:
            confidence += w

    return round(clamp(confidence, 0.4, 0.95), 3)
