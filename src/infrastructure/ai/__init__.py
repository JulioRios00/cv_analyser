"""
AI service implementation using Google Gemini.
This service provides AI-powered analysis for CV and job matching.
"""

import json
import logging

import google.generativeai as genai

from ...config import settings
from ...domain.entities import (
    CV,
    Education,
    Experience,
    Job,
    JobRequirement,
    MatchAnalysis,
    Skill,
    SkillLevel,
)
from ...domain.services import AIAnalysisService
from .converters import (
    convert_to_cv_entity,
    convert_to_job_entity,
    convert_to_match_analysis,
)
from .prompts import (
    create_cv_extraction_prompt,
    create_job_analysis_prompt,
    create_matching_prompt,
)

logger = logging.getLogger(__name__)


class GeminiAIService(AIAnalysisService):
    """AI service implementation using Google Gemini."""

    def __init__(self):
        if not settings.google_api_key:
            raise ValueError("Google API key not configured")

        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        logger.info("Initialized Gemini AI service")

    async def extract_cv_data(self, raw_text: str) -> CV:
        """Extract structured data from raw CV text using Gemini."""
        try:
            prompt = create_cv_extraction_prompt(raw_text)
            response = await self._generate_content(prompt)

            # Clean and validate response
            response = response.strip()
            if not response:
                raise AIServiceError("Empty response from AI service")

            # Try to extract JSON from response (sometimes AI adds extra text)
            response = self._extract_json_from_response(response)

            extracted_data = json.loads(response)

            cv = convert_to_cv_entity(extracted_data, raw_text)
            logger.info("Successfully extracted CV data using Gemini")
            return cv

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            logger.error(f"Raw response: {response[:500]}...")
            raise AIServiceError(f"Invalid JSON response from AI: {str(e)}")
        except Exception as e:
            logger.error(f"Error extracting CV data: {str(e)}")
            raise AIServiceError(f"Failed to extract CV data: {str(e)}")

    async def analyze_job_description(self, description: str) -> Job:
        """Extract job requirements from description using Gemini."""
        try:
            prompt = create_job_analysis_prompt(description)
            response = await self._generate_content(prompt)

            # Clean and validate response
            response = response.strip()
            if not response:
                raise AIServiceError("Empty response from AI service")

            # Try to extract JSON from response
            response = self._extract_json_from_response(response)

            job_data = json.loads(response)

            job = convert_to_job_entity(job_data, description)
            logger.info("Successfully analyzed job description using Gemini")
            return job

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            logger.error(f"Raw response: {response[:500]}...")
            raise AIServiceError(f"Invalid JSON response from AI: {str(e)}")
        except Exception as e:
            logger.error(f"Error analyzing job description: {str(e)}")
            raise AIServiceError(f"Failed to analyze job: {str(e)}")

    async def calculate_match_score(self, cv: CV, job: Job) -> MatchAnalysis:
        """Calculate comprehensive match analysis using Gemini."""
        try:
            prompt = create_matching_prompt(
                cv.skill_names,
                cv.total_experience_years,
                job.all_required_skill_names,
                job.min_experience_years,
            )
            response = await self._generate_content(prompt)

            # Clean and validate response
            response = response.strip()
            if not response:
                raise AIServiceError("Empty response from AI service")

            # Try to extract JSON from response
            response = self._extract_json_from_response(response)

            match_data = json.loads(response)

            cv_id_str = cv.id or "unknown"
            job_id_str = job.id or "unknown"
            analysis = convert_to_match_analysis(
                match_data, cv_id_str, job_id_str
            )

            logger.info("Successfully calculated match score using Gemini")
            return analysis

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            logger.error(f"Raw response: {response[:500]}...")
            raise AIServiceError(f"Invalid JSON response from AI: {str(e)}")
        except Exception as e:
            logger.error(f"Error calculating match score: {str(e)}")
            raise AIServiceError(f"Failed to calculate match: {str(e)}")

    async def match_cv_job(self, cv_data: dict, job_data: dict) -> dict:
        """
        Match CV data against job data and return compatibility analysis.
        This method accepts raw CV and job dictionaries from API.
        """
        try:
            logger.info("Starting CV-Job matching with raw data")

            # Create CV entity from processed data
            cv = CV(
                id=cv_data.get("id"),
                name=cv_data.get("name"),
                email=cv_data.get("email"),
                phone=cv_data.get("phone"),
                skills=[
                    Skill(
                        name=skill.get("name", ""),
                        level=SkillLevel(
                            skill.get("level", "beginner").lower()
                        ),
                        years_experience=skill.get("years_experience"),
                        category=skill.get("category"),
                    )
                    for skill in cv_data.get("skills", [])
                ],
                experience=[
                    Experience(
                        position=exp.get("title", ""),
                        company=exp.get("company", ""),
                        duration_months=exp.get("duration_months", 0),
                        description=exp.get("description", ""),
                        skills_used=exp.get("skills_used", []),
                    )
                    for exp in cv_data.get("work_experience", [])
                ],
                education=[
                    Education(
                        degree=edu.get("degree", ""),
                        institution=edu.get("institution", ""),
                        field_of_study=edu.get("field", ""),
                        graduation_year=edu.get("year"),
                    )
                    for edu in cv_data.get("education", [])
                ],
            )

            # Create Job entity from processed data
            job = Job(
                id=job_data.get("id"),
                title=job_data.get("title", ""),
                company=job_data.get("company", ""),
                description=job_data.get("description", ""),
                min_experience_years=job_data.get("min_experience_years", 0),
                required_skills=[
                    JobRequirement(
                        skill=skill.get("name", ""),
                        required_level=SkillLevel(
                            skill.get("level", "intermediate").lower()
                        ),
                        is_mandatory=skill.get("is_mandatory", True),
                        weight=skill.get("weight", 1.0),
                    )
                    for skill in job_data.get("required_skills", [])
                ],
                preferred_skills=[
                    JobRequirement(
                        skill=skill.get("name", ""),
                        required_level=SkillLevel(
                            skill.get("level", "intermediate").lower()
                        ),
                        is_mandatory=False,
                        weight=skill.get("weight", 0.5),
                    )
                    for skill in job_data.get("preferred_skills", [])
                ],
            )

            # Use the existing match calculation method
            match_analysis = await self.calculate_match_score(cv, job)

            # Convert match analysis to dictionary for API response
            result = {
                "overall_compatibility_score": match_analysis.overall_score,
                "skills_match_score": match_analysis.skills_score,
                "experience_match_score": match_analysis.experience_score,
                "matched_skills": [
                    {
                        "name": skill.skill_name,
                        "cv_level": (
                            skill.cv_skill_level.value
                            if skill.cv_skill_level
                            else "unknown"
                        ),
                        "job_importance": (
                            skill.required_level.value
                            if skill.required_level
                            else "unknown"
                        ),
                    }
                    for skill in match_analysis.skill_matches
                ],
                "missing_skills": [
                    {"name": skill, "importance": "high"}
                    for skill in match_analysis.missing_skills
                ],
                "recommendations": match_analysis.recommendations or [],
            }

            logger.info("Successfully completed CV-Job matching")
            return result

        except Exception as e:
            logger.error(f"Error in match_cv_job: {str(e)}")
            raise AIServiceError(f"Failed to match CV and job: {str(e)}")

    async def _generate_content(self, prompt: str) -> str:
        """Generate content using Gemini with error handling."""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise AIServiceError(f"Gemini API failed: {str(e)}")

    def _extract_json_from_response(self, response: str) -> str:
        """Extract JSON from AI response that might contain extra text."""
        # Look for JSON content between { and }
        start_idx = response.find("{")
        end_idx = response.rfind("}")

        if start_idx == -1 or end_idx == -1:
            raise AIServiceError("No JSON found in AI response")

        return response[start_idx : end_idx + 1]


class AIServiceError(Exception):
    """Custom exception for AI service errors."""

    pass


def create_ai_service() -> AIAnalysisService:
    """Factory function to create the appropriate AI service."""
    if settings.google_api_key:
        return GeminiAIService()
    else:
        raise ValueError("Google Gemini API key not configured")
