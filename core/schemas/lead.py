from datetime import datetime

from pydantic import BaseModel


class LeadResponse(BaseModel):
    id: int
    external_id: str
    created_at: datetime

    class Config:
        from_attributes = True