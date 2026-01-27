from pydantic import BaseModel, Field
from typing import List, Literal


class Timing(BaseModel):
    scheduledStart: str = Field(..., description="Planned event start time (HH:MM)")
    actualStart: str = Field(..., description="Actual event start time (HH:MM)")
    actualEnd: str = Field(..., description="Actual event end time (HH:MM)")


class Attendance(BaseModel):
    registeredCount: int = Field(..., ge=0, description="Total registered attendees")
    checkedInCount: int = Field(..., ge=0, description="Attendees who checked in")


class Refunds(BaseModel):
    refundCount: int = Field(..., ge=0, description="Number of refunds issued")
    refundRate: float = Field(
        ..., ge=0.0, le=1.0, description="Refunds as a fraction of registrations"
    )


class Venue(BaseModel):
    venueCapacity: int = Field(..., ge=0, description="Maximum venue capacity")
    venueType: Literal["open", "closed", "semi-open"] = Field(
        ..., description="Type of venue"
    )


class EventPayload(BaseModel):
    eventId: str = Field(..., min_length=1)
    hostId: str = Field(..., min_length=1)
    venueId: str = Field(..., min_length=1)

    comments: List[str] = Field(
        ..., min_length=1, description="User feedback comments for the event"
    )

    timing: Timing
    attendance: Attendance
    refunds: Refunds
    venue: Venue
