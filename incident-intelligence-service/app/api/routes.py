from typing import List
from fastapi import APIRouter
from app.schemas.event_payload import EventPayload
from app.incident.analyzer import analyze_event
from app.utils.json_store import load_json, save_json

HOST_STORE = "storage/host_risks.json"
VENUE_STORE = "storage/venue_risks.json"

router = APIRouter()


@router.post("/incident/analyze-event")
def analyze_event_api(payload: EventPayload):
    # Load current risk stores
    host_risks = load_json(HOST_STORE)
    venue_risks = load_json(VENUE_STORE)

    # Run full incident intelligence
    result = analyze_event(
        payload.model_dump(),
        host_risks,
        venue_risks
    )

    # Persist updated stores
    save_json(HOST_STORE, result["hostStore"])
    save_json(VENUE_STORE, result["venueStore"])

    # Return only what backend needs
    return {
        "eventId": result["eventId"],
        "incident": result["incident"],
        "hostRisk": result["hostRisk"],
        "venueRisk": result["venueRisk"]
    }


@router.post("/incident/analyze-events-bulk")
def analyze_events_bulk(payloads: List[EventPayload]):
    # Load current risk stores once
    host_risks = load_json(HOST_STORE)
    venue_risks = load_json(VENUE_STORE)
    
    batch_results = []

    for payload in payloads:
        # Run intelligence and update the in-memory stores
        result = analyze_event(
            payload.model_dump(),
            host_risks,
            venue_risks
        )
        
        # Collect response data (excluding the full stores)
        batch_results.append({
            "eventId": result["eventId"],
            "incident": result["incident"],
            "hostRisk": result["hostRisk"],
            "venueRisk": result["venueRisk"]
        })

    # Persist updated stores after batch processing
    save_json(HOST_STORE, host_risks)
    save_json(VENUE_STORE, venue_risks)

    return {
        "processedCount": len(batch_results),
        "results": batch_results
    }
