from pydantic import BaseModel
from typing import List


# ============================
# Request Models
# ============================

class JobRequest(BaseModel):
    job_description: str


class CareerRequest(BaseModel):
    cv_text: str
    job_description: str


# ============================
# Response Models
# ============================

class Course(BaseModel):
    skill: str
    course: str
    provider: str


class RoadmapStep(BaseModel):
    step: int
    skill: str
    difficulty: str
    duration: str


class ATSDetails(BaseModel):
    skill_score: float
    keyword_score: float
    section_score: float
    experience_score: float
    project_score: float
    certification_score: float
    resume_length_score: float


class AnalyzeResponse(BaseModel):
    job_skills: List[str]


class CareerReportResponse(BaseModel):

    cv_skills: List[str]

    job_skills: List[str]

    matched_skills: List[str]

    missing_skills: List[str]

    match_score: float

    ats_score: float

    ats_details: ATSDetails

    recommended_courses: List[Course]

    roadmap: List[RoadmapStep]

    suggestions: List[str]

    resume_feedback: List[str]