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

def analyze_resume(resume_text: str):
    """
    Analyze resume text and generate a complete ATS report.

    Parameters
    ----------
    resume_text : str
        Extracted text from the resume PDF.

    Returns
    -------
    dict
        Complete ATS report.
    """

    print("\n========== ATS ENGINE ==========")

    # ------------------------------------------------------
    # Step 1 - Clean Resume
    # ------------------------------------------------------

    print("\n[ATS] Cleaning Resume...")

    cleaned = clean_resume(resume_text)

    print("Resume cleaned successfully.")

    # ------------------------------------------------------
    # Step 2 - Parse Sections
    # ------------------------------------------------------

    print("\n[ATS] Parsing Resume Sections...")

    sections = parse_resume_sections(
        cleaned["clean_text"]
    )

    print("Sections detected:")
    print(list(sections.keys()))

    # ------------------------------------------------------
    # Step 3 - Skills
    # ------------------------------------------------------

    print("\n[ATS] Analyzing Skills...")

    skills = extract_skills_from_text(
        sections.get("skills", "")
    )

    print(f"Skills Found: {len(skills)}")

    # ------------------------------------------------------
    # Step 4 - Experience
    # ------------------------------------------------------

    print("\n[ATS] Analyzing Experience...")

    experience = analyze_experience(
        sections.get("experience", "")
    )

    print("Experience analysis completed.")

    # ------------------------------------------------------
    # Step 5 - Projects
    # ------------------------------------------------------

    print("\n[ATS] Analyzing Projects...")

    projects = score_projects(
        sections.get("projects", "")
    )

    print("Projects analysis completed.")

    # ------------------------------------------------------
    # Step 6 - Certifications
    # ------------------------------------------------------

    print("\n[ATS] Analyzing Certifications...")

    certifications = analyze_certifications(
        sections.get("certifications", "")
    )

    print("Certification analysis completed.")

    # ------------------------------------------------------
    # Step 7 - Scores
    # ------------------------------------------------------

    print("\n[ATS] Calculating Scores...")

    scores = build_scores(
        skills,
        experience,
        projects,
        certifications
    )

    print("Overall ATS Score:", scores["overall_score"])

    # ------------------------------------------------------
    # Step 8 - Summary
    # ------------------------------------------------------

    print("\n[ATS] Building Summary...")

    summary = build_summary(
        scores,
        skills,
        experience,
        projects,
        certifications
    )

    print("Summary generated.")

    # ------------------------------------------------------
    # Step 9 - Final Report
    # ------------------------------------------------------

    print("\n[ATS] Building Final Report...")

    report = build_report(
        sections,
        skills,
        experience,
        projects,
        certifications,
        scores,
        summary
    )

    print("ATS Engine Finished Successfully.")

    return report