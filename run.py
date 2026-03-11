import asyncio
import uvicorn
from src.infrastructure.config.settings import settings
from src.main.server.server import app

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


async def run():

    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=settings.APP_PORT,
        log_level="info",
        timeout_keep_alive=300,
        timeout_graceful_shutdown=300,
        limit_concurrency=100
    )

    server = uvicorn.Server(config=config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(run())
