from sqlalchemy import select

from core.models.lead import Lead
from core.repository.base_repository import AsyncRepository


class LeadRepository(AsyncRepository[Lead]):
    def __init__(self, session):
        super().__init__(session, Lead)

    async def get_by_external(self, external_id: str) -> Lead | None:
        stmt = select(Lead).where(Lead.external_id == external_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
