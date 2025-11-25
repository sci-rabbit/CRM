from sqlalchemy.ext.asyncio import AsyncSession

from core.repository.lead_repository import LeadRepository


class LeadService:
    def __init__(self, session: AsyncSession):
        self.repo = LeadRepository(session)

    async def get_or_create(self, external_id: str):
        lead = await self.repo.get_by_external(external_id)
        if lead:
            return lead
        return await self.repo.create(external_id=external_id)
