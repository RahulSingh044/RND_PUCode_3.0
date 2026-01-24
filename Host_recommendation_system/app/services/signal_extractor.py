from typing import Dict, List

from app.schemas.internal import HostRiskSignals, VenueRiskSignals


# ==================================================
# HOST SIGNAL EXTRACTION
# ==================================================

def extract_host_signals(host_risk: HostRiskSignals) -> Dict[str, object]:
    """
    Converts HostRiskSignals into high-level reasoning signals
    used by recommendation logic.
    """

    signals: Dict[str, object] = {}

    # -----------------------------
    # Volume & reliability
    # -----------------------------
    signals["has_history"] = host_risk.event_count > 0
    signals["history_depth"] = _bucket_event_count(host_risk.event_count)

    # -----------------------------
    # Incident severity
    # -----------------------------
    signals["avg_incident_level"] = _bucket_incident_score(
        host_risk.avg_incident_score
    )

    # -----------------------------
    # Trend behavior
    # -----------------------------
    signals["trend"] = host_risk.incident_trend

    # -----------------------------
    # Issue dominance
    # -----------------------------
    dominant_issue, dominance_ratio = _dominant_issue(
        host_risk.issue_counts
    )

    signals["dominant_issue"] = dominant_issue
    signals["issue_dominance_ratio"] = dominance_ratio

    # -----------------------------
    # Multi-issue complexity
    # -----------------------------
    signals["issue_complexity"] = _bucket_issue_complexity(
        host_risk.issue_counts
    )

    # -----------------------------
    # Stability
    # -----------------------------
    signals["is_stable"] = (
        host_risk.incident_trend == "stable"
        and dominance_ratio < 0.6
    )

    return signals


# ==================================================
# VENUE SIGNAL EXTRACTION
# ==================================================

def extract_venue_signals(
    venue_risk: VenueRiskSignals
) -> Dict[str, object]:
    """
    Extracts reasoning signals from venue risk data.
    """

    signals: Dict[str, object] = {}

    signals["venue_history_depth"] = _bucket_event_count(
        venue_risk.event_count
    )

    dominant_issue, dominance_ratio = _dominant_issue(
        venue_risk.issue_counts
    )

    signals["dominant_venue_issue"] = dominant_issue
    signals["venue_issue_dominance_ratio"] = dominance_ratio

    signals["venue_issue_complexity"] = _bucket_issue_complexity(
        venue_risk.issue_counts
    )

    return signals


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def _bucket_event_count(count: int) -> str:
    if count >= 5:
        return "deep"
    if count >= 3:
        return "medium"
    if count >= 1:
        return "shallow"
    return "none"


def _bucket_incident_score(score: float) -> str:
    if score >= 0.6:
        return "high"
    if score >= 0.3:
        return "medium"
    return "low"


def _dominant_issue(issue_counts: Dict[str, int]) -> tuple[str, float]:
    if not issue_counts:
        return "none", 0.0

    total = sum(issue_counts.values())
    dominant_issue = max(issue_counts, key=issue_counts.get)
    dominance_ratio = issue_counts[dominant_issue] / total

    return dominant_issue, round(dominance_ratio, 2)


def _bucket_issue_complexity(issue_counts: Dict[str, int]) -> str:
    issue_types = len(issue_counts)

    if issue_types >= 4:
        return "high"
    if issue_types >= 2:
        return "medium"
    if issue_types == 1:
        return "low"
    return "none"
