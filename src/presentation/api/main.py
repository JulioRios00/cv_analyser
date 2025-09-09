"""
FastAPI application main module.
"""

import logging
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ...config import settings
from ..schemas import HealthResponse
from .routes import cv_router, job_router, match_router

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered CV analyzer for job matching",
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version=settings.app_version,
        ai_service_configured=settings.is_ai_configured(),
    )


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
    }


app.include_router(cv_router, prefix="/api/v1/cv", tags=["CV Management"])
app.include_router(job_router, prefix="/api/v1/job", tags=["Job Analysis"])
app.include_router(
    match_router, prefix="/api/v1/match", tags=["CV-Job Matching"]
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.presentation.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
