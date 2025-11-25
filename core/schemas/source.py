from pydantic import BaseModel


class SourceBase(BaseModel):
    name: str


class SourceCreate(SourceBase):
    pass


class SourceResponse(SourceBase):
    id: int

    class Config:
        from_attributes = True