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
def analyze_resume(cv_skills, job_skills):
    """
    Analyze CV skills against job-required skills and generate
    an ATS skill-matching result.

    Parameters
    ----------
    cv_skills : list
        Skills extracted from the candidate's CV.

    job_skills : list
        Skills extracted from the job description.

    Returns
    -------
    tuple
        matched_skills : list
            Skills found in both CV and job requirements.

        missing_skills : list
            Skills required by the job but missing from the CV.

        match_score : float
            Percentage of job-required skills matched by the CV.
    """

    print("\n========== ATS ENGINE ==========")

    # ------------------------------------------------------
    # Step 1 - Validate Skills
    # ------------------------------------------------------

    print("\n[ATS] Validating Skills...")

    if cv_skills is None:
        cv_skills = []

    if job_skills is None:
        job_skills = []

    if isinstance(cv_skills, str):
        cv_skills = [cv_skills]

    if isinstance(job_skills, str):
        job_skills = [job_skills]

    print(f"CV Skills: {len(cv_skills)}")
    print(f"Job Skills: {len(job_skills)}")

    # ------------------------------------------------------
    # Step 2 - Normalize Skills
    # ------------------------------------------------------

    print("\n[ATS] Normalizing Skills...")

    def normalize_skill(skill):
        return " ".join(
            str(skill)
            .strip()
            .lower()
            .split()
        )

    cv_skill_map = {}

    for skill in cv_skills:
        normalized = normalize_skill(skill)

        if normalized:
            cv_skill_map[normalized] = skill

    job_skill_map = {}

    for skill in job_skills:
        normalized = normalize_skill(skill)

        if normalized:
            job_skill_map[normalized] = skill

    cv_normalized = set(cv_skill_map.keys())
    job_normalized = set(job_skill_map.keys())

    # ------------------------------------------------------
    # Step 3 - Match Skills
    # ------------------------------------------------------

    print("\n[ATS] Matching Skills...")

    matched_normalized = cv_normalized.intersection(job_normalized)

    missing_normalized = job_normalized.difference(cv_normalized)

    matched_skills = [
        cv_skill_map[skill]
        for skill in matched_normalized
    ]

    missing_skills = [
        job_skill_map[skill]
        for skill in missing_normalized
    ]

    print(f"Matched Skills: {len(matched_skills)}")
    print(f"Missing Skills: {len(missing_skills)}")

    # ------------------------------------------------------
    # Step 4 - Calculate Match Score
    # ------------------------------------------------------

    print("\n[ATS] Calculating Match Score...")

    if len(job_normalized) == 0:
        match_score = 0.0
    else:
        match_score = (
            len(matched_normalized)
            / len(job_normalized)
        ) * 100

    match_score = round(match_score, 2)

    print(f"Match Score: {match_score}%")

    # ------------------------------------------------------
    # Step 5 - Final Result
    # ------------------------------------------------------

    print("\n[ATS] ATS Engine Finished Successfully.")

    return (
        matched_skills,
        missing_skills,
        match_score
    )