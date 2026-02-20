from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_health import router as health_router
from app.api.routes_runs import router as runs_router
from app.core.config import settings
from app.core.logging import RequestLoggingMiddleware, configure_logging
from app.db.session import Base, engine
from app.db import models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    Base.metadata.create_all(bind=engine)
    yield
    # shutdown (nothing yet)


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title="Category Promotion Analysis API",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestLoggingMiddleware)

    app.include_router(health_router)
    app.include_router(runs_router)

    @app.get("/")
    def root():
        return {"message": "Category Promotion Analysis API", "docs": "/docs"}

    return app


app = create_app()