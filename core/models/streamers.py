from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field, PositiveFloat

from core.models.utils import PyObjectId


class Streamer(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: int = Field(..., description="Streamer ID")
    team_member_id: int = Field(..., description="Streamer team member ID")
    display_name: str = Field(..., description="Streamers display name")
    username: str = Field(..., description="Streamer username")
    goal: PositiveFloat = Field(..., description="Donation goal of the streamer")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class DatabaseStreamer(Streamer):
    created_at: datetime = Field(..., description="Streamer created at")
    updated_at: datetime = Field(..., description="Streamer updated at")
