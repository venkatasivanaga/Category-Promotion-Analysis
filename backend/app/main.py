from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_health import router as health_router
from app.core.config import settings
from app.core.logging import RequestLoggingMiddleware, configure_logging

def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title="Category Promotion Analysis API",
        version="0.1.0",
    )

    allow_origins = settings.cors_origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(RequestLoggingMiddleware)

    app.include_router(health_router)

    @app.get("/")
    def root():
        return {"message": "Category Promotion Analysis API", "docs": "/docs"}

    return app

app = create_app()