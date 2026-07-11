from fastapi import APIRouter, UploadFile, File, Form
import pdfplumber
import io

from app.models.schemas import (
    JobRequest,
    AnalyzeResponse,
    CareerReportResponse
)

# Matching
from app.engines.matching.skill_extractor import extract_skills
from app.engines.matching.match_engine import calculate_match

# Parsers
from app.parsers.job_parser import extract_job_skills

# Recommendation
from app.engines.recommendation.course_engine import recommend_courses
from app.engines.recommendation.roadmap_engine import build_roadmap
from app.engines.recommendation.suggestion_engine import generate_suggestions
from app.engines.recommendation.resume_feedback import generate_resume_feedback

# ATS
from app.engines.ats.ats_engine import calculate_ats_score


router = APIRouter()


# ==========================================
# Root Endpoint
# ==========================================

@router.get("/")
def home():
    return {
        "message": "AI Career Coach API is Running"
    }


# ==========================================
# Analyze Job Description
# ==========================================

@router.post(
    "/analyze",
    response_model=AnalyzeResponse
)
def analyze_job(request: JobRequest):

    job_skills = extract_job_skills(
        request.job_description
    )

    return AnalyzeResponse(
        job_skills=job_skills
    )


# ==========================================
# Helper: PDF Extractor
# ==========================================

def extract_text_from_pdf(file_bytes):

    pages = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

    return "\n".join(pages)


# ==========================================
# Full Career Report
# ==========================================

@router.post(
    "/career-report",
    response_model=CareerReportResponse
)
async def career_report(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    # Read PDF
    file_bytes = await file.read()
    cv_text = extract_text_from_pdf(file_bytes)

    # Extract Skills
    cv_skills = extract_skills(cv_text)
    job_skills = extract_job_skills(job_description)

    # Match Engine
    matched_skills, missing_skills, match_score = calculate_match(
        cv_skills,
        job_skills
    )

    # ATS Engine
    ats_result = calculate_ats_score(
        match_score,
        cv_text,
        cv_skills,
        job_skills
    )

    ats_score = ats_result["ats_score"]

    # Courses
    recommended_courses = recommend_courses(
        missing_skills
    )

    # Roadmap
    roadmap = build_roadmap(
        missing_skills
    )

    # Suggestions
    suggestions = generate_suggestions(
        missing_skills
    )

    # Resume Feedback
    resume_feedback = generate_resume_feedback(
        matched_skills,
        missing_skills
    )

    return CareerReportResponse(

        cv_skills=cv_skills,

        job_skills=job_skills,

        matched_skills=matched_skills,

        missing_skills=missing_skills,

        match_score=match_score,

        ats_score=ats_score,

        ats_details=ats_result["details"],

        recommended_courses=recommended_courses,

        roadmap=roadmap,

        suggestions=suggestions,

        resume_feedback=resume_feedback

    )