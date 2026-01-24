from app.schemas.request import EventContext
from app.schemas.internal import EventContextSignals


def analyze_event_context(event_context: EventContext) -> EventContextSignals:
    """
    Converts backend-provided event context into normalized signals
    used by recommendation, constraint filtering, and confidence logic.
    """

    # -----------------------------
    # Participant load
    # -----------------------------
    if event_context.participant_count >= 300:
        participant_load = "high"
    elif event_context.participant_count >= 120:
        participant_load = "medium"
    else:
        participant_load = "low"

    # -----------------------------
    # Duration bucket
    # -----------------------------
    if event_context.event_duration_minutes <= 60:
        duration_bucket = "short"
    elif event_context.event_duration_minutes <= 150:
        duration_bucket = "medium"
    else:
        duration_bucket = "long"

    # -----------------------------
    # Boolean context flags
    # -----------------------------
    is_free_event = event_context.ticketing_type == "free"
    is_student_audience = event_context.audience_type == "students"
    is_indoor = event_context.venue_type == "indoor"
    has_food = event_context.food_provided

    return EventContextSignals(
        participant_load=participant_load,
        is_free_event=is_free_event,
        is_student_audience=is_student_audience,
        is_indoor=is_indoor,
        has_food=has_food,
        duration_bucket=duration_bucket
    )
