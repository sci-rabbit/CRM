from typing import Optional

from pydantic import BaseModel


class OperatorBase(BaseModel):
    name: str
    is_active: bool = True
    limit: int = 10


class OperatorCreate(OperatorBase):
    pass


class OperatorUpdate(BaseModel):
    is_active: Optional[bool] = None
    limit: Optional[int] = None


class OperatorResponse(OperatorBase):
    id: int

    class Config:
        from_attributes = True
