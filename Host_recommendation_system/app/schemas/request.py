from typing import Literal
from pydantic import BaseModel, Field


class EventContext(BaseModel):
    """
    Context of the event provided by backend.
    This is LIVE data (not historical).
    """

    participant_count: int = Field(
        ...,
        gt=0,
        description="Total expected number of participants"
    )

    event_type: Literal[
        "tech_talk",
        "workshop",
        "conference",
        "concert",
        "meetup",
        "other"
    ] = Field(
        ...,
        description="Type of event"
    )

    venue_type: Literal[
        "indoor",
        "outdoor",
        "semi_indoor"
    ] = Field(
        ...,
        description="Type of venue"
    )

    event_duration_minutes: int = Field(
        ...,
        gt=0,
        description="Total event duration in minutes"
    )

    ticketing_type: Literal[
        "free",
        "paid"
    ] = Field(
        ...,
        description="Whether the event is free or paid"
    )

    audience_type: Literal[
        "students",
        "professionals",
        "mixed"
    ] = Field(
        ...,
        description="Primary audience type"
    )

    food_provided: bool = Field(
        ...,
        description="Whether food is provided in the event"
    )


class HostRecommendationRequest(BaseModel):
    """
    Main request schema sent by backend to Repo-2.
    """

    host_id: str = Field(
        ...,
        min_length=1,
        description="Unique identifier of the host"
    )

    event_context: EventContext
