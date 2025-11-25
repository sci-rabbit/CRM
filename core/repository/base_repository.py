from typing import TypeVar, Generic, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models.base import Base

Model = TypeVar("Model", bound=Base)


class AsyncRepository(Generic[Model]):
    def __init__(self, session: AsyncSession, model: type[Model]):
        self.session = session
        self.model = model

    async def get(self, obj_id: int) -> Model | None:
        return await self.session.get(self.model, obj_id)

    async def list(self) -> Sequence[Model]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, **kwargs) -> Model:
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.flush()  # чтобы получить id
        return obj

    async def delete(self, obj: Model) -> None:
        await self.session.delete(obj)
