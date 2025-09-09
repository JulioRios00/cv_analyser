"""
Domain entities representing the core business concepts.
These are the heart of our application and contain no dependencies on
external frameworks.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional


class MatchStatus(Enum):
    """Status of a CV-Job match analysis."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class SkillLevel(Enum):
    """Skill proficiency levels."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class Skill:
    """Represents a skill with proficiency level."""

    name: str
    level: SkillLevel
    years_experience: Optional[int] = None
    # e.g., "programming", "soft_skills", "tools"
    category: Optional[str] = None


@dataclass
class Education:
    """Represents educational background."""

    degree: str
    institution: str
    field_of_study: str
    graduation_year: Optional[int] = None
    gpa: Optional[float] = None


@dataclass
class Experience:
    """Represents work experience."""

    position: str
    company: str
    duration_months: int
    description: str
    skills_used: List[str]
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


@dataclass
class CV:
    """Core CV entity containing all extracted information."""

    id: Optional[str] = None
    filename: str = ""
    raw_text: str = ""

    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None

    skills: Optional[List[Skill]] = None
    education: Optional[List[Education]] = None
    experience: Optional[List[Experience]] = None
    certifications: Optional[List[str]] = None
    languages: Optional[List[str]] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.skills is None:
            self.skills = []
        if self.education is None:
            self.education = []
        if self.experience is None:
            self.experience = []
        if self.certifications is None:
            self.certifications = []
        if self.languages is None:
            self.languages = []

    @property
    def total_experience_years(self) -> float:
        """Calculate total years of experience."""
        if not self.experience:
            return 0.0
        return sum(exp.duration_months for exp in self.experience) / 12.0

    @property
    def skill_names(self) -> List[str]:
        """Get list of skill names."""
        return [skill.name for skill in self.skills] if self.skills else []


@dataclass
class JobRequirement:
    """Represents a specific job requirement."""

    skill: str
    required_level: SkillLevel
    is_mandatory: bool = True
    weight: float = 1.0  # Importance weight for scoring


@dataclass
class Job:
    """Core Job entity containing job description analysis."""

    id: Optional[str] = None
    title: str = ""
    company: str = ""
    description: str = ""

    required_skills: Optional[List[JobRequirement]] = None
    preferred_skills: Optional[List[JobRequirement]] = None
    min_experience_years: int = 0
    required_education: Optional[List[str]] = None
    required_certifications: Optional[List[str]] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.required_skills is None:
            self.required_skills = []
        if self.preferred_skills is None:
            self.preferred_skills = []
        if self.required_education is None:
            self.required_education = []
        if self.required_certifications is None:
            self.required_certifications = []

    @property
    def all_required_skill_names(self) -> List[str]:
        """Get all required skill names."""
        return (
            [req.skill for req in self.required_skills]
            if self.required_skills
            else []
        )

    @property
    def mandatory_skills(self) -> List[JobRequirement]:
        """Get only mandatory skills."""
        return (
            [req for req in self.required_skills if req.is_mandatory]
            if self.required_skills
            else []
        )


@dataclass
class SkillMatch:
    """Represents how well a CV skill matches a job requirement."""

    skill_name: str
    cv_has_skill: bool
    cv_skill_level: Optional[SkillLevel] = None
    required_level: Optional[SkillLevel] = None
    match_score: float = 0.0  # 0-1 scale
    gap_analysis: Optional[str] = None


@dataclass
class MatchAnalysis:
    """Detailed analysis of how well a CV matches a job."""

    cv_id: str
    job_id: str

    overall_score: float = 0.0  # 0-100 scale
    skills_score: float = 0.0
    experience_score: float = 0.0
    education_score: float = 0.0

    skill_matches: Optional[List[SkillMatch]] = None
    missing_skills: Optional[List[str]] = None
    matching_skills: Optional[List[str]] = None
    experience_gap_years: float = 0.0

    recommendations: Optional[List[str]] = None
    interview_tips: Optional[List[str]] = None

    analysis_date: Optional[datetime] = None
    ai_model_used: Optional[str] = None

    def __post_init__(self):
        if self.skill_matches is None:
            self.skill_matches = []
        if self.missing_skills is None:
            self.missing_skills = []
        if self.matching_skills is None:
            self.matching_skills = []
        if self.recommendations is None:
            self.recommendations = []
        if self.interview_tips is None:
            self.interview_tips = []


@dataclass
class Match:
    """Main entity representing a CV-Job matching session."""

    id: Optional[str] = None
    cv_id: str = ""
    job_id: str = ""
    status: MatchStatus = MatchStatus.PENDING

    analysis: Optional[MatchAnalysis] = None
    error_message: Optional[str] = None

    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    processing_time_seconds: Optional[float] = None

    @property
    def is_completed(self) -> bool:
        """Check if matching is completed successfully."""
        return (
            self.status == MatchStatus.COMPLETED and self.analysis is not None
        )

    @property
    def recommendation_level(self) -> str:
        """Get recommendation level based on overall score."""
        if not self.analysis:
            return "Unknown"

        score = self.analysis.overall_score
        if score >= 80:
            return "Highly Recommended"
        elif score >= 60:
            return "Recommended"
        elif score >= 40:
            return "Consider with Caution"
        else:
            return "Not Recommended"
