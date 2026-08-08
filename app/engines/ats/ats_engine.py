import logging

from app.data.ats_db import (
    SKILL_WEIGHT,
    KEYWORD_WEIGHT,
    SECTION_WEIGHT,
    EXPERIENCE_WEIGHT,
    PROJECT_WEIGHT,
    CERTIFICATION_WEIGHT,
    RESUME_LENGTH_WEIGHT,
    REQUIRED_SECTIONS,
)

from app.engines.ats.section.resume_cleaner import clean_resume
from app.engines.ats.section.section_parser import parse_resume_sections

from app.engines.ats.analyzers.skills.skill_extractor import (
    extract_skills_from_text
)

from app.engines.ats.analyzers.experience.experience import (
    analyze_experience
)

from app.engines.ats.analyzers.projects.project_scoring import (
    score_projects
)

from app.engines.ats.analyzers.certifications.certifications import (
    analyze_certifications
)

from app.engines.ats.scoring.ats.keyword_density import (
    analyze_keyword_density
)

from app.engines.ats.report.score_builder import build_scores
from app.engines.ats.report.summary_builder import build_summary
from app.engines.ats.report.report_builder import build_report

logger = logging.getLogger(__name__)


# ==========================================================
# HELPERS
# ==========================================================

def _compute_section_score(sections):
    found = sum(1 for s in REQUIRED_SECTIONS if s in sections and sections[s].strip())
    return round((found / len(REQUIRED_SECTIONS)) * 10, 2)


def _compute_resume_length_score(text):
    words = len(text.split())
    if 300 <= words <= 800:
        return 10.0
    elif (200 <= words < 300) or (800 < words <= 1000):
        return 7.0
    elif (100 <= words < 200) or (1000 < words <= 1500):
        return 5.0
    else:
        return 3.0


# ==========================================================
# ATS ENGINE
# ==========================================================

def analyze_resume(cv_text, job_skills=None):
    """
    Perform full ATS analysis on a CV.

    Parameters
    ----------
    cv_text : str
        Raw text extracted from the candidate's CV.
    job_skills : list, optional
        Skills extracted from the job description.

    Returns
    -------
    dict
        ATS analysis result containing ats_score, ats_details,
        matched_skills, missing_skills, match_score, and raw
        analyzer outputs.
    """

    logger.info("Starting ATS analysis")

    # ------------------------------------------------------
    # Step 1 - Clean Resume
    # ------------------------------------------------------

    cleaned = clean_resume(cv_text)

    clean_text = cleaned.get("clean_text", cv_text)

    summary_text = cleaned.get("summary", "")

    # ------------------------------------------------------
    # Step 2 - Parse Sections
    # ------------------------------------------------------

    sections = parse_resume_sections(clean_text)

    # ------------------------------------------------------
    # Step 3 - Skill Analysis
    # ------------------------------------------------------

    ats_skills = extract_skills_from_text(clean_text)

    # ------------------------------------------------------
    # Step 4 - Experience Analysis
    # ------------------------------------------------------

    experience = analyze_experience(clean_text)

    # ------------------------------------------------------
    # Step 5 - Project Analysis
    # ------------------------------------------------------

    projects_text = sections.get("projects", "")

    projects = score_projects(projects_text)

    # ------------------------------------------------------
    # Step 6 - Certification Analysis
    # ------------------------------------------------------

    certifications_text = sections.get("certifications", "")

    certifications = analyze_certifications(certifications_text)

    # ------------------------------------------------------
    # Step 7 - Keyword Density
    # ------------------------------------------------------

    keyword_density = {}

    if job_skills:
        keyword_density = analyze_keyword_density(clean_text, job_skills)

    # ------------------------------------------------------
    # Step 8 - Compute Sub-Scores
    # ------------------------------------------------------

    skill_score = min(10, len(ats_skills) * 0.5)

    experience_score = experience.get("score", 0)

    project_score = projects.get("average_score", 0)

    certification_score = min(10, certifications.get("total_certifications", 0) * 2)

    section_score = _compute_section_score(sections)

    resume_length_score = _compute_resume_length_score(clean_text)

    # Keyword score: average density of matched job skills
    keyword_score = 0.0

    if keyword_density:
        total_density = sum(
            v["density"] for v in keyword_density.values()
        )
        keyword_score = min(10, total_density / max(len(keyword_density), 1))

    # ------------------------------------------------------
    # Step 9 - Build Overall ATS Score
    # ------------------------------------------------------

    ats_score = round(
        (
            skill_score * (SKILL_WEIGHT / 100) +
            keyword_score * (KEYWORD_WEIGHT / 100) +
            section_score * (SECTION_WEIGHT / 100) +
            experience_score * (EXPERIENCE_WEIGHT / 100) +
            project_score * (PROJECT_WEIGHT / 100) +
            certification_score * (CERTIFICATION_WEIGHT / 100) +
            resume_length_score * (RESUME_LENGTH_WEIGHT / 100)
        ) * 10,
        2
    )

    # ------------------------------------------------------
    # Step 10 - Skill Matching (if job skills provided)
    # ------------------------------------------------------

    matched_skills = []
    missing_skills = []
    match_score = 0.0

    if job_skills:
        cv_skill_map = {}
        for skill in ats_skills:
            normalized = " ".join(str(skill).strip().lower().split())
            if normalized:
                cv_skill_map[normalized] = skill

        job_skill_map = {}
        for skill in job_skills:
            normalized = " ".join(str(skill).strip().lower().split())
            if normalized:
                job_skill_map[normalized] = skill

        cv_normalized = set(cv_skill_map.keys())
        job_normalized = set(job_skill_map.keys())

        matched_normalized = cv_normalized.intersection(job_normalized)
        missing_normalized = job_normalized.difference(cv_normalized)

        matched_skills = [cv_skill_map[s] for s in matched_normalized]
        missing_skills = [job_skill_map[s] for s in missing_normalized]

        if len(job_normalized) > 0:
            match_score = round(
                (len(matched_normalized) / len(job_normalized)) * 100,
                2
            )

    # ------------------------------------------------------
    # Step 11 - Build Summary
    # ------------------------------------------------------

    summary = build_summary(
        scores={
            "overall_score": ats_score,
            "skills_score": round(skill_score, 2),
            "experience_score": round(experience_score, 2),
            "projects_score": round(project_score, 2),
            "certifications_score": round(certification_score, 2),
        },
        skills=ats_skills,
        experience=experience,
        projects=projects,
        certifications=certifications,
    )

    # ------------------------------------------------------
    # Step 12 - Final Result
    # ------------------------------------------------------

    logger.info("ATS analysis completed successfully")

    return {

        "ats_score": ats_score,

        "ats_details": {

            "skill_score": round(skill_score, 2),

            "keyword_score": round(keyword_score, 2),

            "section_score": round(section_score, 2),

            "experience_score": round(experience_score, 2),

            "project_score": round(project_score, 2),

            "certification_score": round(certification_score, 2),

            "resume_length_score": round(resume_length_score, 2)

        },

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "match_score": match_score,

        "skills": ats_skills,

        "experience": experience,

        "projects": projects,

        "certifications": certifications,

        "sections": sections,

        "summary": summary,

        "keyword_density": keyword_density

    }
