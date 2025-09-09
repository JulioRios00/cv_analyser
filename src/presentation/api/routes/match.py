"""
API routes for CV-Job matching.
"""

import uuid
import logging
from fastapi import APIRouter, HTTPException
from datetime import datetime

from ...schemas import MatchRequest, MatchResponse
from ....infrastructure.ai import GeminiAIService

logger = logging.getLogger(__name__)

match_router = APIRouter()


@match_router.post("", response_model=dict)
async def match_cv_job(request: dict):
    """
    Match a CV against a job description.
    Accepts CV and Job data directly and returns compatibility analysis.
    """
    try:
        logger.info("Processing CV-Job matching request")

        cv_data = request.get("cv")
        job_data = request.get("job")

        if not cv_data or not job_data:
            raise HTTPException(
                status_code=400, detail="Both 'cv' and 'job' data are required"
            )

        ai_service = GeminiAIService()

        match_analysis = await ai_service.match_cv_job(cv_data, job_data)

        logger.info("Successfully completed CV-Job matching")
        return match_analysis

    except Exception as e:
        logger.error(f"Error in CV-Job matching: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Matching failed: {str(e)}")


@match_router.post("/analyze", response_model=MatchResponse)
async def create_match_analysis(request: MatchRequest):
    """
    Create a match analysis between a CV and job.
    This is a placeholder implementation.
    """
    # This is a placeholder - in a real implementation,
    # we would fetch the CV and Job from database,
    # then use the AI service to create the match analysis

    logger.info(f"Match analysis requested: CV {request.cv_id} vs Job {request.job_id}")

    return MatchResponse(
        id=str(uuid.uuid4()),
        cv_id=request.cv_id,
        job_id=request.job_id,
        status="completed",
        analysis=None,  # Would contain actual analysis
        created_at=datetime.now(),
        message="Match analysis placeholder - database integration needed",
    )


@match_router.get("/{match_id}")
async def get_match_result(match_id: str):
    """Get match analysis results by ID."""
    return {"message": f"Match result for {match_id} - not yet implemented"}
