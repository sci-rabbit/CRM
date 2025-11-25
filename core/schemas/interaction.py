from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from core.schemas.lead import LeadResponse


class InteractionResponse(BaseModel):
    id: int
    created_at: datetime
    lead_id: int
    source_id: int
    operator_id: Optional[int]
    is_active: bool

    class Config:
        from_attributes = True


class LeadWithInteractions(LeadResponse):
    interactions: List[InteractionResponse]


class InteractionCreate(BaseModel):
    external_lead_id: str
    source_id: int


class DistributionResponse(BaseModel):
    operator_id: int
    source_id: int
    count: int