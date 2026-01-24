from typing import List, Optional
from pydantic import BaseModel, Field


# -------------------------
# Photo Schema (Host uploads)
# -------------------------
class PhotoPayload(BaseModel):
    photo_id: str = Field(..., description="Unique ID of the photo")
    url: str = Field(..., description="Public or signed URL of the photo")


# -------------------------
# User Schema (Selfie via URL)
# -------------------------
class UserPayload(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    image_url: str = Field(
        ...,
        description="URL of user's selfie image provided by backend"
    )


# -------------------------
# Event Payload (Main Input)
# -------------------------
class EventPayload(BaseModel):
    event_id: str = Field(..., description="Unique event identifier")

    photos: List[PhotoPayload] = Field(
        default_factory=list,
        description="List of event photos uploaded by host"
    )

    users: List[UserPayload] = Field(
        default_factory=list,
        description="List of users with selfie image URLs"
    )


# -------------------------
# Processing Response
# -------------------------
class ProcessResponse(BaseModel):
    event_id: str
    status: str
    message: str
