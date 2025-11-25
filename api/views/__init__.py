from fastapi import APIRouter

from . import interactions, operators


router = APIRouter()
router.include_router(operators.router)
router.include_router(interactions.router)


__all__ = ["router"]
