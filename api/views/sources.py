from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.database import get_session
from core.schemas.source import SourceCreate, SourceResponse
from core.schemas.source_operator import (
    SourceOperatorCreate,
    SourceOperatorResponse,
    SourceOperatorUpdate,
)
from core.services.source_service import SourceService

router = APIRouter(tags=["Sources API"])


@router.post("/sources/")
async def create_source(
    data: SourceCreate, session: AsyncSession = Depends(get_session)
) -> SourceResponse:
    service = SourceService(session)
    source = await service.create_source(name=data.name)
    await session.commit()
    return SourceResponse.model_validate(source)


@router.get("/sources/")
async def list_sources(
    session: AsyncSession = Depends(get_session),
) -> list[SourceResponse]:
    service = SourceService(session)
    sources = await service.list_sources()
    return [SourceResponse.model_validate(source) for source in sources]


@router.get("/sources/{source_id}")
async def get_source(
    source_id: int, session: AsyncSession = Depends(get_session)
) -> SourceResponse:
    service = SourceService(session)
    source = await service.get_source(source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Source not found"
        )
    return SourceResponse.model_validate(source)


@router.post("/sources/{source_id}/operators")
async def add_operator_to_source(
    source_id: int,
    data: SourceOperatorCreate,
    session: AsyncSession = Depends(get_session),
) -> SourceOperatorResponse:
    service = SourceService(session)
    config = await service.add_operator_config(
        source_id=source_id,
        operator_id=data.operator_id,
        weight=data.weight,
    )
    await session.commit()
    return SourceOperatorResponse.model_validate(config)


@router.patch("/sources/{source_id}/operators/{operator_id}")
async def update_operator_weight(
    source_id: int,
    operator_id: int,
    data: SourceOperatorUpdate,
    session: AsyncSession = Depends(get_session),
) -> SourceOperatorResponse:
    if data.weight is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weight is required",
        )
    service = SourceService(session)
    config = await service.update_operator_weight(
        source_id=source_id, operator_id=operator_id, weight=data.weight
    )
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source-Operator configuration not found",
        )
    await session.commit()
    return SourceOperatorResponse.model_validate(config)


@router.delete("/sources/{source_id}/operators/{operator_id}")
async def remove_operator_from_source(
    source_id: int,
    operator_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = SourceService(session)
    deleted = await service.remove_operator_config(source_id, operator_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source-Operator configuration not found",
        )
    await session.commit()
    return {"message": "Operator removed from source"}


@router.get("/sources/{source_id}/operators")
async def list_source_operators(
    source_id: int, session: AsyncSession = Depends(get_session)
) -> list[SourceOperatorResponse]:
    service = SourceService(session)
    configs = await service.list_source_configs(source_id)
    return [SourceOperatorResponse.model_validate(config) for config in configs]
