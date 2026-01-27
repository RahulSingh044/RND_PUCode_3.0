from typing import Optional

from app.schemas.request import EventContext
from app.schemas.internal import FoodPlanInternal


def build_food_plan(event_context: EventContext) -> Optional[FoodPlanInternal]:
    """
    Builds a food management plan if food is provided.

    Enhancements:
    - Food buffer planning
    - Batch/row-wise distribution
    - Food counter estimation based on guest count
    """

    # ----------------------------------
    # If no food, no plan
    # ----------------------------------
    if not event_context.food_provided:
        return None

    participant_count = event_context.participant_count

    # ----------------------------------
    # Buffer time logic
    # ----------------------------------
    buffer_minutes = "10–15"

    if (
        event_context.ticketing_type == "free"
        and event_context.audience_type == "students"
        and participant_count >= 150
    ):
        buffer_minutes = "15–20"

    if participant_count >= 300:
        buffer_minutes = "20–25"

    # ----------------------------------
    # Food counter planning
    # ----------------------------------
    # Rule of thumb:
    # 1 counter can comfortably serve ~60–70 people in 20–25 mins
    if participant_count <= 60:
        counters = 1
    elif participant_count <= 120:
        counters = 2
    elif participant_count <= 200:
        counters = 3
    elif participant_count <= 300:
        counters = 4
    else:
        counters = max(4, participant_count // 70)

    # ----------------------------------
    # Serving strategy
    # ----------------------------------
    serve_after_event = True
    batch_distribution = True

    return FoodPlanInternal(
        buffer_minutes=buffer_minutes,
        serve_after_event=serve_after_event,
        batch_distribution=batch_distribution,
        counters_required=counters
    )
