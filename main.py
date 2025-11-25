from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.views import router as api_router
from core.database import dispose, engine
from core.models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await dispose()


app = FastAPI(title="Mini CRM", lifespan=lifespan)
app.include_router(api_router)


@app.get("/health")
def healthcheck():
    return {"msg": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
