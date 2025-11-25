from sqlalchemy.ext.asyncio import AsyncSession

from core.models.lead import Lead
from core.repository.lead_repository import LeadRepository


class LeadService:
    def __init__(self, session: AsyncSession):
        self.repo = LeadRepository(session)

    async def get_or_create(self, external_id: str) -> Lead:
        lead = await self.repo.get_by_external(external_id)
        if lead:
            return lead
        return await self.repo.create(external_id=external_id)

    async def list_leads_with_interactions(self) -> list[Lead]:
        return await self.repo.list_with_interactions()

    async def get_lead_with_interactions(self, lead_id: int) -> Lead | None:
        return await self.repo.get_with_interactions(lead_id)
