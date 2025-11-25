from typing import Optional

from pydantic import BaseModel


class SourceOperatorCreate(BaseModel):
    operator_id: int
    weight: int


class SourceOperatorUpdate(BaseModel):
    weight: Optional[int] = None


class SourceOperatorResponse(SourceOperatorCreate):
    source_id: int

    class Config:
        from_attributes = True