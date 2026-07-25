# ==========================================================
# SUMMARY BUILDER
# ==========================================================

def build_summary(
    scores,
    skills,
    experience,
    projects,
    certifications
):

    strengths = []

    weaknesses = []

    recommendations = []

    # ------------------------------------------------------
    # Skills
    # ------------------------------------------------------

    if len(skills) >= 10:

        strengths.append(
            "Strong technical skill set."
        )

    else:

        weaknesses.append(
            "Limited technical skills."
        )

        recommendations.append(
            "Add more job-related technical skills."
        )

    # ------------------------------------------------------
    # Projects
    # ------------------------------------------------------

    if projects.get("average_score", 0) >= 8:

        strengths.append(
            "High-quality projects with measurable impact."
        )

    else:

        recommendations.append(
            "Improve project descriptions using metrics."
        )

    # ------------------------------------------------------
    # Experience
    # ------------------------------------------------------

    experience_score = experience.get("score", 0)

    if experience_score == 0:

        weaknesses.append(
            "No work experience detected."
        )

        recommendations.append(
            "Add internships, volunteering or freelance work."
        )

    elif experience_score >= 7:

        strengths.append(
            "Strong professional experience."
        )

    # ------------------------------------------------------
    # Certifications
    # ------------------------------------------------------

    if certifications.get("count", 0) == 0:

        recommendations.append(
            "Consider adding professional certifications."
        )

    # ------------------------------------------------------
    # Final Summary
    # ------------------------------------------------------

    return {

        "strengths": strengths,

        "weaknesses": weaknesses,

        "recommendations": recommendations

    }