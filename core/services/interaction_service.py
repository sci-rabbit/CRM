from sqlalchemy.ext.asyncio import AsyncSession

from core.repository.interaction_repository import InteractionRepository


class InteractionService:
    def __init__(self, session: AsyncSession):
        self.repo = InteractionRepository(session)

    async def create(self, lead_id: int, source_id: int, operator_id: int | None):
        return await self.repo.create(
            lead_id=lead_id,
            source_id=source_id,
            operator_id=operator_id,
        )
