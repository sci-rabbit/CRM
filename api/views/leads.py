from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.database import get_session
from core.schemas.interaction import LeadWithInteractions, InteractionResponse
from core.services.lead_service import LeadService

router = APIRouter(tags=["Leads API"])


@router.get("/leads/")
async def list_leads(
    session: AsyncSession = Depends(get_session),
) -> list[LeadWithInteractions]:
    service = LeadService(session)
    leads = await service.list_leads_with_interactions()

    leads_data = []
    for lead in leads:
        interactions_data = [
            InteractionResponse.model_validate(interaction)
            for interaction in lead.interactions
        ]
        leads_data.append(
            LeadWithInteractions(
                id=lead.id,
                external_id=lead.external_id,
                created_at=lead.created_at,
                interactions=interactions_data,
            )
        )

    return leads_data


@router.get("/leads/{lead_id}")
async def get_lead(
    lead_id: int, session: AsyncSession = Depends(get_session)
) -> LeadWithInteractions:
    service = LeadService(session)
    lead = await service.get_lead_with_interactions(lead_id)

    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found"
        )

    interactions_data = [
        InteractionResponse.model_validate(interaction)
        for interaction in lead.interactions
    ]

    return LeadWithInteractions(
        id=lead.id,
        external_id=lead.external_id,
        created_at=lead.created_at,
        interactions=interactions_data,
    )
