from fastapi import FastAPI
from src.core.config import settings
from starlette.middleware.cors import CORSMiddleware
from src.routers import api_router as template_router
import os
from fastapi.staticfiles import StaticFiles
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

        self.make_middleware()


    
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
        static_dir = os.path.join(os.path.dirname(__file__), "static")
        print(static_dir, '----')
        self.app.mount(
            "/static",
            StaticFiles(directory=static_dir, html=True),
            name="static",
        )
        self.init_routers()
        return self.app
    

fastapi_app = FastApiApp()
app = fastapi_app.create_app()