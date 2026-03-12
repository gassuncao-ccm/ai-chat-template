
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from src.infrastructure.config.settings import settings
from src.main.routes.chat import router as chat_router

# from src.errors.error_handler import ErrorHandlerMiddleware

def create_app() -> FastAPI:
    app = FastAPI(
        title="${{ values.service_name }}",
        description="${{ values.service_description }}",
        version=settings.APP_VERSION,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json"
    )

    app.include_router(chat_router, prefix="/api")

    return app


app = create_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(ErrorHandlerMiddleware)
