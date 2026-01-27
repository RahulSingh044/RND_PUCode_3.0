def aggregate_feedback(feedback_list: list) -> dict:
    total = len(feedback_list)

    # Graceful fallback
    if total == 0:
        return {
            "avgSentiment": 0.0,
            "negativeFeedbackRate": 0.0,
            "highSeverityRatio": 0.0,
            "incidentHintRate": 0.0,
            "feedbackCount": 0,
            "feedbackWeight": 0.0
        }

    negative_score = 0.0
    high_severity = 0
    incident_hints = 0
    sentiment_sum = 0.0

    for fb in feedback_list:
        sentiment = fb.get("sentiment", 0.0)
        severity = fb.get("severity", "low")
        hint = fb.get("incidentHint", False)

        sentiment_sum += sentiment

        # Soft negative scoring (stronger negatives matter more)
        if sentiment < -0.2:
            negative_score += abs(sentiment)

        if severity == "high":
            high_severity += 1

        if hint:
            incident_hints += 1

    # Base rates
    negative_rate = min(negative_score / total, 1.0)
    high_severity_ratio = high_severity / total
    incident_hint_rate = incident_hints / total

    # Dampening factor for low feedback volume
    # (prevents 1–2 comments from dominating)
    feedback_weight = min(total / 10, 1.0)

    return {
        "avgSentiment": round(sentiment_sum / total, 3),
        "negativeFeedbackRate": round(negative_rate * feedback_weight, 3),
        "highSeverityRatio": round(high_severity_ratio * feedback_weight, 3),
        "incidentHintRate": round(incident_hint_rate * feedback_weight, 3),
        "feedbackCount": total,
        "feedbackWeight": round(feedback_weight, 2)
    }
