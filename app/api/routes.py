from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import pdfplumber
import io
import logging

from app.models.schemas import (
    JobRequest,
    AnalyzeResponse,
    CareerReportResponse,
)

from app.engines.matching.skill_extractor import extract_skills
from app.engines.matching.match_engine import calculate_match
from app.parsers.job_parser import extract_job_skills
from app.engines.recommendation.course_engine import recommend_courses
from app.engines.recommendation.roadmap_engine import build_roadmap
from app.engines.recommendation.suggestion_engine import generate_suggestions
from app.engines.recommendation.resume_feedback import generate_resume_feedback
from app.engines.ats.ats_engine import analyze_resume

logger = logging.getLogger(__name__)

router = APIRouter()


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


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_job(request: JobRequest):

    job_skills = extract_job_skills(
        request.job_description
    )

    return AnalyzeResponse(
        job_skills=job_skills
    )


@router.post(
    "/career-report",
    response_model=CareerReportResponse
)
async def career_report(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    # -----------------------------------------------------
    # 1. Validate Upload
    # -----------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file uploaded."
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=415,
            detail="Only PDF files are supported."
        )

    content = await file.read()

    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds 10MB limit."
        )

    if not job_description or not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description is required."
        )

    # -----------------------------------------------------
    # 2. Extract CV Text
    # -----------------------------------------------------

    cv_text = extract_text_from_pdf(content)

    if not cv_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from the uploaded PDF."
        )

    # -----------------------------------------------------
    # 3. Extract CV Skills
    # -----------------------------------------------------

    cv_skills = extract_skills(cv_text)

    # -----------------------------------------------------
    # 4. Extract Job Skills
    # -----------------------------------------------------

    job_skills = extract_job_skills(job_description)

    # -----------------------------------------------------
    # 5. Match CV Against Job
    # -----------------------------------------------------

    matched_skills, missing_skills, match_score = calculate_match(
        cv_skills,
        job_skills
    )

    # -----------------------------------------------------
    # 6. Full ATS Analysis
    # -----------------------------------------------------

    ats_result = analyze_resume(
        cv_text,
        job_skills=job_skills
    )

    # -----------------------------------------------------
    # 7. Extract ATS Score
    # -----------------------------------------------------

    ats_score = ats_result["ats_score"]

    ats_details = ats_result["ats_details"]

    # -----------------------------------------------------
    # 8. Course Recommendations
    # -----------------------------------------------------

    recommended_courses = recommend_courses(
        missing_skills
    )

    # -----------------------------------------------------
    # 9. Career Roadmap
    # -----------------------------------------------------

    roadmap = build_roadmap(
        missing_skills
    )

    # -----------------------------------------------------
    # 10. Career Suggestions
    # -----------------------------------------------------

    suggestions = generate_suggestions(
        missing_skills
    )

    # -----------------------------------------------------
    # 11. Resume Feedback
    # -----------------------------------------------------

    resume_feedback = generate_resume_feedback(
        matched_skills,
        missing_skills
    )

    # -----------------------------------------------------
    # 12. Final Response
    # -----------------------------------------------------

    return CareerReportResponse(

        cv_skills=cv_skills,

        job_skills=job_skills,

        matched_skills=matched_skills,

        missing_skills=missing_skills,

        match_score=match_score,

        ats_score=ats_score,

        ats_details=ats_details,

        recommended_courses=recommended_courses,

        roadmap=roadmap,

        suggestions=suggestions,

        resume_feedback=resume_feedback

    )
