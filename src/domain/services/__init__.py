"""
Domain services containing core business logic.
These services orchestrate complex business operations.
"""

from abc import ABC, abstractmethod
from typing import List

from ..entities import CV, Job, MatchAnalysis


class AIAnalysisService(ABC):
    """Abstract service for AI-powered analysis operations."""

    @abstractmethod
    async def extract_cv_data(self, raw_text: str) -> CV:
        """Extract structured data from raw CV text using AI."""
        pass

    @abstractmethod
    async def analyze_job_description(self, description: str) -> Job:
        """Extract job requirements from description using AI."""
        pass

    @abstractmethod
    async def calculate_match_score(self, cv: CV, job: Job) -> MatchAnalysis:
        """Calculate comprehensive match analysis between CV and job."""
        pass


class PDFProcessingService(ABC):
    """Abstract service for PDF processing operations."""

    @abstractmethod
    async def extract_text_from_pdf(self, file_content: bytes) -> str:
        """Extract text content from PDF file."""
        pass

    @abstractmethod
    async def validate_pdf_file(self, file_content: bytes) -> bool:
        """Validate if the file is a proper PDF."""
        pass


class MatchingService:
    """Domain service for CV-Job matching business logic."""

    def __init__(self, ai_service: AIAnalysisService):
        self.ai_service = ai_service

    async def create_match_analysis(self, cv: CV, job: Job) -> MatchAnalysis:
        """
        Create a comprehensive match analysis between a CV and job.
        This is the core business logic for matching.
        """
        analysis = await self.ai_service.calculate_match_score(cv, job)

        # Apply business rules for scoring
        analysis = self._apply_business_rules(analysis, cv, job)

        return analysis

    def _apply_business_rules(
        self, analysis: MatchAnalysis, cv: CV, job: Job
    ) -> MatchAnalysis:
        """Apply business rules to refine the analysis."""

        # Rule 1: Penalize if missing mandatory skills
        mandatory_skills = [req.skill for req in job.mandatory_skills]
        missing_mandatory = [
            skill for skill in mandatory_skills if skill not in cv.skill_names
        ]

        if missing_mandatory:
            # Reduce overall score by 10% for each missing mandatory skill
            penalty = len(missing_mandatory) * 0.1
            analysis.overall_score = max(
                0, analysis.overall_score - penalty * 100
            )

        # Rule 2: Boost score for relevant experience
        if cv.total_experience_years >= job.min_experience_years:
            exp_diff = cv.total_experience_years - job.min_experience_years
            boost = min(0.1, exp_diff * 0.02)
            analysis.overall_score = min(
                100, analysis.overall_score + boost * 100
            )

        # Rule 3: Add specific recommendations based on gaps
        analysis.recommendations.extend(
            self._generate_recommendations(cv, job, analysis)
        )

        return analysis

    def _generate_recommendations(
        self, cv: CV, job: Job, analysis: MatchAnalysis
    ) -> List[str]:
        """Generate specific recommendations based on analysis."""
        recommendations = []

        # Skill gap recommendations
        if analysis.missing_skills:
            recommendations.append(
                f"Consider learning: {', '.join(analysis.missing_skills[:3])}"
            )

        # Experience recommendations
        if analysis.experience_gap_years > 0:
            gap_text = (
                f"Gain {analysis.experience_gap_years:.1f} more years "
                f"of relevant experience"
            )
            recommendations.append(gap_text)

        # Education recommendations
        if job.required_education and cv.education:
            cv_degrees = [edu.degree.lower() for edu in cv.education]
            missing_education = [
                edu
                for edu in job.required_education
                if edu.lower() not in cv_degrees
            ]
            if missing_education:
                recommendations.append(
                    f"Consider pursuing: {missing_education[0]}"
                )

        return recommendations


class ValidationService:
    """Service for validating domain entities and business rules."""

    @staticmethod
    def validate_cv(cv: CV) -> List[str]:
        """Validate CV entity and return list of validation errors."""
        errors = []

        if not cv.raw_text.strip():
            errors.append("CV must contain text content")

        if not cv.filename:
            errors.append("CV must have a filename")

        return errors

    @staticmethod
    def validate_job(job: Job) -> List[str]:
        """Validate Job entity and return list of validation errors."""
        errors = []

        if not job.title.strip():
            errors.append("Job must have a title")

        if not job.description.strip():
            errors.append("Job must have a description")

        if job.min_experience_years < 0:
            errors.append("Minimum experience years cannot be negative")

        return errors

    @staticmethod
    def validate_match_request(cv_id: str, job_id: str) -> List[str]:
        """Validate match request parameters."""
        errors = []

        if not cv_id or not cv_id.strip():
            errors.append("CV ID is required")

        if not job_id or not job_id.strip():
            errors.append("Job ID is required")

        return errors
