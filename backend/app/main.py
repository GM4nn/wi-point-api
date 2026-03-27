# other libs
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

# db
from app.core.database import engine
from app.core.base import Base

# grapql schema
from app.src.graphql.schema import graphql_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    #Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="WI-POINT-API",
    description=(
        "API para consultar los puntos de acceso WiFi publicos "
        "de la Ciudad de Mexico."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# GraphQL endpoint -> http://localhost:8000/graphql
app.include_router(graphql_router, prefix="/graphql")

@app.get(
    "/",
    tags=["Health"],
    description="Healtch Check para comprar que la api responda"
)
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "wifi-cdmx-api"
    }
