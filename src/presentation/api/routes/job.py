"""
API routes for job analysis.
"""

import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException

from ....infrastructure.ai import AIServiceError, create_ai_service
from ...schemas import JobAnalysisRequest, JobAnalysisResponse

logger = logging.getLogger(__name__)

job_router = APIRouter()


def get_ai_service():
    """Dependency to get AI service."""
    try:
        return create_ai_service()
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))


@job_router.post("/analyze", response_model=JobAnalysisResponse)
async def analyze_job_description(
    request: JobAnalysisRequest, ai_service=Depends(get_ai_service)
):
    """
    Analyze a job description and extract requirements.
    Uses AI to identify required skills, experience, and qualifications.
    """
    try:
        full_description = f"""
Job Title: {request.title}
Company: {request.company}
Location: {request.location or 'Not specified'}

Job Description:
{request.description}
"""

        job = await ai_service.analyze_job_description(full_description)
        job.id = str(uuid.uuid4())

        logger.info(f"Successfully analyzed job: {job.id}")

        return JobAnalysisResponse(
            id=job.id,
            title=job.title,
            company=job.company,
            message="Job description analyzed successfully",
            extracted_requirements={
                "required_skills": [
                    {
                        "skill": req.skill,
                        "level": req.required_level.value,
                        "mandatory": req.is_mandatory,
                    }
                    for req in job.required_skills
                ],
                "preferred_skills": [
                    {"skill": req.skill, "level": req.required_level.value}
                    for req in job.preferred_skills
                ],
                "min_experience_years": job.min_experience_years,
                "required_education": job.required_education,
                "required_certifications": job.required_certifications,
                "location": job.location,
                "salary_range": job.salary_range,
            },
        )

    except AIServiceError as e:
        logger.error(f"AI service error: {str(e)}")
        raise HTTPException(status_code=503, detail=str(e))

    except Exception as e:
        logger.error(f"Unexpected error analyzing job: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@job_router.get("/")
async def list_jobs():
    """List all analyzed jobs (placeholder for future database integration)."""
    return {"message": "Job listing not yet implemented"}
