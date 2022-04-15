from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field

from core.models.utils import PyObjectId


class Donation(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    donation_id: int = Field(..., description="The donation's unique identifier.")
    amount: float = Field(..., description="The donation's amount.", gt=0)
    currency: str = Field("EUR", const=True, description="The donation's currency.")
    donor: str = Field(..., description="The donation's donor.", min_length=1, max_length=140)
    message: str = Field(..., description="The donation's message.", max_length=500)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class OutputDonation(Donation):
    streamer_id: int = Field(..., description="The donation's streamer's unique identifier.")
    created_at: datetime = Field(..., description="The donation's creation date.")
