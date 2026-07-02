from fastapi import FastAPI
from agent.core.config import settings
from agent.api import health

def create_app() -> FastAPI:

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug
    )

    # Routers
    app.include_router(health.router)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agent.main:app", host="0.0.0.0", port=8000, reload=settings.debug)