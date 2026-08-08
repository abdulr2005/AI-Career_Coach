from fastapi import APIRouter, UploadFile, File, Form
import pdfplumber
import io

from app.models.schemas import (
    JobRequest,
    AnalyzeResponse,
    CareerReportResponse,
)

# =========================================================
# Matching
# =========================================================

from app.engines.matching.skill_extractor import extract_skills
from app.engines.matching.match_engine import calculate_match

# =========================================================
# Parsers
# =========================================================

from app.parsers.job_parser import extract_job_skills

# =========================================================
# Recommendation
# =========================================================

from app.engines.recommendation.course_engine import recommend_courses
from app.engines.recommendation.roadmap_engine import build_roadmap
from app.engines.recommendation.suggestion_engine import generate_suggestions
from app.engines.recommendation.resume_feedback import generate_resume_feedback

# =========================================================
# ATS
# =========================================================

from app.engines.ats.ats_engine import analyze_resume


router = APIRouter()


# =========================================================
# Root Endpoint
# =========================================================

@router.get("/")
def home():
    return {
        "message": "AI Career Coach API is Running"
    }


# =========================================================
# Analyze Job Description
# =========================================================

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


# =========================================================
# PDF Text Extraction
# =========================================================

def extract_text_from_pdf(file_bytes: bytes) -> str:

    pages = []

    with pdfplumber.open(
        io.BytesIO(file_bytes)
    ) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

    return "\n".join(pages)


# =========================================================
# Full Career Report
# =========================================================

@router.post(
    "/career-report",
    response_model=CareerReportResponse
)
async def career_report(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    # -----------------------------------------------------
    # 1. Read PDF
    # -----------------------------------------------------

    file_bytes = await file.read()

    cv_text = extract_text_from_pdf(
        file_bytes
    )

    if not cv_text.strip():
        raise ValueError(
            "Could not extract text from the uploaded PDF."
        )

    # -----------------------------------------------------
    # 2. Extract CV Skills
    # -----------------------------------------------------

    cv_skills = extract_skills(
        cv_text
    )

    # -----------------------------------------------------
    # 3. Extract Job Skills
    # -----------------------------------------------------

    job_skills = extract_job_skills(
        job_description
    )

    # -----------------------------------------------------
    # 4. Match CV Against Job
    # -----------------------------------------------------

    matched_skills, missing_skills, match_score = calculate_match(
        cv_skills,
        job_skills
    )

    # -----------------------------------------------------
    # 5. Full ATS Analysis
    # -----------------------------------------------------

    ats_result = analyze_resume(
        cv_text
    )

    # -----------------------------------------------------
    # 6. Extract ATS Score
    # -----------------------------------------------------

    ats_score = ats_result["ats_score"]

    # -----------------------------------------------------
    # 7. Course Recommendations
    # -----------------------------------------------------

    recommended_courses = recommend_courses(
        missing_skills
    )

    # -----------------------------------------------------
    # 8. Career Roadmap
    # -----------------------------------------------------

    roadmap = build_roadmap(
        missing_skills
    )

    # -----------------------------------------------------
    # 9. Career Suggestions
    # -----------------------------------------------------

    suggestions = generate_suggestions(
        missing_skills
    )

    # -----------------------------------------------------
    # 10. Resume Feedback
    # -----------------------------------------------------

    resume_feedback = generate_resume_feedback(
        matched_skills,
        missing_skills
    )

    # -----------------------------------------------------
    # 11. Final Response
    # -----------------------------------------------------

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
