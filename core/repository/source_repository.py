from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.models.source import Source
from core.repository.base_repository import AsyncRepository


class SourceRepository(AsyncRepository[Source]):
    def __init__(self, session):
        super().__init__(session, Source)

    async def get_with_configs(self, source_id: int) -> Source | None:
        stmt = (
            select(Source)
            .options(selectinload(Source.operator_configs))
            .where(Source.id == source_id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()


