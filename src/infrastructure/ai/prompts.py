"""
AI prompts for CV analysis, job analysis, and matching.
"""


def create_cv_extraction_prompt(raw_text: str) -> str:
    """Create prompt for CV data extraction."""
    return f"""
Extract structured information from this CV text and return as JSON.

CV Text:
{raw_text}

Please extract and return ONLY a JSON object with this structure:
{{
    "name": "Full name",
    "email": "email@example.com", 
    "phone": "phone number",
    "location": "city, country",
    "skills": [
        {{
            "name": "Python",
            "level": "advanced", 
            "years_experience": 3,
            "category": "programming"
        }}
    ],
    "education": [
        {{
            "degree": "Bachelor of Science",
            "institution": "University Name", 
            "field_of_study": "Computer Science",
            "graduation_year": 2020
        }}
    ],
    "experience": [
        {{
            "position": "Software Developer",
            "company": "Company Name",
            "duration_months": 24,
            "description": "Job description",
            "skills_used": ["Python", "SQL"]
        }}
    ],
    "certifications": ["AWS Certified"],
    "languages": ["English", "Spanish"]
}}

Important:
- Use skill levels: "beginner", "intermediate", "advanced", "expert"
- Categories: "programming", "soft_skills", "tools", "domain_knowledge"
- If information is missing, use null or empty arrays
- Duration should be in months
- Return ONLY the JSON, no additional text
"""


def create_job_analysis_prompt(description: str) -> str:
    """Create prompt for job description analysis."""
    return f"""
Analyze this job description and extract requirements as JSON.

Job Description:
{description}

Please extract and return ONLY a JSON object with this structure:
{{
    "title": "Job Title",
    "company": "Company Name",
    "required_skills": [
        {{
            "skill": "Python",
            "required_level": "advanced",
            "is_mandatory": true,
            "weight": 1.0
        }}
    ],
    "preferred_skills": [
        {{
            "skill": "Docker",
            "required_level": "intermediate", 
            "is_mandatory": false,
            "weight": 0.5
        }}
    ],
    "min_experience_years": 3,
    "required_education": ["Bachelor's degree in Computer Science"],
    "required_certifications": ["AWS Certified Developer"],
    "location": "San Francisco, CA",
    "salary_range": "$80,000 - $120,000"
}}

Important:
- Use skill levels: "beginner", "intermediate", "advanced", "expert"
- Weight should be 0.1 to 1.0 (importance)
- Separate mandatory vs preferred skills
- If information is missing, use null or empty arrays
- Return ONLY the JSON, no additional text
"""


def create_matching_prompt(
    cv_skills: list, cv_experience: float, job_skills: list, job_experience: int
) -> str:
    """Create prompt for CV-Job matching analysis."""
    return f"""
Analyze how well this CV matches the job requirements.

CV Summary: 
- Skills: {cv_skills}
- Experience: {cv_experience} years

Job Requirements:
- Required Skills: {job_skills}
- Minimum Experience: {job_experience} years

Please analyze and return ONLY a JSON object with this structure:
{{
    "overall_score": 75.5,
    "skills_score": 80.0,
    "experience_score": 70.0,
    "education_score": 85.0,
    "skill_matches": [
        {{
            "skill_name": "Python",
            "cv_has_skill": true,
            "cv_skill_level": "advanced",
            "required_level": "intermediate", 
            "match_score": 0.9,
            "gap_analysis": "CV skill level exceeds requirements"
        }}
    ],
    "missing_skills": ["Docker", "Kubernetes"],
    "matching_skills": ["Python", "SQL", "Git"],
    "experience_gap_years": 0.5,
    "recommendations": [
        "Learn Docker containerization",
        "Gain experience with Kubernetes"
    ],
    "interview_tips": [
        "Prepare examples of Python projects",
        "Show enthusiasm for learning new technologies"
    ]
}}

Important:
- Scores should be 0-100
- match_score should be 0.0-1.0
- Provide specific, actionable recommendations
- Include realistic interview tips
- Return ONLY the JSON, no additional text
"""
