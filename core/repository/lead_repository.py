from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.models.lead import Lead
from core.repository.base_repository import AsyncRepository


class LeadRepository(AsyncRepository[Lead]):
    def __init__(self, session):
        super().__init__(session, Lead)

    async def get_by_external(self, external_id: str) -> Lead | None:
        stmt = select(Lead).where(Lead.external_id == external_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_with_interactions(self) -> list[Lead]:
        stmt = (
            select(Lead)
            .options(selectinload(Lead.interactions))
            .order_by(Lead.created_at.desc())
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().unique().all())

    async def get_with_interactions(self, lead_id: int) -> Lead | None:
        stmt = (
            select(Lead)
            .options(selectinload(Lead.interactions))
            .where(Lead.id == lead_id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
