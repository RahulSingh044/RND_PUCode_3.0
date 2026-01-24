from app.risk_profiles.base import update_rolling_average, classify_risk


MAX_ISSUES_TRACKED = 10
VENUE_DECAY = 0.97  # venues change slower than hosts


def update_venue_risk(profile: dict, event_score: float, issues: list):
    """
    Update venue risk profile.
    Venue risks are structural and evolve slowly.
    """

    # --- Sanitize existing profile ---
    old_avg = float(profile.get("avgIncidentScore", 0.0))
    count = int(profile.get("eventCount", 0))
    issue_counts = profile.get("issueCounts", {})

    if not isinstance(issue_counts, dict):
        issue_counts = {}

    # --- Update rolling average with slower decay ---
    new_avg = update_rolling_average(
        old_avg,
        count,
        event_score,
        decay=VENUE_DECAY
    )

    # --- Update basic stats ---
    profile["avgIncidentScore"] = new_avg
    profile["eventCount"] = count + 1
    profile["riskLevel"] = classify_risk(new_avg)

    # --- Track issues (deduplicated per event) ---
    for issue in set(issues):
        issue_counts[issue] = issue_counts.get(issue, 0) + 1

    # --- Trim issueCounts to avoid unbounded growth ---
    if len(issue_counts) > MAX_ISSUES_TRACKED:
        issue_counts = dict(
            sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:MAX_ISSUES_TRACKED]
        )

    profile["issueCounts"] = issue_counts

    # --- Compute common structural issues ---
    profile["commonIssues"] = [
        issue for issue, _ in sorted(
            issue_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
    ]

    # --- Explainability metadata ---
    profile["lastUpdatedBy"] = "event_incident"
    profile["lastEventScore"] = round(event_score, 3)

    return profile
