from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from core.models.source import Source
from core.models.source_operator import SourceOperator
from core.repository.source_repository import SourceRepository
from core.repository.source_operator_repository import SourceOperatorRepository


class SourceService:
    def __init__(self, session: AsyncSession):
        self.repo = SourceRepository(session)
        self.config_repo = SourceOperatorRepository(session)

    async def create_source(self, name: str) -> Source:
        return await self.repo.create(name=name)

    async def list_sources(self) -> List[Source]:
        return list(await self.repo.list())

    async def get_source(self, source_id: int) -> Source | None:
        return await self.repo.get(source_id)

    async def get_source_with_configs(self, source_id: int) -> Source | None:
        return await self.repo.get_with_configs(source_id)

    async def add_operator_config(
        self,
        source_id: int,
        operator_id: int,
        weight: int,
    ) -> SourceOperator:
        existing = await self.config_repo.get_by_source_and_operator(
            source_id, operator_id
        )
        if existing:
            existing.weight = weight
            self.repo.session.add(existing)
            await self.repo.session.flush()
            return existing

        return await self.config_repo.create(
            source_id=source_id,
            operator_id=operator_id,
            weight=weight,
        )

    async def update_operator_weight(
        self, source_id: int, operator_id: int, weight: int
    ) -> SourceOperator | None:
        return await self.config_repo.update_weight(
            source_id,
            operator_id,
            weight,
        )

    async def remove_operator_config(
        self,
        source_id: int,
        operator_id: int,
    ) -> bool:
        config = await self.config_repo.get_by_source_and_operator(
            source_id, operator_id
        )
        if not config:
            return False
        await self.config_repo.delete(config)
        return True

    async def list_source_configs(self, source_id: int) -> List[SourceOperator]:
        return await self.config_repo.list_by_source(source_id)
