# ==========================================================
# SCORE BUILDER
# ==========================================================

def build_scores(
    skills,
    experience,
    projects,
    certifications
):

    # ------------------------------------------------------
    # Individual Scores
    # ------------------------------------------------------

    skills_score = min(
        10,
        len(skills) * 0.5
    )

    experience_score = experience.get(
        "score",
        0
    )

    projects_score = projects.get(
        "average_score",
        0
    )

    certifications_score = min(
        10,
        certifications.get("total_certifications", 0) * 2
    )

    # ------------------------------------------------------
    # Overall
    # ------------------------------------------------------

    overall = round(

        (
            skills_score +
            experience_score +
            projects_score +
            certifications_score

        ) / 4,

        2

    )

    return {

        "overall_score": overall,

        "skills_score": round(skills_score, 2),

        "experience_score": round(experience_score, 2),

        "projects_score": round(projects_score, 2),

        "certifications_score": round(certifications_score, 2)

    }