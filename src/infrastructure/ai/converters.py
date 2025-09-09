"""
Data converters for AI service responses.
Convert JSON responses to domain entities.
"""

from datetime import datetime
from typing import Any, Dict

from ...domain.entities import (
    CV,
    Education,
    Experience,
    Job,
    JobRequirement,
    MatchAnalysis,
    Skill,
    SkillLevel,
    SkillMatch,
)


def convert_to_cv_entity(data: Dict[str, Any], raw_text: str) -> CV:
    """Convert extracted data to CV entity."""
    skills = []
    for skill_data in data.get("skills", []):
        try:
            level_str = skill_data.get("level", "beginner").lower()
            # Validate skill level
            valid_levels = ["beginner", "intermediate", "advanced", "expert"]
            if level_str not in valid_levels:
                level_str = "beginner"

            skill = Skill(
                name=skill_data.get("name", ""),
                level=SkillLevel(level_str),
                years_experience=skill_data.get("years_experience"),
                category=skill_data.get("category"),
            )
            skills.append(skill)
        except (ValueError, TypeError):
            # Skip invalid skills but continue processing
            continue

    education = []
    for edu_data in data.get("education", []):
        edu = Education(
            degree=edu_data.get("degree", ""),
            institution=edu_data.get("institution", ""),
            field_of_study=edu_data.get("field_of_study", ""),
            graduation_year=edu_data.get("graduation_year"),
        )
        education.append(edu)

    experience = []
    for exp_data in data.get("experience", []):
        exp = Experience(
            position=exp_data.get("position", ""),
            company=exp_data.get("company", ""),
            duration_months=exp_data.get("duration_months", 0),
            description=exp_data.get("description", ""),
            skills_used=exp_data.get("skills_used", []),
        )
        experience.append(exp)

    return CV(
        raw_text=raw_text,
        name=data.get("name"),
        email=data.get("email"),
        phone=data.get("phone"),
        location=data.get("location"),
        skills=skills,
        education=education,
        experience=experience,
        certifications=data.get("certifications", []),
        languages=data.get("languages", []),
        created_at=datetime.now(),
    )


def convert_to_job_entity(data: Dict[str, Any], description: str) -> Job:
    """Convert extracted data to Job entity."""
    required_skills = []
    for skill_data in data.get("required_skills", []):
        try:
            level_str = skill_data.get("required_level", "beginner").lower()
            valid_levels = ["beginner", "intermediate", "advanced", "expert"]
            if level_str not in valid_levels:
                level_str = "beginner"

            req = JobRequirement(
                skill=skill_data.get("skill", ""),
                required_level=SkillLevel(level_str),
                is_mandatory=skill_data.get("is_mandatory", True),
                weight=skill_data.get("weight", 1.0),
            )
            required_skills.append(req)
        except (ValueError, TypeError):
            # Skip invalid skill requirements
            continue

    preferred_skills = []
    for skill_data in data.get("preferred_skills", []):
        try:
            level_str = skill_data.get("required_level", "beginner").lower()
            valid_levels = ["beginner", "intermediate", "advanced", "expert"]
            if level_str not in valid_levels:
                level_str = "beginner"

            req = JobRequirement(
                skill=skill_data.get("skill", ""),
                required_level=SkillLevel(level_str),
                is_mandatory=False,
                weight=skill_data.get("weight", 0.5),
            )
            preferred_skills.append(req)
        except (ValueError, TypeError):
            # Skip invalid skill requirements
            continue

    return Job(
        title=data.get("title", ""),
        company=data.get("company", ""),
        description=description,
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        min_experience_years=data.get("min_experience_years", 0),
        required_education=data.get("required_education", []),
        required_certifications=data.get("required_certifications", []),
        location=data.get("location"),
        salary_range=data.get("salary_range"),
        created_at=datetime.now(),
    )


def convert_to_match_analysis(
    data: Dict[str, Any], cv_id: str, job_id: str
) -> MatchAnalysis:
    """Convert match data to MatchAnalysis entity."""
    skill_matches = []
    for match_data in data.get("skill_matches", []):
        try:
            cv_level = match_data.get("cv_skill_level")
            req_level = match_data.get("required_level")

            # Validate skill levels
            valid_levels = ["beginner", "intermediate", "advanced", "expert"]
            cv_skill_level = None
            required_level = None

            if cv_level and cv_level.lower() in valid_levels:
                cv_skill_level = SkillLevel(cv_level.lower())

            if req_level and req_level.lower() in valid_levels:
                required_level = SkillLevel(req_level.lower())

            skill_match = SkillMatch(
                skill_name=match_data.get("skill_name", ""),
                cv_has_skill=match_data.get("cv_has_skill", False),
                cv_skill_level=cv_skill_level,
                required_level=required_level,
                match_score=match_data.get("match_score", 0.0),
                gap_analysis=match_data.get("gap_analysis"),
            )
            skill_matches.append(skill_match)
        except (ValueError, TypeError):
            # Skip invalid skill matches
            continue

    return MatchAnalysis(
        cv_id=cv_id,
        job_id=job_id,
        overall_score=data.get("overall_score", 0.0),
        skills_score=data.get("skills_score", 0.0),
        experience_score=data.get("experience_score", 0.0),
        education_score=data.get("education_score", 0.0),
        skill_matches=skill_matches,
        missing_skills=data.get("missing_skills", []),
        matching_skills=data.get("matching_skills", []),
        experience_gap_years=data.get("experience_gap_years", 0.0),
        recommendations=data.get("recommendations", []),
        interview_tips=data.get("interview_tips", []),
        analysis_date=datetime.now(),
        ai_model_used="gemini-1.5-flash",
    )
