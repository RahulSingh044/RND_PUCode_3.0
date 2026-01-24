import json
import os
from typing import Optional

from app.schemas.internal import HostRiskSignals, VenueRiskSignals

# ==================================================
# DIRECT PATH TO INCIDENT REPO STORAGE
# ==================================================

INCIDENT_STORAGE_PATH = "../incident-intelligence-service/storage"

HOST_RISK_FILE = "host_risks.json"
VENUE_RISK_FILE = "venue_risks.json"


# ==================================================
# LOADERS
# ==================================================

def load_host_risk(host_id: str) -> HostRiskSignals:
    """
    Reads host risk data directly from
    incident-intelligence-service/storage/host_risks.json
    """

    path = os.path.join(INCIDENT_STORAGE_PATH, HOST_RISK_FILE)
    data = _safe_load_json(path)

    raw = data.get(host_id)
    if not raw:
        return _default_host_risk()

    avg_score = raw.get("avgIncidentScore", 0.0)
    last_score = raw.get("lastEventScore", avg_score)

    if last_score > avg_score + 0.02:
        trend = "worsening"
    elif last_score < avg_score - 0.02:
        trend = "improving"
    else:
        trend = "stable"

    return HostRiskSignals(
        avg_incident_score=avg_score,
        last_event_score=last_score,
        event_count=raw.get("eventCount", 0),
        risk_level=raw.get("riskLevel", "low"),
        common_issues=raw.get("commonIssues", []),
        issue_counts=raw.get("issueCounts", {}),
        incident_trend=trend
    )


def load_venue_risk(venue_id: Optional[str]) -> Optional[VenueRiskSignals]:
    """
    Reads venue risk data directly from
    incident-intelligence-service/storage/venue_risks.json
    """

    if not venue_id:
        return None

    path = os.path.join(INCIDENT_STORAGE_PATH, VENUE_RISK_FILE)
    data = _safe_load_json(path)

    raw = data.get(venue_id)
    if not raw:
        return None

    return VenueRiskSignals(
        avg_incident_score=raw.get("avgIncidentScore", 0.0),
        event_count=raw.get("eventCount", 0),
        risk_level=raw.get("riskLevel", "low"),
        common_issues=raw.get("commonIssues", []),
        issue_counts=raw.get("issueCounts", {})
    )


# ==================================================
# HELPERS
# ==================================================

def _safe_load_json(path: str) -> dict:
    if not os.path.exists(path):
        return {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _default_host_risk() -> HostRiskSignals:
    return HostRiskSignals(
        avg_incident_score=0.0,
        last_event_score=0.0,
        event_count=0,
        risk_level="low",
        common_issues=[],
        issue_counts={},
        incident_trend="stable"
    )
