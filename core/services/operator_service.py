from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from core.models.operator import Operator
from core.repository.operator_repository import OperatorRepository


class OperatorService:
    def __init__(self, session: AsyncSession):
        self.repo = OperatorRepository(session)

    async def get_available_for_source(self, source_id: int):
        return await self.repo.list_available_for_source(source_id)

    async def create_operator(self, name: str, is_active: bool, limit: int) -> Operator:
        return await self.repo.create(
            name=name,
            is_active=is_active,
            limit=limit,
        )

    async def list_operators(self) -> List[Operator]:
        return list(await self.repo.list())

    async def update_operator(
        self,
        operator_id: int,
        is_active: Optional[bool] = None,
        limit: Optional[int] = None,
    ) -> Optional[Operator]:
        kwargs = {}
        if is_active is not None:
            kwargs["is_active"] = is_active
        if limit is not None:
            kwargs["limit"] = limit
        if not kwargs:
            return await self.repo.get(operator_id)
        return await self.repo.update(operator_id, **kwargs)
