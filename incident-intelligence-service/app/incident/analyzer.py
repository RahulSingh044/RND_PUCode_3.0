from collections import Counter
from app.nlp.pipeline import analyze_feedback
from app.incident.aggregator import aggregate_feedback
from app.incident.scorer import compute_incident_score
from app.incident.derived_signal import (
    compute_schedule_delay,
    compute_early_exit_rate,
    normalize_delay
)
from app.risk_profiles.host import update_host_risk
from app.risk_profiles.venue import update_venue_risk


def analyze_event(payload: dict, host_store: dict, venue_store: dict) -> dict:
    """
    Pure orchestration logic:
    - no globals
    - no hidden state
    """

    comments = payload.get("comments", [])

    # 1️⃣ NLP on comments (graceful handling)
    feedback_results = []
    issue_counter = Counter()

    for text in comments:
        result = analyze_feedback(text)
        feedback_results.append(result)
        for aspect in result.get("aspects", []):
            issue_counter[aspect] += 1

    # 2️⃣ Aggregate NLP signals (safe fallback)
    aggregated = (
        aggregate_feedback(feedback_results)
        if feedback_results
        else {
            "avgSentiment": 0,
            "negativeFeedbackRate": 0,
            "highSeverityRatio": 0,
            "incidentHintRate": 0
        }
    )

    # 3️⃣ Derived behavioral signals
    delay_minutes = compute_schedule_delay(payload["timing"])
    early_exit_rate = compute_early_exit_rate(payload["attendance"])

    signals = {
        **aggregated,
        "earlyExitRate": early_exit_rate,
        "scheduleDeviationMinutes": delay_minutes,
        "normalizedScheduleDeviation": normalize_delay(delay_minutes),
        "refundRate": payload["refunds"]["refundRate"]
    }

    # 4️⃣ Incident scoring
    incident = compute_incident_score(signals)
    incident_score = incident["incidentScore"]

    # 5️⃣ Incident issue summary (explainability)
    incident_issues = [
        issue for issue, _ in issue_counter.most_common(3)
    ]

    # 6️⃣ Update HOST risk (stateless)
    host_id = payload["hostId"]
    host_profile = host_store.get(host_id, {
        "avgIncidentScore": 0,
        "eventCount": 0,
        "issueCounts": {}
    })

    updated_host = update_host_risk(
        host_profile,
        incident_score,
        incident_issues
    )
    host_store[host_id] = updated_host

    # 7️⃣ Update VENUE risk
    venue_id = payload["venueId"]
    venue_profile = venue_store.get(venue_id, {
        "avgIncidentScore": 0,
        "eventCount": 0,
        "issueCounts": {}
    })

    updated_venue = update_venue_risk(
        venue_profile,
        incident_score,
        incident_issues
    )
    venue_store[venue_id] = updated_venue

    # 8️⃣ Final structured response
    return {
        "eventId": payload["eventId"],
        "incident": incident,
        "incidentIssues": incident_issues,
        "hostRisk": updated_host,
        "venueRisk": updated_venue,
        "hostStore": host_store,
        "venueStore": venue_store
    }
