from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from core.schemas.interaction import InteractionResponse, InteractionCreate
from core.services.assigment_service import AssignmentService

router = APIRouter(tags=["Interactions API"])


@router.post("/interactions")
async def register_interaction(
    data: InteractionCreate,
    session: AsyncSession = Depends(get_session),
) -> InteractionResponse:
    service = AssignmentService(session)
    interaction = await service.handle_new_interaction(
        external_lead_id=data.external_lead_id,
        source_id=data.source_id,
    )
    return InteractionResponse.model_validate(interaction)
