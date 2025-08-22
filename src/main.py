from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.middleware.validation import validation_exception_handler
from src.routers import api_router as template_router


class FastApiApp:
    def __init__(self) -> None:
        self.app = FastAPI(
            title="FastAPI",
            description="FastAPI",
            version=settings.APP_VERSION,
            DEBUG=settings.DEBUG,
            openapi_url="/api/v1/openapi.json",
            docs_url="/api/v1/docs" if settings.DEBUG else None,
            redoc_url="/api/v1/redoc" if settings.DEBUG else None,
        )
        self.register_exception_handlers()
        self.make_middleware()
        self.init_routers()

    def register_exception_handlers(self) -> None:
        self.app.add_exception_handler(RequestValidationError, validation_exception_handler)

    def make_middleware(self) -> None:
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def init_routers(self) -> None:
        self.app.include_router(template_router)

    def create_app(self) -> FastAPI:
        return self.app


fastapi_app = FastApiApp()
app = fastapi_app.create_app()
