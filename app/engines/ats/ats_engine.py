from app.parsers.pdf_reader import extract_text_from_pdf

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

from app.engines.ats.report.score_builder import build_scores
from app.engines.ats.report.summary_builder import build_summary
from app.engines.ats.report.report_builder import build_report


# ==========================================================
# ATS ENGINE
# ==========================================================

def analyze_resume(pdf_path: str):

    # ------------------------------------------------------
    # Read Resume
    # ------------------------------------------------------

    resume_text = extract_text_from_pdf(pdf_path)

    # ------------------------------------------------------
    # Clean Resume
    # ------------------------------------------------------

    cleaned = clean_resume(resume_text)

    # ------------------------------------------------------
    # Parse Sections
    # ------------------------------------------------------

    sections = parse_resume_sections(
        cleaned["clean_text"]
    )

    # ------------------------------------------------------
    # Skills
    # ------------------------------------------------------

    skills = extract_skills_from_text(
        sections.get("skills", "")
    )

    # ------------------------------------------------------
    # Experience
    # ------------------------------------------------------

    experience = analyze_experience(
        sections.get("experience", "")
    )

    # ------------------------------------------------------
    # Projects
    # ------------------------------------------------------

    projects = score_projects(
        sections.get("projects", "")
    )

    # ------------------------------------------------------
    # Certifications
    # ------------------------------------------------------

    certifications = analyze_certifications(
        sections.get("certifications", "")
    )

    # ------------------------------------------------------
    # Scores
    # ------------------------------------------------------

    scores = build_scores(

        skills,

        experience,

        projects,

        certifications

    )

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    summary = build_summary(

        scores,

        skills,

        experience,

        projects,

        certifications

    )

    # ------------------------------------------------------
    # Final Report
    # ------------------------------------------------------

    return build_report(

        sections,

        skills,

        experience,

        projects,

        certifications,

        scores,

        summary

    )