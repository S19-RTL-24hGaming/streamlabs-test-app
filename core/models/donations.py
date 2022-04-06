from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field

from core.models.utils import PyObjectId


class Donation(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    donation_id: int = Field(..., description="The donation's unique identifier.")
    amount: float = Field(..., description="The donation's amount.")
    currency: str = Field("EUR", const=True, description="The donation's currency.")
    donor: str = Field(..., description="The donation's donor.", min_length=2, max_length=25)
    message: str = Field(..., description="The donation's message.", max_length=255)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class DatabaseDonation(Donation):
    created_at: datetime = Field(..., description="The donation's creation date.")
