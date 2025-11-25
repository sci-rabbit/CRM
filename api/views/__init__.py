from fastapi import APIRouter

from . import interactions, operators, sources, leads


router = APIRouter()
router.include_router(operators.router)
router.include_router(interactions.router)
router.include_router(sources.router)
router.include_router(leads.router)


__all__ = ["router"]
