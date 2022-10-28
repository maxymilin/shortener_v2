import uvicorn
from fastapi import FastAPI

from app import settings
from app.core.models import HealthCheck
from app.router.api_v1.endpoints import api_router


app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    debug=settings.debug,
)


@app.get("/", response_model=HealthCheck, tags=["status"])
async def health_check():
    return {
        "name": settings.project_name,
        "version": settings.version,
        "description": settings.description,
    }


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, host="0.0.0.0", reload=True)
