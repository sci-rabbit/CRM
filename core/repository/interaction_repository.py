from sqlalchemy import select

from core.models.interaction import Interaction
from core.repository.base_repository import AsyncRepository


class InteractionRepository(AsyncRepository[Interaction]):
    def __init__(self, session):
        super().__init__(session, Interaction)

    async def list_by_lead(self, lead_id: int) -> list[Interaction]:
        stmt = select(Interaction).where(Interaction.lead_id == lead_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
