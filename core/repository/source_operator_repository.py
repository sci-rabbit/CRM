from sqlalchemy import select

from core.models.source_operator import SourceOperator
from core.repository.base_repository import AsyncRepository


class SourceOperatorRepository(AsyncRepository[SourceOperator]):
    def __init__(self, session):
        super().__init__(session, SourceOperator)

    async def get_by_source_and_operator(
        self, source_id: int, operator_id: int
    ) -> SourceOperator | None:
        stmt = select(SourceOperator).where(
            SourceOperator.source_id == source_id,
            SourceOperator.operator_id == operator_id,
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_by_source(self, source_id: int) -> list[SourceOperator]:
        stmt = select(SourceOperator).where(SourceOperator.source_id == source_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def update_weight(
        self, source_id: int, operator_id: int, weight: int
    ) -> SourceOperator | None:
        config = await self.get_by_source_and_operator(source_id, operator_id)
        if not config:
            return None
        config.weight = weight
        self.session.add(config)
        await self.session.flush()
        return config
