from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import routes

OVERLAY_PATH: Path = Path.cwd() / "www" / "dist"


class CustomStaticFiles(StaticFiles):
    def get_mimetype(self, path: str) -> str:
        mime_type = super().get_mimetype(path)
        if path.endswith(".js"):
            return "application/javascript"

        if path.endswith(".ts"):
            return "application/typescript"

        return mime_type


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    print("[Server] Startup process complete!")
    yield
    print("[Server] Shutting down...")


def init_routes(app: FastAPI) -> None:
    app.include_router(routes.memory.router)
    app.mount("/", CustomStaticFiles(directory=OVERLAY_PATH, html=True), name="static")


def init_api() -> FastAPI:
    asgi_app = FastAPI(lifespan=lifespan)

    init_routes(asgi_app)

    return asgi_app


asgi_app = init_api()
