from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.database import get_session
from core.schemas.operator import OperatorCreate, OperatorResponse, OperatorUpdate
from core.services.operator_service import OperatorService

router = APIRouter(tags=["Operators API"])


@router.post("/operators/")
async def create_operator(
    data: OperatorCreate, session: AsyncSession = Depends(get_session)
) -> OperatorResponse:
    service = OperatorService(session)
    operator = await service.create_operator(**data.model_dump())
    await session.commit()
    return OperatorResponse.model_validate(operator)


@router.get("/operators/")
async def list_operators(
    session: AsyncSession = Depends(get_session),
) -> list[OperatorResponse]:
    service = OperatorService(session)
    operators = await service.list_operators()
    return [OperatorResponse.model_validate(operator) for operator in operators]


@router.patch("/operators/{operator_id}")
async def update_operator(
    operator_id: int,
    data: OperatorUpdate,
    session: AsyncSession = Depends(get_session),
) -> OperatorResponse:
    service = OperatorService(session)
    updated = await service.update_operator(
        operator_id, **data.model_dump(exclude_unset=True)
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Operator not found"
        )
    return OperatorResponse.model_validate(updated)
