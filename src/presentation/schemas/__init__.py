"""
Pydantic schemas for API request/response validation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CVUploadResponse(BaseModel):
    """Response for CV upload."""

    id: str
    filename: str
    message: str
    extracted_data: dict


class JobAnalysisRequest(BaseModel):
    """Request for job analysis."""

    title: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10, max_length=10000)
    location: Optional[str] = None


class JobAnalysisResponse(BaseModel):
    """Response for job analysis."""

    id: str
    title: str
    company: str
    message: str
    extracted_requirements: dict


class MatchRequest(BaseModel):
    """Request for CV-Job matching."""

    cv_id: str = Field(..., min_length=1)
    job_id: str = Field(..., min_length=1)


class SkillMatchDetail(BaseModel):
    """Detailed skill match information."""

    skill_name: str
    cv_has_skill: bool
    cv_skill_level: Optional[str] = None
    required_level: Optional[str] = None
    match_score: float
    gap_analysis: Optional[str] = None


class MatchAnalysisResponse(BaseModel):
    """Response for match analysis."""

    overall_score: float
    skills_score: float
    experience_score: float
    education_score: float
    skill_matches: List[SkillMatchDetail]
    missing_skills: List[str]
    matching_skills: List[str]
    experience_gap_years: float
    recommendations: List[str]
    interview_tips: List[str]
    recommendation_level: str


class MatchResponse(BaseModel):
    """Response for match creation."""

    id: str
    cv_id: str
    job_id: str
    status: str
    analysis: Optional[MatchAnalysisResponse] = None
    created_at: datetime
    message: str


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str
    message: str
    details: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    timestamp: datetime
    version: str
    ai_service_configured: bool
